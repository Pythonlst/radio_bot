# капаем библиотеки
import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, request
from random_picture import take_image
from csv import insert


class Bot:
    def __init__(self):
        # объявляем переменные чтобы пипка не ругалась
        self.user = None
        # настройка бота
        self.application = Application.builder().token('7098727755:AAHOKBBBIgYnudjOmHeu4_7RzkE4prgVkJs').build()

        self.application.add_handler(CallbackQueryHandler(self.open_site))

        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help))
        self.application.add_handler(CommandHandler("close", self.close_keyboard))
        self.application.add_handler(CommandHandler("open", self.open_keyboard))
        self.application.add_handler(CommandHandler("forum", self.open_site))
        self.application.add_handler(CommandHandler("random_image", self.random_image))

        text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo)
        self.application.add_handler(text_handler)

        # создание главной клавы
        self.btn_keyboard = [
            ['/help'], ['/close', '/forum', '/random_image']
        ]
        self.markup_btns = ReplyKeyboardMarkup(self.btn_keyboard, one_time_keyboard=False, resize_keyboard=True)

        # создание inline клавы
        inline_keyboard = [
            [InlineKeyboardButton('форум радиоэлектроников', url='https://go-radio.ru/start.html')],
            [InlineKeyboardButton('канал про проектирование на ардуино Alex Giver', url='https://www.youtube.com/@AlexGyverShow')],
            [InlineKeyboardButton('канал про электронику HI-DEV', url='https://www.youtube.com/channel/UCY6A_tZAikULMr46WlfntRw')]
                           ]
        self.url_btns = InlineKeyboardMarkup(inline_keyboard)

        # ковальски? - прости, сам не знаю, для показа инфы
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
        )
        logger = logging.getLogger(__name__)

        #включение основного цикла
        self.application.run_polling()

    async def start(self, update, context):
        self.user = update.effective_user
        await update.message.reply_html(
            rf"Привет {self.user.mention_html()}! я бот созданный для помощи в изучении радиоэлектроники, но я пока примитивен)",
            reply_markup=self.markup_btns)

    async def echo(self, update, context):
        await update.message.reply_text('я получил - ' + update.message.text)

    async def help(self, update, context):
        await update.message.reply_text('тут будет инструкция к командам)')

    async def close_keyboard(self, update, context):
        await update.message.reply_text(
            "закрытие меню",
            reply_markup=ReplyKeyboardMarkup([['/open']], one_time_keyboard=False, resize_keyboard=True)
        )

    async def open_keyboard(self, update, context):
        await update.message.reply_text(
            "открытие меню",
            reply_markup=ReplyKeyboardMarkup(self.btn_keyboard, one_time_keyboard=False, resize_keyboard=True)
        )

    async def open_site(self, update, context):
        query = update.callback_query
        await update.message.reply_text("сайты для ознакомления с темой:", reply_markup=self.url_btns)

    async def random_image(self, update, context):
        url = take_image('image')
        print(update)
        print(context)
        print(update.message.chat.id)
        await context.bot.send_photo(update.message.chat.id, url)
        #await update.message.reply_text(
        #    "меме"
        #)




# врубаем все
if __name__ == '__main__':
    Bot()
