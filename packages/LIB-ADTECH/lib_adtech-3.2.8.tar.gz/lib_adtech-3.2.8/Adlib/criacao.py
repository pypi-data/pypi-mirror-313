from selenium import webdriver
from Adlib.funcoes import *
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from urllib.parse import parse_qs, urlparse
from pprint import pprint
from typing import Callable
from selenium.webdriver import ChromeOptions
from dataclasses import dataclass

@dataclass
class CriacaoUsuarioOptions:
    email: bool = False
    customPassword: bool = False
    autoRefreshPage: bool = True
    loginBankPage: bool = False


# Telegram
token = '5929694836:AAGNuG2-f8kJQMIJuVO_GkIeD8g-8Q3MZUo'
chat_id = '-1001716522279'

mapping = {
    "nome": '//*[@id="contaPessoaNome"]',
    "email": '//*[@id="contaEmail"]',
    "telefone": '//*[@id="contaTelefone"]',
    "rg": '//*[@id="contaRg"]',
    "cpf": '//*[@id="contaCpf"]',
    "uf": '//*[@id="contaUF"]',
    "nomeMae": '//*[@id="contaNomeMae"]'
}

dados = None
 
HORA_FINALIZACAO = "18:00"


def criacaoUsuario(nomeFerramenta: str, codigoLoja: str, userBanco: str, senhaBanco: str, loginBanco: Callable[[ChromeOptions, str, str], None],
criarUsuario: Callable[[ChromeOptions,str,str], None], userVirtaus: str, senhaVirtaus: str, options: CriacaoUsuarioOptions = None):
    
    """
    Executa rotina de criação de usuário para banco específico.
    Acessa o Virtaus, buscando por solicitações de criação de usuário do banco especificado
    e executa o fluxo de cadastro de usuário no banco a partir da função criarUsuario()

    Arguments:
        nomeFerramenta: nome da ferramenta do banco (case sensitive)
        userBanco: nome de usuário do banco
        senhaBanco: senha de usuário do banco
        loginBanco: função da rotina de login no banco.
        criarUsuario: função da rotina de cadastro de usuário no banco
        userVirtaus: nome de usuário do Virtaus
        senhaVirtaus: senha do Virtaus
    """
    VALOR_FILTRO_CRIACAO = "938"
    
    driver = setupDriver()

    # Banco
    loginBanco(driver, userBanco, senhaBanco)

    virtaus = driver
    # Cria nova guia para acessar o Virtaus
    virtaus.execute_script("window.open('');")
    virtaus.switch_to.window(virtaus.window_handles[1])
    
    while True:

        # Login Virtaus
        while True:
            try:
                virtaus.get('https://app.fluigidentity.com/ui/login')
                print("Login")
                # Insere credenciais
                esperarElemento(virtaus, '//*[@id="username"]').send_keys(userVirtaus)
                esperarElemento(virtaus, '//*[@id="password"]').send_keys(senhaVirtaus + Keys.ENTER + Keys.ENTER)

                # Busca por span de 'Erro de Login'
                esperarElemento(virtaus, '//*[@id="login_form"]/app-error/table/td[2]')
                sleep(30)
            except:
                break
        
        virtaus.switch_to.window(driver.window_handles[1])
        virtaus.get('https://adpromotora.virtaus.com.br/portal/p/ad/pagecentraltask')

        while True:
            try:
                while True:
                    try:
                        driver.switch_to.window(driver.window_handles[0])
                        driver.refresh()

                        driver.switch_to.window(driver.window_handles[1])
                        driver.refresh()

                        qntBotoes = len(esperarElementos(virtaus, '//*[@id="centralTaskMenu"]/li'))
                        idxBtn = qntBotoes - 1
                        try:
                            # Clica em "Tarefas em Pool: Grupo"
                            clickarElemento(virtaus, f'//*[@id="centralTaskMenu"]/li[{idxBtn}]/a').click()
                        except Exception as e:
                            print(e)

                        # Seleciona o filtro de "Criação de Login Externo"
                        tipoFiltro = "Atendimento | CriacaoDeLoginExternoParaParceiro"
                        clickarElemento(virtaus, f'//*[@id="centralTaskMenu"]/li[{idxBtn}]/ul//a[contains(text(), "{tipoFiltro}")]').click()

                        # Seleciona filtro de criação
                        filtro = Select(esperarElemento(virtaus, '//*[@id="ecm-centralTask-filters"]/select'))
                        filtro.select_by_value(VALOR_FILTRO_CRIACAO)
                        sleep(2)

                        # Busca pelo nome da ferramenta
                        esperarElemento(virtaus, '//*[@id="inputSearchFilter"]').send_keys(nomeFerramenta)#.send_keys("3495956")
                        sleep(2)

                        # Clica no primeira item da lista de solicitações
                        clickarElemento(virtaus, f"//td[contains(@title, '{nomeFerramenta}')]").click()
                        break

                    except Exception as e:
                        agora = datetime.datetime.now()
                        # hora = "0" + str(agora.hour) if agora.hour < 10 else str(agora.hour)
                        # minutos = "0" + str(agora.minute) if agora.minute < 10 else str(agora.minute)
                        hora = agora.strftime("%H:%M")
                        print(f"Não há solicitações do banco {nomeFerramenta} no momento {hora}")
                        if HORA_FINALIZACAO == f"{hora}":
                            sys.exit()
                        sleep(30)
                        #virtaus.refresh()

                try:
                    print("Assumindo Tarefa")
                    # Clica em Assumir Tarefa e vai para o menu de Cadastro de usuário
                    clickarElemento(virtaus, '//*[@id="workflowActions"]/button[1]').click()

                    # Troca de Frame e clica em Dados Adicionais
                    menuFrame = esperarElemento(virtaus, '//*[@id="workflowView-cardViewer"]')
                    virtaus.switch_to.frame(menuFrame)
                    clickarElemento(virtaus, '//*[@id="ui-id-3"]').click()

                    try:
                        print("Obtendo dados")
                        dados = { k : esperarElemento(virtaus, xpath).get_attribute('value') for k, xpath in mapping.items() }
                    except Exception as e:
                        print(e)
                        print("Erro ao obter dados do Virtaus")

                    # Volta para o menu de Cadastro de Usuário
                    clickarElemento(virtaus, '//*[@id="ui-id-2"]').click()

                except Exception as e:
                    print("Erro ao assumir tarefa")
                    msg = f"""Erro na criação usuário \n Usuário: {usuario} \n Solicitação {solicitacaoVirtaus} {nomeFerramenta} ❌"""
                    mensagemTelegam(token, chat_id, msg)
                    break

                try:
                    urlAtual = virtaus.current_url

                    parsed_url = urlparse(urlAtual)
                    query_params = parse_qs(parsed_url.query)

                    if 'app_ecm_workflowview_processInstanceId' in query_params:
                        solicitacaoVirtaus = query_params['app_ecm_workflowview_processInstanceId'][0]

                        print(solicitacaoVirtaus)
                    else:
                        print('O parâmetro "app_ecm_workflowview_processInstanceId" não foi encontrado na URL atual.')
                except:
                    pass

                cpf = dados["cpf"]
                usuario = dados["uf"] + '.' + cpf

                pprint(dados)
                # Chamar função para criação de usuário no banco
                try:
                    driver.switch_to.window(driver.window_handles[0])

                    loginBanco(driver, userBanco, senhaBanco)

                    sleep(10)

                    print("Criando Usuario")
                    usuario, senha = criarUsuario(driver, cpf, usuario)

                    print(usuario, senha)
                except Exception as e: 
                    print(e)
                    print("Erro na criação de usuário no Banco")
                    msg = f"""Erro na criação usuário \nUsuário: {usuario} \nSolicitação {solicitacaoVirtaus} {nomeFerramenta}  ❌"""
                    mensagemTelegam(token, chat_id, msg)
                    break

                try:
                    driver.switch_to.window(driver.window_handles[1])
                    
                    menuFrame = esperarElemento(virtaus, '//*[@id="workflowView-cardViewer"]')
                    virtaus.switch_to.frame(menuFrame)

                    esperarElemento(virtaus, '//*[@id="nomeLogin"]').send_keys(usuario)
                    esperarElemento(virtaus, '//*[@id="senhaLogin"]').send_keys(senha)
                    esperarElemento(virtaus, '//*[@id="groupCodigoDeLoja"]/span/span[1]/span/ul/li/input').send_keys(codigoLoja)
                    esperarElemento(virtaus, '//*[@id="select2-codigoDeLojaId-results"]/li[2]').click()
                    sleep(5)

                    virtaus.switch_to.default_content()
                    esperarElemento(virtaus, '//*[@id="send-process-button"]').click()

                    proximaAtividade = Select(esperarElemento(virtaus, '//*[@id="nextActivity"]'))
                    proximaAtividade.select_by_value("7")
                    sleep(1)
                    esperarElemento(virtaus, '//*[@id="moviment-button"]').click()
                    sleep(5)
                    msg = f"Criação de usuário efetuada com sucesso!\nUsuário: {usuario}\nSolicitação {solicitacaoVirtaus} {nomeFerramenta.title()}  ✅"

                    mensagemTelegam(token, chat_id, msg)
                    virtaus.get('https://adpromotora.virtaus.com.br/portal/p/ad/pagecentraltask')

                except Exception as e:
                    print(e)
                    print("Erro ao enviar solicitação")

                    msg = f"""Erro na criação usuário \nUsuário: {usuario} \nSolicitação {solicitacaoVirtaus} {nomeFerramenta}  ❌"""
                    mensagemTelegam(token, chat_id, msg)
                
            except Exception as e:
                print(e)
                break


if __name__=="__main__":

    # Credenciais Virtaus
    userVirtaus = 'dannilo.costa@adpromotora.com.br'
    senhaVirtaus = 'Costa@36'

    # Credenciais Banco
    userDigio = "03478690501_204258"
    senhaDigio = "Adpromo10*"

    def loginDigio():
        pass

    def criarUsuario():
        pass

    criacaoUsuario("DIGIO", "4258", userDigio, senhaDigio, loginDigio, criarUsuario, userVirtaus, senhaVirtaus)