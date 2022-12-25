from tkinter import *
import pickle

back = 'gray60'
USERS = 'roma', 'sasha', 'maxim', 'dima'

root = Tk()
root['bg'] = back
root.resizable(0, 0)
root.title("Система карт")
root.geometry("300x200")

cardNomerLbl = Label(root, text='Войдите в аккаунт', bg=back, fg='yellow', font='Arial 15')
cardNomerLbl.place(x=5, y=10)

Label(text='Баланс:', bg=back, fg='blue', font='Arial 13').place(x=5, y=43)

cardMoneyLbl = Label(root, text='No', bg=back, fg='cyan', font='Arial 15')
cardMoneyLbl.place(x=80, y=40)

cardUserLbl = Label(root, text='User', bg=back, fg='cyan', font='Arial 15')
cardUserLbl.place(x=200, y=40)


def set_card(dictionary, file):
    with open(file, 'wb') as out:
        pickle.dump(dictionary, out)

#  {0: {'cardNumber': 2202183577208129, 'cvv': 329, 'secretCode': 78241, 'money': 1000}, 1: {'cardNumber': 1202926791824011, 'cvv': 593, 'secretCode': 37194, 'money': 0}}

# write_dict({'cardNumber': 2202183577208129, 'cvv': 329, 'secretCode': 78241, 'money': 1000, 'user': 'roma'}, 'roma')
# set_card({'cardNumber': 1202926791824011, 'cvv': 593, 'secretCode': 37194, 'money': 0, 'user': 'maxim'}, 'maxim')
# write_dict({'cardNumber': 3202881186172455, 'cvv': 914, 'secretCode': 10199, 'money': 500, 'user': 'sasha'}, 'sasha')
# set_card({'cardNumber': 2202_1456_2011_1941, 'cvv': 228, 'secretCode': 5237, 'money': 2000, 'user': 'dima'}, 'dima')

def get_card(file):
    with open(file, 'rb') as inp:
        d_in = pickle.load(inp)
    return d_in

print(get_card('dima'))

# ==========================================
# user_card = {'cardNumber': 2202183577208129, 'cvv': 329, 'secretCode': 78241, 'money': 1000, 'user': 'roma'}
user_card = None
# ==========================================


def login():
    lg = Tk()
    lg['bg'] = back
    lg.resizable(0, 0)
    lg.title("Вход")
    lg.geometry("300x200")
    lg.eval('tk::PlaceWindow . center')
    cardNumber = StringVar(lg)
    cvv = StringVar(lg)
    secretCode = StringVar(lg)
    stayLoginned = BooleanVar(lg)


    def _auth():
        global user_card, cardData, send_moneyBnt
        user_card = cardData

        card_num = str(user_card['cardNumber'])
        card_no_beautiful =  " ".join([card_num[::-1][i:i+4] for i in range(0, len(card_num), 4)])[::-1]

        cardMoneyLbl.configure(text=user_card['money'])
        cardNomerLbl.configure(text=card_no_beautiful)
        cardUserLbl.configure(text=user_card['user'])

        if stayLoginned.get():
            print(1)
            set_card(user_card['secretCode'], 'fastLogin')
        else:
            with open('fastLogin', 'w') as f:
                f.write('')
            
        send_moneyBnt['state'] = NORMAL
        lg.destroy()

    def authCode():
        global user_card, cardData
        code = secretCode.get()
        for user in USERS:
            cardData = get_card(user)
            if cardData['secretCode'] == int(code):
                _auth()

    def authNumberCard():
        global user_card, cardData
        for user in USERS:
            cardData = get_card(user)
            if cardData['cardNumber'] == int(cardNumber.get().replace(" ", "")) and cardData['cvv'] == int(cvv.get()):
                _auth()

    Label(lg, text='Номер карты:').place(x=5, y=20)
    Label(lg, text='Cvv Код:').place(x=5, y=50)
    Label(lg, text='Код доступа:').place(x=5, y=130)
    Label(lg, text='Или используйте код доступа', fg='blue', bg='gray60', font='Arial 14').place(x=20, y=80)

    Entry(lg, textvariable=cardNumber).place(x=100, y=20)
    Entry(lg, textvariable=cvv, width=4).place(x=100, y=50)
    Entry(lg, textvariable=secretCode, width=10).place(x=100, y=130)

    Button(lg, text='Войти по коду', bg=back, width=20, command=authCode).place(x=60, y=160)
    Button(lg, text='Войти по номеру карты', bg=back, width=20, command=authNumberCard).place(x=140, y=50)

    Checkbutton(lg, text="Оставаться в системе", bg=back, activebackground=back, variable=stayLoginned).place(x=5, y=105)


def send_money():
    money_now = int(user_card['money'])
    card_num_now = str(user_card['cardNumber'])
    card_no_beautiful =  " ".join([card_num_now[::-1][i:i+4] for i in range(0, len(card_num_now), 4)])[::-1]
    mney = Tk()
    mney['bg'] = back
    mney.resizable(0, 0)
    mney.title("Перевод")
    mney.geometry("300x200")
    mney.eval('tk::PlaceWindow . center')

    card_num_receiver = StringVar(mney)
    money_to_send = StringVar(mney)

    Label(mney, text=card_no_beautiful, bg=back, fg='yellow', font='Arial 15').place(x=5, y=5)

    Label(mney, text='Перевести номеру:', bg=back, fg='blue', font='Arial 13').place(x=5, y=30)

    Entry(mney, textvariable=card_num_receiver).place(x=5, y=60)
    Label(mney, text='Перевести сумму:', bg=back, fg='blue', font='Arial 13').place(x=5, y=90)
    Entry(mney, textvariable=money_to_send).place(x=20, y=120)
    money_nowLbl = Label(mney, text=f'Баланс: {money_now}', bg=back)
    money_nowLbl.place(x=180, y=120)
    
    b = Button(mney, text='Отправить', width=20)
    b.place(x=5, y=170)

    percent_sending = 0
    null = False
    percent_sending_lbl = Label(mney, text=percent_sending, bg=back)
    percent_sending_lbl.place(x=170, y=170)

    def send():
        nonlocal b
        money_to_send_int = int(money_to_send.get())
        card_num_receiver_str = card_num_receiver.get().replace(" ", "")
        for user in USERS:
            cardData = get_card(user)
            if cardData['cardNumber'] == int(card_num_receiver_str):
                new_money_reciver = cardData['money'] + money_to_send_int
                cardData['money'] = new_money_reciver
                set_card(cardData, cardData['user'])

                new_money_user = user_card['money'] - money_to_send_int
                user_card['money'] = new_money_user
                set_card(user_card, user_card['user'])

                cardMoneyLbl.configure(text=new_money_user)
                b['state'] = DISABLED
                money_nowLbl.configure(text=f'Баланс: {new_money_user}')

    
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

def fastLoginOff():
    with open('fastLogin', 'w') as f:
        f.write('')
    fastLoginOffBtn['state'] = DISABLED

root.eval('tk::PlaceWindow . center')

Button(root, text='Войти', bg='gray30', command=login).place(x=5, y=170)
send_moneyBnt = Button(root, text='Отправить деньги', bg='gray30', command=send_money, state=DISABLED)
send_moneyBnt.place(x=5, y=100)

with open('fastLogin', 'rb') as f:
    if f.read():
        for user in USERS:
            cardData = get_card(user)
            if cardData['secretCode'] == int(get_card('fastLogin')):
                user_card = cardData

                card_num = str(user_card['cardNumber'])
                card_no_beautiful =  " ".join([card_num[::-1][i:i+4] for i in range(0, len(card_num), 4)])[::-1]

                cardMoneyLbl.configure(text=user_card['money'])
                cardNomerLbl.configure(text=card_no_beautiful)
                cardUserLbl.configure(text=user_card['user'])

                send_moneyBnt['state'] = NORMAL
        fastLoginOffBtn = Button(root, text='Выйти из FastLogin', command=fastLoginOff, bg='gray30')
        fastLoginOffBtn.place(x=180, y=170)

root.mainloop()