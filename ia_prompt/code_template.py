code_imports = '''import os
               import json
               from datetime import datetime
               '''

tarefa_class =  '''
                class Tarefa:
                    """
                    Classe que representa uma tarefa.
                    """

                    def __init__(self, titulo, descricao, prazo, concluida=False):
                        " q""
                        Inicializa uma nova tarefa.

                        :param titulo: Título da tarefa.
                        :param descricao: Descrição detalhada da tarefa.
                        :param prazo: Prazo para conclusão da tarefa (formato 'dd/mm/yyyy').
                        :param concluida: Status de conclusão da tarefa. Padrão é False.
                        """
                        self.titulo = titulo
                        self.descricao = descricao
                        self.prazo = prazo
                        self.concluida = concluida
                        self.data_criacao = datetime.now()

                    def __str__(self):
                        """
                        Retorna uma representação em string da tarefa com suas informações.

                        :return: Representação da tarefa como string.
                        """
                        status = "Concluída" if self.concluida else "Pendente"
                        return f"Título: {self.titulo}\nDescrição: {self.descricao}\nPrazo: {self.prazo}\nStatus: {status}\nCriada em: {self.data_criacao.strftime('%d/%m/%Y %H:%M:%S')}\n"

                    def concluir(self):
                        """
                        Marca a tarefa como concluída.
                        """
                        self.concluida = True

                    def to_dict(self):
                        """
                        Converte a tarefa para um dicionário para ser salva em formato JSON.

                        :return: Dicionário com os dados da tarefa.
                        """
                        return {
                            "titulo": self.titulo,
                            "descricao": self.descricao,
                            "prazo": self.prazo,
                            "concluida": self.concluida,
                            "data_criacao": self.data_criacao.strftime('%d/%m/%Y %H:%M:%S')
                        }
                '''

gerenciador_class = '''
                    class GerenciadorTarefas:
                        """
                        Classe que gerencia as tarefas, permitindo adicionar, listar, concluir e excluir tarefas.
                        """

                        def __init__(self, arquivo='tarefas.json'):
                            """
                            Inicializa o gerenciador de tarefas.

                            :param arquivo: Nome do arquivo para armazenar as tarefas em formato JSON. Padrão é 'tarefas.json'.
                            """
                            self.arquivo = arquivo
                            self.tarefas = []
                            self.carregar_tarefas()

                        def carregar_tarefas(self):
                            """
                            Carrega as tarefas armazenadas no arquivo JSON.
                            """
                            if os.path.exists(self.arquivo):
                                with open(self.arquivo, 'r') as f:
                                    tarefas_json = json.load(f)
                                    self.tarefas = [Tarefa(**tarefa) for tarefa in tarefas_json]

                        def salvar_tarefas(self):
                            """
                            Salva as tarefas no arquivo JSON.
                            """
                            with open(self.arquivo, 'w') as f:
                                json.dump([tarefa.to_dict() for tarefa in self.tarefas], f, indent=4)

                        def adicionar_tarefa(self, titulo, descricao, prazo):
                            """
                            Adiciona uma nova tarefa à lista de tarefas.

                            :param titulo: Título da tarefa.
                            :param descricao: Descrição detalhada da tarefa.
                            :param prazo: Prazo para conclusão da tarefa.
                            """
                            nova_tarefa = Tarefa(titulo, descricao, prazo)
                            self.tarefas.append(nova_tarefa)
                            self.salvar_tarefas()

                        def listar_tarefas(self, concluida=None):
                            """
                            Lista as tarefas, podendo filtrar por status de conclusão.

                            :param concluida: Se for None, lista todas as tarefas. Caso contrário, filtra as tarefas
                                            com base no status de conclusão (True para concluídas, False para pendentes).
                            """
                            tarefas_filtradas = self.tarefas
                            if concluida is not None:
                                tarefas_filtradas = [tarefa for tarefa in self.tarefas if tarefa.concluida == concluida]
                            for tarefa in tarefas_filtradas:
                                print(tarefa)

                        def concluir_tarefa(self, titulo):
                            """
                            Marca uma tarefa como concluída, caso não tenha sido concluída anteriormente.

                            :param titulo: Título da tarefa a ser concluída.
                            """
                            for tarefa in self.tarefas:
                                if tarefa.titulo == titulo and not tarefa.concluida:
                                    tarefa.concluir()
                                    self.salvar_tarefas()
                                    print(f"Tarefa '{titulo}' concluída.")
                                    return
                            print(f"Tarefa '{titulo}' não encontrada ou já concluída.")

                        def excluir_tarefa(self, titulo):
                            """
                            Exclui uma tarefa pela sua título.

                            :param titulo: Título da tarefa a ser excluída.
                            """
                            self.tarefas = [tarefa for tarefa in self.tarefas if tarefa.titulo != titulo]
                            self.salvar_tarefas()
                            print(f"Tarefa '{titulo}' excluída.")
                    '''

menu_function = '''
                def menu():
                    """
                    Função que exibe o menu interativo e gerencia as ações do usuário.
                    """
                    gerenciador = GerenciadorTarefas()
                    
                    while True:
                        print("\n===== Gerenciador de Tarefas =====")
                        print("1. Adicionar Tarefa")
                        print("2. Listar Tarefas")
                        print("3. Concluir Tarefa")
                        print("4. Excluir Tarefa")
                        print("5. Sair")
                        
                        opcao = input("Escolha uma opção: ")
                        
                        if opcao == '1':
                            titulo = input("Digite o título da tarefa: ")
                            descricao = input("Digite a descrição da tarefa: ")
                            prazo = input("Digite o prazo da tarefa (dd/mm/yyyy): ")
                            gerenciador.adicionar_tarefa(titulo, descricao, prazo)
                            print("Tarefa adicionada com sucesso!")
                        
                        elif opcao == '2':
                            filtro = input("Deseja listar as tarefas concluídas? (s/n): ")
                            if filtro.lower() == 's':
                                gerenciador.listar_tarefas(concluida=True)
                            else:
                                gerenciador.listar_tarefas(concluida=False)
                        
                        elif opcao == '3':
                            titulo = input("Digite o título da tarefa a ser concluída: ")
                            gerenciador.concluir_tarefa(titulo)
                        
                        elif opcao == '4':
                            titulo = input("Digite o título da tarefa a ser excluída: ")
                            gerenciador.excluir_tarefa(titulo)
                        
                        elif opcao == '5':
                            print("Saindo... Até logo!")
                            break
                        
                        else:
                            print("Opção inválida. Tente novamente.")

                if __name__ == "__main__":
                    menu()
                '''