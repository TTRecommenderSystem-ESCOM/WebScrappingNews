import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.jornada.com.mx/feeds/rss'

resp = requests.get(url)  # Realiza una solicitud GET al URL especificado
soup = BeautifulSoup(resp.content, features='xml')  # Parsea el contenido de la respuesta como XML
print(soup.prettify())  # Imprime el contenido HTML/XML formateado

itemss = soup.findAll('item')  # Encuentra todos los elementos 'item' en el XML
len(itemss)  # Imprime la cantidad de elementos 'item' encontrados

item = itemss[0]  # Obtiene el primer elemento 'item'
item

item.link.text  # Imprime el texto dentro de la etiqueta 'link' del primer elemento 'item'

news_items = []  # Lista para almacenar los diccionarios de noticias

# Itera sobre cada elemento 'item' en itemss
for item in itemss:
    noticia_articulo = {}  # Crea un diccionario para almacenar los datos de la noticia

    # Guarda el título de la noticia en el diccionario
    noticia_articulo['Titulo'] = item.title.text

    # Guarda el resumen de la noticia en el diccionario
    noticia_articulo['Resumen'] = item.description.text

    # Guarda la URL de la noticia en el diccionario
    noticia_articulo['URL'] = item.link.text

    # Guarda la sección de la noticia en el diccionario
    noticia_articulo['Seccion'] = item.category.text

    # Guarda el nombre del sitio de publicación en el diccionario
    noticia_articulo['Sitio de publicacion'] = 'La Jornada'

    # Guarda la fecha de publicación de la noticia en el diccionario
    noticia_articulo['Fecha de publicacion'] = item.pubDate.text

    # Guarda el autor de la noticia en el diccionario
    noticia_articulo['Autor'] = item.find('dc:creator')

    news_items.append(noticia_articulo)  # Agrega el diccionario a la lista de noticias

df = pd.DataFrame(news_items,
                  columns=['Titulo', 'Resumen', 'Contenido', 'Seccion', 'Sitio de publicacion', 'URL',
                           'Fecha de publicacion', 'Autor', 'Imagen'])  # Crea un DataFrame con los datos

print(news_items)  # Imprime la lista de diccionarios de noticias

df = pd.DataFrame(news_items)  # Crea un DataFrame con los datos de las noticias

print(df)  # Imprime el DataFrame

Titulos_noticias = []  # Lista para almacenar los títulos de las noticias
Contenido = []  # Lista para almacenar el contenido de las noticias

# Itera sobre cada enlace de noticia en la lista de noticias
for noticia_link in news_items:
    url_news = noticia_link.get('URL')  # Obtiene la URL de la noticia

    # Realiza una solicitud GET a la URL de la noticia
    page_noticia = requests.get(url_news, headers={'User-Agent': 'Mozilla/5.0'})
    soup_noticia = BeautifulSoup(page_noticia.content, "html.parser")  # Parsea el contenido de la página de la noticia

    # Encuentra el título de la noticia
    for i in soup_noticia.find('h2', attrs={'id': 'article-title-tts'}):
        try:
            titulo = i
        except:
            titulo = 'none'
        Titulos_noticias.append(str(titulo))

    # Encuentra el contenido de la noticia
    for i in soup_noticia.findAll("div", class_="article-content ljn-nota-contenido"):
        try:
            content = i.find_all('p')
        except:
            content = 'none'
        Contenido.append(str(content))

# Inserta la columna 'Contenido' en el DataFrame 'df'
df.insert(7, 'Contenido', Contenido, allow_duplicates=False)

df.to_csv('noticias_jornada.csv', index=False)  # Guarda el DataFrame en un archivo CSV sin incluir los índices

