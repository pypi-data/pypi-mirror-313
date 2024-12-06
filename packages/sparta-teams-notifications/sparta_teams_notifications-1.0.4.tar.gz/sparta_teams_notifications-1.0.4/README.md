# Airflow Teams Notifications

Este pacote permite enviar notificações de tarefas do Apache Airflow para canais do Microsoft Teams usando Adaptive Cards. A função `teams_notification` envia um cartão de notificação para múltiplos canais do Teams, com informações sobre a tarefa que foi executada no Airflow.

## Requisitos

- **Apache Airflow**: Para usar a função dentro de um DAG do Airflow.
- **requests**: Para enviar a solicitação HTTP para os webhooks do Teams.

## Instalação

1. Instale os requisitos do pacote:

    ```bash
    pip install sparta-teams-notifications
    ```

## Como usar

### Função `teams_notification`

A função `teams_notification` envia uma notificação para os canais do Microsoft Teams informando o status de uma tarefa no Airflow.

### Parâmetros:

- **`ctx`** (dict): O contexto da execução da tarefa do Airflow, geralmente disponível em um operador de tarefa. 
- **`channels`** (list): Uma lista de canais do Teams para os quais a notificação será enviada. Cada canal deve ser uma chave no dicionário de webhooks.
- **`webhooks_dict_variable`** (str, opcional): O nome da variável do Airflow que contém o dicionário de webhooks. O valor padrão é `TEAMS_WEBHOOKS`. A variável deve ser um dicionário no formato `{ "channel_name": "webhook_url" }`.
- **`airflow_host_variable`** (str, opcional): O nome da variável do Airflow que contém o host do Airflow. O valor padrão é `AIRFLOW_HOST`.

### Exemplo de uso:

```python
from airflow.utils.dates import days_ago
from airflow.decorators import dag, task
from sparta_teams_notifications.notifications import teams_notification

@dag(
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    on_failure_callback=lambda ctx: teams_notification(ctx, ["CHANNEL1", "CHANNEL2"])
)
def example_dag():
    @task()
    def failing_task():
        raise ValueError("This is a test failure!")

    failing_task()

example_dag()

