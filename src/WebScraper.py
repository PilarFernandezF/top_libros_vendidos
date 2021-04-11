import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

#url a la que accederemos para hacer web scraping
url = 'https://www.casadellibro.com/top-libros'

#Fichero donde grabaremos el dataset con la información que hemos recuperado de la url anterior
myFile = 'top_libros_vendidos.csv'
          
#Hacemos la petición de la url y recuperamos el código devuelto en la petición y los datos de la página
page = requests.get(url)
statusCode = page.status_code
htmlText = page.text

#En esta lista almacenaremos los libros que hemos recuperado de la url 
listaLibros = list()        

#Si el statusCode es 200 aceptamos los contenidos leídos si no, devolvemos null
if statusCode == 200:
    #Parseamos la página con BeautifulSoup para poder recorrerla y acceder a la información que queremos recuperar
    html = BeautifulSoup(htmlText, "html.parser")
    
    #Recuperamos los libros más vendidos de la url indicada
    libros = html.find_all('div', {'class': 'col-sm-4 col-md-2 col-6'})

    #Recorremos la información de cada uno de los libros para obtener la información que queremos
    for j, libro in enumerate(libros):
        #Recuperamos la información del título
        tituloConSaltos = libro.find('a', {'class': 'product-title text-left secondary--text text--darken-1'}).getText()
        #Eliminamos los saltos de línea y espacios en blanco contenidos en el título
        titulo = tituloConSaltos.strip()
        #Recuperamos lo datos del autor del libro
        autor = libro.find('span', {'span data-v-388927d3': ''}).getText()
        
        #Recuperamos la información adicional para cada libro
        datosLibro = libro.find_all('span', {'span data-v-7a943a50':'', 'class':'text-caption'})
        tipoTapa = ''
        puntuacion = ''
        for k, datoLibro in enumerate(datosLibro):
            dato = datoLibro.getText();
            #En datosLibro tenemos puntuacion y tipo de tapa pero no siempre viene puntuación. Si el primer item es un valor entero es puntuacion y el siguiente es
            #el tipo de tapa, en caso de no ser el primero un entero ponemos la puntuación a nulo porque no la tendremos
            if k==0:
                puntuacion = None
                for conv in (int, float, complex):
                    try:
                        puntuacion = conv(dato)
                        break
                    except ValueError:
                        puntuacion=''
                        tipoTapa = dato
                        pass
            else:
                tipoTapa = dato

        #Creamos un diccionario con los datos que hemos recuperado del libro
        diccionarioLibro = {'titulo':titulo, 'autor': autor, 'puntuacion': str(puntuacion), 'tipoTapa': tipoTapa}
        #Incluimos el diccionario con los datos del libro en una lista donde tendremos todos los libros obtenidos
        listaLibros.append(diccionarioLibro)      

    #Vamos a escribir los datos obtenidos en un fichero csv que contendrá el dataset
    with open(myFile, 'w', newline='') as file:
        writer = csv.writer(file)
        #Escribimos los datos de la cabecera
        writer.writerow(["TITULO","AUTOR","PUNTUACION","TIPO_TAPA"])
        for x in range(0, len(listaLibros)):
            #Para cada uno de los libros obtenidos escribimos los datos recuperados
            writer.writerow([listaLibros[x].get('titulo'),listaLibros[x].get('autor'),listaLibros[x].get('puntuacion'),listaLibros[x].get('tipoTapa')])

    #Proceso finalizado correctamente
    print("Proceso finalizado")    
else:
    #Si no recibimos un 200 como respuesta a la petición no habremos recuperado la página y no podremos acceder a la información de la misma
    print("No hemos podido recuperar la página")
            