import requests
from bs4 import BeautifulSoup
import pandas as pd

link = 'https://www.razon.com.mx/rss/feed.xml'
resp = requests.get(link)  # Realiza una solicitud GET al URL especificado
soup = BeautifulSoup(resp.content, features='xml')  # Parsea el contenido de la respuesta como XML
# print(soup.prettify())  # Imprime el contenido HTML/XML formateado

articulos = soup.findAll('item')  # Encuentra todos los elementos 'item' en el XML
len(articulos)  # Imprime la cantidad de elementos 'item' encontrados

# Ejemplo para verificar componentes
articulo = articulos[4]  # Obtiene el quinto elemento 'item' (los índices comienzan en 0)
articulo

noticias_articulos = []  # Lista para almacenar los diccionarios de noticias

# Itera sobre cada elemento 'item' en articulos
for articulo in articulos:
    noticia_articulo = {}  # Crea un diccionario para almacenar los datos de la noticia

    # Guarda el título de la noticia en el diccionario
    noticia_articulo['Titulo'] = articulo.title.text

    # Guarda el resumen de la noticia en el diccionario
    noticia_articulo['Resumen'] = articulo.description.text

    # Guarda la URL de la noticia en el diccionario
    noticia_articulo['URL'] = articulo.link.text

    # Guarda la sección de la noticia en el diccionario
    noticia_articulo['Seccion'] = articulo.category.text

    # Guarda el nombre del sitio de publicación en el diccionario
    noticia_articulo['Sitio de publicacion'] = 'Razón'

    # Guarda la fecha de publicación de la noticia en el diccionario
    noticia_articulo['Fecha de publicacion'] = articulo.pubDate.text

    # Guarda el autor de la noticia en el diccionario
    noticia_articulo['Autor'] = articulo.find('dc:creator')

    contenido = articulo.find('content:encoded')

    if contenido is not None:
        # Si se encontró contenido, guarda el texto en el diccionario
        noticia_articulo['Contenido'] = contenido.text
    else:
        # Si no se encontró contenido, guarda una cadena vacía en el diccionario
        noticia_articulo['Contenido'] = ""

    # Guarda la URL de la imagen de la noticia en el diccionario
    noticia_articulo['Imagen'] = articulo.find('media:content')['url']

    noticias_articulos.append(noticia_articulo)  # Agrega el diccionario a la lista de noticias

df = pd.DataFrame(noticias_articulos,
                  columns=['Titulo', 'Resumen', 'Contenido', 'Seccion', 'Sitio de publicacion', 'URL',
                           'Fecha de publicacion', 'Autor', 'Imagen'])  # Crea un DataFrame con los datos

df.head()  # Muestra las primeras filas del DataFrame

df.to_csv('noticiaslarazon.csv', index=False)  # Guarda el DataFrame en un archivo CSV sin incluir los índices

print('Se han guardado las noticias')  # Imprime un mensaje indicando que las noticias se han guardado
