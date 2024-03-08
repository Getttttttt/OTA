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
