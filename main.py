from AlgoritmGame import AlgoritmGame 
from AlgoritmGameFriend import AlgoritmGameFriend 
import matplotlib.pyplot as plt
import telebot
import random
import pandas as pd
from telebot import types
import psycopg2
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Параметры подключения к базе данных
dbname = 'telegrambot'  # имя вашей базы данных
user = 'artem'       # ваше имя пользователя в PostgreSQL
password = '1234'   # ваш пароль
host = 'localhost'      # адрес сервера базы данных, обычно localhost

# Строка подключения
conn_string = f"dbname='{dbname}' user='{user}' password='{password}' host='{host}'"


bot = telebot.TeleBot('7116510541:AAEG8bAOOthupEDUteJWjTkP3lkQ7BVlgtQ')
@bot.message_handler(commands=['start'])
def main(message):
    register_player(message.from_user.username, message.from_user.id)
    markup = types.InlineKeyboardMarkup()
    button_rating = types.InlineKeyboardButton('Рейтинг игроков', callback_data='rating')
    markup.add(button_rating)
    button1 = types.InlineKeyboardButton('Играть с ботом', callback_data = 'play_with_bot')
    button2 = types.InlineKeyboardButton('Играть с другом', callback_data = 'play_with_friend')
    button3 = types.InlineKeyboardButton('Поделиться', switch_inline_query="Поделитесь этим ботом с друзьями!")
    button4 = types.InlineKeyboardButton('Сбросить текущую игру с ботом', callback_data = 'restart_play_with_bot')
    markup.add(button1)
    markup.add(button4)
    markup.add(button2)
    markup.add(button3)
    text = f'Привет, капитан {message.from_user.first_name} {message.from_user.last_name}!'
    photo = open('capitan.jpg', 'rb')  
    bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup)

games = {}  
game_sessions = {}

@bot.callback_query_handler(func=lambda call: call.data == 'rating')
def query_rating(call):
    show_rating(call.message)

@bot.callback_query_handler(func=lambda callback: callback.data == 'play_with_friend')
def handle_play_with_friend(callback):
    chat_id = callback.message.chat.id 
    if chat_id in games:
        del games[chat_id] 
    chat_id = callback.message.chat.id 
    unique_id = 'uniq_id' + str(random.randint(1, 100))
    if unique_id in game_sessions:
        del game_sessions[unique_id]   
    
    game_sessions[unique_id] = {
        'player_1': callback.from_user.id,
        'player_2': None,
        'game_state': 'waiting_for_player_2',
        'player1': AlgoritmGameFriend(), 'player2': AlgoritmGameFriend(),
        'game_id': unique_id,
        'current_move': callback.from_user.id
    }
    bot.send_message(chat_id=chat_id, text = 'Отправьте этот id другу для начала игры (подключение по команде: /join id)')
    bot.send_message(chat_id, unique_id)
    bot.answer_callback_query(callback.id)
      

@bot.message_handler(commands=['join'])
def join_game(message):
    game_id = message.text.split()[1] if len(message.text.split()) > 1 else None
    
    if game_id and game_id in game_sessions:
        session = game_sessions[game_id]
        if session['player_2'] is None:
            session['player_2'] = message.from_user.id
            session['game_state'] = 'ready_to_start'
            bot.send_message(session['player_1'], "Ваш друг присоединился к игре! Начинаем...")
            bot.send_message(session['player_2'], "Вы присоединились к игре!")
            send_field_update_friend(session['player_1'])
            send_field_update_friend(session['player_2'])
        else:
            bot.send_message(message.chat.id, "Извините, эта игровая сессия уже заполнена.")
    else:
        bot.send_message(message.chat.id, "Извините, невозможно найти игру. Проверьте свою ссылку.")


@bot.callback_query_handler(func=lambda callback: callback.data == 'play_with_bot')
def handle_play_with_bot(callback):
    chat_id = callback.message.chat.id
    if chat_id not in games:
        games[chat_id] = AlgoritmGame()  # Создание игры с ботом
    bot.send_message(chat_id, 'Игра c ботом началась!')
    send_field_update(chat_id)

@bot.callback_query_handler(func=lambda callback: callback.data == 'restart_play_with_bot')
def handle_restart_play_with_bot(callback):
    chat_id = callback.message.chat.id
    if chat_id in games:
        del games[chat_id]  
    games[chat_id] = AlgoritmGame()  # Создаем новую игру с ботом
    bot.send_message(chat_id, 'Новая игра с ботом началась!')
    send_field_update(chat_id)
    bot.answer_callback_query(callback.id)

def create_table_image(df):
    #  объект фигуры (fig) и объект оси (ax) для построения графика
    fig, ax = plt.subplots(figsize=(3, 3.7))  
    #  отключаес оси
    ax.axis('off')
    the_table = ax.table(cellText=df.values,
                         colLabels=df.columns,
                         rowLabels=df.index,
                         cellLoc='center', # выравнивает текст в ячейках по центру
                         loc='center', # помещает таблицу в центр фигуры
                         cellColours=None)  
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(10) 
    plt.savefig('table.png')
    plt.close(fig)



def send_field_update(chat_id):
    player_game = games[chat_id]
    bot.send_message(chat_id, "Ваше поле:")
    get_display_player_field = ['*'] * 10

    for i in range(0, 10):
            get_display_player_field[i] = ['*'] * 10

    for i in range(1, 11):
        for j in range(1, 11):
                get_display_player_field[i-1][j-1] = player_game.display_player_field()[i][j]
    
    df_copy_player_field  = pd.DataFrame(get_display_player_field, index=range(1, 11), columns=range(1, 11))
    create_table_image(df_copy_player_field)
    bot.send_photo(chat_id, photo=open('table.png', 'rb'))
    get_display_bot_field = ['*'] * 10

    for i in range(0, 10):
            get_display_bot_field[i] = ['*'] * 10

    for i in range(1, 11):
        for j in range(1, 11):
                if(player_game.display_enemy_field()[i][j] == '■'):
                      get_display_bot_field[i-1][j-1] = '-'
                else: get_display_bot_field[i-1][j-1] = player_game.display_enemy_field()[i][j]
    
    df_copy_bot_field = pd.DataFrame(get_display_bot_field, index=range(1, 11), columns=range(1, 11))
    create_table_image(df_copy_bot_field)

    bot.send_message(chat_id, "Поле бота:")
    bot.send_photo(chat_id, photo=open('table.png', 'rb'))  # Поле бота с замаскированными кораблями




@bot.message_handler(func=lambda message: message.chat.id in games)
def handle_move(message):
    chat_id = message.chat.id
    player_game = games[chat_id]
    try:
        x, y = map(int, message.text.split())
        if (x >= 1 and x <= 10) and (y >= 1 and y <= 10):
            # Передаем в make_move поле бота, чтобы игрок атаковал бота
            response = player_game.make_move(player_game.bot_field, x, y)
            bot.send_message(chat_id, response)
            send_field_update(chat_id)
            
            if player_game.check_victory(player_game.bot_field):
                bot.send_message(chat_id, "Вы победили! Игра окончена.")
                del games[chat_id]
            elif(player_game.bot_field[x][y] == 'X' or player_game.bot_field[x][y] == 'S'):
                bot.send_message(chat_id, "Сделайте ещё ход")
                return
            else:
                bot_move(chat_id)
        else: bot.send_message(chat_id, "Введите значения от 1 до 10")
    except ValueError: 
        bot.send_message(chat_id, "Введите координаты выстрела (x y). Например: 2 1")
   

def bot_move(chat_id):
    bot_game = games[chat_id]
    player_game = games[chat_id]
    x, y = bot_game.get_bot_next_move()

    response = bot_game.make_move(player_game.player_field, x, y)
    bot.send_message(chat_id, f"Ход бота: {x} {y}\n{response}")
    send_field_update(chat_id)  # Отправляем обновленное поле игрока и бота
    if bot_game.check_victory(player_game.player_field):
        bot.send_message(chat_id, "Бот победил! Игра окончена.")
        del games[chat_id]
    elif(player_game.player_field[x][y] == 'X' or player_game.player_field[x][y] == 'S'):
        bot.send_message(chat_id, "Бот делает ещё ход")
        bot_move(chat_id)
     
####### friend

#функция ищет, участвует ли данный чат 
        #(пользователь) в какой-либо из текущих игровых сессий
def get_game_id_by_chat_id(chat_id):
    for game_id, session in game_sessions.items():
        if chat_id in (session['player_1'], session['player_2']):
            return game_id
    return None

def send_field_update_friend(chat_id):
    get_game_id = get_game_id_by_chat_id(chat_id)
    session_tmp = game_sessions[get_game_id]
    if chat_id == session_tmp['player_1']:
        player_game_player_1 = game_sessions[get_game_id]['player1']
        player_game_player_2 = game_sessions[get_game_id]['player2']
        bot.send_message(chat_id, "Ваше поле:")
        get_display_player1_field = ['*'] * 10

        for i in range(0, 10):
                get_display_player1_field[i] = ['*'] * 10

        for i in range(1, 11):
            for j in range(1, 11):
                    get_display_player1_field[i-1][j-1] = player_game_player_1.display_player1_field()[i][j]
        
        df_copy_player1_field  = pd.DataFrame(get_display_player1_field, index=range(1, 11), columns=range(1, 11))
        create_table_image(df_copy_player1_field)
        bot.send_photo(chat_id, photo=open('table.png', 'rb'))
        get_display_player2_field = ['*'] * 10

        for i in range(0, 10):
                get_display_player2_field[i] = ['*'] * 10

        for i in range(1, 11):
            for j in range(1, 11):
                    if(player_game_player_2.display_player2_field()[i][j] == '■'):
                        get_display_player2_field[i-1][j-1] = '-'
                    else: get_display_player2_field[i-1][j-1] = player_game_player_2.display_player2_field()[i][j]
                    
        df_copy_player2_field = pd.DataFrame(get_display_player2_field, index=range(1, 11), columns=range(1, 11))
        create_table_image(df_copy_player2_field)

        bot.send_message(chat_id, "Поле друга:")
        bot.send_photo(chat_id, photo=open('table.png', 'rb')) 
    if chat_id == session_tmp['player_2']:
        player_game_player_1 = game_sessions[get_game_id]['player1']
        player_game_player_2 = game_sessions[get_game_id]['player2']
        bot.send_message(chat_id, "Ваше поле:")
        get_display_player2_field = ['*'] * 10

        for i in range(0, 10):
                get_display_player2_field[i] = ['*'] * 10

        for i in range(1, 11):
            for j in range(1, 11):
                    get_display_player2_field[i-1][j-1] = player_game_player_2.display_player2_field()[i][j]
        
        df_copy_player2_field  = pd.DataFrame(get_display_player2_field, index=range(1, 11), columns=range(1, 11))
        create_table_image(df_copy_player2_field)
        bot.send_photo(chat_id, photo=open('table.png', 'rb'))
        get_display_player1_field = ['*'] * 10

        for i in range(0, 10):
                get_display_player1_field[i] = ['*'] * 10

        for i in range(1, 11):
            for j in range(1, 11):
                    if(player_game_player_1.display_player1_field()[i][j] == '■'):
                        get_display_player1_field[i-1][j-1] = '-'
                    else: get_display_player1_field[i-1][j-1] = player_game_player_1.display_player1_field()[i][j]
        df_copy_player1_field = pd.DataFrame(get_display_player1_field, index=range(1, 11), columns=range(1, 11))
        create_table_image(df_copy_player1_field)

        bot.send_message(chat_id, "Поле друга:")
        bot.send_photo(chat_id, photo=open('table.png', 'rb')) 


@bot.message_handler(func=lambda message: True)
def handle_move_players(message):
    chat_id = message.chat.id
    get_game_id = get_game_id_by_chat_id(chat_id)
    if get_game_id is None or get_game_id not in game_sessions:
        return
    session = game_sessions[get_game_id]

    if chat_id != session['current_move']:
        bot.send_message(chat_id, "Сейчас не ваш ход.")
        return

    player_game_player_1 = session['player1']
    player_game_player_2 = session['player2']

    if chat_id == game_sessions[get_game_id]['player_1']:
        current_player = player_game_player_1
        field_opponent = player_game_player_2.player2_field
    elif chat_id == game_sessions[get_game_id]['player_2']:
        current_player = player_game_player_2
        field_opponent = player_game_player_1.player1_field

    try:
        x, y = map(int, message.text.split())
        if (x >= 1 and x <= 10) and (y >= 1 and y <= 10):
            response = current_player.make_move(field_opponent, x, y)
            bot.send_message(chat_id, response)
            send_field_update_friend(chat_id)
            
            if current_player.check_victory(field_opponent):
                bot.send_message(chat_id, "Вы победили! Игра окончена.")
                opponent_chat_id = session['player_1'] if chat_id == session['player_2'] else session['player_2']
                send_field_update_friend(opponent_chat_id)
                bot.send_message(opponent_chat_id, "Вы проиграли :( Игра окончена.")
                del game_sessions[get_game_id]
            elif(field_opponent[x][y] == 'X' or field_opponent[x][y] == 'S'):
                bot.send_message(chat_id, "Сделайте ещё ход")
                opponent_chat_id = session['player_1'] if chat_id == session['player_2'] else session['player_2']
                send_field_update_friend(opponent_chat_id)
                bot.send_message(opponent_chat_id, "Вы пропускаете ход")
                return
            elif(field_opponent[x][y] == '*'):
                opponent_chat_id = session['player_1'] if chat_id == session['player_2'] else session['player_2']
                session['current_move'] = opponent_chat_id
                send_field_update_friend(opponent_chat_id)
                bot.send_message(opponent_chat_id, "Теперь ваш ход.")
                bot.send_message(chat_id, "Теперь ход друга.")
        else: bot.send_message(chat_id, "Введите значения от 1 до 10")
    except ValueError: 
        bot.send_message(chat_id, "Введите координаты выстрела (x y). Например: 2 1")

def get_rating():
    with psycopg2.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT username, wins, losses FROM players ORDER BY wins DESC LIMIT 15;")
            rating = cur.fetchall()
    return rating

def update_player_stats(player_id, won):
    try:
        with psycopg2.connect(conn_string) as conn:
            with conn.cursor() as cur:
                if won:
                    logging.info(f"Updating win count for player {player_id}.")
                    cur.execute("UPDATE players SET wins = wins + 1 WHERE telegram_id = %s", (player_id,))
                else:
                    logging.info(f"Updating loss count for player {player_id}.")
                    cur.execute("UPDATE players SET losses = losses + 1 WHERE telegram_id = %s", (player_id,))
                conn.commit()
                logging.info("Database update successful.")
    except Exception as e:
        logging.error(f"Error updating player stats: {e}")


def register_player(username, telegram_id):
    with psycopg2.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO players (username, telegram_id, wins, losses) 
                VALUES (%s, %s, 0, 0) 
                ON CONFLICT (telegram_id) DO NOTHING;
                """, (username, telegram_id))
            conn.commit()

@bot.message_handler(commands=['rating'])
def show_rating(message):
    rating = get_rating()
    response = "🏆 Рейтинг игроков:\n"
    for idx, (username, wins, losses) in enumerate(rating, start=1):
        response += f"{idx}. {username} - Побед: {wins}, Поражений: {losses}\n"
    bot.send_message(message.chat.id, response)
bot.polling(none_stop=True)