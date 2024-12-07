import asyncio
import pandas as pd
from selenium.webdriver.remote.webelement import WebElement


async def aguardarTempo(intervalo: int = 900):

    async def countdown(intervalo: int):
        """
        Contagem assíncrona que mostra os minutos e segundos restantes
        
        Args:
            intervalo (int): A duração da contagem (em segundos).
        """
        tempo = 0
        while tempo < intervalo:
            for suffix in ["   ", ".  ", ".. ", "..."]:
                remaining = intervalo - tempo
                minutos, segundos = divmod(remaining, 60)
                print(f"Próxima checagem em {minutos:02}:{segundos:02} - Aguardando{suffix}", end="\r")
                await asyncio.sleep(1)
                tempo += 1
        print(f"                                                                           ", end="\r")

    await countdown(intervalo)


def convertHTMLTable2Dataframe(tableElement: WebElement) -> pd.DataFrame:
    """
    Converte um elemento <table> (Selenium WebElement) em um DataFrame

    Args:
        tableElemento (WebElement): O elemento do Selenium que representa a tabela em HTML <table>

    Returns:
        pd.DataFrame: A DataFrame containing the table data.
    """
    headers = [header.text for header in tableElement.find_elements("xpath", './/th')]
    
    rows = []
    for row in tableElement.find_elements("xpath", './/tr'):
        cells = row.find_elements("xpath", './/td')
        rows.append([cell.text for cell in cells])
    
    rows = [row for row in rows if row]
    
    if headers:
        return pd.DataFrame(rows, columns=headers)
    else:
        return pd.DataFrame(rows)