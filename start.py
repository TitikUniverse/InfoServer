import threading
import encrypt as en
from client import Client

# Получаем никнейм пользователя
name = input("Your name: ")

# Вызываем класс с параметрами ника, айпи сервера и порта
user = Client(name, '127.0.0.1', 11719)
user.connect()

# Функция чтение серверных запросов
def read_sock():
    while True:
        data = user.get()
        if data != "": print('\033[A\n' + en.decrypt(data.decode(), user.encrypt_key) + '\033[A')

# Проверка введенных сообщений и отправка
def check():
    while True:
        user.send(name, en.encrypt(input("[me] > "), user.encrypt_key))

# Многопоточное чтение запросов с сервера
thread = threading.Thread(target= read_sock)
thread.start()

# Обработка исключений, чтобы перекрыть подключение к серверу
try:
    check()
except:
    user.disconnect()