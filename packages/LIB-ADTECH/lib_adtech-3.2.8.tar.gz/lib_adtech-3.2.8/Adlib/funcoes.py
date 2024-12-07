import requests
import datetime
import subprocess
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

def setupDriver(
    webdrivePath: str = r"C:\Users\yan.fontes\Documents\webdriver\chromedriver-win32\chromedriver.exe", 
    numTabs: int = 1, 
    options: list[str] = []
) -> webdriver.Chrome:
    """
    Configura e inicializa uma instância do navegador Google Chrome utilizando o Selenium WebDriver.

    Args:
        webdrivePath (str): Caminho para o executável do ChromeDriver.
        numTabs (int): Número de guias a serem abertas no navegador.
        options (list[str]): Lista de argumentos adicionais para o ChromeOptions.

    Returns:
        webdriver.Chrome: Uma instância configurada do WebDriver do Chrome pronta para ser usada em automações de teste ou navegação.
    """
    chrome_service = ChromeService(executable_path=webdrivePath)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("log-level=3")

    for option in options:
        chrome_options.add_argument(option)

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.maximize_window()

    for _ in range(numTabs - 1):
        driver.execute_script("window.open('');")

    driver.switch_to.window(driver.window_handles[0])

    return driver



def getCredenciais(id: int) -> tuple[str, str] | tuple[None, None]:
    """
    Recupera as credenciais (login e senha) de uma API com base no ID fornecido.

    Esta função faz uma requisição `GET` para uma API REST usando o ID fornecido e tenta recuperar as credenciais de login e senha. Se a requisição for bem-sucedida (status code 200) e os dados estiverem presentes, ela retorna uma tupla contendo o login e a senha. Caso contrário, retorna uma tupla com `None` nos dois valores.

    Args:
        id (int): O ID utilizado para buscar as credenciais na API.

    Returns:
        tuple[str, str] | tuple[None, None]: 
            - Uma tupla contendo `login` e `senha` se a requisição for bem-sucedida e os dados estiverem presentes.
            - Uma tupla `(None, None)` se a requisição falhar ou os dados não estiverem disponíveis.
    """
    url = f"http://172.16.10.6:8080/credenciais/{id}"
    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados = resposta.json()
            login = dados.get('login')
            senha = dados.get('senha')
            return login, senha
        return None, None
    except Exception as e:
        print(e)
        print("Não foi possível acessar a API")


def instalarPacote(pacote: str):
    """
    Instala uma biblioteca do python
    Arguments:
        pacote: nome do pacote disponível no PyPI
    """
    subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])
 
 
def importarLibs():
    """Importa e instala, caso necessário, os pacotes e bibliotecas necessárias"""
    import time
    try:
        import pandas as pd
    except ImportError:
        instalarPacote("pandas")
        import pandas as pd
 
    try:
        from typing import Text
    except ImportError:
        instalarPacote("typing-extensions")
        from typing import Text
 
    try:
        from bs4 import element, BeautifulSoup, BeautifulStoneSoup
        from bs4.element import ProcessingInstruction
 
    except ImportError:
        instalarPacote("beautifulsoup4")
        from bs4 import element, BeautifulSoup, BeautifulStoneSoup
        from bs4.element import ProcessingInstruction
 
    try:
        from numpy import SHIFT_DIVIDEBYZERO, False_, exp
    except ImportError:
        instalarPacote("numpy")
        from numpy import SHIFT_DIVIDEBYZERO, False_, exp
 
    try:
        from pandas.io import html
    except ImportError:
        instalarPacote("pandas")
        from pandas.io import html
 
    try:
        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.chrome.options import Options
        
        
    except ImportError:
        instalarPacote("selenium")
        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.chrome.options import Options
        
        
 
    try:
        from openpyxl import Workbook, load_workbook
    except ImportError:
        instalarPacote("openpyxl")
        from openpyxl import Workbook, load_workbook
 
    try:
        import os
    except ImportError:
        instalarPacote("os")
        import os
 
    try:
        import tkinter as tk
        from tkinter import messagebox
    except ImportError:
        instalarPacote("tk")
        import tkinter as tk
        from tkinter import messagebox
 
    try:
        from discord_webhook import DiscordWebhook, DiscordEmbed
    except ImportError:
        instalarPacote("discord-webhook")
        from discord_webhook import DiscordWebhook, DiscordEmbed
 
    try:
        from datetime import datetime
    except ImportError:
        instalarPacote("datetime")
        from datetime import datetime
 
    bibliotecas = {
        'os.path': os.path,
        'pd': pd,
        'Text': Text,
        'element': element,
        'ProcessingInstruction': ProcessingInstruction,
        'SHIFT_DIVIDEBYZERO': SHIFT_DIVIDEBYZERO,
        'False_': False_,
        'exp': exp,
        'html': html,
        'webdriver': webdriver,
        'Keys': Keys,
        'ActionChains': ActionChains,
        'time': time,
        'DataFrame': pd.DataFrame,
        'read_csv': pd.read_csv,
        'Options': Options,
        'BeautifulSoup': BeautifulSoup,
        'BeautifulStoneSoup': BeautifulStoneSoup,
        'Workbook': Workbook,
        'load_workbook': load_workbook,
        'datetime': datetime,
        'tk': tk,
        'messagebox': messagebox,
        'DiscordWebhook': DiscordWebhook,
        'DiscordEmbed': DiscordEmbed,
        'WebDriverWait': WebDriverWait,
    }
 
    return bibliotecas


def esperarElemento(driver: webdriver.Chrome, xpath: str, tempo_espera=10):
    """
    Aguarda o elemento ser renderizado
    Arguments:
        driver: driver do site
        xpath: XPath do elemento
        tempo_espera: Tempo máximo de espera, em segundos
    Returns:
        Elemento
    """
    
    
 
    return WebDriverWait(driver, tempo_espera).until(EC.visibility_of_element_located(('xpath', xpath)))
 
 
def esperarElementos(driver: webdriver.Chrome, xpath: str, tempo_espera=10):
    """
    Aguarda todos os elementos serem renderizados.
    Arguments:
        driver: driver do site
        xpath: XPath dos elementos
        tempo_espera: Tempo máximo de espera, em segundos
    Returns:
        Lista de elementos
    """
 
    return WebDriverWait(driver, tempo_espera).until(EC.presence_of_all_elements_located(('xpath', xpath)))
 
 
def clickarElemento(driver: webdriver.Chrome, xpath: str, time_wait=10):
    """
    Retorna o elemento do Xpath de entrada
    Args:
        driver: driver do site
        xpath: XPath do elemento
    Returns:
        Elemento
    """
    
    return WebDriverWait(driver, time_wait).until(EC.element_to_be_clickable(('xpath', xpath)))


def clickElement(driver: webdriver.Chrome, xpath: str, tempoEspera: int = 20):
    """
        Aguarda o elemento entrar em estado clicável e executa um clique
    """
    driver.execute_script("arguments[0].click();", WebDriverWait(driver, tempoEspera).until(EC.element_to_be_clickable((By.XPATH, xpath))))


def mensagemTelegam(token: str, chat_id: int, mensagem: str):
    """
    Envia uma mensagem pela API do Telegram
    Arguments:
        token: token do bot do Telegram
        chat_id: id do chat
        mensagem: mensagem a ser enviada
    Returns:
        JSON com a resposta da requisição
    """
    mensagem_formatada = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=HTML&text={mensagem}'
    resposta = requests.get(mensagem_formatada)
    return resposta.json()
 
 
def importar_bibliotecas():
    import pandas as pd
    from typing import Text
    from bs4 import element
    from bs4.element import ProcessingInstruction
    from numpy import SHIFT_DIVIDEBYZERO, False_, exp
    from pandas.io import html
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
    import time
    import pandas as pd
    from pandas.core.frame import DataFrame
    from pandas.io.parsers import read_csv
    from selenium import webdriver
    from selenium.webdriver.chrome.webdriver import WebDriver
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support import expected_conditions
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.chrome.options import Options
    from bs4 import BeautifulSoup, BeautifulStoneSoup
    from selenium import webdriver
    from openpyxl import Workbook, load_workbook
    import os
    from datetime import datetime
    from selenium.webdriver.chrome.service import Service
    from bs4 import BeautifulSoup, BeautifulStoneSoup
    from selenium import webdriver
    from openpyxl import Workbook, load_workbook
    from datetime import datetime
    import tkinter as tk
    from tkinter import messagebox
    from discord_webhook import DiscordWebhook, DiscordEmbed
    
    
    from selenium.webdriver.common.keys import Keys
 
    bibliotecas = {
        'os.path': os.path,
        'pd': pd,
        'Text': Text,
        'element': element,
        'ProcessingInstruction': ProcessingInstruction,
        'SHIFT_DIVIDEBYZERO': SHIFT_DIVIDEBYZERO,
        'False_': False_,
        'exp': exp,
        'html': html,
        'webdriver': webdriver,
        'Keys': Keys,
        'ActionChains': ActionChains,
        'time': time,
        'DataFrame': DataFrame,
        'read_csv': read_csv,
        'Options': Options,
        'BeautifulSoup': BeautifulSoup,
        'BeautifulStoneSoup': BeautifulStoneSoup,
        'Workbook': Workbook,
        'load_workbook': load_workbook,
        'datetime': datetime,
        'Service': Service,
        'tk': tk,
        'messagebox': messagebox,
        'DiscordWebhook': DiscordWebhook,
        'DiscordEmbed': DiscordEmbed,
        'WebDriverWait': WebDriverWait,
    }
 
    return bibliotecas
 
       
def esperar_elemento(driver: webdriver.Chrome, xpath: str, tempo_espera=10):
    
    
    from selenium.webdriver.common.keys import Keys
    return WebDriverWait(driver, tempo_espera).until(EC.visibility_of_element_located(('xpath', xpath)))


def aguardarDownload(pastaDownloads: str, substringNomeArquivo: str):
    pass


def finalizarPorHora(hora, minutes):
    agora = datetime.datetime.now()
    t = agora.strftime('%H:%M')
    t2 = agora.replace(hour=hora, minute=minutes)
    t_simplificado = t2.strftime('%H:%M')

    return t >= t_simplificado