# from logging import exception

from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter, CommandObject
from aiogram.fsm.context import FSMContext

from aiogram import types
from aiogram import Router, F
from aiogram.types import Message
from calcs import *
from random import choice
from string import ascii_letters


router = Router()

users_dict = {}

def gen_letter_id(l=16):
    """
    вероятность коллизии маленькая
    16 ^ 52 вариантов как сгенерировать
    """
    letter_id = ''.join(choice(ascii_letters) for _ in range(l))
    return letter_id


class ProfileForm(StatesGroup):
    weight = State()
    height = State()
    activity_level = State()
    city = State()


@router.message(Command("start"))
async def set_profile(message: Message):
    await message.answer("use /set_profile")


@router.message(StateFilter(None), Command("set_profile"))
async def set_profile(message: Message, state: FSMContext):
    await message.answer("Hello! Let's register your data")
    await message.answer("What's your weight (in kg)?")
    await state.set_state(ProfileForm.weight)


@router.message(ProfileForm.weight)
async def process_weight(message: Message, state: FSMContext):
    async def validate_weight(wei):
        try:
            wei = int(wei)
            if wei <= 0 or wei > 300:
                message.answer("Введите вес числом в кг")
                return None
        except Exception:
            message.answer("Введите вес числом в кг")
            return None
        return wei

    wei = await validate_weight(message.text)
    if wei is None:
        return
    await state.update_data(weight= wei)
    await message.answer("What's your height (in cm)?")
    await state.set_state(ProfileForm.height)


@router.message(ProfileForm.height)
async def process_height(message: Message, state: FSMContext):
    async def validate_height(hei):
        try:
            hei = int(hei)
            if hei <= 0 or hei > 300:
                message.answer("Введите рост числом в сантиметрах")
        except Exception:
            return None
        return hei

    hei = await validate_height(message.text)
    if hei is None:
        return

    await state.update_data(height=hei)
    curr_text = "Do you have physical activity every day? \nGym, sports, walk and home work included. \nType 'yes' or 'no' "
    await message.answer(curr_text)
    await state.set_state(ProfileForm.activity_level)


@router.message(ProfileForm.activity_level)
async def process_activity_level(message: Message, state: FSMContext):
    async def validate_act(val):
        val = val.lower()
        if val == "yes" or val == "y":
            return 1
        if val == "no" or val == "n":
            return 0
        else:
            await message.answer("Нужные форматы ответа: 'yes', 'y', 'no', 'n'")
            return None

    act = await validate_act(message.text)

    if act is None:
        return

    await state.update_data(activity_level=act)
    await message.answer("In which city you are now?")
    await state.set_state(ProfileForm.city)


@router.message(ProfileForm.city)
async def process_city_living(message: Message, state: FSMContext):
    async def validate_city(val):
        val = val.capitalize()
        if val == "":
            return None
        return val
    await state.update_data(city=validate_city(message.text))

    city = await validate_city(message.text)

    if city is None:
        return

    new_user = get_new_user_form()
    data = await state.get_data()
    new_user["weight"] = data.get("weight")
    new_user["height"] = data.get("height")
    new_user["everyday_activity"] = data.get("activity_level")
    new_user["city"] = data.get("city")
    print(new_user["weight"])
    new_user["water_goal"] = calc_base_water_norm(new_user["weight"], new_user["everyday_activity"])
    new_user["calorie_goal"] = calc_calorie_norm(new_user["weight"], new_user["height"])
    user_id = gen_letter_id()
    users_dict[user_id] = new_user  # in bot.py
    print(users_dict)

    await message.answer("Умничка")
    await message.answer(f"Your id: {user_id}")
    await message.answer("/check_progress is accessable")
    await message.answer(f"/check_progress {user_id}")
    await state.clear()


def get_new_user_form():
    new_user = {
        "weight": None,
        "height": None,
        "everyday_activity": None,
        "city": None,
        "water_goal": None,
        "calorie_goal": None,
        "logged_water": 0,
        "logged_calories": 0,
        "burned_calories": 0,
    }
    return new_user


@router.message(Command("check_progress"))
async def check_progress(message: Message, command: CommandObject):
    if command.args is None:
        await message.answer(
            "Ошибка: ты не передал(a) свой id"
        )
        return
    try:
        user_id = command.args  # .split(" ", maxsplit=1)
        print(user_id)
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/check_progress <your_id>"
        )
        return

    water_goal = users_dict[user_id]["water_goal"]
    calo_goal =  users_dict[user_id]["calorie_goal"]
    curr_text = f"""Your progress:
    \nВода: 
    \t0 мл из {water_goal}
    \nКаллории:
    \t0 ккал из {calo_goal}
    """
    await message.answer(curr_text)


