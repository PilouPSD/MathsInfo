from tkinter import *
from rays_handler import *
from time import sleep
import threading
import random

types = {"default":"snow","mirroir":"light blue","obstacle":"black","obstacle_rouge":"red","obstacle_bleu":"blue"}

angle_torche = pi / 4
delta = 1


class Point():
	def __init__(self,can,x,y,tag="points"):
		self.x = x
		self.y = y
		self.can = can
		self.tag = tag
		self.dessiner()

	def __str__(self):
		#return("point | tag:{} | coords:{},{}".format(self.tag,self.x,self.y))
		return("{},{}".format(self.x,self.y))

	def dessiner(self):	# Affichage du point
		self.id=self.can.create_oval(self.x-4,self.y-4,self.x+4,self.y+4,fill="yellow",outline="black",width=2,tag=self.tag)

	def effacer(self):	# Effacement graphique du polygone
		self.can.delete(self.id)


class Polygone():
	global types
	def __init__(self,can,tag,points=[],material="default"):
		self.can = can
		self.tag = tag
		self.points = points
		self.material = material
		self.dessiner()

	def __str__(self):
		return("poly  | tag:{}".format(self.tag))

	def dessiner(self):	# Affichage du polygone
		self.id = self.can.create_polygon([(p.x,p.y) for p in self.points], tag=self.tag, fill=types[self.material],outline="grey",width=2)

	def effacer(self):	# Effacement graphique du polygone
		self.can.delete(self.tag)

	def kill(self):	# Supression totale du polygone
		self.can.delete(self.tag)
		self.can.delete(self.points[0].tag[0])


class Editor(Tk):
	def __init__(self,can,tools, fen):
		self.main = can
		self.fen = fen
		self.toolbar = tools
		self.poly = []	# Stockage des polygones

		self.saisir = False				# Mode de saisie
		self.moving = None				# Id de l'objet qu'on déplace
		self.prevX, self.prevY = -1,-1	# Position de l'objet qu'on déplace
		self.deleting = False			# Mode d'effacement de polygone
		self.nbPoly = 0					# Id unique du dernier polygone créé
		self.doCreateRayons = False		# Si Vrai, crée les rayons quand on clique dans la fenêtre
		self.rayonsDessin = False
		self.angle_souris = -pi / 2
		self.ray = False
		self.ongame = False
		self.souris = {}

		# Menu déroulant pour le matériau
		self.polygonType = StringVar()
		self.polygonType.set("default")
		self.menu = OptionMenu(self.toolbar, self.polygonType, "default", "mirroir", "obstacle","obstacle_rouge","obstacle_bleu")
		self.menu.place(x=20,y=300,width=115)


		self.main.bind("<ButtonPress>", self.buttonPressed) # Appui bouton souris
		self.main.bind("<Motion>", self.drag)				# Mouvement souris
		self.main.bind("<ButtonRelease>", self.stopDrag)	# Bouton souris relaché
		self.fen.bind('<KeyPress>', self.KeyEvent)	# touche presser


	def KeyEvent(self, e):
		if(self.ray):

				if(e.keycode == 37):

					self.rayons.x += -delta
					self.rayons.y += 0

					aux = self.main.find_overlapping(self.rayons.x,self.rayons.y,self.rayons.x,self.rayons.y)
					print_ = True
					tr = False
					for i in aux:
						default = False
						for k in self.poly:
							if k.material=="default" and k.id == i:
								default = True
								tr = True
								break
						for j in self.main.gettags(i):
							if(default or j == "center" or j == "Rayon" or j == "current" or j == "vwpoly"or j == "Souris"):
								pass
							else:
								print_ = False
								print("probleme")
								print(j)

					if(print_ and tr):	
						self.rayons.deleteRayons()
						self.rayons.drawRayons()
					else:
						self.rayons.x += +delta
						self.rayons.y += 0

				elif(e.keycode == 38):

					self.rayons.x += 0
					self.rayons.y += -delta

					aux = self.main.find_overlapping(self.rayons.x,self.rayons.y,self.rayons.x,self.rayons.y)
					print_ = True
					tr = False
					for i in aux:
						default = False
						for k in self.poly:
							if k.material=="default" and k.id == i:
								default = True
								tr = True
								break
						for j in self.main.gettags(i):
							if(default or j == "center" or j == "Rayon" or j == "current"or j == "vwpoly"or j == "Souris"):
								pass
							else:
								print_ = False
								print("probleme")
								print(j)

					if(print_ and tr):	
						self.rayons.deleteRayons()
						self.rayons.drawRayons()
					else:
						self.rayons.x += 0
						self.rayons.y += delta
				elif(e.keycode == 39):

					self.rayons.x += delta
					self.rayons.y += 0

					aux = self.main.find_overlapping(self.rayons.x,self.rayons.y,self.rayons.x,self.rayons.y)
					print_ = True
					tr = False
					for i in aux:
						default = False
						for k in self.poly:
							if k.material=="default" and k.id == i:
								default = True
								tr = True
								break
						for j in self.main.gettags(i):
							if(default or j == "center" or j == "Rayon" or j == "current"or j == "vwpoly"or j == "Souris"):
								pass
							else:
								print_ = False
								print("probleme")
								print(j)

					if(print_ and tr):	
						self.rayons.deleteRayons()
						self.rayons.drawRayons()
					else:
						self.rayons.x += -delta
						self.rayons.y += 0
				elif(e.keycode == 40):

					self.rayons.x += 0
					self.rayons.y += delta

					aux = self.main.find_overlapping(self.rayons.x,self.rayons.y,self.rayons.x,self.rayons.y)
					print_ = True
					tr = False
					for i in aux:
						default = False
						for k in self.poly:
							if k.material=="default" and k.id == i:
								default = True
								tr = True
								break
						for j in self.main.gettags(i):
							if(default or j == "center" or j == "Rayon" or j == "current"or j == "vwpoly" or j == "Souris"):
								pass
							else:
								print_ = False
								print("probleme")
								print(j)

					if(print_ and tr):	
						self.rayons.deleteRayons()
						self.rayons.drawRayons()
					else:
						self.rayons.x += 0
						self.rayons.y += -delta

				elif(e.keycode == 65):			
					self.rayons.start_angle += 0.1
					if(-pi < self.rayons.start_angle < pi):				
						self.rayons.deleteRayons()
						self.rayons.drawRayons()
					else:				
						self.rayons.start_angle -= 2 * pi				
						self.rayons.deleteRayons()
						self.rayons.drawRayons()
				elif(e.keycode == 90):		
					self.rayons.start_angle += -0.1
					if(-pi < self.rayons.start_angle < pi):				
						self.rayons.deleteRayons()
						self.rayons.drawRayons()
					else:				
						self.rayons.start_angle += 2 * pi				
						self.rayons.deleteRayons()
						self.rayons.drawRayons()
				else:
					print(e.keycode)

	def saisie(self,event=None):	# Début ou validation de la création d'un polygone
		if event!=None: print(event.x,event.y)

		if self.saisir:	# Désactivation du mode de saisie
			self.main.unbind("<Button-1>")
			self.main.unbind("<Double-Button-1>")

			self.main.bind("<ButtonPress>", self.buttonPressed)
			self.main.bind("<Motion>", self.drag)
			self.main.bind("<ButtonRelease>", self.stopDrag)
			try:
				self.poly += [Polygone(self.main,"poly"+str(self.nbPoly),self.points,self.polygonType.get())]	# Création du polygone
				self.main.delete("tempLines")	# Suppression des lignes temporaires
				self.nbPoly += 1
			except:pass
		
		else:	# Activation du mode de saisie

			self.main.unbind("<ButtonPress>")
			self.main.unbind("<Motion>")
			self.main.unbind("<ButtonRelease>")

			self.deleting = False	# On vérifie qu'on est pas en mode de supression de polygone
			self.points = []		# On vide la tableau temporaire des points
			self.main.bind("<Button-1>", self.newPoint)
			self.main.bind("<Double-Button-1>", self.saisie)

		self.saisir = not self.saisir



	def newPoint(self,event):	# Création d'un nouveau point à l'emplacement du clic
		self.points+=[Point(self.main,event.x,event.y,["points"+str(self.nbPoly),self.nbPoly])]
		if len(self.points)>=2:
			self.main.create_line(self.points[-2].x, self.points[-2].y, self.points[-1].x, self.points[-1].y,fill="grey",width=2,tag="tempLines")

	def buttonPressed(self,event):
		print(event.x,event.y)
		aux = self.main.find_overlapping(event.x-1,event.y-1,event.x+1,event.y+1)	# Détection de l'objet cliqué
		
		if len(aux)!=0:	# Si on clique sur un objet
			if self.deleting:	# On supprime le polygone cliqué
				if self.main.gettags(aux[0])[0][:6]!="points":	# Si on clique sur un polygone
					self.selectedPoly = self.getPolyId(self.main.gettags(aux[0])[0])
					self.poly[self.selectedPoly].kill()
					self.poly.pop(self.selectedPoly)
					self.deleting = False
			
			elif self.moving == None: # Start drag point
				for sel in range(len(aux)):
					if self.main.gettags(aux[sel])[0][:6]=="points": # Si on clique sur un point
						self.moving = aux[sel]	# On récupère l'id du point qu'on bouge
						self.selectedPoly =  self.getPolyId("poly"+self.main.gettags(aux[sel])[1]) # On récupère le tag id du polygone
						break
					elif self.main.gettags(aux[sel])[0] == "center":
						self.moving = aux[sel]
						self.selectedPoly = "rayon"

		if self.doCreateRayons:	# On crée les rayons
			centre = [event.x, event.y]
			self.rayons = Rayons(self.main,event.x,event.y,angle_torche, 7* pi / 8, self.poly) #- 5* pi / 8
			self.ray = True
			#self.souris = Souris(self.main,100,100, self.poly) #- 5* pi / 8
			threading.Thread(target=self.souri).start()
			self.doCreateRayons = False
			self.rayonsDessin = True

	def init_game_souris(self, nb):
		self.nb_souris = nb
		self.nb_souris_gg = nb
		self.souris = []
		self.main.delete("Souris")
		for i in range(nb):

			print_ = True
			tr = False

			while (not print_ or not tr):
				tr = False
				print_ = True
				x = random.randint(0, 800)
				y = random.randint(0, 800)
				aux = self.main.find_overlapping(x-2,y-2,x+2,y+2)
				for i in aux:
					default = False
					for k in self.poly:
						if k.material=="default" and k.id == i:
							default = True
							tr = True
							break
					for j in self.main.gettags(i):
						if(default or j == "center" or j == "Rayon" or j == "current"):
							pass
						else:
							print_ = False
			self.souris += [Souris(self.main,x,y, self.poly)]


	def souri(self):
		while 1:
			if(self.ongame):
				for ji in self.souris:
					aux = self.main.find_overlapping(ji.x,ji.y,ji.x,ji.y)
					print_ = True
					tr = False
					for i in aux:
						default = False
						for k in self.poly:
							if k.material=="default" and k.id == i:
								default = True
								tr = True
								break
						for j in self.main.gettags(i):
							if(j == "vwpoly"):
								print_ = False

					if(not print_):
						ji.win()
						if(ji.find == False):
							self.nb_souris = self.nb_souris - 1
							if(self.nb_souris == 0):
								self.main.delete("errasetxt")
								self.main.create_text(110,40, text="vous avez gagné", tag="errasetxt")
							else:
								str_aff = str(self.nb_souris) + ' / ' + str(self.nb_souris_gg)
								self.main.delete("errasetxt")
								self.main.create_text(110,40, text=str_aff, tag="errasetxt")
						ji.find = True
				sleep(0.001)
		'''
		for i in range (1000):			
			self.souris.x = self.souris.x - delta * cos(self.angle_souris)
			self.souris.y = self.souris.y - delta * sin(self.angle_souris)


			aux = self.main.find_overlapping(self.souris.x,self.souris.y,self.souris.x,self.souris.y)
			print_ = True
			tr = False
			pb = ""
			for i in aux:
				default = False
				for k in self.poly:
					if k.material=="default" and k.id == i:
						default = True
						tr = True
						break
				for j in self.main.gettags(i):
					if(default or j == "center" or j == "Rayon" or j == "current"):
						pass
					else:
						print_ = False
						pb = j

			if(print_ and tr):					
				self.souris.draw()
			else:
				test = True
				for pol in self.poly: # Pour chaque polygone
					if(pol.tag == pb):
						for k in range(len(pol.points) - 1):
							b1 = [pol.points[k-1].x,pol.points[k-1].y]
							b2 = [pol.points[k].x,pol.points[k].y]

							coef1 = (b1[1] - b2[1]) / (b1[0] - b2[0])

							if(b1[0] != self.souris.x):
								coef2 = (b1[1] - self.souris.y) / (b1[0] - self.souris.x)
							else:
								coef2 = 1000000000
							if(test):
								if(coef1 - 10 < coef2 < coef1 + 10):
									angle = atan2(b2[0] - b1[0], b2[1] - b1[1])
									#self.main.create_oval(b1[0]-3,b1[1]-3,b1[0]+3,b1[1]+3,fill="red",outline="red",width=1,tag=["center"])	# Affichage du centre
									#self.main.create_oval(b2[0]-3,b2[1]-3,b2[0]+3,b2[1]+3,fill="green",outline="green",width=1,tag=["center"])	# Affichage du centre

									if(self.angle_souris >= pi):
										self.angle_souris = self.angle_souris - 2 * pi
									elif(self.angle_souris <= -pi):
										self.angle_souris = self.angle_souris + 2 * pi

									angle1 = pi / 2 - (self.angle_souris - angle)

									self.angle_souris = - self.angle_souris

									print(self.angle_souris)
									test = False
								
			sleep(0.01)

		'''

	def getPolyId(self,tag):	# Récupération de l'id d'un polygone par son tag
		for i in range(len(self.poly)):
			if self.poly[i].tag == tag:
				return i

	def stopDrag(self,event):	# Arrêt du déplacement d'un point
		self.moving = None
		self.prevX = -1
		self.prevY = -1
	
	def drag(self,event):	# Déplacement d'un point

		if self.moving!=None: # Si un point est sélectionné
			if self.prevX==-1:
				self.prevX,self.prevY = event.x,event.y

			dx,dy = event.x-self.prevX,event.y-self.prevY
			self.prevX,self.prevY = event.x,event.y
			self.main.move(self.moving,dx,dy)		# Déplacement du point

			if self.selectedPoly != "rayon":
				for i in self.poly[self.selectedPoly].points:	# On sauvegarde les nouvelles coordonées du point
					if i.id==self.moving:
						i.x+=dx
						i.y+=dy
				self.poly[self.selectedPoly].effacer()	# Supression et recréation du polygone avec le nouveau point
				self.poly[self.selectedPoly] = Polygone(self.main,self.poly[self.selectedPoly].tag,self.poly[self.selectedPoly].points,self.poly[self.selectedPoly].material)

				for pol in self.poly:	# On remet le polygone de fond à l'arrière
					if pol.material=="default":
						self.main.tag_lower(pol.id)
			else:
				self.rayons.x += dx
				self.rayons.y += dy

			if self.rayonsDessin:
				self.rayons.deleteRayons()
				self.rayons.drawRayons()

if __name__ == '__main__':
	from main import *
	app = Application().mainloop()