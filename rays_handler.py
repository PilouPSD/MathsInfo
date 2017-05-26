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
						self.can.create_oval(passant[0]-2,passant[1]-2,passant[0]+2,passant[1]+2,outline="blue",width=2,tag=self.tag) # Affichage intersection

		self.tri()

		if not self.drawMode:
			self.can.create_polygon([p[:2] for p in self.usefulPoints],fill="gold",tag = self.tag)	# Affichage du polygone
		self.can.create_oval(self.x-3,self.y-3,self.x+3,self.y+3,fill="red",outline="red",width=1,tag=["center",self.tag])	# Affichage du centre


		#DEBUG
		if 1:
			#for p in self.usefulPoints:
			#	print(p)
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
		anglePassant1 = None # Uniquement utilisé pour sauver coordonées des points où le rayon passe par un angle mais continue plus loin
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
					dist = sqrt((x-self.x)**2 + (y-self.y)**2)	# Calcul de la distance centre - point d'intersection


					if [int(x),int(y)]==b1 or [int(x),int(y)] == b2: # Vérification qu'on est en bout de segment
						
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
							dist = sqrt((x-self.x)**2 + (y-self.y)**2)
							if angle<=0:	# Si on va dans un sens
								if dist < minDist1 or minDist1 == -1: 	# Si initialisation ou distance minimale
									minDist1 = dist
									ray1 = [int(x),int(y),angle]

							elif angle >0:	# Si on va dans l'autre sens
								if dist < minDist2 or minDist2 == -1:	# Si initialisation ou distance minimale
									minDist2 = dist
									ray2 = [int(x),int(y),angle]
						else:	# Le rayon touche le coin mais continue
							if angle<=0 and ray1 != None:	# Si on va dans un sens
								anglePassant1 = [int(x),int(y),angle]

							elif angle>0 and ray2 != None:	# Si on va dans l'autre sens
								anglePassant2 = [int(x),int(y),angle]

					elif ((b1[0] >= x >= b2[0]) or (b1[0] <= x <= b2[0])) and ((b1[1] >= y >= b2[1]) or (b1[1] <= y <= b2[1])): # Vérification qu'on est dans le segment
						
						if angle<=0:	# Si on va dans un sens
							if dist < minDist1 or minDist1 == -1: 	# Si initialisation ou distance minimale
								minDist1 = dist
								ray1 = [int(x),int(y),angle]

						elif angle >0:	# Si on va dans l'autre sens
							if dist < minDist2 or minDist2 == -1:	# Si initialisation ou distance minimale
								minDist2 = dist
								ray2 = [int(x),int(y),angle]

		if anglePassant1 != None:
			distp1 = sqrt((anglePassant1[0]-self.x)**2+(anglePassant1[1]-self.y)**2)
			dist1 = sqrt((ray1[0]-self.x)**2+(ray1[1]-self.y)**2)
			if dist1 < distp1:
				anglePassant1 = None
		
		if anglePassant2 != None:
			distp2 = sqrt((anglePassant2[0]-self.x)**2+(anglePassant2[1]-self.y)**2)
			dist2 = sqrt((ray2[0]-self.x)**2+(ray2[1]-self.y)**2)
			if dist2 < distp2:
				anglePassant2 = None


		return [ray1, ray2, anglePassant1, anglePassant2]


	def tri(self):
		self.usefulPoints = sorted(self.usefulPoints, key=itemgetter(2))
		for p in self.usefulPoints:
			if self.usefulPoints.index(p) < len(self.usefulPoints)-1:
				if p[:2] == self.usefulPoints[self.usefulPoints.index(p)+1][:2]:
					print(p,self.usefulPoints[self.usefulPoints.index(p)+1])
					self.usefulPoints.pop(self.usefulPoints.index(p)+1)
			else:
				if p[:2] == self.usefulPoints[-1][:2]:
					print(p,self.usefulPoints[self.usefulPoints.index(p)])


		for p in self.usefulPoints:

			if self.usefulPoints.index(p) == len(self.usefulPoints)-1:
				p1 = self.usefulPoints[-1]
				p2 = self.usefulPoints[-2]
			elif self.usefulPoints.index(p) == len(self.usefulPoints)-2:
				p1 = self.usefulPoints[self.usefulPoints.index(p)+1]
				p2 = self.usefulPoints[-1]
			else:
				p1 = self.usefulPoints[self.usefulPoints.index(p)+1]
				p2 = self.usefulPoints[self.usefulPoints.index(p)+2]

			if round(p1[2],5) == round(p[2],5): # Les deux points ont le même angle -> savoir lequel est premier
				self.can.create_line(p[0],p[1],p1[0],p1[1],width=3, tag = self.tag,dash=True)
				p0 = self.usefulPoints[self.usefulPoints.index(p)-1]

				distP0P= sqrt( (p0[0]-p[0])**2 + (p0[1]-p[1])**2 )
				distPP1 = sqrt( (p[0]-p1[0])**2 + (p[1]-p1[1])**2 )
				distP0P1 = sqrt( (p0[0]-p1[0])**2 + (p0[1]-p1[1])**2 )
				distP2P = sqrt( (p2[0]-p[0])**2 + (p2[1]-p[1])**2 )
				distP2P1 = sqrt( (p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 )


				if distP0P + distPP1 + distP2P1 > distP0P1 + distPP1 + distP2P:
					index1 = self.usefulPoints.index(p)
					index2 = self.usefulPoints.index(p1)
					self.usefulPoints[index1] = p1
					self.usefulPoints[index2] = p
					print("inversion des deux points")
					print("p0:{} p:{} p1:{} | p0p:{} p0p1:{} pp1:{}".format(p0[:2],p[:2],p1[:2],int(distP0P),int(distPP1),int(distP0P1)))
					#print(p0[:2],p[:2],p1[:2]," ancien")
					#print(p0[:2],p1[:2],p[:2]," nouveau")

				else:
					print("----")
					print("p0:{} p:{} p1:{} | p0p:{} p0p1:{} pp1:{}".format(p0[:2],p[:2],p1[:2],int(distP0P),int(distPP1),int(distP0P1)))
					print("----")




	def deleteRayons(self):
		self.can.delete(self.tag)

if __name__ == '__main__':
	from main import *
	app = Application().mainloop()