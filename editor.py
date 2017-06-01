from tkinter import *
from rays_handler import *

types = {"default":"snow","mirroir":"light blue","obstacle":"black","obstacle_rouge":"red","obstacle_bleu":"blue"}

angle_torche = pi / 4
delta = 5

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
		if(e.keycode == 37):

			self.rayons.x += -delta
			self.rayons.y += 0

			aux = self.main.find_overlapping(self.rayons.x,self.rayons.y,self.rayons.x,self.rayons.y)
			print_ = True
			for i in aux:
				for j in self.main.gettags(i):
					if(j == "poly0" or j == "center" or j == "Rayon" or j == "current"):
						pass
					else:
						print_ = False
						print("probleme")
						print(j)

			if(print_):
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
			for i in aux:
				for j in self.main.gettags(i):
					if(j == "poly0" or j == "center" or j == "Rayon" or j == "current"):
						pass
					else:
						print_ = False
						print("probleme")
						print(j)

			if(print_):
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
			for i in aux:
				for j in self.main.gettags(i):
					if(j == "poly0" or j == "center" or j == "Rayon" or j == "current"):
						pass
					else:
						print_ = False
						print("probleme")
						print(j)

			if(print_):
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
			for i in aux:
				for j in self.main.gettags(i):
					if(j == "poly0" or j == "center" or j == "Rayon" or j == "current"):
						pass
					else:
						print_ = False
						print("probleme")
						print(j)

			if(print_):
				self.rayons.deleteRayons()
				self.rayons.drawRayons()
			else:
				self.rayons.x += 0
				self.rayons.y += -delta

		elif(e.keycode == 65):			
			self.rayons.start_angle += 0.1
			print(self.rayons.start_angle)
			if(-pi < self.rayons.start_angle < pi):				
				self.rayons.deleteRayons()
				self.rayons.drawRayons()
			else:				
				self.rayons.start_angle -= 2 * pi				
				self.rayons.deleteRayons()
				self.rayons.drawRayons()
		elif(e.keycode == 90):		
			self.rayons.start_angle += -0.1
			print(self.rayons.start_angle)
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
			self.doCreateRayons = False
			self.rayonsDessin = True

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