import socket

def main():
    server_addr = ("127.0.0.1", 2000)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect(server_addr)
    except Exception as e:
        print("\nConnection Failed. Error!!!!")
        return -1

    print("\nConnected")

    server_message = ""
    client_message = ""
    server_message = client_socket.recv(2000).decode()

    if not server_message:
        print("\nReceive Failed. Error!!!!!")
        return -1

    print("\nServer Message:\n", server_message)

    client_message = input("\nEnter Message: ")

    try:
        client_socket.send(client_message.encode())
    except Exception as e:
        print("\nSend Failed. Error!!!!")
        client_socket.close()
        return -1

    server_message = client_socket.recv(2000).decode()

    if not server_message:
        print("\nReceive Failed. Error!!!!!")
        return -1

    print("\nServer info Message:", server_message)

    name, ip, port = server_message.split(',')
    sub_server_port = int(port)

    print("\nName:", name)
    print("IP:", ip)
    print("Port:", sub_server_port)

    client_socket.close()

    # Now connect to the Sub-Server

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((ip, sub_server_port))
    except Exception as e:
        print("\nConnection Failed with Sub Server. Error!!!!!")
        return -1

    print("\nConnected to Sub Server")

    server_message = client_socket.recv(2000).decode()

    if not server_message:
        print("\nReceive Failed. Error!!!!!")
        return -1

    print("\nSub Server Message:\n", server_message)

    client_message = input("\nEnter Message: ")

    try:
        client_socket.send(client_message.encode())
    except Exception as e:
        print("\nSub Server Send Failed. Error!!!!")
        client_socket.close()
        return -1

    server_message = client_socket.recv(2000).decode()

    if not server_message:
        print("\nSub Server Receive Failed. Error!!!!!")
        return -1

    print("\nSub Server Message:", server_message)

    client_socket.close()

if __name__ == "__main__":
    main()
