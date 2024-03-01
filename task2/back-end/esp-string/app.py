import socket
import os

# 创建一个socket对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))  # 绑定到80端口
s.listen(5)  # 开始监听

print("Waiting for connections...")

while True:
    conn, addr = s.accept()  # 接受一个新连接
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)  # 接收请求数据
    request_str = str(request, 'utf-8')
    
    # 简单地查找特定标志来判断是否为文件上传
    if "POST /upload" in request_str:
        # 提取文件内容，这里需要根据实际的请求格式进行适当调整
        start = request_str.find('\r\n\r\n') + 4
        end = request_str.rfind('\r\n------')  # 假设使用multipart/form-data格式
        file_content = request[start:end]
        
        # 写入文件，这里假设文件名是固定的
        with open('script.py', 'w') as file:
            file.write(file_content)
        
        # 发送响应
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall('File uploaded successfully.')
        print("File uploaded successfully.")
        
        # 执行上传的脚本
        exec(open('script.py').read(), globals())
    
    conn.close()
