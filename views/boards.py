import telebot

main_board = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
main_board.row('Получить конфиг')
main_board.row('Создать дополнительный конфиг')
main_board.row('Гайд', 'VPN не работает!')

admin_board = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
admin_board.row('Получить конфиг')
admin_board.row('Создать дополнительный конфиг')
admin_board.row('Гайд', 'VPN не работает!', '/admin')
