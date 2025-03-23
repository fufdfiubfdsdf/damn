import requests
import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, InlineKeyboardMarkup, InlineKeyboardButton

# Получаем токен из переменных окружения
TOKEN = "7741979722:AAEBzPjM4HqoTdNajwdv2plXvdraARgMbhQ"
YOOMONEY_WALLET = "4100118178122985"  # Укажи свой YooMoney кошелек
YOOMONEY_AMOUNT = "650"  # Укажи сумму оплаты

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
CURRENCY = "XTR"

@dp.message()
async def command_start_handler(message: Message):
    # Создаем ссылку на оплату через YooMoney
    yoomoney_payment_link = (
        f"https://yoomoney.ru/quickpay/confirm.xml?receiver={YOOMONEY_WALLET}"
        f"&sum={YOOMONEY_AMOUNT}&quickpay-form=shop&paymentType=AC"
    )

    # Создаем кнопки
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💫 Telegram Stars", callback_data="pay_stars")],
        [InlineKeyboardButton(text="💰 Pay with Card (YooMoney)", url=yoomoney_payment_link)]
    ])

    await message.answer("Monthly subscription\nВыберите способ оплаты:", reply_markup=keyboard)

@dp.callback_query()
async def handle_payment_callback(callback_query):
    if callback_query.data == "pay_stars":
        await bot.send_invoice(
            chat_id=callback_query.from_user.id,
            title="30-Day Subscription",
            description="Pay and get a link",
            payload="access_to_private",
            currency="XTR",
            prices=[LabeledPrice(label="XTR", amount=1)]
        )

@dp.pre_checkout_query()
async def pre_checkout_handler(event: PreCheckoutQuery):
    await event.answer(True)

@dp.message(F.successful_payment)
async def successful_payment(message: Message):
    link = await bot.create_chat_invite_link(-1002291268265, member_limit=1)
    await message.answer(f"Твоя ссылка: (Your link:)\n{link.invite_link}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
