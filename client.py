import socket
import server
from threading import Thread
from time import sleep

class Client():
	def __init__(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect(('localhost', 1337))
		print('[CLIENT] Connexion')

	def read(self, buffSize = 1024):
		text = self.s.recv(buffSize)
		text.decode()
		return str(text)

class ClientServ(Client):

	def __init__(self):
		Client.__init__(self)
		self.server = None

	def startServ(self, port):
		self.server = Server(port)

	def endServ(self):
		pass

	def statusServ(self):
		pass

c = Client()
while True:
	print(c.read(100000))
	pos = '0;200;621'
	c.s.send(pos.encode())
	sleep(0.01)