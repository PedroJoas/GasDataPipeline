import requests
import re
import os
from tqdm import tqdm
from requests.exceptions import ChunkedEncodingError

class ExtractGLPData:
    
    def __init__(self) -> None:
        self.url_base = 'https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsas/glp/glp-{}-0{}.csv'
        self.diretorio = 'data/'
        pass

    def _gera_urls(self):
        anos = list(range(2004, 2025))
        semestres = [1,2]
        urls = []

        for semestre in semestres:
            for ano in anos:
                url_modificada = self.url_base.format(ano, semestre)
                urls.append(url_modificada)

        return urls
    
    def baixa_urls(self):
        urls = self._gera_urls()

        for url in tqdm(urls):
            # Fazendo a requisição GET
            try:
                response = requests.get(url)
                m = re.search(r"glp-(\d{4})-(\d{2})", url)

                if m:
                    ano = m.group(1)  # Captura o ano
                    semestre = m.group(2)  # Captura o semestre
                    nomeArquivo = f"glp-{ano}-{semestre}"
    
                # Especificando o nome do arquivo onde o CSV será salvo
                nomeArquivo = f"{nomeArquivo}.csv"
                fullPath = os.path.join(self.diretorio, nomeArquivo)

                # Salvando o conteúdo da resposta no arquivo
                with open(fullPath, "wb") as file:
                    file.write(response.content)
                    print(f'{fullPath} Baixado por completo')

            except ChunkedEncodingError as e:
                print(f'Erro na leitura do site: {e}')





        