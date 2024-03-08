# OTA

## 0308 Update task2

OTA实现字符流传输：

该部分代码正在本地测试中，代码基本完整给出。我在本地已经完成前后端交互的调试，但是后端和ESP32主板的交互在等待进一步调试。

该部分的主要逻辑是：

1. 前端有一个很简单的界面，支持一个input，和一个submit。input的内容是一个后端的文件路径，点击提交按钮后，前端将文件路径传输到后端的一个API。
2. 后端的第一个API接受前端发出的文件路径，检查文件路径是否存在，若不存在，给前端返回一个文件不存在的错误信息。若存在，给前端返回一个正在传输的信息，并将文件路径发送给后端的另一个API。前端接收到信息后以alert的形式展示。
3. 后端的另一个api将文件中的内容以字符流的形式读取，并以字符流发送给esp32主板上面的一个在持续监听的micropython程序。
4. esp32主板上的micropython程序进行字符流接受。创建同名文件并写入一个esp32主板上。
要使前端页面、Flask后端和ESP32的MicroPython程序配合工作，需要确保它们都正确配置并且相互之间能够通信。下面是一个整合三者的逻辑框架、实现技术细节以及部署步骤的总结。

### 1. 前端页面

因为前端页面需求比较简单，我就用了一个原生页面，提供一个输入框供用户输入文件路径和一个提交按钮用于发送路径到后端。
#### 实现代码
remote-transfer.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>ESP32 File Sender</title>
</head>
<body>
    <input type="text" id="filePath" placeholder="Enter file path">
    <button onclick="submitFilePath()">Submit</button>

    <script>
        function submitFilePath() {
            var filePath = document.getElementById('filePath').value;
            fetch('http://127.0.0.1:5000/api/upload', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({filePath: filePath}),
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('Failed to send the file path.');
            });
        }
    </script>
</body>
</html>
```

#### 部署步骤和注意事项

我是直接通过vscode插件本地部署的。当然使用其他的部署工具也都可以。
- 通过Vscode打开html文件
- Vscode安装live-server插件，进入html右键选择open with live server

### 2. Flask后端
Flask后端提供2个简单的API接收前端发送的文件路径，验证文件路径并转发文件内容到ESP32。
#### 实现代码
app.py
```python
from flask import Flask, request, jsonify
from flask_cors import CORS  # 处理同源策略
import os
import socket  # 用于与ESP32通信

app = Flask(__name__)
CORS(app)  # 允许所有域的跨域请求，这里其实最后调整一下，只允许前端的请求会更好

ESP32_HOST = 'ESP32的IP地址' #记得修改为esp32的IP哈~
ESP32_PORT = 12345  # 记得修改为ESP32监听的端口

@app.route('/api/upload', methods=['POST'])
def upload_file():
    data = request.get_json()
    file_path = data['filePath']
    
    if not os.path.exists(file_path):
        return jsonify({'message': 'File does not exist.'}), 404

    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            send_to_esp32(file_content, file_path)
        return jsonify({'message': 'File is being transmitted to ESP32.'})
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500

def send_to_esp32(file_content, file_path):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ESP32_HOST, ESP32_PORT))
            # 发送文件名和内容
            s.sendall(f'{file_path}\n{file_content}'.encode())
    except Exception as e:
        print(f'Failed to send file to ESP32: {e}')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
```

#### 部署步骤和注意事项

- 确保已安装Python和Flask库。
- 下载相关文件，vscode打开并运行python app.py以启动后端服务器。
- 根据实际部署环境替换ESP32_HOST和ESP32_PORT值。

### 3. ESP32的MicroPython程序

ESP32程序持续监听连接，接收文件名和内容，然后存储。

#### 实现代码
```python
import socket

port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', port))
s.listen(1)

print('Waiting for a connection...')

while True:
    conn, addr = s.accept()
    print('Connected by', addr)
    received_data = conn.recv(1024).decode('utf-8')
    file_path, file_content = received_data.split('\n', 1)
    file_name = file_path.split('/')[-1]  # 获取文件名
    with open(file_name, 'w') as file:
        file.write(file_content)
    print(f'File {file_name} has been written.')
    conn.close()
```

#### 部署步骤和注意事项

- 将上述脚本通过MicroPython的REPL或其他方式上传到ESP32。
- 确保ESP32已连接到与服务器相同的网络，并且ESP32_HOST变量正确指向ESP32的IP地址。
- MicroPython环境通常有限，确保不要发送过大的文件。
- 确保传输文件过程中避免网络中断。

### 其他注意事项

- 在更换部署环境时，需要更新Flask后端中的ESP32_HOST以匹配ESP32在新网络中的IP地址。
- 确保ESP32的固件支持使用的库。
- 我在Flask应用中设置CORS策略是允许所有的请求，但是实际上应该根据到时候部署的情况进行调整，以避免潜在的安全风险。

## 0227 Update
Micropython and arduino to realize OTA.

