from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import os.path
import time
from Adlib.funcoes import *
from Adlib.api import EnumBanco, EnumProcesso, putRequestFunction, IntegracaoStatus
from time import sleep

global NUM_TABS

ENUM_PROCESSO = 0


def loginVirtaus(virtaus, usuario: str, senha: str):
    """
        Realiza o login automático no portal Virtaus.

        Parâmetros:
        - virtaus: webdriver.Chrome - WebDriver do Selenium.
        - usuario: str - Nome de usuário para o login.
        - senha: str - Senha associada ao usuário.
        
        Fluxo:
        1. Abre uma nova aba no navegador.
        2. Acessa a página de login do portal Virtaus.
        3. Insere as credenciais do usuário e faz o login.
    """
    virtaus.execute_script("window.open('');")
    NUM_TABS = len(virtaus.window_handles) - 1
    virtaus.switch_to.window(virtaus.window_handles[NUM_TABS])
    virtaus.maximize_window()

    virtaus.get('https://app.fluigidentity.com/ui/login')

    esperarElemento(virtaus, '//*[@id="username"]').send_keys(usuario)
    esperarElemento(virtaus, '//*[@id="password"]').send_keys(senha + Keys.ENTER)

    sleep(5)


def importarArquivos(virtaus, enumBanco: EnumBanco, codigoBanco: int, nomeBanco: str, substring: str, formatoArquivo: str, usuarioWindows: str):
    """
        Filtra arquivos na pasta de downloads do usuário e os envia para o sistema Virtaus.

        Parâmetros:
        - virtaus: webdriver.Chrome - WebDriver do Selenium.
        - enumBanco: EnumBanco
        - codigoBanco: int - Código do banco no Virtaus (disponível na URL de integração do banco)
        - nomeBanco: str - Nome descritivo do banco (usado para gerar mensagens de feedback).
        - substring: str - Substring para filtrar os arquivos na pasta de downloads.
        - formatoArquivo: str - Extensão dos arquivos a serem filtrados (por exemplo, 'pdf').
        - usuarioWindows: str - Nome de usuário do sistema Windows (usado para localizar a pasta de downloads).

        Fluxo:
        1. Acessa a URL específica do banco no sistema Virtaus.
        2. Filtra os arquivos na pasta de downloads com base na substring e na extensão fornecida.
        3. Faz o upload de cada arquivo filtrado para o sistema Virtaus.
        4. Remove o arquivo da pasta de downloads após o upload bem-sucedido.
        5. Exibe uma mensagem de sucesso ou erro no console.
    """
    token = '7506259919:AAEpbbkg5Xu7YXK0T8IVM76LM23pzIvt6wY'
    chatId = '-4579971115'

    virtaus.get('https://adpromotora.virtaus.com.br/portal/p/ad/ecmnavigation')
    time.sleep(5)

    try:
        putRequestFunction(IntegracaoStatus.IMPORTANDO, EnumProcesso(ENUM_PROCESSO), enumBanco)

        virtaus.get(f'https://adpromotora.virtaus.com.br/portal/p/ad/ecmnavigation?app_ecm_navigation_doc={codigoBanco}')
        time.sleep(5)
        downloadsDirectory = os.path.join(r"C:\Users", usuarioWindows, "Downloads")
        
        arquivos = os.listdir(downloadsDirectory)
        print(arquivos)

        arquivosFiltrados = [arquivo for arquivo in arquivos if (substring in arquivo) and arquivo.endswith('.' + formatoArquivo)]
        
        qntArquivos = len(arquivosFiltrados)

        if qntArquivos == 0:
            putRequestFunction(IntegracaoStatus.SEM_ARQUIVOS, EnumProcesso(ENUM_PROCESSO), enumBanco)

        for i, arquivo in enumerate(arquivosFiltrados, start=1):
            caminho = os.path.join(downloadsDirectory, arquivo)
            print(f'Arquivo encontrado: {caminho}')
            
            # Envia o arquivo usando o elemento XPath
            try:
                # Simula o envio do arquivo
                try:
                    importarArquivo = virtaus.find_element('xpath', '//*[@id="ecm-navigation-inputFile-clone"]')
                    importarArquivo.send_keys(caminho)

                    print(f'Arquivo {caminho} enviado com sucesso')
                
                except Exception as e:
                    print(e)

                # Aguarda o upload finalizar
                sleep(10)

                # Remove o arquivo da pasta de downloads
                os.remove(caminho)
                print(f'Arquivo {caminho} removido da pasta de downloads')

                # Mensagem de sucesso
                mensagem = f"Documento integrado!  <b>{nomeBanco}</b> \nDocumentos importados: {i}/{qntArquivos}"
                print(mensagem)
                mensagemTelegam(token, chatId, mensagem)
                putRequestFunction(IntegracaoStatus.LIGADO, EnumProcesso(ENUM_PROCESSO), enumBanco)

            except Exception as e:
                print(e)
                print(f"Erro ao processar o arquivo {caminho}: {e}")
                mensagem = f"""Não haviam documentos para integrar! ⚠️ <b>{nomeBanco}</b>"""
                
        else:
            mensagem = f"Todos os documentos foram integrados com sucesso!\n<b>{nomeBanco}</b> ✅"
            print(mensagem)
            mensagemTelegam(token, chatId, mensagem)
            print("Todos os arquivos foram processados.")
            
    
    except Exception as erro:
        print(erro)
        print('Não deu certo')
        putRequestFunction(IntegracaoStatus.ERRO, EnumProcesso(ENUM_PROCESSO), enumBanco)


def integracaoVirtaus(driver, usuario: str, senha: str, enumBanco: EnumBanco, codigoBanco: int, nomeBanco: str,
                      substring: str, formatoArquivo:str, usuarioWindows:str):
    """
        Função principal que coordena a automação de login e importação de arquivos para o Virtaus.

        Parâmetros:
        - driver: webdriver.Chrome - WebDriver do Selenium
        - usuario: str - Nome de usuário para o login no Virtaus.
        - senha: str - Senha para o login no Virtaus.
        - codigoBanco: int - Código do banco no Virtaus (disponível na URL de integração do banco)
        - nomeBanco: str - Nome do banco para gerar mensagens de log e feedback.
        - substring: str - Substring usada para filtrar os arquivos na pasta de downloads.
        - formatoArquivo: str - Extensão dos arquivos a serem filtrados (por exemplo, 'xlsx', 'csv').
        - usuarioWindows: str - Nome de usuário no Windows para acessar a pasta de downloads (por exemplo, 'yan.fontes').

        Fluxo:
        1. Realiza o login no sistema Virtaus usando a função loginVirtaus.
        2. Filtra e envia arquivos da pasta de downloads para o sistema Virtaus utilizando a função importarArquivos.
    """
    loginVirtaus(driver, usuario, senha)
    importarArquivos(driver, enumBanco, codigoBanco, nomeBanco, substring, formatoArquivo, usuarioWindows)


if __name__=="__main__":

    driver = setupDriver()

    nomeBanco = "Paulista"
    codigoBanco = 2865957
    userVirtaus = "dannilo.costa@adpromotora.com.br"
    senhaVirtaus = "Costa@36"
    substringNomeArquivo = "FE361338-299B-429B-8F57-79B0AA2D872A"
    formatoArquivo = "xlsx"
    usuarioWindows = "dannilo.costa"

    integracaoVirtaus(driver, userVirtaus, senhaVirtaus, EnumBanco.PAULISTA, codigoBanco, nomeBanco,
                      substringNomeArquivo, formatoArquivo, usuarioWindows)