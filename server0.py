# -*- coding: utf-8 -*-
"""


@author: User
"""

import socket
import ssl
from datetime import datetime
import time

PORT = 12009
SERVER = socket.gethostname()
FORMAT="utf-8"

addr = (SERVER, PORT)


try:
    server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #here we are binding our server with the host which is the local host name of the machine and the port
    server.bind(addr)
    print("socket initialized and binded ")

    
except:
    print("[] unable to initialize socket")
    
    
server.listen(1)
print(f"Server is listening on port {PORT}...")

# Accept an incoming connection and handle it
while True:
    #store in client_socket the new socket object returned 
    #store in client_address the IP type string and the port type integer in a tuple 
    client_socket, client_address = server.accept()
    print(f"Received connection from {client_address}")
    
    #convert it to string
    ip_address = client_socket.recv(1024).decode().strip()
    #received the request
    requestt_time = time.time()
    # Convert the current time to a human-readable string
    formatted_timee = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(requestt_time))
    # Print the formatted time
    print("Request received from client at:", formatted_timee)
    print("the IP adress is"+ip_address)
    print("now we will connect and get the time from the site")
    
    try:
        # Connect to the specified IP address using SSL
        website_socket = ssl.wrap_socket(socket.socket())
        # the port 443 is for HTTPS
        website_socket.connect((ip_address, 443))
        
        # Send an HTTP GET request to the IP address
        # the request is specified as a string with the website name
        #request for HTML response
        request = "GET / HTTP/1.1\r\nHost: time.is\r\n\r\n"
        #then we encoded to bytes and send it
        website_socket.sendall(request.encode())
        
        
        #send the request
        sendd_time = time.time()
        # Convert the current time to a human-readable string
        formatted_timeee = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sendd_time))
        # Print the formatted time
        print("Request sent to the site at:", formatted_timee)
        
        # Receive the response from the IP address
        #initialize the response of type bytes
        response = b""
        
        #the while loop is used to receive the data
        #data will be received into chunks of 1024 bytes
        #it will break when all the data is received
        while True:
            data = website_socket.recv(1024)
            if not data:
                break
            response += data
            
        #received the request
        requesttt_time = time.time()
        # Convert the current time to a human-readable string
        formatted_timeeee = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(requesttt_time))
        # Print the formatted time
        print("Request received from the site at:", formatted_timeeee)
         
         
        # Parse the HTML content to get the current time
        #convert it to string with the decode
        html_content = response.decode()
        #then we search for this string which appears at the location of the current time
        #the find method searches for the first occurence of the string
        #we add to it the lenght of the string to have the start index
        start_index = html_content.find("<div id=\"twd\">") + len("<div id=\"twd\">")
        #starting from the start index it searches for the occurence of the string after the time
        end_index = html_content.find("</div>", start_index)
        #having the html in type string we extract the time which is between start and end previously found
        time_string = html_content[start_index:end_index].strip()
        #we convert the string to a datetime object, hours minutes and secondes
        time = datetime.strptime(time_string, "%H:%M:%S")
        
        # Send the time to the client
        #change the response to string with PM/AM and then encode to bytes to send it to the client
        response = time.strftime("%I:%M:%S %p").encode()
        
        print("Time string extracted from web page:", time_string)
        print("Formatted current time:", time.strftime("%I:%M:%S %p"))
        
        client_socket.sendall(response)
        
        #received the request
        senddd_time = time.time()
        # Convert the current time to a human-readable string
        formatd_timee = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sendd_time))
        # Print the formatted time
        print("Request sent for client at:", formatd_timee)
        
    except:
        # Send an error message to the client if the time could not be obtained
        error_message = "Could not obtain the time."
        client_socket.sendall(error_message.encode())
        
    client_socket.close()