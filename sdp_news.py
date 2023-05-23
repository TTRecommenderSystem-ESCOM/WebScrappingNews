import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# URL de prueba
url = 'https://www.sdpnoticias.com/arc/outboundfeeds/rss/?outputType=xml'

# Realiza una solicitud GET a la URL del artículo para obtener el contenido de la página web.
resp = requests.get(url)

# Parsea el contenido de la respuesta como XML
soup = BeautifulSoup(resp.content, 'xml')

items = soup.findAll('item')  # Encuentra todos los elementos 'item' en el XML

news_items = []  # Lista para almacenar los diccionarios de noticias

# Itera sobre cada elemento 'item' en items
for item in items:
    news_item = {}  # Crea un diccionario para almacenar los datos de la noticia

    # Guarda el título de la noticia en el diccionario
    news_item['Titulo'] = item.title.text

    # Guarda el resumen de la noticia en el diccionario
    news_item['Resumen'] = item.description.text

    # Guarda la URL de la noticia en el diccionario
    news_item['URL'] = item.link.text

    Categoria = item.link.text

    # Extrae la categoría de la URL utilizando una expresión regular
    pattern = r"https:\/\/www\.sdpnoticias\.com\/([^\/]+)"
    match = re.search(pattern, Categoria)
    category = match.group(1)

    # Guarda la categoría de la noticia en el diccionario
    news_item['Seccion'] = category

    # Guarda el nombre del sitio de publicación en el diccionario
    news_item['Sitio de publicacion'] = 'SDP Noticias'

    # Guarda la fecha de publicación de la noticia en el diccionario
    news_item['Fecha de publicacion'] = item.pubDate.text

    # Guarda el autor de la noticia en el diccionario
    news_item['Autor'] = item.find('dc:creator')

    # Guarda el contenido de la noticia en el diccionario
    news_item['Contenido'] = item.find('content:encoded')

    # Guarda la URL de la imagen de la noticia en el diccionario
    news_item['Imagen'] = item.find('media:content')['url']

    news_items.append(news_item)  # Agrega el diccionario a la lista de noticias

df = pd.DataFrame(news_items, columns=['Titulo', 'Resumen', 'Contenido', 'Seccion', 'Sitio de publicacion', 'URL',
                                       'Fecha de publicacion', 'Autor', 'Imagen'])  # Crea un DataFrame con los datos

df.to_csv('C:/Users/Tania/PycharmProjects/TTwebscrapping/noticias_csv/sdp_news.csv',
          index=False)  # Guarda el DataFrame en un archivo CSV sin incluir los índices

print(
    'Se guardó el archivo CSV correctamente')  # Imprime un mensaje indicando que el archivo CSV se guardó correctamente
