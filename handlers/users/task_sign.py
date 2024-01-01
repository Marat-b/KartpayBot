from aiogram.types import CallbackQuery

from data.config import MANAGERS, f_application_total, f_executor
from data.enquiry import Enquiry
from data.users import Users
from loader import dp, bot
from utils.format_enquiry import format_enquiry_for_paying


@dp.callback_query_handler(regexp="^task_sign\&.+")
async def task_sign(call: CallbackQuery):
    # await call.answer(cache_time = 60)
    # print("task_sign id = {}".format(call.from_user.id))
    user_id = call.from_user.id
    # user_id = "2454"  # for test only
    enquiry = Enquiry(user_id)
    entities = enquiry.get_entities_for_paying("УПД подписан", "Нет")
    bonus = 0
    count_entities = 0
    for entity in entities:
        bonus += int(entity[f_application_total])
        count_entities += 1
    # print("entities = {}".format(entities))
    # print("bonus = {}".format(bonus))
    summary_message = (
        "Исполнитель <b>{}</b> запросил выплату в размере <b>{}</b> рублей по следующим заявкам, "
        "в количестве <b>{}</b> шт."
    ).format(Users.get_user_fio(entities[0][f_executor]), bonus, count_entities)

    for manager in MANAGERS:
        await bot.send_message(manager, summary_message)
        for entity in entities:
            # print(format_enquiry_for_paying(entity))
            await bot.send_message(manager, format_enquiry_for_paying(entity))

    await call.answer(
        "Запрос на выплату в размере {} рублей по заявкам, в количестве {} шт. - отправлен".format(
            bonus, count_entities
        ),
        show_alert=True,
    )  # , cache_time = 120
