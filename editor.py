from tkinter import *
from math import cos, sin, pi, atan2, sqrt
from time import sleep
types = {"default":"snow","mirroir":"light blue","obstacle":"black","obstacle_rouge":"red","obstacle_bleu":"blue"}

class Rayons():
	def __init__(self,can,x,y,poly):
		self.can = can
		self.x = x
		self.y = y
		self.poly=poly
		self.nbRayons = 10 # Nb de rayons tracés (dans les 2 sens)
		self.tag = "Rayon"

		self.drawRayons()

	def drawRayons(self):
		self.can.delete(self.tag)	# Supression des anciens rayons
		
		a1 = [self.x,self.y] # Centre d'application

		for pol in self.poly:
			for k in range(len(pol.points)):

				a2 = [pol.points[k].x,pol.points[k].y]				
				#self.can.create_line(self.x,self.y,a2[0],a2[1],fill="red",tag=self.tag)


				rays = self.testRay(a1,a2)
				ray = rays[0]
				if ray!=None:
					if(ray[0] == a2[0] and ray[1] == a2[1]):
						x = self.x - 1000 * sin(ray[2])
						y = self.y - 1000 * cos(ray[2])
						#self.can.create_oval(ray[0]-1,ray[1]-1,ray[0]+1,ray[1]+1,outline="red",width=2,tag=self.tag) # Affichage intersection
						self.can.create_line(self.x,self.y,x,y,fill="black",tag=self.tag)	# Affichage du rayon
					else:						
						self.can.create_line(self.x,self.y,ray[0],ray[1],fill="red",tag=self.tag)	# Affichage du rayon


				ray = rays[1]
				if ray!=None:
					if(ray[0] == a2[0] and ray[1] == a2[1]):
						x = self.x - 1000 * sin(ray[2])
						y = self.y - 1000 * cos(ray[2])
						#self.can.create_oval(ray[0]-1,ray[1]-1,ray[0]+1,ray[1]+1,outline="red",width=2,tag=self.tag) # Affichage intersection
						self.can.create_line(self.x,self.y,x,y,fill="black",tag=self.tag)	# Affichage du rayon
					else:						
						self.can.create_line(self.x,self.y,ray[0],ray[1],fill="red",tag=self.tag)	# Affichage du rayon

		self.can.create_oval(self.x-1,self.y-1,self.x+1,self.y+1,fill="red",outline="black",width=1,tag=self.tag)	# Affichage du centre

		#DEBUG
		if 1:
			#self.can.create_line(self.x-800,self.y,self.x+800,self.y,dash=True,tag=self.tag)
			#self.can.create_line(self.x,self.y-800,self.x,self.y+800,dash=True,tag=self.tag)
			self.can.create_text(50,50,text="cadran 3")
			self.can.create_text(750,50,text="cadran 4")
			self.can.create_text(50,750,text="cadran 2")
			self.can.create_text(750,750,text="cadran 1")


	def testRay(self,a1,a2):
		minDist1 = -1
		minDist2 = -1
		ray1 = None
		ray2 = None

		for pol in self.poly: # Pour chaque polygone
			for k in range(len(pol.points)):
				# On prend 2 points de chaque droite formée par le polygone (extrémités de chaque segment)
				b1 = [pol.points[k-1].x,pol.points[k-1].y]
				b2 = [pol.points[k].x,pol.points[k].y]

				det1 = b1[1]*(a2[0]-b2[0]) + b2[1]*(b1[0]-a2[0]) + a2[1]*(b2[0]-b1[0])	# |B1B2A2|
				det2 = b2[1]*(a1[0]-b1[0]) + b1[1]*(b2[0]-a1[0]) + a1[1]*(b1[0]-b2[0])	# |B2B1A1|

				if det1+det2!=0: # On évite la division par 0
					# Coordonées du point d'intersection
					x = (det1 * a1[0] + det2 * a2[0])/(det1+det2)
					y = (det1 * a1[1] + det2 * a2[1])/(det1+det2)

					angle = atan2(self.x - x,self.y - y)

					dist = sqrt((x-self.x)**2 + (y-self.y)**2)	# Calcul de la distance centre - point d'intersection
					if ((b1[0] >= x >= b2[0]) or (b1[0] <= x <= b2[0])) and ((b1[1] >=y >= b2[1]) or (b1[1] <= y <= b2[1])):
						if(x == a2[0] and (y == a2[1])):
							self.can.create_oval(x-4,y-4,x+4,y+4,fill="red",outline="black",width=2,tag=self.tag)
							if angle<=0:	# Si on va dans un sens
								if(dist < minDist1)or(minDist1 == -1):
									ray1 = [x,y,angle]
							elif angle >0:	# Si on va dans l'autre sens
								if(dist < minDist2)or(minDist2 == -1):
									ray2 = [x,y,angle]
							
						else:
							self.can.create_oval(x-4,y-4,x+4,y+4,fill="yellow",outline="black",width=2,tag=self.tag)
							if angle<=0:	# Si on va dans un sens
								if dist < minDist1 or minDist1 == -1: 	# Si initialisation ou distance minimale
									minDist1 = dist
									ray1 = [x,y,angle]
									self.can.create_oval(x-4,y-4,x+4,y+4,fill="yellow",outline="blue",width=2,tag=self.tag)
									print("&									1 :				:	", ray1)
							elif angle >0:	# Si on va dans l'autre sens
								if dist < minDist2 or minDist2 == -1:	# Si initialisation ou distance minimale
									minDist2 = dist
									ray2 = [x,y,angle]
									print("&									2 :				:	", ray2)
		print(ray1,ray2)
		return [ray1, ray2]

	def deleteRayons(self):
		self.can.delete(self.tag)

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
	def __init__(self,can,tools):
		self.main = can
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

		if self.doCreateRayons:	# On crée les rayons
			self.rayons = Rayons(self.main,event.x,event.y,self.poly)
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

			for i in self.poly[self.selectedPoly].points:	# On sauvegarde les nouvelles coordonées du point
				if i.id==self.moving:
					i.x+=dx
					i.y+=dy

			self.poly[self.selectedPoly].effacer()	# Supression et recréation du polygone avec le nouveau point
			self.poly[self.selectedPoly] = Polygone(self.main,self.poly[self.selectedPoly].tag,self.poly[self.selectedPoly].points,self.poly[self.selectedPoly].material)

			for pol in self.poly:	# On remet le polygone de fond à l'arrière
				if pol.material=="default":
					self.main.tag_lower(pol.id)

			if self.rayonsDessin:
				self.rayons.deleteRayons()
				self.rayons.drawRayons()

if __name__ == '__main__':
	from main import *
	app = Application().mainloop()