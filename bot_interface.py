import os
import re

import requests
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType

nl = '\n' # New line for f-strings
VK_TOKEN = os.getenv('VK_TOKEN')
session = vk_api.VkApi(token=VK_TOKEN)


def send_message(user_id: int, message: str, keyboard: VkKeyboard|None=None, carousel=None):
    """
    Send message to user_id
    """
    payload = {
        'user_id': user_id,
        'message': message,
        'random_id': 0
    }

    if keyboard is not None:
        payload['keyboard'] = keyboard.get_keyboard()
    payload['template'] = {
    "type": "carousel",
    "elements": [
    {
        "title": "Title",
        "description": "Description",
        "action": {
                "type": "open_link",
                "link": "https://vk.com"
        },
        "photo_id": "-109837093_457242809",
        "buttons": [{
                "action": {
                        "type": "text",
                        "label": "Label"
                }
        }]
}
]
}

    session.method('messages.send', payload)


def begin(user_id: int) -> None:
    """
    When user press button 'начать'.
    """
    keyboard = VkKeyboard()
    keyboard.add_button('проверить', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    btns = ('весь список', 'добавить', 'удалить')
    btn_colors = (VkKeyboardColor.SECONDARY, VkKeyboardColor.POSITIVE, VkKeyboardColor.NEGATIVE)
    for btn, color in zip(btns, btn_colors):
        keyboard.add_button(btn, color)
    send_message(user_id, 'Выбери что хочешь сделать', keyboard)


def get_all_products(user_id: int) -> None:
    """
    Send all products from file to user.
    """
    list_of_products = []
    with open('list_of_products.txt', 'r') as f:
        for link in f:
            link = link.rstrip('\n')
            list_of_products.append(link)
    send_message(user_id, f'{nl.join(list_of_products)}')


def add(user_id: int, text: str) -> None:
    """
    Add new product to file if it`s not there.
    """
    if match := re.search('https.*', text):
        with open('list_of_products.txt', 'a+') as f:
            f.seek(0)
            data = f.read()
            if data.find(match[0]) >= 0:
                send_message(user_id, f'{match[0]} уже есть в списке!')
            else:
                f.write(f'{match[0]}\n')
                send_message(user_id, f'{match[0]} успешно добавлен!')
    else:
        send_message(user_id, 'Чтобы добавить какой-либо товар напишите слово "добавить" и ссылку на товар')


def delete(user_id: int, text: str) -> None:
    """
    Delete product from file.
    """
    if match := re.search('https.*', text):
        with open('list_of_products.txt', 'r') as f:
            data = f.read()
        with open('list_of_products.txt', 'w') as f:
            new_data = data.replace(f'{match[0]}\n', '')
            new_data = new_data.replace(f'{match[0]}', '')
            f.write(new_data)
        send_message(user_id, f'{match[0]} успешно удален!')
    else:
        send_message(user_id, 'Чтобы удалить какой-либо товар напишите слово "удалить" и ссылку на товар из списка')


def check_now(user_id: int) -> None:
    """
    Check discount products from file.
    """
    list_of_discount_products = []
    with open('list_of_products.txt', 'r') as f:
        for link in f:
            link = link.rstrip('\n')
            response =  requests.get(link)
            discount = response.content.find(b'abs_discount')
            if discount >=0:
                list_of_discount_products.append(link)
    send_message(user_id, f'{nl.join(list_of_discount_products)} - беги скорее покупай')


def listen() -> None:
    """
    Start bot.
    """
    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text = event.text.lower()
            user_id = event.user_id
            if 'начать' in text:
               begin(user_id)
            if text == 'весь список':
                get_all_products(user_id)
            if text == 'проверить':
                check_now(user_id)
            if 'добавить' in text:
                add(user_id, text)
            if 'удалить' in text:
                delete(user_id, text)