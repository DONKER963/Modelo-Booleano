from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import os
from collections import Counter
import re
import numpy as np
import pandas as pd
from collections import deque

class app(tk.Frame):
    con = ""
    repositorio = "repositorio"
    documentos = []
    nombres = []
    palabras = []
    matrizBoleana = None
    qposfija = None
    def __init__(self,master = None):#constructor
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        Label(text="Modelo Booleano",font=("Arial",22)).place(x=280,y=10)#las empaquetamos en la ventana
        Label(text="Ejemplo:\t( ( clave1 AND clave2 ) AND clave3 ) OR  ( clave4 OR claveN )", font=("Helvetica", 12, "italic"),foreground="gray").place(x=200,y=50)
        Label(text="Ingrese la Consulta Q: ",font=("Arial",16,)).place(x=60,y=80)
        self.consulta = Entry(self.master)
        self.consulta.place(x=275,y=80,width=300,height=25)
        #Button(text="Notación Posfija",command=self.notacion_Posifja).place(x=600,y=80)
        Button(text="Actualizar Repositorio",command=self.actualizarRepositorio).place(x= 100,y=120)
        Button(text="Actualizar Diccionarios",command=self.actualizarDiccionarios).place(x=325,y=120)
        Button(text="Aplicación Del Metodo",command=self.modelo_Booleano).place(x = 550, y =120)
        
    def notacion_Posifja(self):
        label_Q=""
        self.con = self.consulta.get()#leemos la consulta q
        if self.con != None:
            self.qposfija=self.notacionPosfija(self.con)
            for i in self.qposfija:
                label_Q =  label_Q +" "+i
            Label(text=label_Q).place(x=100,y=170)
            self.busquedaConsulta(self.qposfija)
            
        

    def actualizarDiccionarios(self):
        with os.scandir(self.repositorio) as ficheros:
            self.documentos, self.nombres = self.diccionario(ficheros)

    def diccionario(self,repositorio): #metodo para crear los diccionarios
        textos = []
        nombres = []
        for doc in repositorio:#recorremos los archivos del repositorio
            print(doc.name)
            nombres.append(doc.name)
            with open(doc.path,'r',encoding="utf-8") as file:#abrimos documento x doc
                texto = file.read()#leemos el contenido
            palabras = re.findall(r'\b\w+\b',texto.lower())#Convertimos a minuscula y separamos palabras
            #hacemos stopword
            stop_words = set(stopwords.words('spanish'))
            palabras_stopwords = [word for word in palabras if word.lower() not in stop_words]
            #aplicamos stemming
            stemmer = PorterStemmer()
            palabras_stemming = [stemmer.stem(word) for word in palabras_stopwords]
            # Convertir las palabras stemmizadas de nuevo a un texto
            texto_stemmed = ' '.join(palabras_stemming)
            textos.append(texto_stemmed)
            #contamos las frecuencias de:
            #texto limpio // texto con stopwords // texto con stemming
            frecuencias =+ Counter(palabras)#cuenta las frecuencias
            frecuencias_stopwords =+ Counter(palabras_stopwords)#cuenta las frecuencias
            frecuencias_stemming =+ Counter(palabras_stemming)#cuenta las frecuencias
        #creamos la tabla de frecuencias para el texto limpio
        tabla_frecuencias = pd.DataFrame(data=frecuencias.items(), columns=['Palabra', 'Frecuencia'])#lo lista en 2 colm
        tabla_frecuencias = tabla_frecuencias.sort_values(by='Frecuencia', ascending=False)#ordena
        tabla_frecuencias.to_csv("diccionarios/diccionario.txt",index=False,sep=" ",header=False)#guarda
        #creamos la tabla de frecuencias para el texto sin stopwords
        tabla_frecuencias_stopwords = pd.DataFrame(data=frecuencias_stopwords.items(), columns=['Palabra', 'Frecuencia'])#lo lista en 2 colm
        tabla_frecuencias_stopwords = tabla_frecuencias_stopwords.sort_values(by='Frecuencia', ascending=False)#ordena
        tabla_frecuencias_stopwords.to_csv("diccionarios/diccionario_stopwords.txt",index=False,sep=" ",header=False)#guarda
        #creamos la tabla de frecuencias para el texto con stemming
        tabla_frecuencias_stemming = pd.DataFrame(data=frecuencias_stemming.items(), columns=['Palabra', 'Frecuencia'])#lo lista en 2 colm
        tabla_frecuencias_stemming = tabla_frecuencias_stemming.sort_values(by='Frecuencia', ascending=False)#ordena
        tabla_frecuencias_stemming.to_csv("diccionarios/diccionario_stemming.txt",index=False,sep=" ",header=False)
        return textos,nombres

    def actualizarRepositorio(self):
        self.repositorio = filedialog.askdirectory(mustexist=True)
        Label(text=self.repositorio).place(x = 100, y=150)
    def modelo_Booleano(self):
        self.actualizarDiccionarios()
        with open("diccionarios\diccionario_stemming.txt", 'r',encoding='utf-8') as archivo:
            self.palabras = archivo.read().split()
        for i in self.palabras:
            if i >='0' and i<='9':
                self.palabras.remove(i)
        self.matrizBoleana = self.crear_matriz_booleana(self.documentos,self.palabras,self.nombres)
        self.tabla_hash = self.tablaHash(self.matrizBoleana)
        self.notacion_Posifja()
        

    def crear_matriz_booleana(self,documentos, palabras, nombres):
        matriz = np.zeros((len(documentos) , len(palabras) ), dtype=object)
        for i, doc in enumerate(documentos):
            tokens = nltk.word_tokenize(doc)
            for j, palabra in enumerate(palabras):
                matriz[i, j ] = int(palabra in tokens)
        DF = pd.DataFrame(matriz,index=nombres,columns=palabras)
        DF.transpose()
        DF.to_csv("matriz/matriz booleana.csv",sep=",")
        return DF
    
    def Hash_func(self,value):
        key = 0
        for i in range(0,len(value)):
            key += (ord(value[i]))**(i+1)
        return key % 512

    def tablaHash(self,DF):
        indices = {"Termino": [],
                "Aparicion":[],
                "Documento": []}
        D = []
        for colum in DF:
            Total = DF[str(colum)].sum()
            for i in DF.index:
                if DF[colum][i] == 1:
                    D.append(i)
            indices["Termino"].append(str(colum))
            indices["Aparicion"].append(Total)
            indices["Documento"].append(str(D))
            D.clear()
        hash = []
        indiceInvertido = pd.DataFrame(indices)
        for row in indiceInvertido.itertuples():
            key = self.Hash_func(row.Termino)
            hash.append(key)
        indiceInvertido['HASH'] = hash
        
        indiceInvertido = indiceInvertido.sort_values(by=["HASH"])
        indiceInvertido.to_csv("matriz/tabla Hash.csv",sep=",",index=False)
        return indiceInvertido

    def vaciado(self,a,b):
        while a[-1] != "(":
            temp = a.pop()
            b.append(temp)
        a.pop()
        return a,b
    
    def busquedaConsulta(self,qposfija):
        while(qposfija != None):
            a = qposfija.popleft()
            match a:
                case "NOT":
                    pass
                case "AND":
                    pass
                case "OR":
                    pass
    def precesadoConsulta(self,a):
        #hacemos stopword
        stop_words = set(stopwords.words('spanish'))
        palabras_stopwords = [word for word in a if word.lower() not in stop_words]
        #aplicamos stemming
        stemmer = PorterStemmer()
        palabras_stemming = [stemmer.stem(word) for word in palabras_stopwords]

    def notacionPosfija(self,consulta):
        a = []
        b = []
        expresion = consulta.split()
        for i in expresion:
            match i:
                case "NOT":
                    a.append(i)
                case "(":
                    a.append(i)
                case ")":
                    a,b = self.vaciado(a,b)
                case "AND":
                    a.append(i)
                case "OR":
                    a.append(i)
                case _:
                    b.append(i)
        qpos = deque(b)
        return qpos

class notacion():
    consulta =  ""
    pila_operandos = []
    pila_posifja = []
    def __init__(self,master,consulta):
        self.master = master
        self.ventana_notacion = tk.Toplevel(self.master)
        self.ventana_notacion.geometry("600x700+100+10")
        self.consulta = consulta
        self.create_widgets()
        
    def create_widgets(self):
        Label(self.ventana_notacion, text="Consulta: "+self.consulta).place(x=50,y=30)
        self.pila_posifja = self.notacionPosfija()
        Label(self.ventana_notacion,text=f"Consulta Posfija: {self.pila_posifja}").place(x=50,y=60)

    def vaciado(self,a,b):
        while a[-1] != "(":
            temp = a.pop()
            b.append(temp)
        a.pop()
        return a,b
    
    def precesadoConsulta(self,a):
        #hacemos stopword
        stop_words = set(stopwords.words('spanish'))
        palabras_stopwords = [word for word in a if word.lower() not in stop_words]
        #aplicamos stemming
        stemmer = PorterStemmer()
        palabras_stemming = [stemmer.stem(word) for word in palabras_stopwords]

    def notacionPosfija(self):
        a = []
        b = []
        expresion = self.consulta.split()
        for i in expresion:
            match i:
                case "NOT":
                    a.append(i)
                case "(":
                    a.append(i)
                case ")":
                    a,b = self.vaciado(a,b)
                case "AND":
                    a.append(i)
                case "OR":
                    a.append(i)
                case _:
                    b.append(i)
        return b


if __name__ == "__main__":#funcion principal
    root = tk.Tk()#creamos interfaz grafica
    app = app(master=root)#la instanciamos en nuestra clase
    ancho_ventana = 800
    alto_ventana = 600
    x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
    y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2
    posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
    root.geometry(posicion)
    root.mainloop()#inicializamos