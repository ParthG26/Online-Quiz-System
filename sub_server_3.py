import socket
import threading
import os

def send_msg_to_main_server(msg):
    server_addr = ("127.0.0.1", 2001)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect(server_addr)
    except Exception as e:
        print("Connection Failed. Error!!!!")
        return -1

    print("Connected")

    try:
        client_socket.send(msg.encode())
    except Exception as e:
        print("Send Failed. Error!!!!")
        client_socket.close()
        return -1

    client_socket.close()
    return 0

class ClientInfo:
    def __init__(self, socket, port, ip, loc):
        self.socket = socket
        self.port = port
        self.ip = ip
        self.loc = loc

def client_thread_func(c_info):
    print("starting client_thread_func")

    server_message = "Enter your test type:\nAnalogies\nAntonyms\nRC Questions\n"
    client_message = ""
    port_buffer = str(c_info.port)

    client_sock = c_info.socket

    print("\nSocket:", client_sock)
    print("\nPort:", c_info.port)
    print("\nIP:", c_info.ip)
    print("\nmalloc:", c_info.loc)

    # Cleaning the Buffers
    client_sock.send(server_message.encode())

    try:
        client_message = client_sock.recv(2000).decode()
    except Exception as e:
        print("client_thread_func Receive Failed. Error!!!!!")
        client_sock.close()
        return -1

    print("client_thread_func Client Sock:", client_sock)
    print("client_thread_func Client Message:", client_message)

    server_message = ""
    if client_message in ["Analogies", "Antonyms", "RC Questions"]:
        server_message = f"{c_info.ip},{c_info.port},English,{client_message},20"
    else:
        server_message = "Invalid Input!!!"

    try:
        client_sock.send(server_message.encode())
    except Exception as e:
        print("client_thread_func Send Failed. Error!!!!!")
        client_sock.close()
        return -1

    if send_msg_to_main_server(server_message) == -1:
        return -1

    client_sock.close()
    c_info.loc = None
    threading.current_thread().join()

def set_connection_for_clients(my_ip, my_port):
    port = int(my_port)

    socket_desc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if socket_desc < 0:
        print("Could Not Create Socket. Error!!!!!")
        return -1

    print("Socket Created")

    server_addr = (my_ip, port)

    try:
        socket_desc.bind(server_addr)
    except Exception as e:
        print("Bind Failed. Error!!!!!")
        return -1

    print("Bind Done")

    try:
        socket_desc.listen(1)
    except Exception as e:
        print("Listening Failed. Error!!!!!")
        return -1

    print("Listening for Incoming Connections.....")

    while True:
        client_sock, client_addr = socket_desc.accept()

        if client_sock < 0:
            print("Accept Failed. Error!!!!!!")
            return -1
        else:
            c_info = ClientInfo(client_sock, client_addr[1], client_addr[0], None)
            thread = threading.Thread(target=client_thread_func, args=(c_info,))
            thread.start()

def main():
    my_test_name = "English"
    my_ip = "127.0.0.1"
    my_port = "2030"
    msg = f"{my_test_name},{my_ip},{my_port}"

    if send_msg_to_main_server(msg) == -1:
        return -1

    set_connection_for_clients(my_ip, my_port)

if __name__ == "__main__":
    main()
