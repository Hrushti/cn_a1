# import modules
import socket 
import os
import os.path as path
import crypto_c as crypto

# create socket
c = socket.socket()
port = 4000
c.connect(('localhost', port)) 

# client_dir, the folder where all files will be downloaded
# to/uploaded from the client side, this directory is fixed.
client_dir = 'C:/Users/hrush/Documents/Acads/Sem_7/cn/assignments/cn_a1/p1/client/'        

while True:
	inputs = input().split(' ')
	command = inputs[0].casefold()
	c.send(command.encode())

	# get working directory of server
	if command == 'cwd':
		print(c.recv(1024).decode())
		print()

	# get list of files on server's folder
	elif command == 'ls':
		file_list = c.recv(1024).decode().split("$")
		print(file_list)
		print()

	# change server's working directory to one mentioned by user
	# returns NOK if error, OK if changed
	elif command == 'cd':
		new_dir = inputs[1]
		c.send(new_dir.encode())
		print(c.recv(1024).decode())
		print()
			
	# download file on server to client
	elif command == 'dwd':
		# should only contain name of file, with extension, not subfolders
		filename = inputs[1]
		encryptmode = '-pt'
		try:
			encryptmode = inputs[2]
		except:
			if encryptmode != '-pt' or encryptmode != '-sb' or encryptmode != 'tp':
				encryptmode = '-pt'

		c.send(encryptmode.encode())
		c.send(filename.encode())

		# receives NOK if some problem with downloading file
		err = c.recv(1024).decode()

		if err == 'OK':
			filedir = path.join(client_dir, filename)
			with open(filedir, 'wb') as writefile:
				filedata = c.recv(1024)
				if not filedata:
					err = 'NOK'
					break
				writefile.write(filedata)
			writefile.close()
			if encryptmode == '-sb':
				crypto.substitute_decode(filedir)
			elif encryptmode == '-tp':
				crypto.transpose(filedir)
			elif encryptmode == '-pt':
				crypto.plain_text(filedir)
			print(err)
		elif err == 'NOK': print(err)

		# upload file on client to server
	elif command == 'upd':
		# should only contain name of file, with extension, not subfolders
		filename = inputs[1]
		encryptmode = '-pt'
		try:
			encryptmode = inputs[2]
		except:
			if encryptmode != '-pt' or encryptmode != '-sb' or encryptmode != 'tp':
				encryptmode = '-pt'

		c.send(encryptmode.encode())
		c.send(filename.encode())

		filedir = path.join(client_dir, filename)
		if (path.isfile(filedir) == False):
			print('NOK')
			print()
		else:
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
			print('OK')
			print()

			if encryptmode == '-sb':
				crypto.substitute_decode(filedir)
			elif encryptmode == '-tp':
				crypto.transpose(filedir)
			elif encryptmode == '-pt':
				crypto.plain_text(filedir)

	elif command == 'exit':
		break
		
	else:
		print('invalid command, type exit to quit')
	
# close the connection
c.close()
