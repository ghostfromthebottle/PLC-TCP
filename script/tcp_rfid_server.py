import socket
import threading

carriers_dict = dict()

IP = '172.20.66.156'
PORT = 60106
BUFFER_SIZE = 4096

def carrier_logic(rfid):
	command = carriers_dict.get(rfid,0)
	if command:
		carriers_dict[rfid] += 1
	else:
		carriers_dict[rfid] = 1;
	print 'Sending command: {}'.format(command)
	return str(command)

def handle_client_connection(client_s,): 
	rfid = 'rfid' + client_s.recv(BUFFER_SIZE)
	print 'Received: {}'.format(rfid)
	client_s.send(carrier_logic(rfid))
	client_s.shutdown(1)
	client_s.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP,PORT))
s.listen(2)
print 'Listening on {}:{}'.format(IP,PORT)

try:
	while True:
		conn, client_addr = s.accept()
		print 'Accepted connection from {}:{}'.format(client_addr[0], client_addr[1])
		client_handler = threading.Thread(target=handle_client_connection, args=(conn,))
		client_handler.start()
finally:
	s.shutdown(2)
	s.close()