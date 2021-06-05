

import pandas
import telebot
# import aioschedule as schedule
# import parser
 
class KivanoBot:
    help_text = '''
    /categories** выдать названия всех категорий, которые вы спарсили.
    /categories** {название категории} выдать товары этой категории. (название и ссылку)
    /product** {название продукта} выдать информацию о данном товаре. (название, название категории, ссылка)
    '''
    __data = pandas.read_csv('lab_parser.csv')
    categoriesset = set(__data.categories.to_list())
 
    def show(self, args):
        if len(args) == 0:
            return '\n'.join(self.categoriesset)
        else:
            if args == "Компьютеры":
                categories = (f"Продукт {args}")

 
            if (categories) not in self.categoriesset:
                return f'Такой категории: {args} не существует'
            else:
                prod = self.__data[self.__data.products == categories]
                prod = prod[['product_names', 'category']][1:11].to_string()
                print(prod)
                return prod
 

TOKEN = '1790983874:AAFsvwDh0ktO6Dh5_EnpsT4QpzUB_n_gevM'
 
bot = telebot.TeleBot(TOKEN)
kbot= KivanoBot()
 
@bot.message_handler(commands=['start', 'help'])
def show(message):
    bot.send_message(message.chat.id, kbot.help_text)
 
@bot.message_handler(commands=['fractions'])
def fractions(message):
    args = message.text[11:]
    bot.send_message(message.chat.id, kbot.show(args))


 
if __name__ == '__main__':
    bot.polling()