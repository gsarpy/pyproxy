#! /usr/bin/env python

import socket, sys
from _thread import *

try:
    listening_port = int(input("[*] Enter Port Number to Listen on: "))

except KeyboardInterrupt:
    print("\n\n\n[*] Interruption requested by user!")
    print ("\n[*] Proxy server is now exiting...")
    sys.exit()

# Max connections to hold
max_conn = 5
# Max socket buffer
buffer_size = 4096

def start():
    try:
        # Activate socket
        active_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the listening port
        active_socket.bind(('', listening_port))
        active_socket.listen(max_conn)

        print("[*] Initializing sockets!........ Done")
        print("[*] Sockets successfully binded.....")
        print("Server started successfully..... [ %d ]\n" % (listening_port))
    except Exception:
        # If the server/socket fails throw an error
        print("[!] ERROR: Unable to initialize socket/server!")
        sys.exit(2)

    while 1:
        try:
            # Accept the connection stream from the client
            connection_stream, address = active_socket.accept()
            # Accept data from client
            data = connection_stream.recv(buffer_size)
            
            start_new_thread(connection_string, (connection_stream, data, address))
        except KeyboardInterrupt:
            # If client socket fails error and close the socket
            active_socket.close()
            print("\n[!] Proxy shutting down...")
            print("\n[!] Thanks for proxying your requests through me!")
            sys.exit(1)
    active_socket.close()

def connection_string(connection_stream, data, address):
    try:
        first_line = data.split('\n')[0]

        url = first_line.split(' ')[1]

        # Get the position of ://
        http_position = url.find("://")
        if (http_position == -1):
            temp = url
        else:
            # Get the rest of the URl
            temp = url[(http_position+3):]

        # Find the position of the port if there is one
        port_position = temp.find(":")
        
        webserver_position = temp.find("/")
        if webserver_position == -1:
            webserver_position = len(temp)

        webserver = ""
        port = -1
        if (port_position == -1 or webserver_position < port_position):
            port = 80
            webserver = temp[:webserver_position]
        else:
            # Set supplied port
            port = int((temp[(port_position+1):])[:webserver_position-port_position-1])
            webserver = temp[:port_position]
        
        proxy_server(webserver, port, connection_stream, address, data)
    
    except Exception:
        pass


def proxy_server(webserver, port, connection_stream, client_data, address):
    print("Trying Proxy Connection")
    try:
        active_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        active_socket.connect((host, port))
        socket.send(client_data)

        while 1:
            # Read reply from client data
            reply = active_socket.recv(buffer_size)
            
            if (len(reply) > 0):
                # Send the reply back to the client
                connection_stream.send(reply)
                
                # Send the response to the proxy server
                relay = float(len(reply))
                relay = float(relay / 1024)
                relay = "%.3s" % (str(relay))
                relay = "%s KB" % (relay)
                'Print a custom message for request complete'
                print("[*] Request completed: %s => %s <=" % (str(address[0]), str(relay)))
            else: 
                print("Error receiving data. Breaking connection!")
                break
        # Close the socket once complete
        active_socket.close()

        connection_stream.close()
    except socket.error (value, message):
        active_socket.close()
        connection_stream.close()
        sys.exit(1)



            
start()            
