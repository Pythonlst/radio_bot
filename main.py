# капаем библиотеки
import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, Update


class Bot:
    def __init__(self):
        # настройка бота
        application = Application.builder().token('7098727755:AAHOKBBBIgYnudjOmHeu4_7RzkE4prgVkJs').build()

        application.add_handler(CallbackQueryHandler(self.open_site))

        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help))
        application.add_handler(CommandHandler("close", self.close_keyboard))
        application.add_handler(CommandHandler("forum", self.open_site))

        text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo)
        application.add_handler(text_handler)

        # создание клавы
        btn_keyboard = [
            ['/start', '/help'], ['/close', '/forum']
        ]
        self.markup_btns = ReplyKeyboardMarkup(btn_keyboard, one_time_keyboard=False, resize_keyboard=True)

        # создание inline клавы
        inline_keyboard = [
            [InlineKeyboardButton('форум радиоэлектроников', url='https://go-radio.ru/start.html')]
                           ]
        self.url_btns = InlineKeyboardMarkup(inline_keyboard)

        # ковальски? - прости, сам не знаю, для показа инфы
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
        )
        logger = logging.getLogger(__name__)

        #включение основного цикла
        application.run_polling()

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
            "Ok",
            reply_markup=ReplyKeyboardRemove()
        )

    async def open_site(self, update, context):
        query = update.callback_query
        await update.message.reply_text("сайты для ознакомления с темой:", reply_markup=self.url_btns)







# врубаем все
if __name__ == '__main__':
    Bot()
