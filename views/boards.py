import telebot

main_board = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
main_board.row('Получить конфиг', 'Статистика')