# Importar Bibliotecas
from tkinter import *
from tkinter import messagebox # Un cuadro de mensaje es un cuadro de diálogo modal, lo que significa que no se puede producir ninguna entrada.
from tkinter import ttk 
import sqlite3

# Desarrollo de la Interfaz grafica (ventana principal)
root=Tk()
root.title("REGISTRO DE PERSONAL")
root.geometry("600x350")
root.configure(bg="white")

#definir variables
miId=StringVar()
miNombre=StringVar()
miCargo=StringVar()
miSalario=StringVar()

#crear una funcion y conectar la base de datos
def conexionBBDD():
	miConexion=sqlite3.connect("base")
	miCursor=miConexion.cursor()

	try:#crear la tabla de la base de datos
		miCursor.execute('''
			CREATE TABLE empleado (
			ID INTEGER PRIMARY KEY AUTOINCREMENT,
			NOMBRE VARCHAR(50) NOT NULL,
			CARGO VARCHAR(50) NOT NULL,
			SALARIO INT NOT NULL)
			''')
		messagebox.showinfo("CONEXION","Base de Datos Creada exitosamente")
	except:
		messagebox.showinfo("CONEXION", "Conexión exitosa con la base de datos")

def eliminarBBDD():#funcion para eliminar la base de datos
	miConexion=sqlite3.connect("base")
	miCursor=miConexion.cursor()
	if messagebox.askyesno(message="¿Los Datos se perderán definitivamente, Desea continuar?", title="ADVERTENCIA"):#ventana permite preguntar  a cerca de alguna desicion
		miCursor.execute("DROP TABLE IF EXISTS empleado")
		miConexion.commit()
	else:
		pass
	limpiarCampos()
	mostrar()
	miConexion.close()

def eliminarRegistro():
	miConexion=sqlite3.connect("base")
	miCursor=miConexion.cursor()
	try:
		if messagebox.askyesno(message="¿Realmente desea eliminar el registro?", title="ADVERTENCIA"):
			miCursor.execute("DELETE FROM empleado WHERE ID = ?", (miId.get(),))
			miConexion.commit()
	except:
		messagebox.showwarning("ADVERTENCIA","Ocurrió un error al tratar de eliminar el registro")
		pass
	limpiarCampos()
	mostrar()
	miConexion.close()

def salirAplicacion():#funcion de consulta para salir de la aplicacion
	valor=messagebox.askquestion("Salir","¿Está seguro que desea salir de la Aplicación?")
	if valor=="yes":
		root.destroy()#este comando omite la funcion

def limpiarCampos():#limpiar campos
	miId.set("")
	miNombre.set("")
	miCargo.set("")
	miSalario.set("")

def mensaje():#mostrar informacion de la apliaccion
	acerca='''
	Aplicación Python
	Proyecto Licyt
	'''
	messagebox.showinfo(title="INFORMACION", message=acerca)

################################ Creacion Métodos CRUD ##############################

def crear():#funcion crear cursor y conectar con base de datos
	miConexion=sqlite3.connect("base")
	miCursor=miConexion.cursor()
	try:
		datos=miNombre.get(),miCargo.get(),miSalario.get()
		miCursor.execute("INSERT INTO empleado VALUES(NULL,?,?,?)", (datos))#valores extraidos de las cajas de texto
		miConexion.commit()#actualiza cambios en la tabla
	except:
		messagebox.showwarning("ADVERTENCIA","Ocurrió un error al crear el registro, verifique conexión con BBDD")#mensaje de error
		pass
	limpiarCampos()
	mostrar()#

def mostrar():#muestra los registros relizaddos automaticamente
	miConexion=sqlite3.connect("base")
	miCursor=miConexion.cursor()
	registros=tree.get_children()#extraer los elementos de la tabla
	for elemento in registros:
		tree.delete(elemento)#permite no duplicar valores

	try:
		miCursor.execute("SELECT * FROM empleado")#llena la tabla con los valores extraidos de la base de datos
		for row in miCursor:
			tree.insert("",0,text=row[0], values=(row[1],row[2],row[3]))
	except:
		pass
	miConexion.close()

                ################################## Tabla ################################
tree=ttk.Treeview(height=10, columns=('#0','#1','#2'))#creacion y configuracion de la tabla
tree.place(x=0, y=130)
tree.column('#0',width=100)
tree.heading('#0', text="ID", anchor=CENTER)
tree.heading('#1', text="Nombre del Empleado", anchor=CENTER)
tree.heading('#2', text="Cargo", anchor=CENTER)
tree.column('#3', width=100)
tree.heading('#3', text="Salario", anchor=CENTER)


def seleccionarUsandoClick(event):
	item=tree.identify('item',event.x,event.y)
	miId.set(tree.item(item,"text"))
	miNombre.set(tree.item(item,"values")[0])
	miCargo.set(tree.item(item,"values")[1])
	miSalario.set(tree.item(item,"values")[2])

tree.bind("<Double-1>", seleccionarUsandoClick)

def actualizar():
	miConexion=sqlite3.connect("base")
	miCursor=miConexion.cursor()
	try:
		datos=miNombre.get(),miCargo.get(),miSalario.get()
		miCursor.execute("UPDATE empleado SET NOMBRE=?, CARGO=?, SALARIO=? WHERE ID="+miId.get(), (datos))#concatena con los datos
		miConexion.commit()
	except:
		messagebox.showwarning("ADVERTENCIA","Ocurrió un error al actualizar el registro")
		pass
	limpiarCampos()
	mostrar()
	miConexion.close()

def borrar():
	miConexion=sqlite3.connect("base")
	miCursor=miConexion.cursor()
	try:
		if messagebox.askyesno(message="¿Realmente desea eliminar el registro?", title="ADVERTENCIA"):
			miCursor.execute("DELETE FROM empleado WHERE ID="+miId.get())
			miConexion.commit()
	except:
		messagebox.showwarning("ADVERTENCIA","Ocurrió un error al tratar de eliminar el registro")
		pass
	limpiarCampos()
	mostrar()
	miConexion.close()

###################### Colocar widgets en la VISTA ######################
########## Creando Los menus ###############
menubar=Menu(root)
menubasedat=Menu(menubar,tearoff=0, bg="gray")#permite separar menús para la mayoría de las ventanas haciendo menús flotantes.
menubasedat.add_command(label="Crear/Conectar Base de Datos", command=conexionBBDD)
menubasedat.add_command(label="Eliminar Base de Datos", command=eliminarBBDD)
menubasedat.add_command(label="Salir", command=salirAplicacion)
menubar.add_cascade(label="Inicio", menu=menubasedat)

ayudamenu=Menu(menubar,tearoff=0, bg="gray")
ayudamenu.add_command(label="Resetear Campos", command=limpiarCampos)
ayudamenu.add_command(label="Acerca", command=mensaje)
menubar.add_cascade(label="Ayuda",menu=ayudamenu)

############## Creando etiquetas y cajas de texto ###########################
e1=Entry(root, textvariable=miId)#esta variable es una ventana oculta

l2=Label(root, text="Nombre")
l2.place(x=50,y=9)
e2=Entry(root, textvariable=miNombre, width=50)
e2.place(x=100, y=10)

l3=Label(root, text="Cargo")
l3.place(x=50,y=40)
e3=Entry(root, textvariable=miCargo)
e3.place(x=100, y=40)

l4=Label(root, text="Salario")
l4.place(x=280,y=40)
e4=Entry(root, textvariable=miSalario, width=10)
e4.place(x=320, y=40)

l5=Label(root, text="BS")
l5.place(x=380,y=40)

################# Creando botones ###########################

b1=Button(root, text="Crear Registro", bg="purple", command=crear)
b1.place(x=50, y=90)
b2=Button(root, text="Modificar Registro", bg="gray", command=actualizar)
b2.place(x=180, y=90)
b3=Button(root, text="Mostrar Lista", bg="green", command=mostrar)
b3.place(x=320, y=90)
b4=Button(root, text="Eliminar Registro",bg="red", command=eliminarRegistro)
b4.place(x=450, y=90)

root.config(menu=menubar)

root.mainloop()
