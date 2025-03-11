import requests
from google import genai
# from code_template import code_imports, tarefa_class, gerenciador_class, menu_function
from reader import RepoScraper

def extract_info():
    repo_url = "https://github.com/lucasvec/readme-generator"
    scraper = RepoScraper(repo_url)
    response = scraper.run()
    return response

def create_readme(extracted_text):

    # Substitua pela sua chave de API
    client = genai.Client(api_key='AIzaSyAv7OGICVlYJm6tI6S7j8SjhJKP4YPa75U')

    # code_list = [code_imports, tarefa_class, gerenciador_class, menu_function]

    # overview = ''
    # for fragment in code_list:
    #     # Texto para ser resumido
    #
    #     texto = f'Analise o pedaço de código recebido e resuma o que está acontecendo nesse código utilizando um número não muito grande de linhas, em português brasileiro: {fragment}'
    #
    #     response = client.models.generate_content(
    #         model="gemini-2.0-flash",
    #         contents=texto,
    #     )
    #
    #     overview += response.text + '\n'

    # texto = f'Analise o texto a seguir, ele contém a estrutura de todos os arquivos e pastas do repositorio no github. Sua estrutura está separada por identação, e todas as pastas que contém itens dentro delas também estão separadas por identação. O seu trabalho é analisar o texto recebido e retornar um READ.md com base no nome dos arquivos e pastas que contém no texto, que será adicionado via github no repositório do próprio código. Lembre-se de retornar em forma de MARKDOWN para que seja corretamente formatado pelo github. MUITO IMPORTANTE: NÃO ESCREVA NENHUMA MENSAGEM ADICIONAL DE SAUDAÇÃO OU DESPEDIDA OU EXPLICAÇÃO DA TAREFA, APENAS O TEXT EM MARKDOWN DOCUMENTANDO O CÓDIGO BASEADO NO RESUMO FORNECIDO E NÃO PRECISA ADICIONAR NEHUMA INFORMAÇÃO INICIAL INDICANDO QUE O RESTORNO É UM MARKDOWN. Resumo para análise: {extracted_text}'
    
    texto = f"""
O TEXTO A SEGUIR CONTÉM A ESTRUTURA COMPLETA DE TODOS OS ARQUIVOS E PASTAS DE UM REPOSITÓRIO DO GITHUB.  

### **FORMATO DA ESTRUTURA:**  
- Cada linha representa um arquivo ou pasta.  
- **PASTAS** são seguidas de dois-pontos (`:`) e podem conter subitens indentados abaixo delas.  
- **ARQUIVOS** são listados diretamente.  

#### **EXEMPLO DE FORMATO RECEBIDO:**  
ia_prompt:
  __pycache__:
    code_template.cpython-312.pyc
  code_template.py
  ia_request.py
  test.ipynb
.gitignore
LICENSE
README.md
update.py
---

### **INSTRUÇÕES PARA CRIAR O README.md:**  
1. **ANALISE A ESTRUTURA FORNECIDA:**  
   - Cada **pasta principal** deve ser documentada com um título (`## NomeDaPasta`).  
   - Subpastas e arquivos devem ser descritos dentro da respectiva seção.  
   - Se um arquivo tiver um nome sugestivo (`config.json`, `main.py`, `Dockerfile`), explique brevemente sua função.  

2. **FORMATE O README.md UTILIZANDO MARKDOWN:**  
   - Utilize **títulos (`#`, `##`)** para destacar seções.  
   - Use **listas (`-`)** para organizar arquivos dentro de cada pasta.  
   - Se necessário, formate nomes de arquivos como código: `` `arquivo.py` ``  

3. **MUITO IMPORTANTE:**  
   - **NÃO ESCREVA NENHUMA MENSAGEM ADICIONAL DE SAUDAÇÃO OU DESPEDIDA.**  
   - **NÃO EXPLIQUE A TAREFA.**  
   - **NÃO ADICIONE INFORMAÇÕES DESNECESSÁRIAS.**  
   - **RETORNE APENAS O TEXTO FORMATADO EM MARKDOWN.**  

---

### **ESTRUTURA DO REPOSITÓRIO PARA ANÁLISE:**  
{extracted_text}
"""



    response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=texto,
    )

    readme = response.text

    return readme

extracted_info = extract_info()
print(create_readme(extracted_info))
