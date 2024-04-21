# main.py
from src.channel import Channel

if __name__ == '__main__':
    # Создаем два экземпляра класса с тестовыми данными
    moscowpython = Channel('UC-OVMPlMA3-YCIeg4z5z23A')
    highload = Channel('UCwHL6WHUarjGfUM_586me8w')

    # Используем различные магические методы
    print(moscowpython)
    print(moscowpython + highload)
    print(moscowpython - highload)
    print(highload - moscowpython)
    print(moscowpython > highload)
    print(moscowpython >= highload)
    print(moscowpython < highload)
    print(moscowpython <= highload)
    print(moscowpython == highload)