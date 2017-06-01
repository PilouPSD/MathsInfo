from tkinter import *
from math import cos, sin, pi, atan2, sqrt
from operator import itemgetter

gap = 0.005
#self.angle_torche = pi / 4
#self.start_angle = - pi / 2
long_torche = 300

class Rayons():
	def __init__(self,can,x,y, angle_torche, start_angle, poly):
		self.can = can
		self.x = x
		self.y = y
		self.angle_torche = angle_torche
		self.start_angle = start_angle
		self.poly=poly
		self.tag = "Rayon"
		self.drawMode = True
		self.drawRayons()

	def drawRayons(self):
		self.usefulPoints = []
		self.can.delete(self.tag)	# Supression des anciens rayons
		
		a1 = [int(self.x),int(self.y), -2 * pi] # Centre d'application

		if(-pi < self.start_angle + self.angle_torche < pi):
			signes_angle_probleme = True
		else:
			signes_angle_probleme = False
			


		a2 = [a1[0] - 1000 * sin(self.start_angle),a1[1] - 1000 * cos(self.start_angle), self.start_angle]
				
		angle = atan2(self.x - a2[0],self.y - a2[1])

		#self.can.create_line(self.x,self.y,a2[0],a2[1],fill="red",tag=self.tag)
		if(signes_angle_probleme):	
			rays = self.testRay(a1,a2, True)

			for ray in rays[:2]:	# Affichage des rayons si ils existent
				if ray!=None:
					if(self.start_angle - 0.01 <= ray[2] <= self.start_angle + self.angle_torche + 0.01):
						self.usefulPoints += [ray]
						if self.drawMode:
							self.can.create_oval(ray[0]-1,ray[1]-1,ray[0]+1,ray[1]+1,outline="red",width=2,tag=self.tag) # Affichage intersection
							self.can.create_line(self.x,self.y,ray[0],ray[1],fill="black",tag=self.tag)	# Affichage du rayon


			for passant in rays[2:]:
				if passant != None:
					if(self.start_angle - 0.01 <= ray[2] <= self.start_angle + self.angle_torche + 0.01):
						self.usefulPoints+=[passant]

		else:
			rays = self.testRay(a1,a2, True)

			for ray in rays[:2]:	# Affichage des rayons si ils existent
				if ray!=None:
					if((self.start_angle - 0.01 <= ray[2] <= pi + 0.01) or (- pi - 0.01 <= ray[2] <= self.start_angle + self.angle_torche - 2* pi + 0.01)):
						if(ray[2] < 0):
							ray[2] = ray[2] + 2 * pi
						self.usefulPoints += [ray]
						if self.drawMode:
							self.can.create_oval(ray[0]-1,ray[1]-1,ray[0]+1,ray[1]+1,outline="red",width=2,tag=self.tag) # Affichage intersection
							self.can.create_line(self.x,self.y,ray[0],ray[1],fill="black",tag=self.tag)	# Affichage du rayon

			for passant in rays[2:]:
				if passant != None:
					if((self.start_angle - 0.01 <= passant[2] <= pi + 0.01) or (- pi - 0.01 <= passant[2] <= self.start_angle + self.angle_torche - 2* pi + 0.01)):
						if(passant[2] < 0):
							passant[2] = passant[2] + 2 * pi
						self.usefulPoints += [passant]
						if self.drawMode:
							self.can.create_oval(passant[0]-1,passant[1]-1,passant[0]+1,passant[1]+1,outline="red",width=2,tag=self.tag) # Affichage intersection
							self.can.create_line(self.x,self.y,passant[0],passant[1],fill="black",tag=self.tag)	# Affichage du rayon





		a2 = [a1[0] - 1000 * sin(self.start_angle + self.angle_torche),a1[1] - 1000 * cos(self.start_angle+ self.angle_torche), self.start_angle]		
				
		angle = atan2(self.x - a2[0],self.y - a2[1])

		#self.can.create_line(self.x,self.y,a2[0],a2[1],fill="red",tag=self.tag)
		if(signes_angle_probleme):	
			rays = self.testRay(a1,a2, True)

			for ray in rays[:2]:	# Affichage des rayons si ils existent
				if ray!=None:					
					if(self.start_angle - 0.01 <= ray[2] <= self.start_angle + self.angle_torche + 0.01):
						self.usefulPoints += [ray]
						if self.drawMode:
							self.can.create_oval(ray[0]-1,ray[1]-1,ray[0]+1,ray[1]+1,outline="red",width=2,tag=self.tag) # Affichage intersection
							self.can.create_line(self.x,self.y,ray[0],ray[1],fill="black",tag=self.tag)	# Affichage du rayon


			for passant in rays[2:]:
				if passant != None:
					if(self.start_angle - 0.01 <= ray[2] <= self.start_angle + self.angle_torche + 0.01):
						self.usefulPoints+=[passant]

		else:
			rays = self.testRay(a1,a2, True)

			for ray in rays[:2]:	# Affichage des rayons si ils existent
				if ray!=None:
					if((self.start_angle - 0.01 <= ray[2] <= pi + 0.01) or (- pi - 0.01 <= ray[2] <= self.start_angle + self.angle_torche - 2* pi + 0.01)):
						if(ray[2] < 0):
							ray[2] = ray[2] + 2 * pi
						self.usefulPoints += [ray]
						if self.drawMode:
							self.can.create_oval(ray[0]-1,ray[1]-1,ray[0]+1,ray[1]+1,outline="red",width=2,tag=self.tag) # Affichage intersection
							self.can.create_line(self.x,self.y,ray[0],ray[1],fill="black",tag=self.tag)	# Affichage du rayon



			for passant in rays[2:]:
				if passant != None:
					if((self.start_angle - 0.01 <= passant[2] <= pi + 0.01) or (- pi - 0.01 <= passant[2] <= self.start_angle + self.angle_torche - 2* pi + 0.01)):
						if(passant[2] < 0):
							passant[2] = passant[2] + 2 * pi
						self.usefulPoints += [passant]
						if self.drawMode:
							self.can.create_oval(passant[0]-1,passant[1]-1,passant[0]+1,passant[1]+1,outline="red",width=2,tag=self.tag) # Affichage intersection
							self.can.create_line(self.x,self.y,passant[0],passant[1],fill="black",tag=self.tag)	# Affichage du rayon






		for pol in self.poly:	# On parcourt tous les polygones
			for k in pol.points:	# parcourt tous les points de chaque polygone

				a2 = [k.x,k.y]
				
				angle = atan2(self.x - a2[0],self.y - a2[1])

				#self.can.create_line(self.x,self.y,a2[0],a2[1],fill="red",tag=self.tag)
				if(signes_angle_probleme):	
					if(angle > self.start_angle and angle < self.start_angle + self.angle_torche):
						rays = self.testRay(a1,a2, True)

						for ray in rays[:2]:	# Affichage des rayons si ils existent
							if ray!=None:
								if(ray[2] > self.start_angle and ray[2] < self.start_angle + self.angle_torche):
									self.usefulPoints += [ray]
									if self.drawMode:
										self.can.create_oval(ray[0]-1,ray[1]-1,ray[0]+1,ray[1]+1,outline="red",width=2,tag=self.tag) # Affichage intersection
										self.can.create_line(self.x,self.y,ray[0],ray[1],fill="black",tag=self.tag)	# Affichage du rayon


						for passant in rays[2:]:
							if passant != None:
								if(passant[2] > self.start_angle and passant[2] < self.start_angle + self.angle_torche):
									self.usefulPoints+=[passant]

				else:
					if((angle > self.start_angle and angle < pi) or (angle < self.start_angle - 2 * pi + self.angle_torche and angle > - pi)):
						rays = self.testRay(a1,a2, True)

						for ray in rays[:2]:	# Affichage des rayons si ils existent
							if ray!=None:
								if(signes_angle_probleme):	
									if(ray[2] > self.start_angle and ray[2] < self.start_angle + self.angle_torche):
										self.usefulPoints += [ray]
										if self.drawMode:
											self.can.create_oval(ray[0]-1,ray[1]-1,ray[0]+1,ray[1]+1,outline="red",width=2,tag=self.tag) # Affichage intersection
											self.can.create_line(self.x,self.y,ray[0],ray[1],fill="black",tag=self.tag)	# Affichage du rayon
								else:
									if((ray[2] >= self.start_angle and ray[2] <= pi) or (ray[2] <= self.start_angle - 2*pi + self.angle_torche and ray[2] > - pi)):
										if(ray[2] < 0):
											ray[2] = ray[2] + 2 * pi
										self.usefulPoints += [ray]
										if self.drawMode:
											self.can.create_oval(ray[0]-1,ray[1]-1,ray[0]+1,ray[1]+1,outline="red",width=2,tag=self.tag) # Affichage intersection
											self.can.create_line(self.x,self.y,ray[0],ray[1],fill="black",tag=self.tag)	# Affichage du rayon



					for passant in rays[2:]:
						if passant != None:
							if(signes_angle_probleme):	
								if(passant[2] > self.start_angle and passant[2] < self.start_angle + self.angle_torche):
									self.usefulPoints+=[passant]
									self.can.create_oval(passant[0]-2,passant[1]-2,passant[0]+2,passant[1]+2,outline="blue",width=2,tag=self.tag) # Affichage intersection
							else:
								if((passant[2] >= self.start_angle and passant[2] <= pi) or (passant[2] <= self.start_angle - 2*pi + self.angle_torche and passant[2] > - pi)):
									if(passant[2] < 0):
										passant[2] = passant[2] + 2 * pi
									self.usefulPoints += [passant]
									if self.drawMode:
										self.can.create_oval(passant[0]-1,passant[1]-1,passant[0]+1,passant[1]+1,outline="red",width=2,tag=self.tag) # Affichage intersection
										self.can.create_line(self.x,self.y,passant[0],passant[1],fill="black",tag=self.tag)	# Affichage du rayon



		self.usefulPoints+=[a1]
		self.usefulPoints = sorted(self.usefulPoints, key=itemgetter(2))

		for i in range(len(self.usefulPoints)):
			longueur = sqrt((self.usefulPoints[0][0] - self.usefulPoints[i][0])**2 + (self.usefulPoints[0][1] - self.usefulPoints[i][1])**2)
			if(longueur > long_torche):
				self.usefulPoints[i] = [a1[0] - long_torche * sin(self.usefulPoints[i][2]),a1[1] - long_torche * cos(self.usefulPoints[i][2]),self.usefulPoints[i][2]]

		if not self.drawMode:
			self.can.create_polygon([p[:2] for p in self.usefulPoints],fill="gold",tag = self.tag)	# Affichage du polygone
		self.can.create_oval(self.x-3,self.y-3,self.x+3,self.y+3,fill="red",outline="red",width=1,tag=["center",self.tag])	# Affichage du centre

		self.can.update()


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


	def testRay(self,a1,a2, verif):
		minDist1 = -1
		minDist2 = -1
		ray1 = None
		ray2 = None
		anglePassant1 = None # Uniquement utilisé pour sauver coordonées des points où le rayon passe par un angle mais continue
		anglePassant2 = None
		#self.can.create_oval(a2[0]-1,a2[1]-1,a2[0]+1,a2[1]+1,outline="red",width=2,tag=self.tag) # Affichage intersection



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
							#self.can.create_oval(int(x)-6,int(y)-6,int(x)+6,int(y)+6,fill="black",outline="black",width=1,tag=["center",self.tag])

							if angle<=0:	# Si on va dans un sens	
								#ray1 = [int(x),int(y),angle]							
								dist = sqrt((x-self.x)**2 + (y-self.y)**2)
								#self.can.create_oval(int(x)-60,int(y)-60,int(x)+60,int(y)+60,fill="red",outline="red",width=1,tag=["center",self.tag])
								tryangle = angle - gap
								dista = -1
								distb = -1

								nx = self.x - 100 * sin(tryangle)
								ny = self.y - 100 * cos(tryangle)
								if(verif):
									point1 = self.testRay(a1, [nx,ny,tryangle], False)
									if(point1[0] != None):
										if((tryangle - point1[0][2]) ** 2 < 0.01):
											xa = point1[0][0]
											ya = point1[0][1]
											#self.can.create_oval(int(x)-10,int(y)-10,int(x)+10,int(y)+10,fill="blue",outline="blue",width=1,tag=["center",self.tag])
											ray1 = [int(xa),int(ya),tryangle]	
											dista = sqrt((xa-self.x)**2 + (ya-self.y)**2)

								tryangle = angle + gap

								nx = self.x - 100 * sin(tryangle)
								ny = self.y - 100 * cos(tryangle)
								if(verif):
									point1 = self.testRay(a1, [nx,ny,tryangle], False)
									if(point1[0] != None):
										if((tryangle - point1[0][2]) ** 2 < 0.01):
											xa = point1[0][0]
											ya = point1[0][1]
											#self.can.create_oval(int(x)-10,int(y)-10,int(x)+10,int(y)+10,fill="green",outline="green",width=1,tag=["center",self.tag])
											anglePassant1 = [int(xa),int(ya),tryangle + 4 * pi]	
											distb = sqrt((xa-self.x)**2 + (ya-self.y)**2)
									

								if((dista > dist > distb)or(dista < dist < distb)):	
									if(dista <= distb):
										ray1 = [int(x),int(y),angle]	


									elif(dista > distb):
										anglePassant1 = [int(x),int(y),angle]
								else:
									#self.can.create_oval(int(x)-10,int(y)-10,int(x)+10,int(y)+10,fill="green",outline="green",width=1,tag=["center",self.tag])
									pass


							elif angle>=0:	# Si on va dans l'autre sens
								#anglePassant2 = [int(x),int(y),angle]									
								dist = sqrt((x-self.x)**2 + (y-self.y)**2)
								#self.can.create_oval(int(x)-60,int(y)-60,int(x)+60,int(y)+60,fill="blue",outline="blue",width=1,tag=["center",self.tag])

								tryangle = angle - gap
								dista = -1
								distb = -1

								nx = self.x - 100 * sin(tryangle)
								ny = self.y - 100 * cos(tryangle)
								if(verif):
									point1 = self.testRay(a1, [nx,ny,tryangle], False)

									if(point1[1] != None):
										if((tryangle - point1[1][2]) ** 2 < 0.01):
											xb = point1[1][0]
											yb = point1[1][1]
											#self.can.create_oval(int(x)-10,int(y)-10,int(x)+10,int(y)+10,fill="red",outline="red",width=1,tag=["center",self.tag])
											ray2 = [int(xb),int(yb),tryangle]	
											dista = sqrt((xb-self.x)**2 + (yb-self.y)**2)

								tryangle = angle + gap

								nx = self.x - 100 * sin(tryangle)
								ny = self.y - 100 * cos(tryangle)
								if(verif):
									point1 = self.testRay(a1, [nx,ny,tryangle], False)

									if(point1[1] != None):
										if((tryangle - point1[1][2]) ** 2 < 0.01):
											xb = point1[1][0]
											yb = point1[1][1]
											#self.can.create_oval(int(x)-10,int(y)-10,int(x)+10,int(y)+10,fill="black",outline="black",width=1,tag=["center",self.tag])
											anglePassant2 = [int(xb),int(yb),tryangle + 4 * pi]											
											distb = sqrt((xb-self.x)**2 + (yb-self.y)**2)	

								if((dista > dist > distb)or(dista < dist < distb)):											
									if(dista <= distb):
										ray2 = [int(x),int(y),angle]	


									elif(dista > distb):
										anglePassant2 = [int(x),int(y),angle]
								else:
									#self.can.create_oval(int(x)-10,int(y)-10,int(x)+10,int(y)+10,fill="green",outline="green",width=1,tag=["center",self.tag])
									pass


					elif ((b1[0] >= x >= b2[0]) or (b1[0] <= x <= b2[0])) and ((b1[1] >= y >= b2[1]) or (b1[1] <= y <= b2[1])): # Vérification qu'on est dans le segment
						if angle<=0:	# Si on va dans un sens
							if dist < minDist1 or minDist1 == -1: 	# Si initialisation ou distance minimale
								minDist1 = dist
								ray1 = [int(x),int(y),angle]	# Affichage du centre

						elif angle >0:	# Si on va dans l'autre sens
							if dist < minDist2 or minDist2 == -1:	# Si initialisation ou distance minimale
								minDist2 = dist
								ray2 = [int(x),int(y),angle]	# Affichage du centre


		if anglePassant1 != None:
			if(anglePassant1[2] < 2 * pi):
				distp1 = sqrt((anglePassant1[0]-self.x)**2+(anglePassant1[1]-self.y)**2)
				dist1 = sqrt((ray1[0]-self.x)**2+(ray1[1]-self.y)**2)
				if dist1 < distp1:
					anglePassant1 = None
			else:
				anglePassant1[2] = anglePassant1[2] - 4 * pi
		if anglePassant2 != None:
			if(anglePassant2[2] < 2 * pi):
				distp2 = sqrt((anglePassant2[0]-self.x)**2+(anglePassant2[1]-self.y)**2)
				dist2 = sqrt((ray2[0]-self.x)**2+(ray2[1]-self.y)**2)
				if dist2 < distp2:
					anglePassant2 = None
			else:
				anglePassant2[2] = anglePassant2[2] - 4 * pi
		return [ray1, ray2, anglePassant1, anglePassant2]

	def deleteRayons(self):
		self.can.delete(self.tag)

if __name__ == '__main__':
	from main import *
	app = Application().mainloop()