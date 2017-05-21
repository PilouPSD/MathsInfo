from tkinter import *
from math import cos, sin, pi, atan2, sqrt
from operator import itemgetter

class Rayons():
	def __init__(self,can,x,y,poly):
		self.can = can
		self.x = x
		self.y = y
		self.poly=poly
		self.tag = "Rayon"
		self.drawMode = True
		self.drawRayons()

	def drawRayons(self):
		self.usefulPoints = []
		self.can.delete(self.tag)	# Supression des anciens rayons
		
		a1 = [self.x,self.y] # Centre d'application

		for pol in self.poly:	# On parcourt tous les polygones
			for k in pol.points:	# parcourt tous les points de chaque polygone

				a2 = [k.x,k.y]

				#self.can.create_line(self.x,self.y,a2[0],a2[1],fill="red",tag=self.tag)

				rays = self.testRay(a1,a2)

				for ray in rays[:2]:	# Affichage des rayons si ils existent
					if ray!=None:
						self.usefulPoints += [ray]
						if self.drawMode:
							self.can.create_oval(ray[0]-1,ray[1]-1,ray[0]+1,ray[1]+1,outline="red",width=2,tag=self.tag) # Affichage intersection
							self.can.create_line(self.x,self.y,ray[0],ray[1],fill="black",tag=self.tag)	# Affichage du rayon

				for passant in rays[2:]:
					if passant != None:
						self.usefulPoints+=[passant]

		self.usefulPoints = sorted(self.usefulPoints, key=itemgetter(2))

		if not self.drawMode:
			self.can.create_polygon([p[:2] for p in self.usefulPoints],fill="yellow",tag = self.tag)	# Affichage du polygone
		self.can.create_oval(self.x-3,self.y-3,self.x+3,self.y+3,fill="red",outline="red",width=1,tag=["center",self.tag])	# Affichage du centre


		#DEBUG
		if 0:
			for p in self.usefulPoints:
				print(p)
			self.can.create_line(self.x-800,self.y,self.x+800,self.y,dash=True,tag=self.tag)
			self.can.create_line(self.x,self.y-800,self.x,self.y+800,dash=True,tag=self.tag)
			self.can.create_text(50,50,text="cadran 3")
			self.can.create_text(750,50,text="cadran 4")
			self.can.create_text(50,750,text="cadran 2")
			self.can.create_text(750,750,text="cadran 1")


	def testRay(self,a1,a2):
		minDist1 = -1
		minDist2 = -1
		ray1 = None
		ray2 = None
		anglePassant1 = None # Uniquement utilisé pour sauver coordonées des points où le rayon passe par un angle mais continue
		anglePassant2 = None

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

					if ((b1[0] > x > b2[0]) or (b1[0] < x < b2[0])) and ((b1[1] > y > b2[1]) or (b1[1] < y < b2[1])): # Vérification qu'on est dans le segment

						dist = sqrt((x-self.x)**2 + (y-self.y)**2)	# Calcul de la distance centre - point d'intersection
						
						if angle<=0:	# Si on va dans un sens
							if dist < minDist1 or minDist1 == -1: 	# Si initialisation ou distance minimale
								minDist1 = dist
								ray1 = [int(x),int(y),angle]

						elif angle >0:	# Si on va dans l'autre sens
							if dist < minDist2 or minDist2 == -1:	# Si initialisation ou distance minimale
								minDist2 = dist
								ray2 = [int(x),int(y),angle]

					elif (b1[0] == int(x) and b1[1] == int(y)) or (b2[0] == int(x) and  b2[1] == int(y)): # Vérification qu'on est en bout de segment bout de segment
						
						if [int(x),int(y)]==b1:		# Si l'intersection est le premier point
							angle1 = atan2(self.x - b2[0],self.y - b2[1])
							angle2 = atan2(self.x - pol.points[k-2].x, self.y - pol.points[k-2].y)

						elif [int(x),int(y)] == b2:	# Si l'intersection est le deuxième point
							angle1 = atan2(self.x - b1[0],self.y - b1[1])

							if k<len(pol.points)-1: # Si on est pas en bout de tableau
								angle2 = atan2(self.x - pol.points[k+1].x, self.y - pol.points[k+1].y)
							else:
								angle2 = atan2(self.x - pol.points[0].x, self.y - pol.points[0].y)

						if ((angle1<0 and angle2>0) or (angle1>0 and angle2<0)) and not (-pi/2 < angle < pi/2):	# Si les angles sont de signes opposés
							
							if angle < 0:
								if angle1 > 0:
									angle1=-pi
								elif angle2 > 0:
									angle2=-pi
							else:
								if angle1 < 0:
									angle1=pi
								elif angle2 < 0:
									angle2=pi

						if angle1<angle<angle2 or angle1>angle>angle2:	# Si le rayon est arrêté par le polygone
							#print("ça passe pas : " + str(round(angle1,2)) + ' ' + str(round(angle,2)) + ' ' + str(round(angle2,2)))
							dist = sqrt((x-self.x)**2 + (y-self.y)**2)
							if angle<=0:	# Si on va dans un sens
								if dist < minDist1 or minDist1 == -1: 	# Si initialisation ou distance minimale
									minDist1 = dist
									ray1 = [int(x),int(y),angle]

							elif angle >0:	# Si on va dans l'autre sens
								if dist < minDist2 or minDist2 == -1:	# Si initialisation ou distance minimale
									minDist2 = dist
									ray2 = [int(x),int(y),angle]
						else:
							if angle<=0:	# Si on va dans un sens
									anglePassant1 = [int(x),int(y),angle]

							elif angle >0:	# Si on va dans l'autre sens
								anglePassant2 = [int(x),int(y),angle]

		return [ray1, ray2, anglePassant1, anglePassant2]

	def deleteRayons(self):
		self.can.delete(self.tag)

if __name__ == '__main__':
	from main import *
	app = Application().mainloop()