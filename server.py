import socket
import select
from threading import Thread

class Server():

	def __init__(self, port, map, nbMax):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.s.bind(("",port))
		self.s.listen(5)

		self.start = False
		self.clients = []
		self.map = map
		self.nbMax = nbMax
		self.clientsSocket = []
		self.players = -1

		self.pos = []

	def waitForPlayers(self):
		while (len(self.clients) < self.nbMax and self.start == False):
			(clientSocket, (ip, port)) = self.s.accept()
			self.clients.append(SocketClient(ip, port, clientSocket))
			self.clientsSocket.append(clientSocket)
			self.players += 1
			self.clients[-1].run(str(self.players))
			print('[SERV] Nouveau joueur')
			self.pos.append('')
		self.startGame()

	def startGame(self):

		self.sendToAll(self.map)
		print('[SERV] Map transmise')

		self.sendToAll('START')
		print('[SERV] Jeu démarré')

		self.game()

	def game(self):
		stop = False

		while not stop:
			read, write, error = select.select(self.clientsSocket, [], [], 0.01)
			for client in read:
				msg = client.recv(1024).decode()
				print(msg)
				self.pos[int(msg[0:1])] = msg[2:]
			newPos = ''
			for i in range(len(self.pos)):
				newPos += str(i) + ';' + self.pos[i] + '-'
			newPos = newPos[:-1]
			print(newPos)

	def sendToAll(self, msg):
		for client in self.clients:
			client.run(msg)
		nbOk = 0
		while (nbOk < self.nbMax):
			nbOk = 0
			for client in self.clients:
				if not client.isAlive():
					nbOk += 1


class SocketClient(Thread):

	def __init__(self, ip, port, socket):
		Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.socket = socket

	def run(self, msg):
		self.socket.send(msg.encode())

if __name__ == '__main__':
	serv = Server(1337, 'LELELELELELE', 1)
	serv.waitForPlayers()
