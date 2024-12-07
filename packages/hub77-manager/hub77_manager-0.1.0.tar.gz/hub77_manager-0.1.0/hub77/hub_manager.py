import requests
import logging

class ClientManager:
    def __init__(self, api_url, cliente=None, query=None):
        """
        Inicializa o gerenciador de clientes.
        
        :param api_url: URL base da API.
        :param cliente: Nome do cliente padrão (opcional).
        :param query: Nome da query padrão (opcional).
        """
        self.api_url = api_url.rstrip("/")
        self.cliente = cliente
        self.query = query

        # Configuração do logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        # Substituir FileHandler por StreamHandler para saída no terminal
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        # Formatação das mensagens
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        # Adiciona o handler ao logger
        self.logger.addHandler(handler)

    def log_event(self, log_content, level="INFO"):
        """
        Registra um evento de log tanto localmente quanto na API.
        
        :param log_content: Conteúdo do log.
        :param level: Nível do log (INFO, ERROR, etc.).
        """
        # Log local
        if level == "ERROR":
            self.logger.error(log_content)
        else:
            self.logger.info(log_content)

    def set_config(self, cliente=None, query=None):
        """
        Configura ou atualiza o cliente e query padrão.
        
        :param cliente: Nome do cliente.
        :param query: Nome da query.
        """
        if cliente:
            self.cliente = cliente
        if query:
            self.query = query
        self.log_event(f"Configuração atualizada: cliente={self.cliente}, query={self.query}")

    def add_cliente(self, cliente=None):
        """
        Adiciona um cliente.
        
        :param cliente: Nome do cliente. Se não informado, usa o padrão.
        :return: Resposta da API.
        """
        cliente = cliente or self.cliente
        if not cliente:
            raise ValueError("Cliente não especificado.")
        response = requests.post(f"{self.api_url}/add_cliente", json={"cliente": cliente})
        self.log_event(f"Cliente adicionado: {cliente}")
        return response.json()

    def remove_cliente(self, cliente=None):
        """
        Remove um cliente.
        
        :param cliente: Nome do cliente. Se não informado, usa o padrão.
        :return: Resposta da API.
        """
        cliente = cliente or self.cliente
        if not cliente:
            raise ValueError("Cliente não especificado.")
        response = requests.post(f"{self.api_url}/remove_cliente", json={"cliente": cliente})
        self.log_event(f"Cliente removido: {cliente}")
        return response.json()

    def add_query(self, cliente=None, query=None):
        """
        Adiciona uma query a um cliente.
        
        :param cliente: Nome do cliente. Se não informado, usa o padrão.
        :param query: Nome da query. Se não informado, usa o padrão.
        :return: Resposta da API.
        """
        cliente = cliente or self.cliente
        query = query or self.query
        if not cliente or not query:
            raise ValueError("Cliente ou query não especificados.")
        response = requests.post(f"{self.api_url}/add_query", json={"cliente": cliente, "query": query})
        self.log_event(f"Query adicionada: {query} ao cliente {cliente}")
        return response.json()

    def remove_query(self, cliente=None, query=None):
        """
        Remove uma query de um cliente.
        
        :param cliente: Nome do cliente. Se não informado, usa o padrão.
        :param query: Nome da query. Se não informado, usa o padrão.
        :return: Resposta da API.
        """
        cliente = cliente or self.cliente
        query = query or self.query
        if not cliente or not query:
            raise ValueError("Cliente ou query não especificados.")
        response = requests.post(f"{self.api_url}/remove_query", json={"cliente": cliente, "query": query})
        self.log_event(f"Query removida: {query} do cliente {cliente}")
        return response.json()

    def update_query_status(self, cliente=None, query=None, status=None, log_content=None):
        """
        Atualiza o status de uma query e adiciona o log correspondente.
        
        :param cliente: Nome do cliente. Se não informado, usa o padrão.
        :param query: Nome da query. Se não informado, usa o padrão.
        :param status: Novo status da query.
        :param log_content: Conteúdo do log.
        :return: Resposta da API.
        """


        
        cliente = cliente or self.cliente
        query = query or self.query
        if not cliente or not query or not status or not log_content:
            raise ValueError("Cliente, query, status ou log não especificados.")

        response = requests.post(f"{self.api_url}/update", json={"cliente": cliente, "query": query, "status": status, "log_content": log_content})
        self.log_event(log_content)
        return response.json()

    def get_log(self, cliente=None, query=None):
        """
        Obtém o log de uma query de um cliente.
        
        :param cliente: Nome do cliente. Se não informado, usa o padrão.
        :param query: Nome da query. Se não informado, usa o padrão.
        :return: Resposta da API contendo o log.
        """
        cliente = cliente or self.cliente
        query = query or self.query
        if not cliente or not query:
            raise ValueError("Cliente ou query não especificados.")
        response = requests.post(f"{self.api_url}/get_log", json={"cliente": cliente, "query": query})
        self.log_event(f"Log obtido para a query {query} do cliente {cliente}")
        return response.json()
