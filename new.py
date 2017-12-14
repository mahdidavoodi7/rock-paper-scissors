import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import mysql.connector
from mysql.connector import Error
import logging

# create a file handler for saving logs
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('hello.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info('App started ...')

# initializa the keyboard that show when 2 players are playing
keyboardd = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='سنگ ✊🏻', callback_data='1'),InlineKeyboardButton(text='کاغذ ✋🏻', callback_data='2'),
                                                 InlineKeyboardButton(text='قیچی ✌🏻', callback_data='3')]]
                                                 )
#define the array that use many time in this app
arr=["سنگ","کاغذ","قیچی"]
wait_for_opp = {}
#define the RPS game law
def game_result(first,last):
    if first == "1":
        if last == "2":
            return -1
        elif last == "3":
            return 1
        elif last=="4":
            return 1
        elif last=="5":
            return -1
        else:
            return 0
    if first == "2":
        if last == "1":
            return 1
        elif last == "3":
            return -1
        elif last=="4":
            return -1
        elif last=="5":
            return 1
        else:
            return 0
    if first == "3":
        if last == "1":
            return -1
        elif last == "2":
            return 1
        elif last=="4":
            return 1
        elif last=="5":
            return -1
        else:
            return 0

class player:
    battle_id = 0
    def __init__(self,chat__id,status,score,user_name):
        self.chat__id = chat__id
        self.status = status
        self.score = score
        self.user_name = user_name

class db_player:
    player_db = {}
    def __init__(self):
        conn = mysql.connector.connect(host='localhost',
                                       database='mahdidav_123',
                                       user='mahdidav_123',
                                       password='neymar1107')
        cur = conn.cursor()
        cur.execute("SELECT * FROM players")
        row = cur.fetchall()
        cur.close()
        conn.close()
        for val in row:
            print(val)
            p = player(str(val[1]), "available", int(val[3]), val[2])
            self.player_db[str(val[1])] = p
    def add_player(self,chat__id,status,score,user_name):
        #print("added to the database")
        a = player(chat__id,status,score,user_name)
        self.player_db[str(chat__id)] = a
    def exist(self,chat__id):
        if str(chat__id) in self.player_db:
            return True
        else:
            return False

    #This method return an object from player class with chat__id condition
    def find_player_by_id(self,chat__id):
        return self.player_db[str(chat__id)]

    def leaderboard(self,chat_id):
        show = ""
        x = 0
        sorted_name = []
        sorted_scores = []
        sorted_chat_id = []
        for key in self.player_db:
            sorted_chat_id.append(key)
            sorted_name.append(self.player_db[key].user_name)
            sorted_scores.append(self.player_db[key].score)
        for i in range(0, len(sorted_scores)):
            for j in range(i + 1, len(sorted_scores)):
                if sorted_scores[j] > sorted_scores[i]:
                    temp = sorted_scores[i]
                    temp_string = sorted_name[i]
                    temp_chat = sorted_chat_id[i]
                    sorted_scores[i] = sorted_scores[j]
                    sorted_name[i] = sorted_name[j]
                    sorted_chat_id[i] = sorted_chat_id[j]
                    sorted_scores[j] = temp
                    sorted_name[j] = temp_string
                    sorted_chat_id[j] = temp_chat
        for i in range(0, len(sorted_chat_id)):
            if str(chat_id) == sorted_chat_id[i]:
                x = i
                break
        for i in range(0, len(sorted_chat_id)):
            if len(sorted_chat_id) < 11:
                if i == 0:
                    show += "🥇 " + sorted_name[i] + "    :    " + str(sorted_scores[i]) + "\n"
                elif i == 1:
                    show += "🥈 " + sorted_name[i] + "    :    " + str(sorted_scores[i]) + "\n"
                elif i == 2:
                    show += "🥉 " + sorted_name[i] + "    :    " + str(sorted_scores[i]) + "\n"
                else:
                    show += "  " + str(i + 1) + " - " + sorted_name[i] + "    :    " + str(sorted_scores[i]) + "\n"
            else:
                if i < 5:
                    if i == 0:
                        show += "🥇 " + sorted_name[i] + "    :    " + str(sorted_scores[i]) + "\n"
                    elif i == 1:
                        show += "🥈 " + sorted_name[i] + "    :    " + str(sorted_scores[i]) + "\n"
                    elif i == 2:
                        show += "🥉 " + sorted_name[i] + "    :    " + str(sorted_scores[i]) + "\n"
                    else:
                        if int(sorted_chat_id[i]) == chat_id:
                            show += "  " + "➡️" + " - " + sorted_name[i] + "    :    " + str(
                                sorted_scores[i]) + "\n"
                        else:
                            show += "  " + str(i + 1) + " - " + sorted_name[i] + "    :    " + str(sorted_scores[i]) + "\n"
                        if i == 4:
                            if 5 < x:
                                show+= ".\n.\n.\n.\n"
                else:
                    if x - i < 3 and x - i > -3:
                        if int(sorted_chat_id[i]) == chat_id:
                            show += "  " + "➡️" + " - " + sorted_name[i] + "    :    " + str(
                                sorted_scores[i]) + "\n"
                        else:
                            show += "  " + str(i + 1) + " - " + sorted_name[i] + "    :    " + str(sorted_scores[i]) + "\n"
        bot.sendMessage(chat_id,show)
logger.info('player_db created.')
player_db = db_player()
class battle:
    p1 = player(0,"",0,"")
    p2 = player(0,"",0,"")
    time_played1 = 0
    time_played2 = 0
    score1 = 0
    score2 = 0
    selected_op1 = 0
    selected_op2 = 0
    forbid_chat = 0
    #errorrrrrrrrrrrrrrr ehtemaale ziaad
    def __init__(self,player1,player2,max_point):
        self.p1 = player1
        self.p2 = player2
        self.max_point = max_point
        self.p1.status = "in_battle"
        self.p2.status = "in_battle"
    def ended(self):
        if self.score1==self.max_point:
            player_db.add_player(self.p1.chat__id,'available',self.p1.score + self.score1 - self.score2,self.p1.user_name)
            bot.sendMessage(int(self.p1.chat__id),"ماشالا بازی رو بردی")
            player_db.add_player(self.p2.chat__id, 'available', self.p2.score + self.score2 - self.score1,self.p2.user_name)
            bot.sendMessage(int(self.p2.chat__id), "بازم که باختی ...")
        elif self.score2 == self.max_point:
            player_db.add_player(self.p1.chat__id, 'available', self.p1.score + self.score1 - self.score2,
                                 self.p1.user_name)
            bot.sendMessage(int(self.p1.chat__id), "بازم که باختی ...")
            bot.sendMessage(int(self.p2.chat__id), "ماشالا بازی رو بردی")
            player_db.add_player(self.p2.chat__id, 'available', self.p2.score + self.score2 - self.score1,
                                 self.p2.user_name)
        bot.sendMessage(int(self.p1.chat__id), 'خوب از کیبورد زیر بگو واست چی کار کنم', reply_markup=ReplyKeyboardMarkup(
                                                        keyboard=[[KeyboardButton(text=menu_array[1])],
                                                                  [KeyboardButton(text=menu_array[2]),
                                                                   KeyboardButton(text=menu_array[3])],
                                                                  [KeyboardButton(text=menu_array[5]),
                                                                   KeyboardButton(text=menu_array[6])]],
                                                        resize_keyboard=True))
        bot.sendMessage(int(self.p2.chat__id), 'خوب از کیبورد زیر بگو واست چی کار کنم', reply_markup=ReplyKeyboardMarkup(
                                                        keyboard=[[KeyboardButton(text=menu_array[1])],
                                                                  [KeyboardButton(text=menu_array[2]),
                                                                   KeyboardButton(text=menu_array[3])],
                                                                  [KeyboardButton(text=menu_array[5]),
                                                                   KeyboardButton(text=menu_array[6])]],
                                                        resize_keyboard=True))
        conn = mysql.connector.connect(host='localhost',
                                       database='mahdidav_123',
                                       user='mahdidav_123',
                                       password='neymar1107')
        cur = conn.cursor()
        try:
            cur.execute("""UPDATE players SET score=%s WHERE chat_id=%s""", (int(self.p1.score + self.score1 - self.score2),str(self.p1.chat__id)))
            cur.execute("""UPDATE players SET score=%s WHERE chat_id=%s""", (int(self.p2.score + self.score2 - self.score1),str(self.p2.chat__id)))
        except Error as e:
            print(str(e) + " :  this error has been occured ")
        conn.commit()
        cur.close()
        conn.close()
    def concede(self):
        if self.score1 == self.max_point:
            player_db.add_player(self.p1.chat__id,'available',self.p1.score + self.score1 - self.score2,self.p1.user_name)
            player_db.add_player(self.p2.chat__id, 'available', self.p2.score + self.score2 - self.score1,self.p2.user_name)
        else:
            player_db.add_player(self.p1.chat__id, 'available', self.p1.score + self.score1 - self.score2,
                                 self.p1.user_name)
            player_db.add_player(self.p2.chat__id, 'available', self.p2.score + self.score2 - self.score1,
                                 self.p2.user_name)

        if int(self.p1.chat__id) in wait_for_opp:
            del(wait_for_opp[int(self.p1.chat__id)])
        elif int(self.p2.chat__id) in wait_for_opp:
            del (wait_for_opp[int(self.p2.chat__id)])

        conn = mysql.connector.connect(host='localhost',
                                       database='mahdidav_123',
                                       user='mahdidav_123',
                                       password='neymar1107')
        cur = conn.cursor()
        cur.execute("""UPDATE players SET score=%s WHERE chat_id=%s""", (int(self.p1.score + self.score1 - self.score2), str(self.p1.chat__id)))
        cur.execute("""UPDATE players SET score=%s WHERE chat_id=%s""", (int(self.p2.score + self.score2 - self.score1), str(self.p2.chat__id)))
        conn.commit()
        cur.close()
        conn.close()
    def play(self,selected1,selected2):
        bot.sendMessage(self.p1.chat__id, "حریفت " + str(arr[int(selected2)-1]) + " رو انتخاب کرد")
        bot.sendMessage(self.p2.chat__id, "حریفت " + str(arr[int(selected1)-1]) + " رو انتخاب کرد")
        if game_result(selected1,selected2) == 1:
            self.score1 += 1
        elif game_result(selected1,selected2) == -1:
            self.score2 += 1

        bot.sendMessage(self.p2.chat__id,"🛑🛑 "+self.p1.user_name + " : " + str(self.score1) + "\n\n"+"🛑🛑 "+ self.p2.user_name + " : " + str(self.score2))
        bot.sendMessage(self.p1.chat__id,"🛑🛑 "+self.p1.user_name + " : " + str(self.score1) + "\n\n" +"🛑🛑 "+ self.p2.user_name + " : " + str(self.score2))
        if self.score1 == self.max_point or self.score2 == self.max_point:
            self.ended()
        else:
            bot.sendMessage(self.p1.chat__id,"شانستو امتحان کن",reply_markup = keyboardd)
            bot.sendMessage(self.p2.chat__id, "شانستو امتحان کن", reply_markup = keyboardd)
class db_battle:
    battles={}
    p1 = player(0, "", 0, "")
    p2 = player(0, "", 0, "")
    b = battle(p1,p2,0)
    def add_battle(self,b):
        self.battles[str(b.p1.chat__id)] = b
        self.battles[str(b.p2.chat__id)] = b

    def del_battle(self,b):
        del(self.battles[b.battle_id])

    def show_battles(self):
        print("Battle Database :")
        for key in self.battles:
            print(str(key) + " :: " + str(self.battles[key].p1.chat__id) + " vs " + str(self.battles[key].p2.chat__id))

    def find(self,chad):
        for key in self.battles:
            #print(str(key) + "   "+ str(chad))
            if str(key) == str(chad):
                return self.battles[key]
        return 0

allow_to_play = 1
send_to_all = {}
battle_db = db_battle()
wait_room10 = []
wait_room5 = []
wait_room15 = []
response_wait10 = {}
last_message_sent = {}
intro = {}
menu_array=["مسابقه دوستانه 👬","مسابقه رده بندی 🏆","رده بندی 🏅","راهنما ❓","انصراف ❌","دعوت از دوستان 👥","جوایز 🎁"]
sub_menu_array=["۵ امتیازی ⭐️","۱۰ امتیازی ⭐️⭐️","۱۵ امتیازی ⭐️⭐️⭐️"]

def handle(msg):
    global allow_to_play
    content_type,chat_type,chat_id = telepot.glance(msg)
    try:
        if content_type == 'text':
            if chat_id != 217339724:
                if player_db.exist(chat_id):
                    x = player_db.find_player_by_id(str(chat_id))
                    if x.status == 'available':
                        if msg['text'] == "جوایز 🎁":
                            logger.info(str(chat_id) + ' want gift menu.')
                            bot.sendMessage(chat_id,'خوب همونجور که میدونید این بات تازه کاره و باگ زیاد داره تصمیم گرفتیم هر کی کوچکترین باگی رو که پیدا کنه به ما بگه ۲۰ امتیاز میگیره \n واقعا برای بهتر شدن ربات به کمکتون نیازه \nخوش باشید . :))))')
                        elif msg['text'] == menu_array[3]:
                            logger.info(str(chat_id) + ' want help menu.')
                            bot.sendMessage(chat_id,
                                            'راهنمای بازی :\n⭕️از زمانی که مسابقه رو شروع میکنید شما برای بازی کردن دست خودتون ۳ دیقه وقت دارید اگه تو این ۳ دیقه دست رو بازی نکنی میبازی :(\n⭕️ بازی چند قسمت مختلف داره به صورتی که میتونید تفریحی با دوستانتون بازی کنید یا اینکه توی مسابقات رده بندی شرکت کنید .\n⭕️ مسابقه های رده بندی ۵ و ۱۰ و ۱۵ امتیازیه .\n⭕️ همچنین به بازی دوستانه امتیازی تعلق نمیگیره . \n⭕️ اگر نمیخوایید ادامه بدید میتونید از مسابقه انصراف بدید اما این انصراف به این معنیه که شکست رو قبول کردین و امتیاز کل بازی رو از دست میدین و اون رو تقدیم به حریفتون میکنید .\n⭕️ در صورتی که دوستاتون رو به این بات دعوت کنید و اونها از کد دعوت شما به بات استفاده کنند ۱۰ امتیاز به شما اضافه میشه .\n⭕توی هر بازی میتونی با حریفت چت کنی ولی اگه نمیخوای با حریفت چت کنی ممنوع کردن چت رو بزن تا دیگه پیامی برات نیاد')
                        elif msg['text'] == menu_array[2]:
                            logger.info(str(chat_id) + ' want leader menu.')
                            player_db.leaderboard(chat_id)
                        elif msg['text'] == menu_array[5]:
                            logger.info(str(chat_id) + ' want invite menu.')
                            bot.sendMessage(chat_id, "سلام رفیق\nپاشو بیا تو این بات سنگ کاغذ قیچی بازی کن و ته هر فصل جایزه ببر\nفقط اومدی اولش این کد رو هم به ربات بده \n\nکد معرف : " +str(chat_id) +"\n" +"لینک ربات : @paper_rock_scissors_bot"+"\n.")
                        elif msg['text'] == menu_array[1]:
                            logger.info(str(chat_id) + ' want to start a match .')
                            if msg['text'] not in sub_menu_array:
                                if allow_to_play == 1:
                                    bot.sendMessage(chat_id,'میخوای مسابقه چند امتیازی باشه ؟',reply_markup=ReplyKeyboardMarkup(
                                        keyboard=[[KeyboardButton(text=sub_menu_array[0])],
                                                  [KeyboardButton(text=sub_menu_array[1])],
                                                  [KeyboardButton(text=sub_menu_array[2])],[KeyboardButton(text="بازگشت ⬅️")]],
                                        resize_keyboard=True))
                                else:
                                    bot.sendMessage(chat_id, 'با عرض پوزش میخوایم بات رو آپدیت کنیم\n چن ساعت دیگه دوباره امتحان کن ',
                                                    reply_markup=ReplyKeyboardMarkup(
                                                        keyboard=[[KeyboardButton(text=menu_array[1])],
                                                                  [KeyboardButton(text=menu_array[2]),
                                                                   KeyboardButton(text=menu_array[3])],
                                                                  [KeyboardButton(text=menu_array[5]),
                                                                   KeyboardButton(text=menu_array[6])]],
                                                        resize_keyboard=True))
                        elif msg['text'] == sub_menu_array[0]:
                            logger.info(str(chat_id) + ' want to start a 5 point match .')
                            if len(wait_room5) == 0:
                                wait_room5.append(x)
                                bot.sendMessage(chat_id, "منتظر وایسا تا یکی رو پیدا کنم", reply_markup=ReplyKeyboardMarkup(
                                    keyboard=[[KeyboardButton(text=menu_array[2]), KeyboardButton(text=menu_array[3])],
                                              [KeyboardButton(text="انصراف از انتظار ❌")]], resize_keyboard=True))
                                player_db.add_player(chat_id, 'in_wait_room', x.score, x.user_name)
                            else:
                                b = battle(x, wait_room5[0], 5)
                                battle_db.add_battle(b)
                                player_db.add_player(x.chat__id, "in_battle", x.score, x.user_name)
                                player_db.add_player(wait_room5[0].chat__id, "in_battle", wait_room5[0].score,
                                                     wait_room5[0].user_name)
                                bot.sendMessage(x.chat__id, "خوب یکی رو پیدا کردم که باهاش بازی کنی"+ "\n" + "حریفت : "+ wait_room5[0].user_name,
                                                reply_markup=ReplyKeyboardMarkup(
                                                    keyboard=[[KeyboardButton(text=menu_array[2]),
                                                               KeyboardButton(text=menu_array[3])],
                                                              [KeyboardButton(text="انصراف از مسابقه ❌"),
                                                               KeyboardButton(text="غیر فعال کردن چت 🚫")]],
                                                    resize_keyboard=True))

                                bot.sendMessage(wait_room5[0].chat__id, "خوب یکی رو پیدا کردم که باهاش بازی کنی"+ "\n" + "حریفت : "+ x.user_name,
                                                reply_markup=ReplyKeyboardMarkup(
                                                    keyboard=[[KeyboardButton(text=menu_array[2]),
                                                               KeyboardButton(text=menu_array[3])],
                                                              [KeyboardButton(text="انصراف از مسابقه ❌"),
                                                               KeyboardButton(text="غیر فعال کردن چت 🚫")]],
                                                    resize_keyboard=True))
                                bot.sendMessage(b.p1.chat__id, "شانستو امتحان کن",
                                                                                   reply_markup=keyboardd)
                                bot.sendMessage(b.p2.chat__id, "شانستو امتحان کن",
                                                                                   reply_markup=keyboardd)
                                wait_room5.clear()
                        elif msg['text'] == sub_menu_array[1]:
                            logger.info(str(chat_id) + ' want to start a 10 point match .')
                            if len(wait_room10) == 0:
                                wait_room10.append(x)
                                bot.sendMessage(chat_id,"منتظر وایسا تا یکی رو پیدا کنم",reply_markup=ReplyKeyboardMarkup(
                                    keyboard=[[KeyboardButton(text=menu_array[2]),KeyboardButton(text=menu_array[3])],
                                              [KeyboardButton(text="انصراف از انتظار ❌")]],resize_keyboard=True))
                                player_db.add_player(chat_id,'in_wait_room',x.score,x.user_name)
                            else:
                                b = battle(x,wait_room10[0],10)
                                battle_db.add_battle(b)
                                player_db.add_player(x.chat__id,"in_battle",x.score,x.user_name)
                                player_db.add_player(wait_room10[0].chat__id,"in_battle",wait_room10[0].score,wait_room10[0].user_name)
                                bot.sendMessage(x.chat__id,"خوب یکی رو پیدا کردم که باهاش بازی کنی"+ "\n" + "حریفت : "+ wait_room10[0].user_name,reply_markup=ReplyKeyboardMarkup(
                                    keyboard=[[KeyboardButton(text=menu_array[2]),KeyboardButton(text=menu_array[3])],
                                              [KeyboardButton(text="انصراف از مسابقه ❌"),KeyboardButton(text="غیر فعال کردن چت 🚫")]],resize_keyboard=True))

                                bot.sendMessage(wait_room10[0].chat__id,"خوب یکی رو پیدا کردم که باهاش بازی کنی"+ "\n" + "حریفت : "+ x.user_name,reply_markup=ReplyKeyboardMarkup(
                                    keyboard=[[KeyboardButton(text=menu_array[2]),KeyboardButton(text=menu_array[3])],
                                              [KeyboardButton(text="انصراف از مسابقه ❌"),KeyboardButton(text="غیر فعال کردن چت 🚫")]],resize_keyboard=True))
                                bot.sendMessage(b.p1.chat__id, "شانستو امتحان کن",
                                                                                   reply_markup=keyboardd)
                                bot.sendMessage(b.p2.chat__id, "شانستو امتحان کن",
                                                                                   reply_markup=keyboardd)
                                wait_room10.clear()
                        elif msg['text'] == sub_menu_array[2]:
                            logger.info(str(chat_id) + ' want to start a 15 point match .')
                            if len(wait_room15) == 0:
                                wait_room15.append(x)
                                bot.sendMessage(chat_id, "منتظر وایسا تا یکی رو پیدا کنم", reply_markup=ReplyKeyboardMarkup(
                                    keyboard=[[KeyboardButton(text=menu_array[2]), KeyboardButton(text=menu_array[3])],
                                              [KeyboardButton(text="انصراف از انتظار ❌")]], resize_keyboard=True))
                                player_db.add_player(chat_id, 'in_wait_room', x.score, x.user_name)
                            else:
                                b = battle(x, wait_room15[0], 15)
                                battle_db.add_battle(b)
                                player_db.add_player(x.chat__id, "in_battle", x.score, x.user_name)
                                player_db.add_player(wait_room15[0].chat__id, "in_battle", wait_room15[0].score,
                                                     wait_room15[0].user_name)
                                bot.sendMessage(x.chat__id, "خوب یکی رو پیدا کردم که باهاش بازی کنی" + "\n" + "حریفت : "+ wait_room15[0].user_name,
                                                reply_markup=ReplyKeyboardMarkup(
                                                    keyboard=[[KeyboardButton(text=menu_array[2]),
                                                               KeyboardButton(text=menu_array[3])],
                                                              [KeyboardButton(text="انصراف از مسابقه ❌"),
                                                               KeyboardButton(text="غیر فعال کردن چت 🚫")]],
                                                    resize_keyboard=True))

                                bot.sendMessage(wait_room15[0].chat__id, "خوب یکی رو پیدا کردم که باهاش بازی کنی"+ "\n" + "حریفت : "+ x.user_name,
                                                reply_markup=ReplyKeyboardMarkup(
                                                    keyboard=[[KeyboardButton(text=menu_array[2]),
                                                               KeyboardButton(text=menu_array[3])],
                                                              [KeyboardButton(text="انصراف از مسابقه ❌"),
                                                               KeyboardButton(text="غیر فعال کردن چت 🚫")]],
                                                    resize_keyboard=True))
                                bot.sendMessage(b.p1.chat__id, "شانستو امتحان کن",
                                                                       reply_markup=keyboardd)
                                bot.sendMessage(b.p2.chat__id, "شانستو امتحان کن",
                                                                                   reply_markup=keyboardd)
                                wait_room15.clear()
                        else:
                            bot.sendMessage(chat_id, 'خوب از کیبورد زیر بگو واست چی کار کنم',
                                            reply_markup=ReplyKeyboardMarkup(
                                                keyboard=[[KeyboardButton(text=menu_array[1])],
                                                          [KeyboardButton(text=menu_array[2]),
                                                           KeyboardButton(text=menu_array[3])],
                                                          [KeyboardButton(text=menu_array[5]),
                                                           KeyboardButton(text=menu_array[6])]],
                                                resize_keyboard=True))
                    elif x.status == 'in_battle':
                        bat = battle_db.find(chat_id)
                        if msg['text'] == "انصراف از مسابقه ❌":
                            logger.info(str(chat_id) + ' want to concede match .')
                            if int(bat.p1.chat__id) == chat_id:
                                bat.score2=bat.max_point
                                bot.sendMessage(bat.p1.chat__id,"خوب از مسابقه انصراف دادی و باختی بازی رو",reply_markup=ReplyKeyboardMarkup(
                                    keyboard=[[KeyboardButton(text=menu_array[1])],
                                              [KeyboardButton(text=menu_array[2]),KeyboardButton(text=menu_array[3])],
                                                                  [KeyboardButton(text=menu_array[5]),
                                                                   KeyboardButton(text=menu_array[6])]],
                                    resize_keyboard=True))
                                bot.sendMessage(bat.p2.chat__id,"حریفت انصراف داد مثل این که شانسی شانسی بردی :)",reply_markup=ReplyKeyboardMarkup(
                                                        keyboard=[[KeyboardButton(text=menu_array[1])],
                                                                  [KeyboardButton(text=menu_array[2]),
                                                                   KeyboardButton(text=menu_array[3])],
                                                                  [KeyboardButton(text=menu_array[5]),
                                                                   KeyboardButton(text=menu_array[6])]],
                                                        resize_keyboard=True))
                            elif int(bat.p2.chat__id) == chat_id:
                                bat.score1 = bat.max_point
                                bot.sendMessage(bat.p2.chat__id,"خوب از مسابقه انصراف دادی و باختی بازی رو",reply_markup=ReplyKeyboardMarkup(
                                                        keyboard=[[KeyboardButton(text=menu_array[1])],
                                                                  [KeyboardButton(text=menu_array[2]),
                                                                   KeyboardButton(text=menu_array[3])],
                                                                  [KeyboardButton(text=menu_array[5]),
                                                                   KeyboardButton(text=menu_array[6])]],
                                                        resize_keyboard=True))
                                bot.sendMessage(bat.p1.chat__id,"حریفت انصراف داد مثل این که شانسی شانسی بردی :)",reply_markup=ReplyKeyboardMarkup(
                                                        keyboard=[[KeyboardButton(text=menu_array[1])],
                                                                  [KeyboardButton(text=menu_array[2]),
                                                                   KeyboardButton(text=menu_array[3])],
                                                                  [KeyboardButton(text=menu_array[5]),
                                                                   KeyboardButton(text=menu_array[6])]],
                                                        resize_keyboard=True))
                            bat.concede()
                        elif msg['text'] == menu_array[2]:
                            logger.info(str(chat_id) + ' want leaderboard menu .')
                            player_db.leaderboard(chat_id)
                        elif msg['text'] == menu_array[3]:
                            logger.info(str(chat_id) + ' want to invite .')
                            bot.sendMessage(chat_id,
                                            'راهنمای بازی :\n⭕️از زمانی که مسابقه رو شروع میکنید شما برای بازی کردن دست خودتون ۳ دیقه وقت دارید اگه تو این ۳ دیقه دست رو بازی نکنی میبازی :(\n⭕️ بازی چند قسمت مختلف داره به صورتی که میتونید تفریحی با دوستانتون بازی کنید یا اینکه توی مسابقات رده بندی شرکت کنید .\n⭕️ مسابقه های رده بندی ۵ و ۱۰ و ۱۵ امتیازیه .\n⭕️ همچنین به بازی دوستانه امتیازی تعلق نمیگیره . \n⭕️ اگر نمیخوایید ادامه بدید میتونید از مسابقه انصراف بدید اما این انصراف به این معنیه که شکست رو قبول کردین و امتیاز کل بازی رو از دست میدین و اون رو تقدیم به حریفتون میکنید .\n⭕️ در صورتی که دوستاتون رو به این بات دعوت کنید و اونها از کد دعوت شما به بات استفاده کنند ۱۰ امتیاز به شما اضافه میشه .\n⭕توی هر بازی میتونی با حریفت چت کنی ولی اگه نمیخوای با حریفت چت کنی ممنوع کردن چت رو بزن تا دیگه پیامی برات نیاد')
                        elif msg['text'] == "غیر فعال کردن چت 🚫":
                            logger.info(str(chat_id) + ' want to forbid the chat .')
                            bat.forbid_chat = 1
                            bot.sendMessage(chat_id,"چت غیر فعال شد .")
                        else:
                            if bat.forbid_chat == 0:
                                if chat_id == int(bat.p1.chat__id):
                                    bot.sendMessage(int(bat.p2.chat__id),bat.p1.user_name + " گفت : " + msg['text'])
                                elif chat_id == int(bat.p2.chat__id):
                                    bot.sendMessage(int(bat.p1.chat__id), bat.p2.user_name + " گفت : " + msg['text'])
                            else:
                                bot.sendMessage(chat_id, "چت غیر فعال شده است و تا پایان این بازی فعال نمیشود")
                    else:
                        if msg['text'] not in menu_array and msg['text']!="انصراف از انتظار ❌":

                            bot.sendMessage(chat_id,"منتظر وایسا تا یکی رو پیدا کنم",reply_markup=ReplyKeyboardMarkup(
                                keyboard=[[KeyboardButton(text=menu_array[2]),KeyboardButton(text=menu_array[3])],
                                          [KeyboardButton(text="انصراف از انتظار ❌")]],resize_keyboard=True))

                        if msg['text'] == "انصراف از انتظار ❌":
                            logger.info(str(chat_id) + ' want to go out from wait room .')
                            if len(wait_room10)!=0 and int(x.chat__id) == int(wait_room10[0].chat__id):
                                x.status = 'available'
                                player_db.add_player(str(chat_id),'available',x.score,str(x.user_name))
                                wait_room10.clear()
                            elif len(wait_room5)!=0 and int(x.chat__id) == int(wait_room5[0].chat__id):
                                x.status = 'available'
                                player_db.add_player(str(chat_id), 'available', x.score, x.user_name)
                                wait_room5.clear()
                            elif len(wait_room15)!=0 and int(x.chat__id) == int(wait_room15[0].chat__id):
                                x.status = 'available'
                                player_db.add_player(str(chat_id), 'available', x.score, x.user_name)
                                wait_room15.clear()
                            bot.sendMessage(chat_id,'خوب از کیبورد زیر بگو واست چی کار کنم',reply_markup=ReplyKeyboardMarkup(
                                                        keyboard=[[KeyboardButton(text=menu_array[1])],
                                                                  [KeyboardButton(text=menu_array[2]),
                                                                   KeyboardButton(text=menu_array[3])],
                                                                  [KeyboardButton(text=menu_array[5]),
                                                                   KeyboardButton(text=menu_array[6])]],
                                                        resize_keyboard=True))
                        elif msg['text'] == menu_array[2]:
                            logger.info(str(chat_id) + ' want leaderboard menu .')
                            player_db.leaderboard(chat_id)
                        elif msg['text'] == menu_array[3]:
                            logger.info(str(chat_id) + ' want to invite (3).')
                            bot.sendMessage(chat_id,
                                            'راهنمای بازی :\n⭕️از زمانی که مسابقه رو شروع میکنید شما برای بازی کردن دست خودتون ۳ دیقه وقت دارید اگه تو این ۳ دیقه دست رو بازی نکنی میبازی :(\n⭕️ بازی چند قسمت مختلف داره به صورتی که میتونید تفریحی با دوستانتون بازی کنید یا اینکه توی مسابقات رده بندی شرکت کنید .\n⭕️ مسابقه های رده بندی ۵ و ۱۰ و ۱۵ امتیازیه .\n⭕️ همچنین به بازی دوستانه امتیازی تعلق نمیگیره . \n⭕️ اگر نمیخوایید ادامه بدید میتونید از مسابقه انصراف بدید اما این انصراف به این معنیه که شکست رو قبول کردین و امتیاز کل بازی رو از دست میدین و اون رو تقدیم به حریفتون میکنید .\n⭕️ در صورتی که دوستاتون رو به این بات دعوت کنید و اونها از کد دعوت شما به بات استفاده کنند ۱۰ امتیاز به شما اضافه میشه .\n⭕توی هر بازی میتونی با حریفت چت کنی ولی اگه نمیخوای با حریفت چت کنی ممنوع کردن چت رو بزن تا دیگه پیامی برات نیاد')
                else:
                    if chat_id not in intro:
                        logger.info(str(chat_id) + ' started the bot for the first time')
                        bot.sendMessage(chat_id, "خوش اومدی \nاگه کسی تو رو به بات معرفی کرده شماره معرف رو وارد کن",reply_markup=ReplyKeyboardMarkup(
                            keyboard=[[KeyboardButton(text="معرف ندارم")]],resize_keyboard=True))
                        intro[chat_id] = 0
                    else:
                        if msg['text'] != "معرف ندارم":
                            logger.info(str(chat_id) + ' has not any introducer')
                            for key in player_db.player_db:
                                if str(key) == str(msg['text']):
                                    xx = player_db.find_player_by_id(key)
                                    xx.score += 10
                                    bot.sendMessage(int(key), "یکی از اونایی که دعوتشون کرده بودی به بات اضافه شد و ۱۰ امتیاز گرفتی")
                                    intro[chat_id] += 1
                                    break
                            if intro[chat_id] == 0:
                                bot.sendMessage(chat_id,"معرفی با این شماره موجود نیست")
                        if 'username' in msg['from']:
                            username = msg['from']['username']
                        else:
                            if 'last_name' in msg['from']:
                                username = msg['from']['first_name'] + msg['from']['last_name']
                            else:
                                username = msg['from']['first_name']
                        player_db.add_player(chat_id,'available',0,username)
                        logger.info("write " + str(chat_id) + ' to the database .')
                        try:
                            conn = mysql.connector.connect(host='localhost',
                                                           database='mahdidav_123',
                                                           user='mahdidav_123',
                                                           password='neymar1107')
                            cur = conn.cursor()
                            cur.execute("""INSERT INTO players(chat_id, username, score) VALUES(%s,%s,%s)""",((str(chat_id)),username,0))
                            conn.commit()
                            cur.close()
                            conn.close()
                        except Exception as e:
                            logger.error("an error has been occured : " + str(e))
                        bot.sendMessage(chat_id,'خوب از کیبورد زیر بگو واست چی کار کنم',reply_markup=ReplyKeyboardMarkup(
                                                        keyboard=[[KeyboardButton(text=menu_array[1])],
                                                                  [KeyboardButton(text=menu_array[2]),
                                                                   KeyboardButton(text=menu_array[3])],
                                                                  [KeyboardButton(text=menu_array[5]),
                                                                   KeyboardButton(text=menu_array[6])]],
                                                        resize_keyboard=True))
            else:
                if msg['text'] == "رده بندی":
                    player_db.leaderboard(chat_id)
                    logger.info("admin want leaderboard")
                elif msg['text'] == "آمار":
                    logger.info("admin want analyze")
                    all_player = 0
                    in_battle_player = 0
                    for key in player_db.player_db:
                        if player_db.player_db[key].status == "in_battle":
                            in_battle_player += 1
                        all_player += 1
                    all_battle = len(battle_db.battles)
                    bot.sendMessage(chat_id, "اینم آمار بات :\nتعداد کل نفراتی که تا حالا بازی کردند : " + str(all_player) + "\nتعداد نفراتی که الان در حال بازی هستند : " + str(in_battle_player) + "\nتعداد کل بازی هایی که توی این فصل انجام شده : " + str(all_battle))
                elif msg['text'] == "عدم اجازه برای بازی":
                    logger.info("admin want change access to play")
                    if allow_to_play == 1:
                        allow_to_play = 0
                        bot.sendMessage(chat_id, 'الان دیگه کسی نمیتونه بازی کنه',
                                        reply_markup=ReplyKeyboardMarkup(
                                            keyboard=[[KeyboardButton(text="آمار"),
                                                       KeyboardButton(text="ارسال پیام برای همه")],
                                                      [KeyboardButton(text="عدم اجازه برای بازی"),
                                                       KeyboardButton(text="رده بندی")]], resize_keyboard=True))
                    else:
                        allow_to_play = 1
                        bot.sendMessage(chat_id, 'الان همه میتونن بازی کنن',
                                        reply_markup=ReplyKeyboardMarkup(
                                            keyboard=[[KeyboardButton(text="آمار"),
                                                       KeyboardButton(text="ارسال پیام برای همه")],
                                                      [KeyboardButton(text="عدم اجازه برای بازی"),
                                                       KeyboardButton(text="رده بندی")]], resize_keyboard=True))
                elif msg['text'] == "ارسال پیام برای همه":
                    send_to_all[chat_id] = 0
                    bot.sendMessage(chat_id, "مطلبی رو که میخوای برای همه بفرستی رو بده")
                else:
                    if chat_id in send_to_all:
                        if send_to_all[chat_id] == 0:
                            bot.sendMessage(chat_id, "مطمئنی این متن رو میخوای برای همه بفرستی ؟", reply_markup=ReplyKeyboardMarkup(
                            keyboard=[[KeyboardButton(text="تایید"), KeyboardButton(text="لغو")]], resize_keyboard=True))
                            send_to_all[chat_id] = msg['text']
                        else:
                            if msg['text'] == "تایید":
                                logger.info("admin accept the change access to play")
                                try:
                                    delete_array=[]
                                    for key in player_db.player_db.keys():
                                        try:
                                            bot.sendMessage(int(key), send_to_all[chat_id])
                                        except:
                                            delete_array.append(key)
                                    for key in delete_array:
                                        conn = mysql.connector.connect(host='localhost',
                                                                       database='mahdidav_123',
                                                                       user='mahdidav_123',
                                                                       password='neymar1107')
                                        cur = conn.cursor()
                                        cur.execute("DELETE FROM players WHERE chat_id=%s", (str(key),))
                                        conn.commit()
                                        cur.close()
                                        conn.close()
                                    del delete_array
                                    send_to_all.clear()
                                    bot.sendMessage(chat_id, 'پیام برای همه ارسال شد',
                                                    reply_markup=ReplyKeyboardMarkup(
                                                        keyboard=[[KeyboardButton(text="آمار"),
                                                                   KeyboardButton(text="ارسال پیام برای همه")],
                                                                  [KeyboardButton(text="عدم اجازه برای بازی"),
                                                                   KeyboardButton(text="رده بندی")]], resize_keyboard=True))
                                except Exception as e:
                                    logger.error("an error has been occured in admin accept : " + str(e))
                            else:
                                bot.sendMessage(chat_id, 'ارسال پیام لغو شد',
                                                reply_markup=ReplyKeyboardMarkup(
                                                    keyboard=[[KeyboardButton(text="آمار"),
                                                               KeyboardButton(text="ارسال پیام برای همه")],
                                                              [KeyboardButton(text="عدم اجازه برای بازی"),
                                                               KeyboardButton(text="رده بندی")]], resize_keyboard=True))
                                send_to_all.clear()
                    else:
                        bot.sendMessage(chat_id, 'خوب از کیبورد زیر بگو واست چی کار کنم', reply_markup=ReplyKeyboardMarkup(
                            keyboard=[[KeyboardButton(text="آمار"), KeyboardButton(text="ارسال پیام برای همه")],
                                      [KeyboardButton(text="عدم اجازه برای بازی"), KeyboardButton(text="رده بندی")]], resize_keyboard=True))
        else:
            bot.sendMessage(chat_id, "فقط میتونی متن بفرستی عزیز")
    except Exception as e:
        bot.sendMessage(217339724,str(e))

def on_callback_query(msg):
    query_id,from_id,query_data = telepot.glance(msg,flavor='callback_query')
    bot.answerCallbackQuery(query_id, arr[int(query_data) - 1])
    x = player_db.find_player_by_id(str(from_id))
    if x.status == 'in_battle':
        logger.info(str(from_id) + " choose : " + str(query_data))
        bat = battle_db.find(from_id)
        try:
            if str(from_id) == str(bat.p1.chat__id):
                if int(bat.p2.chat__id) in wait_for_opp:
                    bat.play(query_data,wait_for_opp[int(bat.p2.chat__id)]['selected'])
                    del(wait_for_opp[int(bat.p2.chat__id)])
                else:
                    #print("4")
                    dicss = {}
                    dicss['selected'] = query_data
                    dicss['time'] = 0
                    wait_for_opp[from_id] = dicss
            else:
                if int(bat.p1.chat__id) in wait_for_opp:
                    # print("5")
                    bat.play(wait_for_opp[int(bat.p1.chat__id)]['selected'],query_data)
                    del(wait_for_opp[int(bat.p1.chat__id)])
                else:
                    # print("6")
                    dicss = {}
                    dicss['selected'] = query_data
                    dicss['time'] = 0
                    wait_for_opp[from_id] = dicss
        except Exception as e:
            logger.error("This Error had been occured : in the call back query : " + str(e))

# bot = telepot.Bot('375880514:AAHYHQea8YqJUxN87MxBQP9vFyMMFMzI5Mw')
bot = telepot.Bot('375880514:AAHYHQea8YqJUxN87MxBQP9vFyMMFMzI5Mw')
MessageLoop(bot,{'chat': handle,
                  'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')
while 1:
    time.sleep(10)
    for key in wait_for_opp:
        wait_for_opp[key]['time'] += 10
        if wait_for_opp[key]['time'] >= 180:
            try:
                logger.info(str(wait_for_opp[key]) + " is in wait for opp for 3 min")
                bat = battle_db.find(key)
                if int(key) == int(bat.p1.chat__id):
                    bat.score1 = bat.max_point
                    bot.sendMessage(int(bat.p1.chat__id),"حریفت بیشتر از ۳ دیقه است که بازی نکرده پس تو شانسی بردی")
                    bot.sendMessage(int(bat.p2.chat__id), "بیشتر از ۳ دیقه است که دستتو بازی نکردی پس باختی :(")
                    bat.ended()
                else:
                    bat.score2 = bat.max_point
                    bot.sendMessage(int(bat.p2.chat__id), "حریفت بیشتر از ۳ دیقه است که بازی نکرده پس تو شانسی بردی")
                    bot.sendMessage(int(bat.p1.chat__id), "بیشتر از ۳ دیقه است که دستتو بازی نکردی پس باختی :(")
                    bat.ended()
                del wait_for_opp[key]
                break
            except Exception as e:
                if 'Forbidden' in e:
                    try:
                        bot.sendMessage(bat.p1.chat__id,"حریفت کاملا انصراف داد")
                        bat.score1 = bat.max_point
                        bat.ended()
                        del wait_for_opp[key]
                    except:
                        bot.sendMessage(bat.p2.chat__id, "حریفت کاملا انصراف داد")
                        bat.score2 = bat.max_point
                        bat.ended()
                        del wait_for_opp[key]
                logger.error("an error has been occured in wait for opp : " + str(e))



