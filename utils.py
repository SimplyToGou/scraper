import json
import pprint
import requests


def obtener_id(lista_entradas):
    for entry in lista_entradas:
        try:
            obj_serialized: str = entry.get("message")
            obj = json.loads(obj_serialized)
            if 'request' in obj['message']['params'].keys():
                if 'api.observatorio.sernac.cl' in obj['message']['params']['request']['url']:
                    print(obj['message']['params']['request'])
        except Exception as e:
            raise e from None


def obtener_geografia():
    URL_GEOGRAFIA = "https://api.observatorio.sernac.cl/api/v1/geografia"
    return json.loads(requests.get(URL_GEOGRAFIA).content)


def tamanio_por_producto():
    resultado = []
    with open("productos.json", "r") as archivo:
        productos = json.load(archivo)
    lista_ids = [x["id"] for x in productos["subcategorias"]]

    for pid in lista_ids:
        url = f"https://api.observatorio.sernac.cl/api/v1/subcategorias/{pid}/rangos"
        resultado.append({str(pid): json.loads(requests.get(url).content)['rangos']})

    with open("productos_sizes.json", "w+") as yeison:
        json.dump(resultado, yeison, indent=4)




if __name__ == "__main__":
    tamanio_por_producto()

    """
    nfo = obtener_geografia()
    with open("idcomunas.json", 'w+') as yeison:
        json.dump(nfo, yeison, indent=4)
    
    """
