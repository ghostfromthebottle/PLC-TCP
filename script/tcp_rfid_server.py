import socket
import threading

carriers_dict = dict(
	rfid1=0,
	rfid2=0,
	rfid3=0,
	rfid4=0,
	rfid5=0,
	rfid6=0,
	rfid7=0,
	rfid8=0,
	rfid9=0,
	rfid10=0,
	rfid11=0,
	rfid12=0,
	rfid13=0
	)
FINAL_STATE = 50

#IP = '172.20.66.156'
IP = 'localhost'
PORT = 60104
BUFFER_SIZE = 4096

def save_carrier_states():
	fileHandle = open('carrier_states.txt', 'w')
	for i in carriers_dict:
		fileHandle.write(str(carriers_dict[i])+'\n')
	fileHandle.close()

def load_carrier_states():
	try:
		fileHandle = open('carrier_states.txt', 'r')
		for i in carriers_dict:
			value = int(fileHandle.readline())
			if value:
				carriers_dict[i] = value
		fileHandle.close()
	except Exception as e:
		raise e

def carrier_logic(rfid):
	command = carriers_dict.get(rfid,999)
	if not command == 999 and not command == FINAL_STATE:
		carriers_dict[rfid] += 1
	else:
		print 'Invalid RFID: {}'.format(rfid)

	print 'Sending command: {}'.format(command)
	print 'DICT: {}'.format(carriers_dict)
	return str(command)

def handle_client_connection(client_s,):
	rfid = 'rfid'
	while True:
		data_in = client_s.recv(BUFFER_SIZE)
		if not data_in: break
		rfid += data_in
	print 'Received: {}'.format(rfid)
	cmd = carrier_logic(rfid)
	client_s.send(cmd)
	client_s.shutdown(1)
	client_s.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP,PORT))
s.listen(1)

print 'Listening on {}:{}'.format(IP,PORT)

try:
	load_carrier_states()
	while True:
		conn, client_addr = s.accept()
		print 'Accepted connection from {}:{}'.format(client_addr[0], client_addr[1])
		client_handler = threading.Thread(target=handle_client_connection, args=(conn,))
		client_handler.start()
		#client_handler.join()
finally:
	save_carrier_states()
	s.shutdown(2)
	s.close()