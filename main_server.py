import socket
import threading

def check_format_of_sub_server_msg(string):
    count = string.count(',')
    return count

def sub_server_thread_func(client_sock):
    print("starting sub_server_thread_func")

    server_message = bytearray(2000)
    client_message = bytearray(2000)

    # Receive the message from the client
    bytes_received = client_sock.recv_into(client_message)
    
    if bytes_received < 0:
        print("sub_server_thread_func Receive Failed. Error!!!!!")
        return

    print("\nsub_server_thread_func Client Sock:", client_sock)
    print("\nsub_server_thread_func Client Message:", client_message.decode())

    if check_format_of_sub_server_msg(client_message.decode()) == 2:
        with open("sub_server_info.txt", "a") as sub_server_info_File:
            entry = client_message.decode()
            sub_server_info_File.write(entry + "\n")
            print("Sub Server info Received:", client_message.decode())
    elif check_format_of_sub_server_msg(client_message.decode()) == 4:
        with open("clients_records.txt", "a") as clients_records_File:
            entry = client_message.decode()
            clients_records_File.write(entry + "\n")
            print("Sub Server Message Received\nClient Record:", client_message.decode())
    else:
        print("\nSub_server with socket", client_sock, "msg format is not correct!!!")

    # Close the socket
    client_sock.close()

def get_sub_server_info(test_name):
    info = ""
    with open("sub_server_info.txt", "r") as fp:
        flag = 0
        for line in fp:
            if line.startswith(test_name):
                info = line.rstrip()
                flag = 1
                break
    return info

def client_thread_func(client_sock):
    print("starting client_thread_func")

    server_message = "Please Enter your Test option\nScience\nMath\nEnglish\n\n"
    client_message = bytearray(2000)

    # Send the message to the client
    client_sock.send(server_message.encode())

    # Receive the message from the client
    bytes_received = client_sock.recv_into(client_message)

    if bytes_received < 0:
        print("client_thread_func Receive Failed. Error!!!!!")
        return

    print("client_thread_func Client Sock:", client_sock)
    print("client_thread_func Client Message:", client_message.decode())

    server_message = get_sub_server_info(client_message.decode())
    if not server_message:
        server_message = "Invalid Input!!!"

    # Send the message back to the client
    client_sock.send(server_message.encode())

    # Close the socket
    client_sock.close()

def sub_server_func(sub_socket_desc):
    print("starting sub_server_func")
    while True:
        # Accept incoming connections
        client_sock, _ = sub_socket_desc.accept()

        thread4 = threading.Thread(target=sub_server_thread_func, args=(client_sock,))
        thread4.start()

        client_addr = client_sock.getpeername()
        print("1-Client Connected with IP:", client_addr[0], "and Port No:", client_addr[1])

def client_func(socket_desc):
    print("starting client_func")
    while True:
        # Accept incoming connections
        client_sock, _ = socket_desc.accept()

        thread3 = threading.Thread(target=client_thread_func, args=(client_sock,))
        thread3.start()

        client_addr = client_sock.getpeername()
        print("1-Client Connected with IP:", client_addr[0], "and Port No:", client_addr[1])

def main():
    socket_desc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sub_socket_desc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_addr = ("127.0.0.1", 2000)
    sub_server_addr = ("127.0.0.1", 2001)

    socket_desc.bind(server_addr)
    sub_socket_desc.bind(sub_server_addr)

    socket_desc.listen(1)
    sub_socket_desc.listen(1)

    print("Listening for Incoming Connections.....")
    print("Sub Listening for Incoming Connections.....")

    thread1 = threading.Thread(target=sub_server_func, args=(sub_socket_desc,))
    thread1.start()

    thread2 = threading.Thread(target=client_func, args=(socket_desc,))
    thread2.start()

    thread1.join()
    thread2.join()

    socket_desc.close()

if __name__ == "__main__":
    main()
