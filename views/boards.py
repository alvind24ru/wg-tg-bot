import telebot

main_board = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
main_board.row('Получить конфиг', 'Статистика')
main_board.row('Создать дополнительный конфиг')
main_board.row('VPN не работает!')

admin_board = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
admin_board.row('Получить конфиг', 'Статистика')
admin_board.row('Создать дополнительный конфиг')
admin_board.row('/admin')
