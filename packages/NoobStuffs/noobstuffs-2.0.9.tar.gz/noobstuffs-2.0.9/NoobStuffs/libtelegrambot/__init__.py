from typing import BinaryIO

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder


class TelegramLogBot:
    def __init__(
        self,
        token: str,
        chat_id: int,
        parse_mode: ParseMode,
        disable_web_page_preview: bool,
    ):
        self.app = ApplicationBuilder().token(token).build()
        self.__chat_id = chat_id
        self.__parse_mode = parse_mode
        self.__disable_web_page_preview = disable_web_page_preview
        self.__buttons = []
        self.__button_index = -1

    def build_button(self, text: str, link: str, newline: bool = False):
        button = InlineKeyboardButton(text=text, url=link)
        if newline or len(self.__buttons) == 0:
            self.__button_index += 1
            self.__buttons.append([button])
        else:
            self.__buttons[self.__button_index].append(button)

    def reset_buttons(self):
        self.__button_index = -1
        self.__buttons.clear()

    async def log_msg(self, message: str, use_buttons: bool = False):
        reply_markup = InlineKeyboardMarkup(self.__buttons) if use_buttons else None
        await self.app.bot.send_message(
            text=message,
            chat_id=self.__chat_id,
            reply_markup=reply_markup,
            parse_mode=self.__parse_mode,
            disable_web_page_preview=self.__disable_web_page_preview,
        )

    async def log_img(
        self,
        image: BinaryIO,
        caption: str,
        filename: str,
        use_buttons: bool = False,
    ):
        reply_markup = InlineKeyboardMarkup(self.__buttons) if use_buttons else None
        await self.app.bot.send_photo(
            photo=image,
            chat_id=self.__chat_id,
            caption=caption,
            reply_markup=reply_markup,
            parse_mode=self.__parse_mode,
            filename=filename,
        )

    async def log_doc(
        self,
        document: BinaryIO,
        caption: str,
        filename: str,
        use_buttons: bool = False,
    ):
        reply_markup = InlineKeyboardMarkup(self.__buttons) if use_buttons else None
        await self.app.bot.send_document(
            document=document,
            chat_id=self.__chat_id,
            caption=caption,
            reply_markup=reply_markup,
            parse_mode=self.__parse_mode,
            filename=filename,
        )
