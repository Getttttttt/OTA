from flask import Flask, request, jsonify
from flask_cors import CORS  # 处理同源策略
import os
import socket  # 用于与ESP32通信

app = Flask(__name__)
app.config['upimgs'] = './'
CORS(app)  # 允许所有域的跨域请求，这里其实最后调整一下，只允许前端的请求会更好

ESP32_HOST = '192.168.140.245' #记得修改为esp32的IP哈~
ESP32_PORT = 12345  # 记得修改为ESP32监听的端口

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in multipart form data.'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No file selected for uploading.'}), 400

    if file:
        # 读取文件的内容
        file_content = file.read()
        # 读取完关闭
        file.close()
        print(file_content)
        filename = file.filename
        print(filename)
        # 如果没有创建文件
        if not os.path.exists('./uploads'):
            os.makedirs('./uploads')
        # 打开文件并指定模式为wb
        with open(os.path.join(app.config['upimgs'],'uploads/'+filename), 'wb') as f:
            # 写入文件内容
            f.write(file_content)
        file_path = os.path.join('uploads/',filename)
        try:
            print("开始发送文件")
            # 这里file_path去除前面的uploads/
            file_path=file_path.replace("uploads/","")
            send_to_esp32(file_content, file_path)
            return jsonify({'message': 'File transmitted successfully.'}), 201
        except Exception as e:
            return jsonify({'message': f'An error occurred: {str(e)}'}), 500

def send_to_esp32(file_content, file_path):
    try:
        print("正在发送文件")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ESP32_HOST, ESP32_PORT))
            # 发送文件名和内容
            s.sendall(f'{file_path}\n{file_content}'.encode())
    except Exception as e:
        print(f'Failed to send file to ESP32: {e}')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
