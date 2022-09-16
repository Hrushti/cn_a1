# import modules
import socket 
import os 
import os.path as path
import crypto_s as crypto

s = socket.socket()  
print ("socket created")

port = 4000   

s.bind(('localhost', port))  
print ("socket binded to %s" %(port))
 
s.listen(5) 
print ("socket is listening") 

c, addr = s.accept()
print ('connection to:', addr )

server_dir = os.getcwd()

while True:
  command = c.recv(1024).decode()

  # send server_dir
  if command == 'cwd':
    c.send(server_dir.encode())

  # send list of files on server_dir
  elif command == 'ls':
    sendstring = ''
    filelist = os.listdir(server_dir)
    for file in filelist:
      sendstring += file + '$'
    sendstring = sendstring[:-1]
    c.send(sendstring.encode())
    
  # change server_dir
  elif command == 'cd':
    new_dir = c.recv(1024).decode()
    try:
      os.chdir(new_dir)
      server_dir = os.getcwd()
      c.send('OK'.encode())
    except:
      c.send('NOK'.encode())

  # send file from server to client
  elif command == 'dwd':
    encryptmode = c.recv(1024).decode()
    filename = c.recv(1024).decode()
    filedir = path.join(server_dir, filename)

    if path.isfile(filedir):
      err = 'OK'
      c.send(err.encode())
      if encryptmode == '-sb':
        crypto.substitute_encode(filedir)
      elif encryptmode == '-tp':
        crypto.transpose(filedir)
      elif encryptmode == '-pt':
        crypto.plain_text(filedir)
        
      with open(filedir, 'rb') as readfile:
        for filedata in readfile:
          c.sendall(filedata)
      readfile.close()

      if encryptmode == '-sb':
        crypto.substitute_decode(filedir)
      elif encryptmode == '-tp':
        crypto.transpose(filedir)
      elif encryptmode == '-pt':
        crypto.plain_text(filedir)

    else: err = 'NOK'; c.send(err.encode())

  # receive file from server
  elif command == 'upd':
    encryptmode = c.recv(1024).decode()
    filename = c.recv(1024).decode()
    filedir = path.join(server_dir, filename)

    with open(filedir, 'wb') as writefile:
      filedata = c.recv(1024)
      if not filedata:
        break
      writefile.write(filedata)
    writefile.close()
    
    if encryptmode == '-sb':
      crypto.substitute_encode(filedir)
    elif encryptmode == '-tp':
      crypto.transpose(filedir)
    elif encryptmode == '-pt':
      crypto.plain_text(filedir)
    
  elif command == 'exit':
    c.close()
    
  else: 
    continue
# close the connection
s.close()
