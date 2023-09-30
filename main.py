import re
from collections import Counter
import pandas as pd
import os
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

def diccionario(rep):#metodo
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
        tabla_frecuencias_stopwords.to_csv("diccionarios/diccionario_stopwords_"+doc.name,index=False,sep=":")
        #Diccionario texto stemming
        #stem_words = SnowballStemmer('spanish')
        stemmer = PorterStemmer()
        palabras_stemming = [stemmer.stem(word) for word in palabras_stopwords]
        frecuencias_stemming = Counter(palabras_stemming)#cuenta las frecuencias
        tabla_frecuencias_stemming = pd.DataFrame(data=frecuencias_stemming.items(), columns=['Palabra', 'Frecuencia'])#lo lista en 2 colm
        tabla_frecuencias_stemming = tabla_frecuencias_stemming.sort_values(by='Frecuencia', ascending=False)#ordena
        tabla_frecuencias_stemming.to_csv("diccionarios/diccionario_stemming_"+doc.name,index=False,sep=":")

def matrizBol():
     # Inicializar el vectorizador de conteo binario
    vectorizador = CountVectorizer(binary=True)

    # Ajustar el vectorizador y transformar los documentos en una matriz binaria
    matriz_binaria = vectorizador.fit_transform()

    # Obtener la matriz binaria como una matriz densa (no dispersa)
    matriz_binaria_dense = matriz_binaria.toarray()

    # Guardar la matriz binaria en un archivo de texto
    np.savetxt(, matriz_binaria_dense, fmt='%d')


############################MAIN########################
contenido = 'repositorio'
with os.scandir(contenido) as ficheros:
    diccionario(ficheros)

