import pika
import json
import pandas as pd
import os

# Создаем DataFrame для хранения данных
if not os.path.exists('logs'):
    os.makedirs('logs')

log_file = 'logs/metric_log.csv'
if not os.path.exists(log_file):
    pd.DataFrame(columns=['id', 'y_true', 'y_pred', 'absolute_error']).to_csv(log_file, index=False)

# Словарь для временного хранения сообщений
data_store = {}

def process_message(queue, body):
    message = json.loads(body)
    msg_id = message['id']
    value = message['body']

    if msg_id not in data_store:
        data_store[msg_id] = {}

    data_store[msg_id][queue] = value

    # Проверяем, есть ли обе метки
    if 'y_true' in data_store[msg_id] and 'y_pred' in data_store[msg_id]:
        y_true = data_store[msg_id]['y_true']
        y_pred = data_store[msg_id]['y_pred']
        absolute_error = abs(y_true - y_pred)

        # Записываем в CSV
        df = pd.DataFrame([{
            'id': msg_id,
            'y_true': y_true,
            'y_pred': y_pred,
            'absolute_error': absolute_error
        }])
        df.to_csv(log_file, mode='a', header=False, index=False)

        print(f'ID: {msg_id} | Лог записан: y_true={y_true}, y_pred={y_pred}, error={absolute_error}')
        del data_store[msg_id]

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='y_true')
    channel.queue_declare(queue='y_pred')

    channel.basic_consume(
        queue='y_true',
        on_message_callback=lambda ch, method, properties, body: process_message('y_true', body),
        auto_ack=True
    )

    channel.basic_consume(
        queue='y_pred',
        on_message_callback=lambda ch, method, properties, body: process_message('y_pred', body),
        auto_ack=True
    )

    print('...Ожидание сообщений, для выхода нажмите CTRL+C')
    channel.start_consuming()

except Exception as e:
    print(f'Ошибка: {e}')

