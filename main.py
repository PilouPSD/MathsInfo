from tkinter import *
from editor import *
import fileHandler

class Application(Tk):
	def __init__(self):
		self.buttons = []

		Tk.__init__(self)
		self.title("Maths-Info")	
		self.resizable(0,0)	# Fenêtre non redimentionable 
		self.main = Canvas(self, width=800, height=800, bg="light grey",border=0)
		self.toolbar = Canvas(self,width=150,height=800,border=0)
		self.toolbar.pack(side=LEFT)
		self.main.pack(side=LEFT)
		self.initToolbar()
		self.editor = Editor(self.main,self.toolbar)
		self.ouvrir()

	def initToolbar(self):
		self.openBtn = Button(self.toolbar, text = "Ouvrir", command = self.ouvrir, width=15,height=2)
		self.saveBtn = Button(self.toolbar, text = "Enregistrer", command = lambda:fileHandler.saveMap(self.name.get(),self.editor.poly), width=15,height=2)
		self.newBtn = Button(self.toolbar, text = "Créer Polygone", command = self.newPoly, width=15,height=2)
		self.delBtn = Button(self.toolbar, text = "Supprimer Poly", command = self.supPoly, width=15,height=2)
		self.rayons = Button(self.toolbar, text = "Créer rayons", command = self.createRayons, width=15,height=2)
		self.switchRay = Button(self.toolbar, text = "Switch Rays/Poly", command = self.switchRay, width=15,height=2)
		self.quitBtn = Button(self.toolbar, text = "Quitter", command = self.destroy, width=15,height=2)

		# Création de la zone de texte pour le nom du fichier
		self.fileName = StringVar()
		self.fileName.set("default")
		self.name = Entry(self.toolbar, textvariable=self.fileName, width=18)

		# Affichage btns
		self.toolbar.create_line(0,190,200,190,width=2,fill="grey")
		self.toolbar.create_text(75,30,text="Map Editor",font=("Trebuchet",15,"bold"))
		self.toolbar.create_line(0,50,200,50,width=2,fill="grey")

		self.openBtn.place(x=20,y=60)
		self.name.place(x=20,y=110)
		self.saveBtn.place(x=20,y=140)

		self.newBtn.place(x=20,y=200)
		self.delBtn.place(x=20,y=250)
		self.rayons.place(x=20,y=340)
		self.switchRay.place(x=20,y=390)
		self.quitBtn.place(x=20,y=750)

	def ouvrir(self):
		polygons = fileHandler.openMap(self.name.get())
		if polygons != None:	# Si None -> Fichier non existant

			for p in self.editor.poly:	# On supprime tous les polygones existants
				p.kill()
			self.editor.poly=[]

			for p in polygons:	# On recrée les polygones chargés
				pt = []
				for point in p[1:]:
					coord = point.split(',')
					pt+=[Point(self.main,int(coord[0]),int(coord[1]),["points"+str(self.editor.nbPoly),self.editor.nbPoly])]
				self.editor.poly += [Polygone(self.main,"poly"+str(self.editor.nbPoly),pt,p[0])]
				self.editor.nbPoly+=1

	def newPoly(self):
		self.editor.saisie()

	def supPoly(self):
		self.editor.deleting = not self.editor.deleting

	def createRayons(self):
		self.editor.doCreateRayons = not self.editor.doCreateRayons

	def switchRay(self):
		try:
			self.editor.rayons.drawMode = not self.editor.rayons.drawMode
			self.editor.rayons.deleteRayons()
			self.editor.rayons.drawRayons()
		except:pass

if __name__ == '__main__':
	app = Application().mainloop()