import pandas
import telebot
 
class KivanoBot:
    help_text = '''
    /categories** выдать названия всех категорий, которые вы спарсили.
    /categories** {название категории} выдать товары этой категории. (название и ссылку)
    /product** {название продукта} выдать информацию о данном товаре. (название, название категории, ссылка)
    '''
    __data = pandas.read_csv('products.csv')
    categoriesset = set(__data.category.to_list())
    # productset = set(__data.product_name.to_list())
 
    def show(self, args):
        if len(args) == 0:
            return '\n'.join(self.categoriesset).replace('category\n', '')
        else: 
            categories = f'{args}'
            if (categories) not in self.categoriesset:
                return f'Такой категории: {args} не существует'
            else:
                prod = self.__data[self.__data.category == categories]
                prod = prod[['product_name', 'product_link']][1:11].to_string()
                return prod

    def show_product(self, args):
        product = args
        if (product) not in self.__data.product_name:
            return f'Такого продукта: {args} не существует'
        else:
            prod = self.__data[self.__data.product_name == product]
            prod = prod[['product_name', 'category', 'product_link']][1:3].to_string()
            return prod
 

TOKEN = '1790983874:AAFsvwDh0ktO6Dh5_EnpsT4QpzUB_n_gevM'
 
bot = telebot.TeleBot(TOKEN)
kbot= KivanoBot()
 
@bot.message_handler(commands=['start', 'help'])
def show(message):
    bot.send_message(message.chat.id, kbot.help_text)
 
@bot.message_handler(commands=['categories'])
def categories(message):
    args = message.text[12:]
    bot.send_message(message.chat.id, kbot.show(args))

@bot.message_handler(commands=['product'])
def product(message):
    args = message.text[8:]
    bot.send_message(message.chat.id, kbot.show_product(args))



 
if __name__ == '__main__':
    bot.polling()
