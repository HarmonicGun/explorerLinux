from tkinter import *
from tkinter import messagebox
import os
import subprocess
import sys
import stat

cp = ''
cpwd= ''

root = Tk()
root.title('Gestor Linux')

nframe2=Frame(root, width= 800, height= 600)
nframe2.pack()
nframe=Frame(root, width= 800, height= 600)
nframe.pack()

ngroup = StringVar()
owner = StringVar()
password = StringVar()
nombre = StringVar()
rmuser = StringVar()

def upLevel():
    clearListbox()
    os.chdir(os.getcwd()+'/..')
    explorerListbox.insert(END,*getLs())

def enterFolder(item):
    try:
        os.chdir(os.getcwd()+'/'+item)
        clearListbox()
        explorerListbox.insert(END,*getLs())
    except Exception as e:
        messagebox.showwarning('Imposible','Este no es un  directorio')

def getLs():
    command = subprocess.run('ls',stdout=subprocess.PIPE)
    return command.stdout.decode('utf-8').strip().split('\n')

def getLsLa():
    command = subprocess.run(['ls','-la'],stdout=subprocess.PIPE)
    return command.stdout.decode('utf-8').strip().split('\n')

def copy(cpf, cdpad):
    global cp
    cp = cpf
    global cpwd
    cpwd = cdpad
    print (cp,cpwd)

def paste(pwd):
    print (cp,cpwd)
    if(cpwd != ''):
        if(pwd == cpwd):
            subprocess.run(['cp','-R', cpwd+'/'+cp, cpwd+'/'+cp+'-copy'])
            clearListbox()
            explorerListbox.insert(END,*getLs())
        else:
            subprocess.run(['cp','-R',cpwd+'/'+cp, pwd])
            clearListbox()
            explorerListbox.insert(END,*getLs())

def cowner(cof):
    global cp
    cp = cof
    print(cof)
    if( owner != ''):
        subprocess.run(['chown',owner.get(),':',ngroup.get(),'-f',cp])
    else:
        print("Inserte usuario valido")




explorerListbox = Listbox(nframe2,width=80)
explorerListbox.insert(END,*getLs())
explorerListbox.grid(row=0,column=0)

def clearListbox():
    explorerListbox.delete(0,END)


buttonUp = Button(nframe,text='Atrás', command=upLevel)
buttonUp.grid(row=1,column=0)
buttonIn = Button(nframe,text='Entrar', command=lambda: enterFolder(explorerListbox.get(ANCHOR)))
buttonIn.grid(row=1, column=1)
buttonCp = Button(nframe,text='Copiar', command=lambda: copy(explorerListbox.get(ANCHOR), os.getcwd()))
buttonCp.grid(row=1, column=2)

buttonPs = Button(nframe,text='Pegar', command=lambda: paste(os.getcwd()))
buttonPs.grid(row=1, column=3)

LabelOwner = Label(nframe, text='Nuevo dueño')
LabelOwner.grid(row=2,column=0)

O = Entry(nframe, textvariable=owner)
O.grid(row=2,column=1)

LabelGroup = Label(nframe, text='Nuevo grupo')
LabelGroup.grid(row=3,column=0)
G = Entry(nframe, textvariable=ngroup)
G.grid(row=3,column=1)

buttonNewOwner = Button(nframe, text='Cambiar de propietario' , command=lambda: cowner(explorerListbox.get(ANCHOR)))
buttonNewOwner.grid(row=3,column=2)

LabelUsuario = Label(nframe, text='Nombre del nuevo usuario')
LabelUsuario.grid(row=4,column=0)

N = Entry(nframe, textvariable=nombre)
N.grid(row=4,column=1)

LabelPassword = Label(nframe, text='Password del nuevo usuario')
LabelPassword.grid(row=5,column=0)

P = Entry(nframe, textvariable=password)
P.grid(row=5,column=1)

def createUser():
    if(password.get()==''):
        subprocess.run(['useradd',nombre.get()])
    else:
        subprocess.run(['useradd','-p',password.get(),nombre.get()])


buttonCreateUser = Button(nframe, text='Crear usuario' , compound=CENTER, command=createUser)
buttonCreateUser.grid(row=7,column=2)

LabeldelUser = Label(nframe, text='usuario a eliminar')
LabeldelUser.grid(row=6,column=0)

D = Entry(nframe, textvariable=rmuser)
D.grid(row=6,column=1)

def deleteUser():
    if (rmuser.get() != ''):
        subprocess.run(['userdel','-f',rmuser.get()])

buttonRmUser = Button(nframe,text='Eliminar usuario', compound=CENTER, command=deleteUser)
buttonRmUser.grid(row=5,column=2)

def Lectura(cd,pad):
    global cp
    cp = cd
    global cpwd
    cpwd = pad
    print(cp)
    os.chmod(cpwd+'/'+cp, stat.S_IRUSR)

def Escritura(cd,pad):
    global cp
    cp = cd
    global cpwd
    cpwd = pad
    print(cp)
    os.chmod(cpwd+'/'+cp, stat.S_IWUSR)

def Ejecutar(cd,pad):
    global cp
    cp = cd
    global cpwd
    cpwd = pad
    print(cp)
    os.chmod(cpwd+'/'+cp, stat.S_IXUSR)

def Todos(cd,pad):
    global cp
    cp = cd
    global cpwd
    cpwd = pad
    print(cp)
    os.chmod(cpwd+'/'+cp, stat.S_IRWXU)


buttonEscritura = Button(nframe, text='Escritura',command=lambda: Escritura(explorerListbox.get(ANCHOR),os.getcwd()))
buttonEscritura.grid(row = 4, column = 4)

buttonLectura = Button(nframe, text='Lectura', command=lambda: Lectura(explorerListbox.get(ANCHOR),os.getcwd()))
buttonLectura.grid(row = 4, column = 3)

buttonEjecutar = Button(nframe, text='Ejecución',command=lambda: Ejecutar(explorerListbox.get(ANCHOR),os.getcwd()))
buttonEjecutar.grid(row = 5, column = 3)

buttonTodos = Button(nframe, text='Todos',command=lambda: Todos(explorerListbox.get(ANCHOR),os.getcwd()))
buttonTodos.grid(row = 5, column = 4)

root.mainloop();
