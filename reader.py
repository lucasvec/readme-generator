import requests
from bs4 import BeautifulSoup
import time


class RepoScraper:
    def __init__(self, repo_url):
        self.repo_url = repo_url
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.visitados = set()  # Guarda URLs já visitadas para evitar loops e duplicação

    def get_soup(self, url):
        """Obtém o HTML da página"""
        print(f"🌐 Acessando: {url}")
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print(f"❌ Erro ao acessar {url}: {e}")

        return None

    def get_pastas_e_arquivos(self, url):
        """Retorna dicionário com pastas e arquivos da URL"""
        pastas = {}
        arquivos = set()  # Usa set para evitar duplicação
        soup = self.get_soup(url)

        if soup:
            div_content = soup.find("div", {"data-hpc": True})
            if div_content:
                for link in div_content.find_all("a", class_="Link--primary"):
                    aria_label = link.get("aria-label", "")
                    href = link.get("href", "")

                    if "(Directory)" in aria_label:
                        pasta_nome = link.text.strip()
                        pasta_url = f"https://github.com{href}"
                        if pasta_nome not in pastas:
                            pastas[pasta_nome] = pasta_url
                    elif "(File)" in aria_label:
                        arquivos.add(link.text.strip())  # Adiciona ao set para evitar repetição

        return {"pastas": pastas, "arquivos": list(arquivos)}  # Converte arquivos para lista no final

    def listar_estrutura(self, url, prefixo=""):
        """Recursivamente lista todos os arquivos e pastas"""
        if url in self.visitados:
            return ""  # Se já visitou essa pasta, não processa novamente

        self.visitados.add(url)  # Marca como visitado
        estrutura = ""
        dados = self.get_pastas_e_arquivos(url)

        # Processa todas as pastas
        for pasta, link in sorted(dados["pastas"].items()):  # Ordena para manter a estrutura organizada
            print(f"📂 Entrando na pasta: {pasta}")
            estrutura += f"{prefixo}{pasta}:\n"
            time.sleep(1)  # Evita sobrecarga de requisições no GitHub
            estrutura += self.listar_estrutura(link, prefixo + "  ")

        # Processa todos os arquivos
        for arquivo in sorted(dados["arquivos"]):  # Ordena os arquivos para manter a ordem consistente
            estrutura += f"{prefixo}{arquivo}\n"

        return estrutura

    def run(self):
        """Executa a extração da estrutura do repositório"""
        print("🔄 Iniciando a extração de estrutura completa do repositório...\n")
        estrutura = self.listar_estrutura(self.repo_url)
        print("✅ Extração concluída!\n")
        print(estrutura)
        return estrutura

# Teste
if __name__ == "__main__":
    repo_url = "https://github.com/Luminary-Team/eden-mobile"
    scraper = RepoScraper(repo_url)
    scraper.run()
