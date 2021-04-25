import socket
import random


class Client:
    def __init__(self, name_client, server_ip, server_port): # Инициируем класс
        self.name = name_client
        self.server = (server_ip, server_port)
        self.server_connect = ('', 0)
        self.sock = ''
        self.endtoend = False
        self.encrypt_key = 0


    def connect(self): # Для присоединение к серверу и метода Диффи, Хеллман
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.bind(self.server_connect)
        self.endtoend = True
      
        number_server = 0
        number = random.randint(100000000000000010000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000, 1000000000000000000000100000000000000000000000001000000000000000000000000000100000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000)
        self.sock.sendto(self.tostring({ "alias": "connect", "content": number, "key": 8, "step": 1 }).encode(), self.server)
      
        private_number = random.randint(100000000000000000000000010000000000000000000000000100000000000000000000000000000000000000000000000000000000000, 100000000000001000000000000000000000000000100000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000)
      
        module_number = pow(number, private_number, 2**2048)
        self.sock.sendto(self.tostring({ "alias": "connect", "name": self.name, "content": module_number, "step": 2 }).encode(), self.server)
      
        number_server = int(self.getting().decode())
        self.encrypt_key = pow(number_server, private_number, 2**2048)
      
        self.endtoend = False
      
        print("Key: " + str(self.encrypt_key))
      
        if self.encrypt_key == 0:
            self.disconnect()
            print("Fatal error!")
  

    def disconnect(self): # Разъединение
        self.sock.sendto(self.tostring({ "alias": self.name, "act": "quit" }).encode(), self.server)


    def send(self, alias, message): # Отправить сообщение, alias - вспомогательная переменная, message - сообщение
        self.sock.sendto(self.tostring({ "alias": alias, "message": message }).encode(), self.server)
      

    def get(self): # Получить сообщение
        if not self.endtoend: return self.sock.recv(1024)
      

    def getting(self): # Принудительное получение сообщения
        return self.sock.recv(1024)
      

    def tostring(self, dicts={}): # Перевод словаря в текст для отправки на сервер
        output = '{ '
        dictvalues = list(dicts.values())
        for element in dicts.keys():
            if dicts[element] != dictvalues[-1]:
                output = output + '"' + element + '": "' + str(dicts[element]) + '", '
            else:
                output = output + '"' + element + '": "' + str(dicts[element]) + '" }'
        if output == '{ ':
            output = ""
        return output