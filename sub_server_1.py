import socket
import threading

def send_msg_to_main_server(msg):
    try:
        server_ip = "127.0.0.1"
        server_port = 2001
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))

        client_socket.sendall(msg.encode())
        client_socket.close()
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return -1

def client_thread_func(client_sock, client_addr):
    try:
        print("Starting client_thread_func")
        
        client_ip = client_addr[0]
        client_port = client_addr[1]

        print(f"Socket: {client_sock}")
        print(f"Port: {client_port}")
        print(f"IP: {client_ip}")
        print(f"malloc: {client_sock}")

        test_type = "Enter your test type:\nGeometry\nAlgebra\nIQ\n"

        client_sock.send(test_type.encode())
        
        client_message = client_sock.recv(2000).decode()
        print(f"Client Sock: {client_sock}")
        print(f"Client Message: {client_message}")

        server_message = ""
        port_buffer = str(client_port)

        if client_message in ["Geometry", "Algebra", "IQ"]:
            server_message = f"{client_ip},{port_buffer},Math,{client_message},20"
        else:
            server_message = "Invalid Input!!!"

        client_sock.send(server_message.encode())
        
        if send_msg_to_main_server(server_message) == -1:
            return -1
        
        client_sock.close()
    except Exception as e:
        print(f"Error: {e}")
        return -1

def set_connection_for_clients(my_ip, my_port):
    try:
        server_ip = my_ip
        server_port = int(my_port)
        
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((server_ip, server_port))
        server_socket.listen(1)
        
        print("Socket Created")
        print("Bind Done")
        print("Listening for Incoming Connections.....")
        
        while True:
            client_sock, client_addr = server_socket.accept()
            print(f"Client Connected with IP: {client_addr[0]} and Port No: {client_addr[1]}")
            
            client_thread = threading.Thread(target=client_thread_func, args=(client_sock, client_addr))
            client_thread.start()
    
        server_socket.close()
    except Exception as e:
        print(f"Error: {e}")
        return -1

def main():
    msg = "Math,127.0.0.1,2020"
    
    if send_msg_to_main_server(msg) == -1:
        return -1
    
    set_connection_for_clients("127.0.0.1", "2020")

if __name__ == "__main__":
    main()
