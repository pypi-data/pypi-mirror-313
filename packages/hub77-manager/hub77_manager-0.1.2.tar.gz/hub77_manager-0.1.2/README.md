# HubDados API - Manager

O `HubDados API - Manager` é uma classe Python que facilita a interação com uma API para gerenciar clientes, queries e logs. Ele também registra logs localmente usando a biblioteca `logging`, garantindo que todos os eventos sejam armazenados tanto localmente quanto remotamente.

---

## Funcionalidades

- **Gerenciamento de Clientes**:
  - Adicionar e remover clientes.

- **Gerenciamento de Queries**:
  - Adicionar, remover e atualizar queries associadas aos clientes.

- **Logs**:
  - Registrar eventos localmente usando `logging`.
  - Enviar logs para a API através de uma requisição POST.

---

## Requisitos

- Python 3.7 ou superior.
- Biblioteca `requests`.

---

## Uso

### Exemplo Básico

```python
from client_manager import ClientManager

# Configuração inicial
api_url = "https://sua-api.com"
client_manager = ClientManager(api_url)

# Configuração do cliente e query padrão
client_manager.set_config(cliente="cliente_teste", query="query_teste")

# Adicionar um cliente
response = client_manager.add_cliente()
print("Resposta ao adicionar cliente:", response)

# Adicionar uma query ao cliente
response = client_manager.add_query()
print("Resposta ao adicionar query:", response)

# Atualizar o status de uma query com log
response = client_manager.update_query_status(
    status="completo",
    log_content="Query processada com sucesso."
)
print("Resposta ao atualizar status:", response)

# Obter logs de uma query
response = client_manager.get_log()
print("Log obtido:", response)
```

---

## Endpoints da API

O `ClientManager` espera que a API forneça os seguintes endpoints:

| Endpoint         | Método | Descrição                      |
|-------------------|--------|--------------------------------|
| `/add_cliente`    | POST   | Adiciona um novo cliente.      |
| `/remove_cliente` | POST   | Remove um cliente.             |
| `/add_query`      | POST   | Adiciona uma query a um cliente. |
| `/remove_query`   | POST   | Remove uma query de um cliente. |
| `/update`         | POST   | Atualiza o status de uma query. |
| `/get_log`        | POST   | Obtém o log de uma query.      |
| `/log_event`      | POST   | Registra um evento de log.     |

---

## Estrutura de Logs Locais

Os logs são salvos em um arquivo chamado `client_manager.log`. Cada registro inclui a data, o nível do log e a mensagem associada.

Exemplo de log:

```
2024-12-03 12:00:00 - INFO - Configuração atualizada: cliente=cliente_teste, query=query_teste
2024-12-03 12:01:00 - INFO - Cliente adicionado: cliente_teste
2024-12-03 12:02:00 - INFO - Query adicionada: query_teste ao cliente cliente_teste
2024-12-03 12:03:00 - INFO - Status atualizado para completo e log adicionado para a query query_teste do cliente cliente_teste
```
