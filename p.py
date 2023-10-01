import nltk
import numpy as np
import pandas as pd

#Descarga los recursos necesarios para NLTK
#nltk.download('punkt')

# Cargar los documentos desde archivos .txt y obtener sus nombres
def cargar_documentos(documentos):
    textos = []
    nombres = []
    for documento in documentos:
        with open(documento, 'r', encoding='utf-8') as archivo:
            texto = archivo.read()
            textos.append(texto)
            nombres.append(documento)
    return textos, nombres

# Cargar palabras desde un archivo .txt
def cargar_palabras(archivo_palabras):
    with open(archivo_palabras, 'r', encoding='utf-8') as archivo:
        palabras = archivo.read().split()
    for i in palabras:
        if i >= '0' and i<='9':
            palabras.remove(i)
    return palabras

# Crear una matriz booleana con nombres de documentos y palabras
def crear_matriz_booleana(documentos, palabras, nombres):
    matriz = np.zeros((len(documentos) + 1, len(palabras) + 1), dtype=object)
    # Rellenar la primera fila con nombres de palabras
    matriz[0, 1:] = palabras
    # Rellenar la primera columna con nombres de documentos
    matriz[1:, 0] = nombres
    for i, doc in enumerate(documentos):
        tokens = nltk.word_tokenize(doc)
        for j, palabra in enumerate(palabras):
            matriz[i + 1, j + 1] = int(palabra in tokens)
    return matriz

# Rutas a los archivos .txt de documentos y palabras
archivos_documentos = ["repositorio\evangelio_segun_marcos.txt","repositorio/funes_el_memorioso.txt"]
archivo_palabras = "diccionarios_stemming\diccionario_stemming_evangelio_segun_marcos.txt"

# Cargar documentos, nombres de documentos y palabras
documentos, nombres_documentos = cargar_documentos(archivos_documentos)
palabras = cargar_palabras(archivo_palabras)

# Crear matriz booleana con nombres de documentos y palabras
matriz_booleana = crear_matriz_booleana(documentos, palabras, nombres_documentos)

# Imprimir la matriz
DF = pd.DataFrame(matriz_booleana)
DF.transpose
print(DF)
DF.to_csv("matriz.csv",sep=",",header=False)