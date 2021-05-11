import socket

# host = input("Input IP of the server program: ")
# port = int(input("Enter port number: "))
host = "127.0.0.1"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, 65432))
    received = 0

    while True:
        data = s.recv(1024)
        if received <= 0:
            print(data.decode('utf-8'))
        else:
            print('Pig latin translation: ', data.decode('utf-8'))    # if (repr(data) == "ACK"):
            data2 = s.recv(1024)
            print(data2.decode('utf-8'))
            end_choice = input("Enter choice: ")
            s.sendall(bytes(end_choice, encoding="utf-8"))
            if (end_choice == 'N' or end_choice == 'n'): break

        new_message = input("Enter message to translate: ")
        s.sendall(bytes(new_message, encoding="utf-8"))
        received += 1