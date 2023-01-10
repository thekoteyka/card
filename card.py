from tkinter import *
import pickle
from tkinter import messagebox as mb

back = 'gray60' #  Цвет фона
USERS = 'roma', 'sasha', 'maxim', 'dima'  # Пользователи

root = Tk()
root['bg'] = back
root.resizable(0, 0)
root.title("Система карт")
root.geometry("300x200")

#======================================================================================================================|
# FastLogin - Система, которая запоминает текущего пользователя и при следующем запуске автоматически входит в его акк |
#======================================================================================================================|

# Когда пользователь войдёт в акк, тут будет показывать его данные
cardNomerLbl = Label(root, text='Войдите в аккаунт', bg=back, fg='yellow', font='Arial 15')
cardNomerLbl.place(x=5, y=10)

Label(text='Баланс:', bg=back, fg='blue', font='Arial 13').place(x=5, y=43)

cardMoneyLbl = Label(root, text='No', bg=back, fg='cyan', font='Arial 15')
cardMoneyLbl.place(x=80, y=40)

cardUserLbl = Label(root, text='User', bg=back, fg='cyan', font='Arial 15')
cardUserLbl.place(x=220, y=10)

# Записывает данные карты в файл
def set_card(dictionary, file):
    with open(file, 'wb') as out:
        pickle.dump(dictionary, out)

#  {0: {'cardNumber': 2202183577208129, 'cvv': 329, 'secretCode': 78241, 'money': 1000}, 1: {'cardNumber': 1202926791824011, 'cvv': 593, 'secretCode': 37194, 'money': 0}}

# write_dict({'cardNumber': 2202183577208129, 'cvv': 329, 'secretCode': 78241, 'money': 1000, 'user': 'roma'}, 'roma')
# set_card({'cardNumber': 1202926791824011, 'cvv': 593, 'secretCode': 37194, 'money': 0, 'user': 'maxim'}, 'maxim')
# write_dict({'cardNumber': 3202881186172455, 'cvv': 914, 'secretCode': 10199, 'money': 500, 'user': 'sasha'}, 'sasha')
# set_card({'cardNumber': 2202_1456_2011_1941, 'cvv': 228, 'secretCode': 5237, 'money': 2000, 'user': 'dima'}, 'dima')

# Получает данные карты
def get_card(file):
    with open(file, 'rb') as inp:
        d_in = pickle.load(inp)
    return d_in

# print(get_card('dima'))

# ==========================================
# user_card = {'cardNumber': 2202183577208129, 'cvv': 329, 'secretCode': 78241, 'money': 1000, 'user': 'roma'}
user_card = None  # Когда пользователь войдёт тут будем хранить данные его карты, пример сверху
# ==========================================

def safeInput():
    pinq = Tk()
    pinq.title('Enter pin')
    pinq.geometry('190x290')
    pinq['bg'] = 'cyan'
    inputq = ''
    pinq.eval('tk::PlaceWindow . center')

    def qqww(): print(inputq)

    def clear():
        nonlocal inputq
        inputq = ''
        entry.config(state="normal")
        entry.delete(0,END)
        entry.config(state="readonly")

    def add(n):
        nonlocal entry
        nonlocal inputq
        inputq += str(n)
        entry.config(state="normal")
        entry.delete(0,END)
        entry.insert(0, inputq)
        entry.config(state="readonly")
        
    def ret():
        pinq.destroy()

    entry = Entry(pinq, width=25, show='·')
    entry.place(x=16, y=5)

    Button(pinq, command=qqww, text='More', bg='yellow').place(x=350, y=220)
    Button(pinq, command=lambda: add(1), text='1', width=5, bg='lemon chiffon', activebackground='orange',
           height=3).place(x=10, y=30)
    Button(pinq, command=lambda: add(2), text='2', width=5, bg='lemon chiffon', activebackground='orange',
           height=3).place(x=70, y=30)
    Button(pinq, command=lambda: add(3), text='3', width=5, bg='lemon chiffon', activebackground='orange',
           height=3).place(x=130, y=30)
    Button(pinq, command=lambda: add(4), text='4', width=5, bg='lemon chiffon', activebackground='orange',
           height=3).place(x=10, y=95)
    Button(pinq, command=lambda: add(5), text='5', width=5, bg='lemon chiffon', activebackground='orange',
           height=3).place(x=70, y=95)
    Button(pinq, command=lambda: add(6), text='6', width=5, bg='lemon chiffon', activebackground='orange',
           height=3).place(x=130, y=95)
    Button(pinq, command=lambda: add(7), text='7', width=5, bg='lemon chiffon', activebackground='orange',
           height=3).place(x=10, y=160)
    Button(pinq, command=lambda: add(8), text='8', width=5, bg='lemon chiffon', activebackground='orange',
           height=3).place(x=70, y=160)
    Button(pinq, command=lambda: add(9), text='9', width=5, bg='lemon chiffon', activebackground='orange',
           height=3).place(x=130, y=160)
    Button(pinq, command=lambda: add(0), text='0', width=5, bg='lemon chiffon', activebackground='orange',
           height=3).place(x=70, y=225)
    Button(pinq, command=lambda: clear(), text='Reset', width=5, bg='light grey', activebackground='grey',
           height=3).place(x=10, y=225)
    Button(pinq, command=lambda: ret(), text='Готово', width=5, bg='light grey', activebackground='grey',
           height=3).place(x=130, y=225)

    pinq.wait_window()  # Ждем уничтожения окна
    return inputq

def login():  # Кнопка Войти
    lg = Tk()
    lg['bg'] = back
    lg.resizable(0, 0)
    lg.title("Вход")
    lg.geometry("300x200")
    lg.eval('tk::PlaceWindow . center')  # Делаем окно по центру
    cardNumber = StringVar(lg)
    cvv = StringVar(lg)
    secretCode = StringVar(lg)
    stayLoginned = BooleanVar(lg)  # Оставаться ли в системе после выхода

    lg.bind('<Escape>', lambda x: exit(0))


    def _auth():  # Если данные верны
        global user_card, cardData, send_moneyBnt
        user_card = cardData  # Теперь карта пользователя это карта, которую он ввёл

        card_num = str(user_card['cardNumber'])  # Получаем номер карты
        card_no_beautiful =  " ".join([card_num[::-1][i:i+4] for i in range(0, len(card_num), 4)])[::-1]  # Разбивка по 4 цифры

        cardMoneyLbl.configure(text=user_card['money'])
        cardNomerLbl.configure(text=card_no_beautiful)  # Задаём значения для показа номера карты и тд
        cardUserLbl.configure(text=user_card['user'])

        if stayLoginned.get():  # Если оставаться залогиненым
            set_card(user_card['secretCode'], 'fastLogin') # Записываем секретный ключ в файл fastLogin
        else:
            with open('fastLogin', 'w') as f:  # Иначе очищаем файл
                f.write('')
            
        send_moneyBnt['state'] = NORMAL  # Делаем кнопку для перевода денег рабочей, ведь есть аккаунт
        lg.destroy()  # Уничтожаем окно с логином

    def authCode(codeQ=None):  # Вход по секретному коду
        global user_card, cardData
        if codeQ:
            code = codeQ
        else:
            code = secretCode.get() 
        for user in USERS: # Перебираем данные пользователей, чтобы найти с нужным секретным кодом
            cardData = get_card(user)
            if cardData['secretCode'] == int(code): # Если совпадает с введёным
                _auth() # Разрешаем аунтефикацию

    def authNumberCard(): # Вход по номеру карты и CVV коду
        global user_card, cardData
        for user in USERS: # Также, как и в входе по коду
            cardData = get_card(user)
            if cardData['cardNumber'] == int(cardNumber.get().replace(" ", "")) and cardData['cvv'] == int(cvv.get()):
                _auth()

    def authSafeInput():
        code = safeInput()
        authCode(code)

    # Надписи
    Label(lg, text='Номер карты:').place(x=5, y=20)
    Label(lg, text='Cvv Код:').place(x=5, y=50)
    Label(lg, text='Код доступа:').place(x=5, y=130)
    Label(lg, text='Или используйте код доступа', fg='blue', bg='gray60', font='Arial 14').place(x=20, y=80)

    # Поля ввода
    Entry(lg, textvariable=cardNumber).place(x=100, y=20) #            Номер карты
    Entry(lg, textvariable=cvv, width=4).place(x=100, y=50) #          CVV код
    Entry(lg, textvariable=secretCode, width=10).place(x=100, y=130) # Секретный код

    # Кнопки
    Button(lg, text='Войти по коду', bg=back, width=20, command=authCode).place(x=60, y=160)
    Button(lg, text='Войти по номеру карты', bg=back, width=20, command=authNumberCard).place(x=140, y=50)
    Button(lg, text='Use SafeInput', bg=back, width=13, command=authSafeInput).place(x=170, y=125)

    # Переключатели
    Checkbutton(lg, text="Оставаться в системе", bg=back, activebackground=back, variable=stayLoginned).place(x=5, y=105)


def send_money():  # Отправка денег
    money_now = int(user_card['money']) # Сейчас денег у нас      (Наш - пользователя, который вошёл в аккаунт)
    card_num_now = str(user_card['cardNumber']) # Наш номер карты
    card_no_beautiful =  " ".join([card_num_now[::-1][i:i+4] for i in range(0, len(card_num_now), 4)])[::-1] # Красивое отображение номера
    mney = Tk()  # Окно для перевода денег
    mney['bg'] = back
    mney.resizable(0, 0)
    mney.title("Перевод")
    mney.geometry("300x200")
    # mney.eval('tk::PlaceWindow 100x100')
    mney.bind('<Escape>', lambda x: mney.destroy())
    # mney.attributes("-topmost",True)

    card_num_receiver = StringVar(mney)
    money_to_send = StringVar(mney)

    Label(mney, text=card_no_beautiful, bg=back, fg='yellow', font='Arial 15').place(x=5, y=5) # Наш номер карты

    Label(mney, text='Перевести номеру:', bg=back, fg='blue', font='Arial 13').place(x=5, y=30)

    Entry(mney, textvariable=card_num_receiver).place(x=5, y=60)  # Номер карты получателя
    Label(mney, text='Перевести сумму:', bg=back, fg='blue', font='Arial 13').place(x=5, y=90)
    Entry(mney, textvariable=money_to_send).place(x=20, y=120)  # Сколько перевести
    money_nowLbl = Label(mney, text=f'Баланс: {money_now}', bg=back)
    money_nowLbl.place(x=180, y=120)
    
    b = Button(mney, text='Отправить', width=20)
    b.place(x=5, y=170)

    percent_sending = 0  # | Сделано чтобы считывать удерживание кнопки
    null = False         # |
    percent_sending_lbl = Label(mney, text=percent_sending, bg=back)
    percent_sending_lbl.place(x=170, y=170)

    def send(): # Отправляем деньги
        nonlocal b, money_now  # Доступ к кнопке
        try:
            money_to_send_int = int(money_to_send.get())  # Получаем сколько денег переводить
            card_num_receiver_str = card_num_receiver.get().replace(" ", "")  # Убираем пробелы в номере карты
        except Exception:
            mb.showerror('Где данные??', 'Не введены некоторые данные, либо введены неверно')

        if card_num_receiver_str == '48012':  # Секретный код для получения денег
            new_money_our = money_now + money_to_send_int # Добавляем себе столько денег, сколько указано
            user_card['money'] = new_money_our
            set_card(user_card, user_card['user'])  # Записываем новый баланс
            cardMoneyLbl.configure(text=new_money_our) # Записываем новый баланс в Label
            money_nowLbl.configure(text=f'Баланс: {new_money_our}') # Записываем новый баланс в главном меню
            money_now = new_money_our

        else:

            for user in USERS:
                cardData = get_card(user)
                if cardData['cardNumber'] == int(card_num_receiver_str): # Если совпадает с тем, кому мы переводим
                    new_money_reciver = cardData['money'] + money_to_send_int # Добавляем деньги с счёту получателя
                    cardData['money'] = new_money_reciver 
                    set_card(cardData, cardData['user'])  # Записываем новый баланс

                    new_money_user = user_card['money'] - money_to_send_int  # Забираем у отправителя (Тоесть у нас)
                    user_card['money'] = new_money_user
                    set_card(user_card, user_card['user']) # Записываем новый баланс

                    cardMoneyLbl.configure(text=new_money_user) # Записываем новый баланс в Label
                    # b['state'] = DISABLED # Выключаем кнопку | (BETA, Скорее всего уберу)
                    money_nowLbl.configure(text=f'Баланс: {new_money_user}') # Записываем новый баланс в главном меню
                    money_now = new_money_our
                
            # else:
            #     mb.showwarning('А где пользователь то?', f"Не удалось найти пользователя с номером карты\n{card_num_receiver_str}")

    # ======================
    # Сделано чтобы считывать удерживание кнопки, тут сложно
    def update_clock(e=None):
        nonlocal percent_sending, null
        null = False
        for i in range(100):
            if null:
                break
            percent_sending += 1
            percent_sending_lbl.configure(text=percent_sending)
            mney.after(10)
            mney.update()
            if percent_sending == 100:
                send()
    
    def stop_clock(e=None):
        nonlocal percent_sending, null
        null = True
        percent_sending = 0
        percent_sending_lbl.configure(text=percent_sending)
        mney.after(20)

    b.bind('<ButtonPress-1>', update_clock)
    b.bind('<ButtonRelease-1>', stop_clock)
    # ======================

def fastLoginOff(): # Выключить режим FastLogin
    with open('fastLogin', 'w') as f:
        f.write('')
    fastLoginOffBtn['state'] = DISABLED

root.eval('tk::PlaceWindow . center') # Ставим окно по центру


Button(root, text='Войти', bg='gray30', command=login).place(x=5, y=170)
send_moneyBnt = Button(root, text='Отправить деньги', bg='gray30', command=send_money, state=DISABLED)
send_moneyBnt.place(x=5, y=100)

with open('fastLogin', 'rb') as f: # Проверяем, если ли у нас FastLogin
    if f.read(): # Если в файле есть хоть что-то
        for user in USERS: # Ищем пользователя с этим секретным кодом
            cardData = get_card(user)
            if cardData['secretCode'] == int(get_card('fastLogin')): # Когда нашли
                user_card = cardData # Делаем этого пользователя авторизованым

                card_num = str(user_card['cardNumber'])
                card_no_beautiful =  " ".join([card_num[::-1][i:i+4] for i in range(0, len(card_num), 4)])[::-1]

                cardMoneyLbl.configure(text=user_card['money'])
                cardNomerLbl.configure(text=card_no_beautiful)
                cardUserLbl.configure(text=user_card['user'])

                send_moneyBnt['state'] = NORMAL
        # Делаем кнопку для выключения FastLogin
        fastLoginOffBtn = Button(root, text='Выйти из FastLogin', command=fastLoginOff, bg='gray30')
        fastLoginOffBtn.place(x=180, y=170)

root.bind('<Escape>', lambda x: exit(0))


root.mainloop()
