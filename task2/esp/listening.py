import socket

port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', port))
s.listen(1)

print('Waiting for a connection...')
while True:
    conn, addr = s.accept()
    print('Connected by', addr)
    #received_data = conn.recv(1024)  # 接收原始字节数据
    received_data = bytearray()
    while True:
        data = conn.recv(1024)
        if not data:
            break
        received_data.extend(data)
    received_data = bytes(received_data)  # 将 bytearray 转换为 bytes
    file_path, file_content = received_data.split(b'\n', 1)  # 使用字节串分隔符 b'\n'
    file_name = file_path.decode('utf-8').split('/')[-1]  # 将文件路径解码为字符串并获取文件名
    print('文件路径为'+file_name)
    #print('文件内容'+file_content.decode('utf-8'))
    with open(file_name, 'wb') as file:
        file.write(file_content.decode('utf-8'))  # 直接写入原始字节数据
        print(f'File {file_name} has been written.')
        break
    conn.close()