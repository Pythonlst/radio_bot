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

        self.application.add_handler(CommandHandler("set_timer", self.set_timer))
        self.application.add_handler(CommandHandler("unset_timer", self.unset))

        text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo)
        self.application.add_handler(text_handler)

        # создание главной клавы
        self.btn_keyboard = [
            ['/help', '/unset_timer'], ['/close', '/forum', '/random_image']
        ]
        self.markup_btns = ReplyKeyboardMarkup(self.btn_keyboard, one_time_keyboard=False, resize_keyboard=True)

        # создание inline клавы
        inline_keyboard = [
            [InlineKeyboardButton('форум радиоэлектроников', url='https://go-radio.ru/start.html')],
            [InlineKeyboardButton('форум с расширенным количеством схем', url='https://radioskot.ru')],
            [InlineKeyboardButton('канал про проектирование на ардуино Alex Giver', url='https://www.youtube.com/@AlexGyverShow')],
            [InlineKeyboardButton('канал про электронику HI-DEV', url='https://www.youtube.com/channel/UCY6A_tZAikULMr46WlfntRw')]
                           ]
        self.url_btns = InlineKeyboardMarkup(inline_keyboard)

        # ковальски? - прости, сам не знаю, смотри инфу
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
        )
        logger = logging.getLogger(__name__)

        #включение основного цикла
        self.application.run_polling()

    async def start(self, update, context):
        self.user = update.effective_user
        insert((update.message.chat.id, update.message.chat.first_name, update.message.chat.username,
                update.message.date, update.message.from_user.language_code, update.message.text), table='users')
        await update.message.reply_html(
            rf"Привет {self.user.mention_html()}! я бот созданный для помощи в изучении радиоэлектроники, но я пока примитивен)",
            reply_markup=self.markup_btns)

    async def echo(self, update, context):
        insert((update.message.chat.id, update.message.chat.first_name, update.message.chat.username,
                update.message.date, update.message.from_user.language_code, update.message.text), table='users')
        await update.message.reply_text('я получил - ' + update.message.text)

    async def help(self, update, context):
        await update.message.reply_text('/set_timer мин час - ставит таймер, 2 аргумента обязательны')

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
        print(update.message.chat.id)
        await update.message.reply_text("лови картинку:")
        await context.bot.send_photo(update.message.chat.id, url)

    def remove_job_if_exists(self, name, context):
        """Удаляем задачу по имени.
        Возвращаем True если задача была успешно удалена."""
        current_jobs = context.job_queue.get_jobs_by_name(name)
        if not current_jobs:
            return False
        for job in current_jobs:
            job.schedule_removal()
        return True

    async def task(self, context, text='проснись!'):
        """Выводит сообщение"""
        await context.bot.send_message(context.job.chat_id, text=text)

    async def set_timer(self, update, context):
        info = update.message.text.split()[1:]
        time = 60 * int(info[0]) + int(info[1]) * 3600
        chat_id = update.effective_message.chat_id
        job_removed = self.remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(self.task, time, chat_id=chat_id, name=str(chat_id), data=time)


        text = f'таймер поставлен'
        if job_removed:
            text += ' Старая задача удалена.'
        await update.effective_message.reply_text(text)

    async def unset(self, update, context):
        """Удаляет задачу, если пользователь передумал"""
        chat_id = update.message.chat_id
        job_removed = self.remove_job_if_exists(str(chat_id), context)
        text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
        await update.message.reply_text(text)

#    async def set_timer(self, update, context):
#        timers = insert((update.message.chat.id, update.message.chat.first_name, update.message.chat.username,
#                update.message.date, update.message.from_user.language_code, update.message.text), read_timer=True)
#        await update.message.reply_text(timers)
#        await update.message.reply_text("точка таймера создана")


# врубаем все
if __name__ == '__main__':
    Bot()
