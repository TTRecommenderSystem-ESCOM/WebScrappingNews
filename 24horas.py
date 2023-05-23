#https://www.24-horas.mx/feed/

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.24-horas.mx/feed/'

resp = requests.get(url)  # Realiza una solicitud GET al URL especificado
soup = BeautifulSoup(resp.content, features='xml')  # Parsea el contenido de la respuesta como XML
print(soup.prettify())  # Imprime el contenido HTML/XML formateado

itemss = soup.findAll('item')  # Encuentra todos los elementos 'item' en el XML
len(itemss)  # Imprime la cantidad de elementos 'item' encontrados

item = itemss[0]  # Obtiene el primer elemento 'item'

item.link.text  # Imprime el texto dentro de la etiqueta 'link' del primer elemento 'item'

news_items = []  # Lista para almacenar los diccionarios de noticias

# Itera sobre cada elemento 'item' en itemss
for item in itemss:
    noticia_articulo = {}  # Crea un diccionario para almacenar los datos de la noticia

    # Guarda el título de la noticia en el diccionario
    noticia_articulo['Titulo'] = item.title.text

    # Encuentra el último párrafo en la descripción de la noticia y lo guarda en el diccionario
    last_paragraph = item.find('description').find_all('p')[-1].text
    noticia_articulo['Descripción'] = last_paragraph

    # Guarda la URL de la noticia en el diccionario
    noticia_articulo['URL'] = item.link.text

    # Guarda la sección de la noticia en el diccionario
    noticia_articulo['Seccion'] = item.category.text

    # Guarda el nombre del sitio de publicación en el diccionario
    noticia_articulo['Sitio de publicacion'] = '24 Horas'

    # Guarda la fecha de publicación de la noticia en el diccionario
    noticia_articulo['Fecha de publicacion'] = item.pubDate.text

    # Guarda el autor de la noticia en el diccionario
    noticia_articulo['Autor'] = item.find('dc:creator')

    # Guarda el contenido de la noticia en el diccionario
    noticia_articulo['Contenido'] = item.find('content:encoded').text

    # Parsea el contenido de la noticia
    soup = BeautifulSoup(noticia_articulo['Resumen'], 'html.parser')

    # Busca la etiqueta 'img' en el contenido de la noticia
    imagen = soup.find('img')['src']

    if imagen:  # Si se encontró una imagen, guarda la URL de la imagen en el diccionario
        noticia_articulo['Imagen'] = imagen
    else:  # Si no se encontró una imagen, guarda None en el diccionario
        noticia_articulo['Imagen'] = None

    news_items.append(noticia_articulo)  # Agrega el diccionario a la lista de noticias

df = pd.DataFrame(news_items, columns=['Titulo', 'Resumen', 'Contenido', 'Seccion', 'Sitio de publicacion', 'URL',
                                       'Fecha de publicacion', 'Autor', 'Imagen'])  # Crea un DataFrame con los datos

print(news_items)  # Imprime la lista de diccionarios de noticias

df = pd.DataFrame(news_items)

df = df.drop_duplicates()

print(df)

#Guaramos información de la noticia
df.to_csv('24horas.csv',index=False)
