import requests
from enum import Enum
from requests.exceptions import RequestException, Timeout, ConnectionError

class EnumStatusAcompanhamento(Enum):
    VAZIO = 0
    ERRO = 1
    LIGADO = 2
    DESLIGADO = 3
    IMPORTANDO = 4
    APROVADO = 5
    CANCELADA = 6
    SEM_ARQUIVOS = 8

class EnumStatus(Enum):
    VAZIO = 0
    ERRO = 1
    LIGADO = 2
    DESLIGADO = 3
    IMPORTANDO = 4
    APROVADO = 5
    CANCELADA = 6
    SEM_ARQUIVOS = 8

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

class EnumStatusSolicitacao(Enum):
    EM_ATENDIMENTO = 0
    CONCLUIDO = 1
    ERRO = 2
    TRANSFERIDO = 3

class IdSolicitacaoCriacaoBanco(Enum):
    BMG = 41
    C6 = 42
    DIGIO = 43
    ITAU = 44

    @classmethod
    def getEnum(cls, key):
        try:
            return cls[key].value
        except KeyError:
            raise ValueError(f"Chave {key} não encontrada em {cls.__name__}.")

class IdSolicitacaoResetBanco(Enum):
    BMG = 15
    MASTER = 17
    CREDCESTA = 17
    C6 = 42
    DIGIO = 19
    BANRISUL = 20
    FACTA = 21
    CREFISA = 22
    BRADESCO = 38
    ITAU = 44

    @classmethod
    def getEnum(cls, key):
        try:
            return cls[key].value
        except KeyError:
            raise ValueError(f"Chave {key} não encontrada em {cls.__name__}.")


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
        # print("Resposta:", response.json())
    else:
        print(f"Falha na requisição PUT. Código de status: {response.status_code}")
        # print("Resposta:", response.text)


def putSolicitacao(solicitacao: str, enumProcesso: EnumProcesso, enumBanco: EnumBanco):
    data = {
        "solicitacao": solicitacao
    }
    headers = {
        "Content-Type": "application/json"
    }

    URLChangeStatus = f'http://172.16.10.6:8443/acompanhamentoTotal/processoAndBancoSolicitacao/{enumProcesso.value}/{enumBanco.value}'

    try:
        response = requests.put(URLChangeStatus, headers=headers, json=data)

        if response.status_code == 200:
            print("Requisição PUT bem-sucedida!")
        else:
            print(f"Falha na requisição PUT. Código de status: {response.status_code}")
            print("Resposta:", response.text)
    except Timeout:
        print("A requisição expirou. Verifique sua conexão ou o servidor.")
    except ConnectionError:
        print("Erro de conexão. Verifique sua rede ou o servidor.")
    except RequestException as e:
        print(f"Ocorreu um erro ao realizar a requisição: {e}")


def postSolicitacao(enumStatusSolicitacao: EnumStatusSolicitacao, enumProcesso: EnumProcesso, solicitacao: int, enumBanco: EnumBanco) -> int:
    
    mapping =   {
                    EnumProcesso.CRIACAO : IdSolicitacaoCriacaoBanco,
                    EnumProcesso.RESET: IdSolicitacaoResetBanco
                }
    
    enumBanco = mapping[enumProcesso].getEnum(enumBanco.name)
    
    print(enumBanco)

    data = {
        'enumDetalheSolicitacoesStatus': enumStatusSolicitacao.value,
        'numeroSolicitacao': solicitacao,
        "acompanhamentoDomain": {
            "acompanhamentoId": enumBanco.value
        }
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post('http://172.16.10.6:7118/detalhesSolicitacao/', headers=headers, json=data)

    if response.status_code == 200:
        print("Requisição POST bem-sucedida!")
        print("Resposta:", response.json()) 
    
    else:
        print(f"Falha na requisição POST. Código de status: {response.status_code}")
        print("Resposta:", response.text)

    dataApi = response.json()
    print(dataApi)
    detalhesSolicitacaoId = dataApi['detalhesSolicitacaoId']

    return detalhesSolicitacaoId


if __name__=="__main__":
    putRequestFunction(EnumStatus.LIGADO, EnumProcesso.CRIACAO, EnumBanco.BMG)
    # postSolicitacao(None, EnumProcesso.CRIACAO, 123345, EnumBanco.BANRISUL)
    pass