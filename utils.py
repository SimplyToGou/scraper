import json
import pprint


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

