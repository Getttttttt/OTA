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
