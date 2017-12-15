# Rock Paper Scissors
Wanna play Rock Paper scissors online and challenge yourself ? WELCOME this is your page :)

## Some important tip :
1 - Python must be installed on your PC .

2- I used telepot freamwork for this project you can see installation it in this link -- > https://github.com/nickoala/telepot .

3- I recommend you to use PyCharm as a IDE .

4- Also you need a server and mysql on it to run this code you can do it offline with WampServer ->

## Code 
### Libraries
```python
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import mysql.connector
from mysql.connector import Error
import logging
```

### Logging System
One of the most important things you must do as a programmer is having log of all the event occured in your app so : 
```python
# create a file handler for saving logs
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('events.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info('App started ...')
```
### Game Logic
In this level we must define a function that contain the rock paper scissors game logic 
```python
# Rock = 1, Paper = 2, Scissors = 3

def game_result(first,last):
    if first == "1":
        if last == "2":
            return -1
        elif last == "3":
            return 1
        else:
            return 0
    if first == "2":
        if last == "1":
            return 1
        elif last == "3":
            return -1
        else:
            return 0
    if first == "3":
        if last == "1":
            return -1
        elif last == "2":
            return 1
        else:
            return 0
```
## DataBase
you must have a mysql database and a username and a ** table named players **

here is an example use of database 
```python
conn = mysql.connector.connect(host='localhost',
                                       database='DataBase',
                                       user='DataBase',
                                       password='DataBase-Password ')
cur = conn.cursor()
cur.execute("SELECT * FROM players")
row = cur.fetchall()
cur.close()
conn.close()
```	
#### Table : 
Your Table must has this columns : 
					   
id   -    name     -     chat_id     -      score 

