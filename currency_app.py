###############################################################################
#                            Evolution of Currency                            #
###############################################################################


#BIBLIOTECI UTILIZATE

import requests
from bs4 import BeautifulSoup
from tkinter import *
import tkinter as tk
from time import*
from datetime import date
from datetime import timedelta
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import numpy as np

#BACKEND

url='https://www.cursbnr.ro/'
source_code=requests.get(url)

#Statusul paginii web
print("Statusul paginii web: ",source_code.status_code)

#cream o lista cu principalele monede(prescurtari ale denumirilor) aflate pe piata monetara
soup=BeautifulSoup(source_code.content)
nume_monede=soup.find_all('td',{'class':'text-center hidden-xs'})#informatiile obtinute necesita o "curatare"
lista_monede_prescurtari=[moneda.text for moneda in nume_monede]
print("Lista monedelor este: ",lista_monede_prescurtari)

#cream o lista cu cotatia monedelor in ultimele 3 zile
monede_cotatie=soup.find_all('td',{'class':'text-center'})#informatiile obtinute necesita o "curatare"
lista_cotatie=[cotatia.text for cotatia in monede_cotatie]#lista ce contine cotatiile in ultimele 3 zile pt fiecare moneda

#inlaturam din lista datele irelevante-ultimele 8 elemente din lista
for i in range(8):#s-au sters ultimele 8 elemente din lista
    del lista_cotatie[-1]

#Cream o lista cu catatiile tuturor monedelor pentru ziua curenta
lista_cotatie_curenta=[float(lista_cotatie[i]) for i in range(len(lista_cotatie)) if i%7==1]
print("\nCotatia curenta a monedelor: ",lista_cotatie_curenta)

#Cream o lista cu cotatiile monedelor ieri
lista_cotatie_ieri1=[float(lista_cotatie[i]) for i in range(len(lista_cotatie)) if i%7==3]
print("\nCotatia de ieri a monedelor: ",lista_cotatie_ieri1)
    
#Cream o lista cu cotatiile de acum doua zile
lista_cotatie_ieri2=[float(lista_cotatie[i]) for i in range(len(lista_cotatie)) if i%7==5]
print("\nCotatia de acum doua zile a monedelor: ",lista_cotatie_ieri2)

#Cream o functie ce returneaza cotatia curenta a monedelor: EUR,USD,CHF,GBT
def cotatia():
    label2.config(text=str(lista_cotatie_curenta[0])+" RON",bg='black',fg = "red")
    label3.config(text=str(lista_cotatie_curenta[1])+" RON",bg='black',fg = "red")
    label4.config(text=str(lista_cotatie_curenta[2])+" RON",bg='black',fg = "red")
    label5.config(text=str(lista_cotatie_curenta[3])+" RON",bg='black',fg = "red")

#FRONTEND

#Crearea si configurarea ferestei principale
root  =  Tk()
root.title("CurrencyApp")
root.maxsize(850,600)# setarea dimeniunilor (width x height) ferestrei principale
root.config(bg="black")

#Crearea celor doua frame-uri in care vor fi amplasate widget-urile

#- Cream frame-ul din stanga
left_frame  =  Frame(root,  width=500,  height=  400,  bg='black')
left_frame.grid(row=0,  column=0,  padx=10,  pady=5)

#-Cream frame-ul din dreapta
right_frame  =  Frame(root,  width=650,  height=400,  bg='black')
right_frame.grid(row=0,  column=1,  padx=10,  pady=5)

#Cream graficul amplasat in frame-ul din stanga
plt.style.use('dark_background')
fig = Figure(figsize = (6, 6),dpi = 100)

#-Cream elementele pentru axa Ox, ce vor fi ultimele 3 zile calendaristice, incluzand ziua curenta
zile=[]
x=date.today()#data calendaristica de astazi
y=x - timedelta(days = 1)#data calendaristica de ieri
z=x - timedelta(days = 2)#data calendaristica de alaltaieri
zile.append(str(z))
zile.append(str(y))
zile.append(str(x))

#-lista cotatiilor EUR in ultimele 3 zile
cotatii=[lista_cotatie_ieri2[0],lista_cotatie_ieri1[0],lista_cotatie_curenta[0]]

#-lista cotatiilor USD in ultimele 3 zile
cotatii_usd=[lista_cotatie_ieri2[1],lista_cotatie_ieri1[1],lista_cotatie_curenta[1]]

#-Cream graficul pentru evolutia EUR si USD in ultimele 3 zile: axa Ox-datele calendaristice, axa Oy-cotatii
fig, ax = plt.subplots()
ax.set_xlabel('Day',color="red")
ax.set_ylabel('Currency Quotations',color="red")
ax.spines['top'].set_color('none')# setam cele 4 axe ale conturului graficului
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_color('blue')
ax.spines['left'].set_color('blue')
#--Axa Oy va contine valori numerice cuprinse intre cea mai mare si cea mai mica cotatie avauta de EUR si USD in ultimele 3 zile, luand un pas de discretizare h=0.01
lista_axay=[lista_cotatie_ieri2[0],lista_cotatie_ieri1[0],lista_cotatie_curenta[0],lista_cotatie_ieri2[1],lista_cotatie_ieri1[1],lista_cotatie_curenta[1]]
lista_axay.sort()
l=np.arange(((lista_axay[0]*10000)//100)/100,((lista_axay[-1]*10000)//100)/100+0.01,0.02)
ax.set_yticks(l)#setarea valorilor pentru axa Oy

#--Plotarea efectiva a graficului pentru monedele EUR si USD
ax.plot(zile,cotatii,"o--c",label="EUR")
ax.plot(zile,cotatii_usd,"o--m",label="USD")
ax.legend(loc='best')
ax.tick_params(axis='y', colors='orange')
ax.tick_params(axis='x', colors='orange')

#--cream un Tkinter canvas ce contine Matplotlib figure
canvas = FigureCanvasTkAgg(fig,master = right_frame)
canvas.draw()

#--plasam canvas-ul in fereastra principala Tkinter
canvas.get_tk_widget().grid(row=0,  column=0,  padx=5,  pady=5)

#Cream widget-urile aflate in frame-ul stang
Label(left_frame,  text="Evolution of currency",font=('Verdana',12,'bold'),bg='black',fg='Steel Blue',bd=2,relief=RAISED).grid(row=0,  column=0,  padx=5,  pady=5)

localtime=date.today()
label1= Label(left_frame,text = localtime,font=('arial', 10, 'bold'),bg='black',fg = "Steel Blue",bd = 10, anchor = 'w').grid(row=1,  column=0,  padx=5,  pady=5)

#-Cream un frame ce va contine label-urile monedelor si butonul ce genereaza cotatia curenta a lor
tool_bar  =  Frame(left_frame,  width=180,  height=195,  bg='black')
tool_bar.grid(row=2,  column=0,  padx=5,  pady=5)

#--Cream toate wedget-urile din tool_bar
Label(tool_bar,  text="Currency",  relief=RAISED,bg='black',fg = "Steel Blue").grid(row=0,  column=0,  padx=5,  pady=3,  ipadx=10)
Label(tool_bar,  text="Quote",  relief=RAISED,bg='black',fg = "Steel Blue").grid(row=0,  column=1,  padx=5,  pady=3,  ipadx=10)
Label(tool_bar,  text="EUR",bg='black',fg = "Steel Blue").grid(row=2,  column=0,  padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
label2=Label(tool_bar,  text="__RON",bg='black',fg = "Steel Blue")
label2.grid(row=2,  column=1,  padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
Label(tool_bar,  text="USD",bg='black',fg = "Steel Blue").grid(row=3,  column=0,  padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
label3=Label(tool_bar,  text="__RON",bg='black',fg = "Steel Blue")
label3.grid(row=3,  column=1,  padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
Label(tool_bar,  text="CHF",bg='black',fg = "Steel Blue").grid(row=4,  column=0,  padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
label4=Label(tool_bar,  text="__RON",bg='black',fg = "Steel Blue")
label4.grid(row=4,  column=1,  padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
Label(tool_bar,  text="GBT",bg='black',fg = "Steel Blue").grid(row=5,  column=0,  padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
label5=Label(tool_bar,  text="__RON",bg='black',fg = "Steel Blue")
label5.grid(row=5,  column=1,  padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
buton1=Button(tool_bar,text="Today",font=('arial', 10, 'bold'),bg='black',fg = "brown",anchor = 'w',command=cotatia)
buton1.grid(row=8,  column=1,  padx=5,  pady=5)
root.mainloop














