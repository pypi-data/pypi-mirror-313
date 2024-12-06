import asyncio

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