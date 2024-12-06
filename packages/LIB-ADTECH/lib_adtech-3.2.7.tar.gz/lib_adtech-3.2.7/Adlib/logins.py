from selenium import webdriver
from Adlib.funcoes import esperarElemento, clickarElemento


def loginDigio(digio: webdriver.Chrome, usuario: str, senha: str):

    try:
        digio.get("https://funcaoconsig.digio.com.br/FIMENU/Login/AC.UI.LOGIN.aspx")
        digio.maximize_window()

        esperarElemento(digio, "//*[@id='EUsuario_CAMPO']").send_keys(usuario)
        esperarElemento(digio, "//*[@id='ESenha_CAMPO']").send_keys(senha)
        clickarElemento(digio, '//*[@id="lnkEntrar"]').click()
        
        clickarElemento(digio, '//*[@id="ctl00_ContentPlaceHolder1_DataListMenu_ctl00_LinkButton2"]').click()

    
    except Exception as e:
        print("Erro no login do Digio")
        print(e)
