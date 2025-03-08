import requests
from openai import OpenAI
from google import genai
from code_template import code_imports, tarefa_class, gerenciador_class, menu_function

def create_readme():   
    code_list = [code_imports, tarefa_class, gerenciador_class, menu_function]

    # Substitua pela sua chave de API
    client = genai.Client(api_key='AIzaSyAv7OGICVlYJm6tI6S7j8SjhJKP4YPa75U')

    overview = ''
    for fragment in code_list:
        # Texto para ser resumido
        
        texto = f'Analise o pedaço de código recebido e resuma o que está acontecendo nesse código utilizando um número não muito grande de linhas, em português brasileiro: {fragment}'

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=texto,
        )

        overview += response.text + '\n'

    texto = f'Analise o texto a seguir, ele é um resumo de um código apontando as principais funções de cada uma das classes, juntamente com os imports e a saída, o seu trabalho é analisar o resumo recebido e retornar um READ.md, que será adicionado via github no repositório do próprio código. Lembre-se de retornar em forma de MARKDOWN para que seja corretamente formatado pelo github. MUITO IMPORTANTE: NÃO ESCREVA NENHUMA MENSAGEM ADICIONAL DE SAUDAÇÃO OU DESPEDIDA OU EXPLICAÇÃO DA TAREFA, APENAS O TEXT EM MARKDOWN DOCUMENTANDO O CÓDIGO BASEADO NO RESUMO FORNECIDO E NÃO PRECISA ADICIONAR NEHUMA INFORMAÇÃO INICIAL INDICANDO QUE O RESTORNO É UM MARKDOWN. Resumo para análise: {overview}'

    response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=texto,
    )

    readme = response.text

    return readme

print(create_readme())