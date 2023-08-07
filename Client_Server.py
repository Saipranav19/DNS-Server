
######################

# NAME: Kodari Saipranav Reddy
# Roll Number: CS20B040
# Course: CS3205 Jan. 2023 semester
# Lab number: 2
# Date of submission: Jan 3,2023
# I confirm that the source file is entirely written by me without
# resorting to any dishonest means.
# Website(s) that I used for basic socket programming code are:
# URL(s): NA

########################

import socket 
import os
import signal
import sys
import fileinput
import time
import multiprocessing

num1=2 #number of top-level domain
num2=3 #number of ADS servers per top-level domain

K=int(sys.argv[1])
filename=sys.argv[2]
f=open(filename,'r')
IP_map=dict()
ADS_map=dict()
#taking k and file as inputs

while(True):
    x=f.readline().strip()
    if x=='BEGIN_DATA':
        for i in range(10):
            y=f.readline().split()
            IP_map[y[0]]=y[1]
    elif x=="List_of_ADS1":
        for i in range(5):
            y=f.readline().split()
            IP_map[y[0]]=y[1]
            z=y[0].split('.')
            ADS_map[z[1]]=1
    elif x=="List_of_ADS2":
        for i in range(5):
            y=f.readline().split()
            IP_map[y[0]]=y[1]
            z=y[0].split('.')
            ADS_map[z[1]]=2
    elif x=="List_of_ADS3":
        for i in range(5):
            y=f.readline().split()
            IP_map[y[0]]=y[1]
            z=y[0].split('.')
            ADS_map[z[1]]=3
    elif x=="List_of_ADS4":
        for i in range(5):
            y=f.readline().split()
            IP_map[y[0]]=y[1]
            z=y[0].split('.')
            ADS_map[z[1]]=4
    elif x=="List_of_ADS5":
        for i in range(5):
            y=f.readline().split()
            IP_map[y[0]]=y[1]
            z=y[0].split('.')
            ADS_map[z[1]]=5
    elif x=="List_of_ADS6":
        for i in range(5):
            y=f.readline().split()
            IP_map[y[0]]=y[1]
            z=y[0].split('.')
            ADS_map[z[1]]=6
    elif x=="END_DATA":
        break
#segregating the file contents into ip_addresses and an ADS_map for matching it into respective ADS Server

RDSpointer=open("RDS.output",'w')
NRpointer=open("NR.output",'w')
TLDpointer=open("TDS.output",'w')
ADSpointer=open('ADS.output','w')

#opening the output files

#RDS Server Process
pid=os.fork()

if pid==0:
    RDS_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    RDS_socket.bind(("127.0.0.1",K+54))
    #creating and binding RDS socket

    while(True):
        data,addr=RDS_socket.recvfrom(1024)

        if data.decode()=="bye":
            A1=("127.0.0.1",K+55)
            A2=("127.0.0.1",K+56)
            RDS_socket.sendto(data,A1)
            RDS_socket.sendto(data,A2)
            RDS_socket.close()
            RDSpointer.write(f'Query received : {data.decode()}\nResponse sent : {data.decode()}\n')
            exit()
            #In the case of bye it sends bye command to both the TDS servers and exits
        else:
            temp=data.decode().strip().split('.')
            buffer=" "
            if temp[2]=='com':
                msg='127.0.0.1' + ' ' + str(K+55)
                buffer=IP_map['TDS_com']
            elif temp[2]=="edu":
                msg='127.0.0.1' + ' ' + str(K+56)
                buffer=IP_map['TDS_edu']
            else: 
                msg="Not Found"
                buffer=msg

            RDSpointer.write(f'Query received : {data.decode()}\nResponse sent : {buffer}\n\n')
            #It checks the last keyword .com or .edu and sends respective ip address to the local server and also writes into the file
        
            RDS_socket.sendto(msg.encode(),addr)


#TDS Server process

#TDS1

pid=os.fork()

if pid==0:
    time.sleep(1)
    TDS_sock1=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    TDS_sock1.bind(("127.0.0.1",K+55))
    #creating and binding TDS socket 1

    while(True):
        
        data,addr=TDS_sock1.recvfrom(1024)

        if data.decode()=="bye":
            A11=("127.0.0.1",K+57)
            A12=("127.0.0.1",K+58)
            A13=("127.0.0.1",K+59)
            TDS_sock1.sendto(data,A11)
            TDS_sock1.sendto(data,A12)
            TDS_sock1.sendto(data,A13)
            TDS_sock1.close()
            g="bye"+'\n'
            TLDpointer.write(f'Query received : {g}Response sent : {g}\n')
            ADSpointer.write(f'Query received : {g}Response sent : {" "}\n\n')
            exit()
            #sending the command bye to the three ADS servers and exits in the case of bye
        else:
            msg="Not Found"
            buffer=msg
           
            temp=data.decode().strip().split('.')

            if ADS_map.get(temp[1]) is not None:

                if ADS_map[temp[1]]==1:
                    msg='127.0.0.1' + ' ' + str(K+57)
                    buffer=IP_map["ADS1"]
                elif ADS_map[temp[1]]==2:
                    msg='127.0.0.1' + ' ' + str(K+58)
                    buffer=IP_map["ADS2"]
                elif ADS_map[temp[1]]==3:
                    msg='127.0.0.1' + ' ' + str(K+59)
                    buffer=IP_map["ADS3"]
            else:
                msg="Not Found"
                buffer=msg
          
            TDS_sock1.sendto(msg.encode(),addr)
            TLDpointer.write(f'Query received : {data.decode()}\nResponse sent : {buffer}\n\n')
            #checking the middle keyword and gives respective ip address and sends it to the local server and also writes in the tld output file

#TDS2

pid=os.fork()

if pid==0:
    time.sleep(2)
    TDS_sock2=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    TDS_sock2.bind(("127.0.0.1",K+56))
    #creating and binding TDS socket 2

    while(True):
        data,addr=TDS_sock2.recvfrom(1024)

        if data.decode()=="bye":
            A21=("127.0.0.1",K+60)
            A22=("127.0.0.1",K+61)
            A23=("127.0.0.1",K+62)
            TDS_sock2.sendto(data,A21)
            TDS_sock2.sendto(data,A22)
            TDS_sock2.sendto(data,A23)
            TDS_sock2.close()
            #similarly sending bye command to all the ADS servers and it exits
            exit()
        else:
            msg="Not Found"
            buffer=msg 
          
            temp=data.decode().strip().split('.')

            if ADS_map.get(temp[1]) is not None:

                if ADS_map[temp[1]]==4:
                    msg='127.0.0.1' + ' ' + str(K+60) 
                    buffer=IP_map['ADS4']
                elif ADS_map[temp[1]]==5:
                    msg='127.0.0.1' + ' ' + str(K+61)
                    buffer=IP_map['ADS5']
                elif ADS_map[temp[1]]==6:
                    msg='127.0.0.1' + ' ' + str(K+62)
                    buffer=IP_map['ADS6']
            else:
                msg="Not Found"
                buffer=msg
            
            TDS_sock2.sendto(msg.encode(),addr)
            TLDpointer.write(f'Query received : {data.decode()}\nResponse sent : {buffer}\n\n')
            #respective ip address is sent to the local host and the data is written into the file 

        
#ADS Server process

for i in range(num1):
    for j in range(num2):
        
        pid=os.fork()

        if pid==0:
          
          ADS_sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
          ADS_sock.bind(("127.0.0.1",K+57+(i*num2)+j))
          #creating and binding all the six ADS Servers

          while(True):
            
            data,addr=ADS_sock.recvfrom(1024)

            if data.decode()=="bye":
                ADS_sock.close()
                exit()
                #If there is a bye statement then it closes the server and exits
            else:
                msg="Not Found"
                buffer=msg
              
                if IP_map.get(data.decode()) is not None:
                    #If the respective domain name is present in then it is accessed or else msg would be not found
                    msg=IP_map[data.decode()]
                    buffer=msg
                else: 
                    msg="Not Found"
                    buffer=msg

                ADS_sock.sendto(msg.encode(),addr)
                ADSpointer.write(f'Query received : {data.decode()}\nResponse sent : {buffer}\n\n')
                #sending the reply to the local server and appending the ADS.output file
          exit()

pid=os.fork()

#NR Server process
if pid==0:  
    NR_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    NR_socket.bind(("127.0.0.1",K+53))
    #creating and binding the NR/local Server

    time.sleep(3)

    while(True):

        msg,addr=NR_socket.recvfrom(1024)
        
        if msg.decode()=="bye":
            A=("127.0.0.1",K+54)
            NR_socket.sendto(msg,A)
            NR_socket.close()
            NRpointer.write(f'Query received : {msg.decode()}\nResponse sent : {msg.decode()}\n')
            exit()
            #In the case of bye it sends the bye message to root and it gets closed
        
        else:
            #with RDS

            addressport1=("127.0.0.1",K+54)
            NR_socket.sendto(msg,addressport1)

            NRpointer.write(f'Query received : {msg.decode()}\nResponse sent : {msg.decode()}\n\n')
            #At first it sends the req to RDS Server and gets an ip address of respective TDS server

            data_rds,addr_rds=NR_socket.recvfrom(1024)
            temp_rds=data_rds.decode()
            
            buffer=" "
            if temp_rds=="Not Found":
                NR_socket.sendto(temp_rds.encode(),addr)
                buffer="Not Found"
                NRpointer.write(f'Query received : {buffer}\nResponse sent : {buffer}\n\n')
                continue
                #If thats not found then we will send not found directy to the client server
            
            else:
                temp_rds1=temp_rds.strip().split()
                addressport2=(temp_rds1[0],int(temp_rds1[1]))
                NR_socket.sendto(msg,addressport2)
                #Or else it will take the address from the rds and contacts ths respective tld 

                yp=msg.decode().split('.')
                if yp[2]=='com':
                    buffer=IP_map['TDS_com']
                else: buffer=IP_map['TDS_edu']
            
            NRpointer.write(f'Query received : {buffer}\nResponse sent : {msg.decode()}\n\n')
            #and then the response received and sent are printed into the NR.output file

            #with TLD
            data_tld,addr_tld=NR_socket.recvfrom(1024)
            temp_tld=data_tld.decode()
           
            buffer=" "
            if temp_tld=="Not Found":
                 NR_socket.sendto(temp_tld.encode(),addr)
                 buffer="Not Found"
                 NRpointer.write(f'Query received : {buffer}\nResponse sent : {buffer}\n\n')
                 continue
                #If thats not found the similarly it would send the msg directly to the client
            
            else:
                temp_tld1=temp_tld.strip().split()
                addressport3=(temp_tld1[0],int(temp_tld1[1]))
                NR_socket.sendto(msg,addressport3)

                yp=msg.decode().split('.')
                if ADS_map[yp[1]]==1:
                    buffer=IP_map['ADS1']
                elif ADS_map[yp[1]]==2:
                    buffer=IP_map['ADS2']
                elif ADS_map[yp[1]]==3:
                    buffer=IP_map['ADS3']
                elif ADS_map[yp[1]]==4:
                    buffer=IP_map['ADS4']
                elif ADS_map[yp[1]]==5:
                    buffer=IP_map['ADS5']
                elif ADS_map[yp[1]]==6:
                    buffer=IP_map['ADS6']
                
            NRpointer.write(f'Query received : {buffer}\nResponse sent : {msg.decode()}\n\n')
            #Then TLD would give an address port it contact it for further information and updates its output file

            #with ADS
            data_ads,addr_ads=NR_socket.recvfrom(1024)
            temp_ads=data_ads.decode().strip()

            NRpointer.write(f'Query received : {data_ads.decode()}\nResponse sent : {data_ads.decode()}\n\n')
            #At last ADS would send the final ipaddress it sends it to the client

            NR_socket.sendto(temp_ads.encode(),addr)

#client
time.sleep(4)
Clientserver=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#creating client socket
t1=0
while(True):
    msg=input("Enter Server Name: ")
    
    if len(msg.split('.'))!=3:
        if len(msg.split('.'))==1 and msg=='bye':
            addressport=("127.0.0.1.",K+53)
            Clientserver.sendto(msg.encode(),addressport)
            print("All Server Processes are killed. Exiting.")
            Clientserver.close()
            t1+=1
            #In the case of bye, the server first sends the bye command to the NR Server and gets closed
            break
        else:
            print("Give proper inputs")
            #If any input is not in the proper format it asks for a proper one!
    else:
        addressport=("127.0.0.1",K+53)
        Clientserver.sendto(msg.encode(),addressport)

        ans,addr=Clientserver.recvfrom(1024)

        print("DNS Mapping:",ans.decode())
        #Else it sends the req to NR Server and receives the respective IP_ADDRESS

#many sleeps are written so that by the time user sends a req, every server needs to be active

if t1>0:

    children_active=multiprocessing.active_children()
    for child in children_active:
        child.terminate()
    
    for child in children_active:
        child.join()

    NRpointer.close()
    RDSpointer.close()
    TLDpointer.close()
    ADSpointer.close()
    #closing all the opened files and then exiting the program
    exit()

