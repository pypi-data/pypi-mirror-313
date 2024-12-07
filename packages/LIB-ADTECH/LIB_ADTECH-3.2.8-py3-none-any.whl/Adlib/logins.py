from functools import wraps
from selenium import webdriver
from Adlib.funcoes import esperarElemento, clickarElemento
from selenium.webdriver.common.keys import Keys
from time import sleep


def login_decorator(func):

    @wraps(func)
    def wrapper(driver: webdriver.Chrome, usuario: str, senha: str, *args, **kwargs):
        try:
            func(driver, usuario, senha, *args, **kwargs)
        except Exception as e:
            print(f"Erro ao realizar login: {func.__name__}")
            print(e)
    return wrapper


@login_decorator
def loginDigio(digio: webdriver.Chrome, usuario: str, senha: str):

    digio.get("https://funcaoconsig.digio.com.br/FIMENU/Login/AC.UI.LOGIN.aspx")

    esperarElemento(digio, "//*[@id='EUsuario_CAMPO']").send_keys(usuario)
    esperarElemento(digio, "//*[@id='ESenha_CAMPO']").send_keys(senha)
    clickarElemento(digio, '//*[@id="lnkEntrar"]').click()
    clickarElemento(digio, '//*[@id="ctl00_ContentPlaceHolder1_DataListMenu_ctl00_LinkButton2"]').click()


@login_decorator
def loginBlip(blip: webdriver.Chrome, usuario: str, senha: str):
    
    blip.get('https://takegarage-7ah6a.desk.blip.ai/')

    shadow_host = blip.find_element('css selector', '#email-input')
    shadow_root = blip.execute_script("return arguments[0].shadowRoot", shadow_host)
    
    shadow_root.find_element('class name', 'input__container__text').send_keys(usuario)
    blip.find_element('css selector', ".input__container__text").send_keys(senha + Keys.ENTER + Keys.ENTER)

    sleep(5)


@login_decorator
def loginFacta(facta: webdriver.Chrome, usuario: str, senha: str):

    facta.get('https://desenv.facta.com.br/sistemaNovo/login.php')
    
    userElementFacta = esperarElemento(facta, '//*[@id="login"]').send_keys(usuario)
    passwordElementFacta = esperarElemento(facta, '//*[@id="senha"]').send_keys(senha)
    sleep(2)
    esperarElemento(facta,'//*[@id="btnLogin"]').click()
    sleep(5)


@login_decorator
def loginMargem(acces: webdriver.Chrome, usuario: str, senha: str):
    acces.get('https://adpromotora.promobank.com.br/')
    sleep(10)
 
    loginElementmargem = esperarElemento(acces, '//*[@id="usuario"]').send_keys(usuario)
    passwordElementmargem = esperarElemento(acces, '//*[@id="senha"]').send_keys(senha + Keys.ENTER)
    sleep(10)
    atendimentoAntigo = esperarElemento(acces, '//*[@id="topMenu"]/span[3]/div[1]').click()


@login_decorator
def logarBanrisul(banrisul: webdriver.Chrome, usuario, senha):
    banrisul.get('https://desenv.banrisul.com.br/sistemaNovo/login.php')
    sleep(4)
 
    loginElementBanrisul = banrisul.find_element('xpath', '//*[@id="usuario"]').send_keys(senha)
    passwordElementBanrisul = banrisul.find_element('xpath', '//*[@id="senha"]').send_keys(senha)
    sleep(2)
    banrisul.find_element('xpath','//*[@id="btnLogin"]').click()
    sleep(5)