This is a hierarchial Domain Name Server(DNS) System, with a root DNS Server, top level domain DNS Servers,
authoritative DNS Servers and a Client Server. .With the help of socket library functions, communication pathway 
amongst the servers and the client are established through UDP sockets.The system responds to client's queries with the corresponding IP addresses or respective error messages.

The commands for compiling the program are:

 So at first we will start the script and it would start recording that would  
 be done in terminal
        -- script script_file.txt
 Then for running the code 
        -- Client_Server.py startportnumber input_file

So upon compiling the program, It asks for the input i.e domain name which is in the format xxx.yyy.zzz.
If any of the given input is not in that format then it asks for the user to give the correct inputs.
If the given input domain name is present in the given input file it gives the respective domain name or else it would print "Not Found".
If the user enters bye then every server gets closed and every child program gets terminated.

The querys and the responses of each server through out the given inputs are stored in their respective output files.

A sample input and the respective output files are attached.
