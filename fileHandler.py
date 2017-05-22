
def saveMap(fileName,musee):	# Enregistrement au bon format de fichier : materiau;x1,y1;x2,y2;....;
	file = open("maps/"+fileName+".map",'w',encoding="utf-8")

	for poly in musee:
		file.write(poly.material+";")
		for point in poly.points:
			file.write("{},{};".format(point.x,point.y))
		file.write("\n")
	file.close()
	
	print("Map saved at : maps/{}.map".format(fileName))

def openMap(fileName):
	try:
		file = open("maps/"+fileName+".map",'r',encoding="utf-8")
	except:
		print("File does not exist")
		return None

	polygons = []
	for line in file:
		polygons += [line.strip().split(";")[:-1]]	# On récupère tout, sauf la dernière case, vide (car la ligne se finit par ';')

	return polygons