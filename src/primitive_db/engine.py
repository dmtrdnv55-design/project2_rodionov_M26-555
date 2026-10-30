import prompt


def show_help():
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")


def welcome():
    print("Первая попытка запустить проект!")
    print("\n***")
    show_help()
    while True:
        command = prompt.string("Введите команду: ")
        if command =='help':
            show_help()
        elif command =='exit':
            break
        else:
            print('неизвестная команда')