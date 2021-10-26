from imgurpython import ImgurClient
import urllib.request
import time
import concurrent.futures

secreto_cliente = "5f8c3cce299db5e26a2eb96b0b7809a82805c9ad"
id_cliente = "bfa0e227a1c5643"
cliente = ImgurClient(id_cliente, secreto_cliente)

def descarga_url_img(link):
   linkContenido = link.link
   print(linkContenido)
   # Con esto ya podemos obtener el corte de la url imagen
   nombre_img = linkContenido.split("/")[3]
   formato_img = nombre_img.split(".")[1]
   nombre_img = nombre_img.split(".")[0]
   print(nombre_img, formato_img)
   url_local = "/Users/Usuario/Documents/Practicas de Concurrencia con Python 3.9/Actividad_Imagenes/{}.{}"
   #Guardar nne local las imagenes
   urllib.request.urlretrieve(linkContenido, url_local.format(nombre_img, formato_img))

def main():
    t1 = time.perf_counter() #Contador inicial
    id_album = "bUaCfoz"
    imagenes = cliente.get_album_images(id_album)
    with concurrent.futures.ThreadPoolExecutor(10) as executor: #Diez hilos en una sola iteracion
        executor.map(descarga_url_img, imagenes)
    t2 = time.perf_counter() #Contador final
    print(f'El codigo en base a subprocesos multiples le tomo: {t2 - t1} segundos.')


if __name__ == "__main__":
    main()