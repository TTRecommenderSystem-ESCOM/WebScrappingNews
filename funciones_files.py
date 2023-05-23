import pandas as pd
import numpy as np

def unir(file1, file2, file3, file4):
    # Leer los cuatro archivos CSV
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    df3 = pd.read_csv(file3)
    df4 = pd.read_csv(file4)

    # Unir los DataFrames verticalmente
    df = pd.concat([df1, df2, df3, df4])

    # Guardar el DataFrame unido en un archivo CSV
    df.to_csv('noticias.csv', index=False)



def clase(noticia):
    df = pd.read_csv(noticia)
    # Elimina columnas que no son necesarias para el modelado


    agrupado = df.groupby('Seccion')

    #Calcular el conteo de los valores duplicados y guardar el resultado en una nueva columna
    df['conteo'] = agrupado['Seccion'].transform('count')

    # Identificar los datos duplicados
    duplicados = df.duplicated(subset='Seccion', keep=False)

    # Crear una lista con los valores duplicados y su suma correspondiente
    lista_duplicados = []
    for index, fila in df[duplicados].iterrows():
        lista_duplicados.append((fila['Seccion'], fila['conteo']))

    # Obtener los valores duplicados únicos
    lista_duplicados = list(set(lista_duplicados))

    print(lista_duplicados)
    # Convertir la lista en una tabla
    tabla_duplicados = pd.DataFrame(lista_duplicados, columns=['Seccion', 'conteo'])

    # Imprimir la tabla de duplicados
    print(tabla_duplicados)

#clase('noticias_jornada.csv')


def unificar_clases(noticia):
    df = pd.read_csv(noticia)
    # Elimina columnas que no son necesarias para el modelado

    df['Seccion'] = df['Seccion'].replace('[\[\]]', '', regex=True).replace('', np.nan)
    df = df.dropna(subset=['Seccion'], how='any')
    # Elimanos clases que no contienen información en contenido
    # df = df[~df['Categoria'].isin(['galeria_imagenes', 'cartones','autos','reportaje','opinion','economia','chomsky','sociedad','ciencia-y-tecnologia','cultura','espectaculos'])]

    # Elimina columnas que no son necesarias para el modelado
    # df.drop(['Sitio de publicacion','link', 'Fecha'],axis=1, inplace=True)

    # Elimanos clases que no contienen información en contenido
    df = df[~df['Seccion'].isin(['food-and-drink','colaborador-invitado','DxT'])]
    # Eliminamos valores que estan vacios en la columna contenido

    df['Seccion'] = df['Seccion'].replace('[\[\]]', '', regex=True).replace('', np.nan)
    df = df.dropna(subset=['Seccion'], how='any')

    # df.to_csv('new_check.csv', index=False , encoding="utf-8")
    df['Seccion'] = df['Seccion'].map(lambda x: 'deportes' if x in ['Deportes']

                                                    # else 'entretenimiento' if x == 'Entretenimiento'
                                                    # else 'capital' if x == 'Ciudad'
                                                     else 'mundo' if x== 'Mundo'
                                                     else 'mundo'  if x== 'internacional'
                                                     else 'estados' if x== 'Estados'
                                                     else 'estados' if x== 'México'
                                                     else 'capital' if x== 'CDMX'
                                                     else 'politica' if x== 'Política'
                                                     else  'entretenimiento'if x=='sociedad'
                                                     else 'capital' if x== 'cdmx'
                                                     else 'capital' if x=='mexico'
                                                     else 'nacional' if x== 'estados'
                                                     else 'nacional' if x== 'edomex'
                                                     else 'nacional' if x== 'México'
                                                     else 'nacional' if x== 'monterrey'
                                                     else 'entretenimiento' if x== 'espectaculos'
                                                     else 'empresas' if x== 'Negocios'
                                                     else 'mercados' if x=='empresas'
                                                     else x)


    #df.to_csv('nticiass.csv',index=False)

    return df

#df= pd.read_csv('noticiss.csv')

#df.iloc[:, 2:]
#df = df.drop(df.columns[[0,1,11]], axis=1)
#df.to_csv('noticiasverificar.csv',index=False)


clase('noticias_csv/sdp_news.csv')
clase('noticias_csv/noticias_el_financiero.csv')
clase('noticias_csv/noticiaslarazon.csv')
clase('noticias_csv/25horas.csv')
clase('noticias_csv/noticias_jornada.csv')