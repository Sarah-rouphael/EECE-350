# -*- coding: utf-8 -*-
"""
Sarah Rouphael
ID 202100451

Note that in this file the client will enter the IP adress of time.is
and he will receive the current time

"""

from socket import *
import time
import uuid

#user enter the IP adress of time.is
serverName = input("Enter the IP address of the site please:")

#specifying the port
serverPort = 12009


try:
    #creating a socket an use try and except in case the socket won't connect
    clientSocket = socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
except:
    print("[] unable to connect")
    
    
    
try:
    
  
    
    #use sendall instead of send because it sends all the data at once and the encode is to convert the data to bytes
    clientSocket.sendall(serverName.encode())
    #the request is going to be sent to the server so we get the time and print it
    request_time = time.time()
    # Convert the current time to a human-readable string
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(request_time))
    # Print the formatted time
    print("Request sent at:", formatted_time)
    print("the IP adress has been sent you will soon get the current time")
    
except:
    print("[] your input is invalid rerun the program")
    

    
#this is the response of the server  
#decode is used to convert from bytes to string and the .strip is used to remove spaces  
response = clientSocket.recv(1024).decode().strip()

#take the time after the message is received
received_time = time.time()
# Convert the current time to a human-readable string
formatted_time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(received_time))
# Print the formatted time
print("Request received at:", formatted_time1)
print(f"Round-trip time: {received_time - request_time:.3f} seconds")
print( "From Server:", response)

#mac address from google 
mac_address = uuid.getnode()
mac_bytes = [format((mac_address >> i) & 0xff, '02x') for i in range(0, 48, 8)]
mac_address_formatted = ':'.join(mac_bytes)
print("Physical MAC address: " + mac_address_formatted)

clientSocket.close()