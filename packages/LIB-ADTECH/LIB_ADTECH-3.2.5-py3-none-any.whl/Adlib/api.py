import requests
from enum import Enum


class EnumStatus(Enum):
    VAZIO = 0
    ERRO = 1
    LIGADO = 2
    DESLIGADO = 3
    IMPORTANDO = 4
    APROVADO = 5
    CANCELADA = 6
    SEM_ARQUIVOS = 8

class ImportacaoStatus(Enum):
    VAZIO = 0
    ERRO = 1
    LIGADO = 2
    DESLIGADO = 3
    IMPORTANDO = 4
    APROVADO = 5
    CANCELADA = 6

class EnumProcesso(Enum):
    INTEGRACAO = 0
    IMPORTACAO = 1
    APROVADORES = 2
    BLIP_CONSULTA = 3
    BLIP_LINK = 4
    PAG_DEV = 5
    JURIDICO = 6
    RESET = 7
    COLETAR_DOCUMENTO = 8
    CRIACAO = 9
    NOVA_SENHA = 10

class EnumBanco(Enum):
    VAZIO = 0
    PAN = 1
    OLE = 2
    MEU_CASH_CARD = 3
    BMG = 4
    BRADESCO = 5
    DIGIO = 5
    BANRISUL = 6
    BANCO_DO_BRASIL = 7
    C6 = 8
    ITAU = 9
    MASTER = 10
    PAULISTA = 11
    CREFAZ = 12
    CCB = 13
    DAYCOVAL = 14
    ICRED = 15
    HAPPY_AMIGOZ = 16
    SAFRA = 17
    SANTANDER = 18
    SABEMI = 19
    CREFISA = 20
    FACTA = 21
    JBCRED = 22
    FUTURO_PREVIDENCIA = 23
    CREFISA_CP = 24
    PAN_CARTAO = 25
    PAN_PORT = 26
    HAPPY_PORT = 27
    NUVIDEO = 28
    PROMOBANK = 29
    BLIP = 30
    GETDOC = 31


def putRequestFunction(status: EnumStatus, enumProcesso: EnumProcesso, enumBanco: EnumBanco):
    """
    Envia duas requisições HTTP PUT para atualizar o status de um processo e registrar o horário da atualização.

    Parâmetros:
    ----------
    status : IntegracaoStatus
        Um valor da enumeração `IntegracaoStatus` que representa o status do processo a ser atualizado.
    enumProcesso : int
        Um número inteiro que representa o ID do processo a ser atualizado.
    enumBanco : int
        Um número inteiro que representa o ID do banco a ser atualizado.
    """
    horaFeita = f'http://172.16.10.6:8443/acompanhamentoTotal/horaFeita/{enumProcesso.value}/{enumBanco.value}'
    URLnovaApi = f'http://172.16.10.6:8443/acompanhamentoTotal/processoAndBancoStatus/{enumProcesso.value}/{enumBanco.value}'

    data = { "status": status.value }
    headers = { "Content-Type": "application/json" }
    try:
        response = requests.put(URLnovaApi, headers=headers, json=data)

    except requests.Timeout:
        print("A requisição expirou. Verifique sua conexão ou o servidor.")
    except ConnectionError:
        print("Erro de conexão. Verifique sua rede ou o servidor.")
    except requests.RequestException as e:
        print(f"Ocorreu um erro ao realizar a requisição: {e}")

    if status != EnumStatus.DESLIGADO:
        requests.put(horaFeita)

    if response.status_code == 200: 
        print("Requisição PUT bem-sucedida!")
        print("Resposta:", response.json())
    else:
        print(f"Falha na requisição PUT. Código de status: {response.status_code}")
        print("Resposta:", response.text)


if __name__=="__main__":
    putRequestFunction(EnumStatus.LIGADO, EnumProcesso.CRIACAO, EnumBanco.BMG)
    pass