import random
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import vk
# --
# from commander.commander import Commander
from Bot import VkBot


def get_members(group_id='shut04ka_minut04ka'):
    return list(map(str, api.groups.getMembers(group_id=group_id, v="5.92")['items']))


def write_msg(user_id, message):
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})


def sentrp(user_id, picname):
    upload = vk_api.VkUpload(vk_session)
    photo = upload.photo_messages(picname)[0]
    vk_session.method('messages.send',
                      {'user_id': user_id, 'random_id': random.randint(0, 2048),
                       'attachment': f"photo{photo['owner_id']}_{photo['id']}"})


logging = False

session = requests.Session()
# API-ключ созданный ранее
token = "Не скажу"

# Авторизуемся как сообщество
vk_session = vk_api.VkApi(token=token)
ses = vk.Session(access_token=token)
api = vk.API(ses)
# vk_api.

# Работа с сообщениями
longpoll = VkLongPoll(vk_session)

# commander = Commander()
print("[server started]")
for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            bot = VkBot(event.user_id)
            text = f'Новое сообщение от {" ".join(bot.get_user_name(event.user_id))}'
            print(text)
            if logging:
                write_msg('225133650', text)
            if event.attachments:
                if event.attachments['attach1_type'] == 'photo':
                    photo_id = event.attachments['attach1_type'] + event.attachments['attach1']
                    print(photo_id)
            elif event.text[0] == "/":
                write_msg(event.user_id, 'Доступные комманды: ' + ', '.join(map(lambda x: x.lower(), bot._COMMANDS)))
            elif event.text.upper() == 'РАСПИСАНИЕ':
                sentrp(event.user_id, 'rp.jpg')
            elif event.text.startswith('рассылка') and event.user_id == 225133650:

                for id in get_members():
                    try:
                        write_msg(id, event.text.split()[1])
                    except:
                        pass
            elif event.text.lower().startswith('кто'):
                texte = event.text
                if event.text.endswith('?'):
                    texte = event.text[:-1]
                phrase, who = bot.new_message(texte)
                id = random.choice(get_members())
                guy = f"[id{id}|{' '.join(VkBot(id).get_user_name())}]"
                write_msg(event.user_id, phrase + guy + ' ' + who)
            else:
                write_msg(event.user_id, bot.new_message(event.text))
            text = 'Text: ' + event.text
            print(text)
            if logging:
                write_msg('225133650', text)
            print("-------------------")
