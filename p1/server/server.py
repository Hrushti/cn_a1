# import modules
import socket  
import os   
import os.path as path
import crypto_s as crypto
 
s = socket.socket()        
print ("socket created")

port = 4040             

s.bind(('localhost', port))        
print ("socket binded to %s" %(port))
 
s.listen(5)    
print ("socket is listening")  

c, addr = s.accept()
print ('connection to:', addr )

curr_dir = os.getcwd()

while True:
    inputs = c.recv(1024).decode()

    # send current working directory
    if (inputs.casefold() == 'CWD'.casefold()):
        c.send(curr_dir.encode())

    # send list of files and folders present
    elif (inputs.casefold() == 'LS'.casefold()):
        str = ""
        dir_list = os.listdir(curr_dir)
        for file in dir_list:
            str += file
            str += "$"
        str = str[:-1]
        c.send(str.encode())

    # change current working directory
    elif (inputs.casefold() == 'CD'.casefold()):
        path = c.recv(1024).decode()
        try:
            os.chdir(path)
            curr_dir = os.getcwd()
            c.send('OK'.encode())
        except:
            c.send('NOK'.encode())
    
    # send file (encoded) -> 
    elif (inputs.casefold() == "DWD".casefold()):
        encryptmode = c.recv(1024).decode()
        filename = c.recv(1024).decode()
        serverdir = os.path.join('C:/Users/hrush/Documents/Acads/Sem_7/cn/assignments/cn_a1/p1/server/')
        filedir = path.join(serverdir, filename)
        file_exists = path.isfile(filedir)
        if (file_exists == False):
            c.send('NOK'.encode())
            continue
        else:
            c.send('OK'. encode())
        
        if encryptmode == '-sb':
            crypto.substitute_encode(filedir)
        elif encryptmode == '-tp':
            crypto.transpose_encode_decode(filedir)
        else:
            continue

        with open(filedir, 'rb') as file_to_send:
            for data in file_to_send:
                c.sendall(data)
        os.remove(filedir)
    
    # receive file
    elif (inputs.casefold() == "UPD".casefold()):
        encryptmode = c.recv(1024).decode()
        
        downloadDir = "C:/Users/hrush/Documents/Acads/Sem_7/cn/assignments/cn_a1/p1/server/"
        filename = c.recv(1024).decode()
        filedir = path.join(downloadDir, os.path.basename(filename))
        with open(filedir, 'wb') as file_to_write:
            data = c.recv(1024)
            if not data:
                break
            file_to_write.write(data)
        file_to_write.close()
        if encryptmode == '-sb':
            crypto.substitute_encode(filedir)
        elif encryptmode == '-tp':
            crypto.transpose_encode_decode(filedir)
        else:
            continue
    
    # invalid input, close connection and exit
    else:
        c.send('error'.encode())
        c.close()
