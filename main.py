import re
from collections import Counter
import pandas as pd
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

def diccionario(repositorio): #metodo para crear los diccionarios
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

def diccionario_separados(rep):#metodo  diccionarios por separado
    for doc in rep:#recorremos todos los documentos en el repositorio
        print(doc.name)
        with open(doc.path, 'r',encoding="utf-8") as f:#abre documento
            texto = f.read()#se lo lee
        #palabras ya tokenizadas
        palabras = re.findall(r'\b\w+\b', texto.lower())  # Convertir a minúsculas y dividir en palabras
        #Diccionario texto limpio
        frecuencias = Counter(palabras)#cuenta las frecuencias
        tabla_frecuencias = pd.DataFrame(data=frecuencias.items(), columns=['Palabra', 'Frecuencia'])#lo lista en 2 colm
        tabla_frecuencias = tabla_frecuencias.sort_values(by='Frecuencia', ascending=False)#ordena
        tabla_frecuencias.to_csv("diccionarios/diccionario_"+doc.name,index=False,sep=":")
        #Diccionario texto stopwords
        stop_words = set(stopwords.words('spanish'))
        palabras_stopwords = [word for word in palabras if word.lower() not in stop_words]
        frecuencias_stopwords = Counter(palabras_stopwords)#cuenta las frecuencias
        tabla_frecuencias_stopwords = pd.DataFrame(data=frecuencias_stopwords.items(), columns=['Palabra', 'Frecuencia'])#lo lista en 2 colm
        tabla_frecuencias_stopwords = tabla_frecuencias_stopwords.sort_values(by='Frecuencia', ascending=False)#ordena
        tabla_frecuencias_stopwords.to_csv("diccionarios/diccionario_stopwords_"+doc.name,index=False,sep=":",header=False)
        #Diccionario texto stemming
        #stem_words = SnowballStemmer('spanish')
        stemmer = PorterStemmer()
        palabras_stemming = [stemmer.stem(word) for word in palabras_stopwords]
        frecuencias_stemming = Counter(palabras_stemming)#cuenta las frecuencias
        tabla_frecuencias_stemming = pd.DataFrame(data=frecuencias_stemming.items(), columns=['Palabra', 'Frecuencia'])#lo lista en 2 colm
        tabla_frecuencias_stemming = tabla_frecuencias_stemming.sort_values(by='Frecuencia', ascending=False)#ordena
        tabla_frecuencias_stemming.to_csv("diccionarios_stemming/diccionario_stemming_"+doc.name,index=False,sep=" ",header=False)

def matrizBol(documentos,nombre_archivo):
     # Inicializar el vectorizador de conteo binario
    vectorizador = CountVectorizer(binary=True)

    # Ajustar el vectorizador y transformar los documentos en una matriz binaria
    matriz_binaria = vectorizador.fit_transform(documentos)

    # Obtener la matriz binaria como una matriz densa (no dispersa)
    matriz_binaria_dense = matriz_binaria.toarray()
    matriz_binaria_dense = np.insert(matriz_binaria_dense, 0, nombre_archivo, axis=0)
    
    print(matriz_binaria_dense)
    # Guardar la matriz binaria en un archivo de texto
    np.savetxt("matriz de incidencias.txt", matriz_binaria_dense, fmt='%s',delimiter='\t')


def leer_documentos_stemming(cont):
    documentos = []
    nombre_archivos = []
    for nombre_archivo in os.listdir("diccionarios_stemming"):
        if nombre_archivo.endswith(".txt"):
            ruta_archivo = os.path.join("diccionarios_stemming", nombre_archivo)
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                contenido = archivo.read()
                documentos.append(contenido)
                nombre_archivos.append(nombre_archivo)
    return documentos,nombre_archivos

def crear_matriz_booleana(documentos, palabras, nombres):
    matriz = np.zeros((len(documentos) , len(palabras) ), dtype=object)
    for i, doc in enumerate(documentos):
        tokens = nltk.word_tokenize(doc)
        for j, palabra in enumerate(palabras):
            matriz[i, j ] = int(palabra in tokens)
    DF = pd.DataFrame(matriz,index=nombres,columns=palabras)
    DF.transpose()
    DF.to_csv("matriz_ind.csv",sep=",")
    return DF

"""def matriz(documentos,palabras,nombres):
    mat = np.zeros((len(documentos)+1, len(palabras)+1), dtype=object)
    for i, doc in enumerate(documentos):
        tokens = nltk.word_tokenize(doc)
        for j, palabra in enumerate(palabras):
            mat[i+1, j+1] = int(palabra in tokens)
    matrizInc = pd.DataFrame(matriz,index=palabras,columns=nombres)
    matrizInc.transpose()
    matrizInc.to_csv("matriz_ind.csv",sep=',',header=False)"""

def notacion_Posfija():
    pass

def Hash_func(value):
        key = 0
        for i in range(0,len(value)):
            key += (ord(value[i]))**(i+1)
        return key % 64

def Search(self,value): # Metodo para buscar elementos
    hash = self.Hash_func(value);
    if self.table[hash] is None:
        return None
    else:
        return hex(id(self.table[hash]))
############################   MAIN      ##############################
contenido = 'repositorio'#dado un repositorio
documentos = []
nombres = []
palabras = []
with os.scandir(contenido) as ficheros:
    documentos, nombres = diccionario(ficheros)

with open("diccionarios\diccionario_stemming.txt", 'r',encoding='utf-8') as archivo:
    palabras = archivo.read().split()
for i in palabras:
    if i >='0' and i<='9':
        palabras.remove(i)
#print(palabras)
#matriz(documentos,palabras,nombres)
DF = crear_matriz_booleana(documentos,palabras,nombres)
print(DF)

indices = {"Termino": [],
           "Aparicion":[],
           "Documento": []}
D = []
for colum in DF:
    Total = DF[str(colum)].sum()
    for i in DF.index:
        if DF[colum][i] == 1:
            D.append(i)
        #print(colum," ",i," ",DF[colum][i])
    indices["Termino"].append(str(colum))
    indices["Aparicion"].append(Total)
    #print(indices["Documento"])
    indices["Documento"].append(str(D))
    #print(D)
    D.clear()

hash = []
indiceInvertido = pd.DataFrame(indices)
print(indiceInvertido)
for row in indiceInvertido.itertuples():
    key = Hash_func(row.Termino)
    hash.append(key)
    #print(row.Termino,row.Aparicion,key)
indiceInvertido['HASH'] = hash
print(indiceInvertido)

c = indiceInvertido.loc[indiceInvertido['HASH'] == 4]
d = indiceInvertido.loc[indiceInvertido['HASH'] == 6]
"""
hola OR perro

hola perro OR
"""


print(indiceInvertido.query("HASH == 4"))


#print(indices["Documento"])
#print(indices)
#documentos,nombre_archivos = leer_documentos_stemming(contenido)
# Crear la matriz binaria y guardarla en el archivo .txt
#matrizBol(documentos,nombre_archivos)

    