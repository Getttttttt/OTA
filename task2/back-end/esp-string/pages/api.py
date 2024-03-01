from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    file.save(os.path.join('/path/to/upload', filename))
    # 这里添加将文件烧录到ESP32的代码
    return jsonify({'message': 'File uploaded and burn initiated.'})

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data['message']
    # 这里添加将消息发送到ESP32的代码
    return jsonify({'message': 'Message sent to ESP32.'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
