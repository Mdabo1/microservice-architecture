import pika
import numpy as np
import json
import time
from datetime import datetime
from sklearn.datasets import load_diabetes

# Бесконечный цикл для отправки сообщений
while True:
    try:
        X, y = load_diabetes(return_X_y=True)
        random_row = np.random.randint(0, X.shape[0]-1)

        # Создаём подключение по адресу rabbitmq:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()

        # Создаём очереди
        channel.queue_declare(queue='y_true')
        channel.queue_declare(queue='features')

        # Генерация уникального идентификатора
        message_id = datetime.timestamp(datetime.now())

        # Формируем сообщения
        message_y_true = {
            'id': message_id,
            'body': y[random_row]
        }
        message_features = {
            'id': message_id,
            'body': list(X[random_row])
        }

        # Публикация сообщений
        channel.basic_publish(
            exchange='',
            routing_key='y_true',
            body=json.dumps(message_y_true)
        )
        print(f'ID: {message_id} | Сообщение с правильным ответом отправлено')

        channel.basic_publish(
            exchange='',
            routing_key='features',
            body=json.dumps(message_features)
        )
        print(f'ID: {message_id} | Сообщение с вектором признаков отправлено')

        # Закрываем подключение
        connection.close()

        # Задержка в 5 секунд
        time.sleep(5)

    except Exception as e:
        print(f'Ошибка: {e}')
        time.sleep(5)

