import random
import os
import sys
import time

import requests
import bs4
import traceback
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import vk
import colorama
from colorama import Fore, Back, Style

colorama.init()

# globals
logging = False
session = requests.Session()
token = ""
vk_session = vk_api.VkApi(token=token)
ses = vk.Session(access_token=token)
api = vk.API(ses)
longpoll = VkLongPoll(vk_session)


def get_members(group_id='shut04ka_minut04ka'):
    return list(map(str, api.groups.getMembers(group_id=group_id, v="5.92")['items']))


class VkBot:

    def __init__(self, user_id):
        # print(' создан экземпляр')
        self.user_id = user_id
        self.username = self.get_user_name(user_id)
        self.commands = [{'привет', 'здарова', 'ку', 'хай', 'прив'},
                         set(),
                         {'пока', 'прощай', 'досвидания', 'покедово', 'пок'},
                         {'расписание', 'рп', 'уроки'},
                         {'кто'}]

    def get_user_name(self, user_id=False):
        # Возвращает ('Имя', 'Фамилия')
        if user_id is False:
            user_id = self.user_id
        request = requests.get("https://vk.com/id" + str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")
        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])
        return tuple(user_name.split())

    @staticmethod
    def _clean_all_tag_from_str(string_line):
        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True
        return result

    def write_msg(self, message, attachment=False):
        mes = {'user_id': self.user_id, 'message': message, 'random_id': random.randint(0, 2048)}
        if attachment:
            mes['attachment'] = f"photo{attachment['owner_id']}_{attachment['id']}"
        vk_session.method('messages.send', mes)

    def new_message(self, message):
        print(Fore.BLUE + f'[who]{" ".join(self.get_user_name())}')
        print(f'[inp]{message}')
        message1 = message
        message = {message.lower()}
        if message & self.commands[0]:
            mes = random.choice([f'Привет,  {self.get_user_name()[0]}',
                                 "Ну здарова пешка Переваловой",
                                 'Ну привет, жалкий кусок мяса',
                                 'УНИ4ТОЖИb 4EJl0ВЕKOВ',
                                 f'Мы вас ждали и вы пришли! Привет {self.get_user_name()[0]}'])
        # Пока
        elif message & self.commands[2]:
            mes = random.choice(["Печально что мы прощаемся(((",
                                 "Пиши еще, я всегда жду твоего 'расписание'",
                                 'Ну нормально же общались((',
                                 f'Чикибампока, {self.username[0]}',
                                 f"Ну пока, {self.username[0]}"])
        # Расписание
        elif message & self.commands[3]:
            upload = vk_api.VkUpload(vk_session)
            try:
                photo = upload.photo_messages('rp.jpg')[0]
                mes = "Ваш список мучений:", photo
            except FileNotFoundError:
                mes = 'Соре, но в меня не загрузили расписание, напиши админам если не сложно :З'
        # Кто
        elif {message1.split()[0].lower()} & self.commands[4]:
            message1.replace('?', '', message1.count('?'))
            iss = ' '.join(message1.split()[1:])
            whoid = random.choice(get_members())
            who = f'[id{whoid}|{" ".join(self.get_user_name(whoid))}]'
            start = random.choice(['Ничего себе, оказывается ', 'Определенно ', 'Очевидно, что '])
            mes = f'{start}{who} {iss}'
        else:
            mes = random.choice(
                ['каво? /', 'не панимау /', 'скажи /', 'не понял', 'Соре, отвечать на это меня не научили('])

        if mes.__class__.__name__ == 'tuple':
            print(Fore.GREEN + f'[bot]{mes[0]}')
            self.write_msg(mes[0], mes[1])
        else:
            self.write_msg(mes)
            print(Fore.GREEN + f'[bot]{mes}')


print(Fore.LIGHTRED_EX + "[server started]")
print(f'Папка логов: {os.getcwd()}')
print('Файл с расписанием кидайте в папку с прогой, должен называться rp.jpg')

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            try:
                bot = VkBot(event.user_id)
                if event.text == '/'.strip():
                    bot.write_msg('Доступные комманды: привет, пока, расписание, кто *текст*')
                elif event.text.startswith('/'):
                    bot.new_message(event.text[1:])
                else:
                    bot.new_message(event.text)
            except Exception:
                print(Fore.RED + '[ERROR]')
                f = open('errors.log', 'a')
                f.write('{}'.format(traceback.format_exc()))
                mon, day, hour, min, sec = time.localtime()[1:6]
                f.write(f'{sec}:{min}:{hour} {mon}.{day}.2019\n')
                f.close()
# TODO: Написать помощь вместо /
