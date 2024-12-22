import reflex as rx
import os


import os


def get_image_path(image_id, base_path: str = "quinchau.com/webmaster2/weberp/img/p/") -> str:

    image_id_str = str(image_id)
    lista_digitos = list(image_id_str)
    # Unir cada dígito con una barra inclinada
    image_path = base_path + \
        '/'.join(lista_digitos) + "/" + image_id_str + ".jpg"
    return image_path

    # print(image_path)
