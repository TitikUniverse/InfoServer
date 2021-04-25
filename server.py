import socket
import json
import random


sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # Настройка сокетов
sock.bind(('127.0.0.1',11719)) # Айпи и порт сервера

clients = []
encrypts = []

number = 0
number_client = 0
module_number = 0
private_number = 0

print('Start Server')


def send(message, dont, client=""): # Отправка сообщения клиенту(-ам), dont - массив адресов клиентов, кому НЕ надо отправлять
    if client != "":
        sock.sendto(message.encode(), client)
    else:
        for client in clients:
            if client not in dont:
                sock.sendto(message.encode(), client)


while True: # Проверка сообщений
    data, address = sock.recvfrom(1024) # Запись адреса и сообщения
    conn = False # Вспомогательная для шифрования
    conn_client = '' # Вспомогательная для шифрования
    # Полученные данные преобразовываем в словарь
    data_string = json.dumps(data.decode())
    data_dict = json.loads(data.decode())
    if address not in clients:
        clients.append(address)
    # Если словарь полученных данных содержит ключ 'message', то отправить всем соодержимое
    if "message" in data_dict:
        if data_dict["message"].strip() != "":
            message = ("[" + data_dict["alias"] + "] > " + data_dict["message"])
            send(message, [address])
    # Если ключ 'act' равен 'quit', то выйти. Данный ключ тоже вспомогательный для подобных запросов
    elif "act" in data_dict:
        if data_dict["act"] == "quit":
            del encrypts[clients.index(address)]
            del clients[clients.index(address)]
            message = "[SERVER] > " + data_dict["alias"] + " quit from server"
            send(message, [])
    for client in clients:
        if client == address:
            if data_dict["alias"] == "connect": # Снова 'alias', значение 'connect' означает, что будет передача ключа для End-To-End
                conn = True # Включаем режим получения ключа
                conn_client = client # Записываем адресс клиента
            continue
    if conn == True:
        if data_dict["step"] == '1':
            private_number = random.randint(10000000000000000000000100000000000000000000000000000000000000000000000000, 10000000000000000000000000001000000000000000000000000100000000000000000000000000000000000000000000000000000000000000)
            number = int(data_dict["content"])
            module_number = pow(number, private_number, 2**2048)
        elif data_dict["step"] == '2':
            number_client = int(data_dict["content"])
            send(str(module_number), [], conn_client)
            encrypt_key = pow(number_client, private_number, 2**2048)
            encrypts.append(encrypt_key)
            message = "[SERVER] > " + data_dict["name"] + " join to server"
            send(message, [])
            print("Key: " + str(encrypt_key))
        conn = False