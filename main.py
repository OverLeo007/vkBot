import random
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

# --
# from commander.commander import Commander
from Bot import VkBot


# --

def write_msg(user_id, message):
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})


def msg_with_photo(user_id, message, pic_url):
    vk = vk_session.get_api()
    attachments = []
    upload = vk_api.VkUpload(vk_session)
    image_url = pic_url
    image = session.get(image_url, stream=True)
    photo = upload.photo_messages(photos=image.raw)[0]
    attachments.append(
        'photo{}_{}'.format(photo['owner_id'], photo['id'])
    )
    vk.messages.send(
        user_id=user_id,
        attachment=','.join(attachments),
        message='Фотка для проверки'
    )


session = requests.Session()
# API-ключ созданный ранее
token = "1455eb26498f0d6ab33db6575afbd7d7e604bef57ee87b2f86a38269f4f227d5ff38f4cf3750cf5f21f36"

# Авторизуемся как сообщество
vk_session = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk_session)

# commander = Commander()
print("Server started")
for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:
        # print('>>', event)
        if event.to_me:

            bot = VkBot(event.user_id)
            text = f'Новое сообщение от {" ".join(bot._get_user_name(event.user_id))}'
            print(text, end=' ')
            write_msg('225133650', text)
            if event.text[0] == "/":
                write_msg(event.user_id, 'Доступные комманды: ' + ', '.join(map(lambda x: x.lower(), bot._COMMANDS)))
            elif event.text[0].upper() == 'РАСПИСАНИЕ':
                msg_with_photo(event.user_id, bot.new_message('расписание'),
                               'https://static-ru.insales.ru/images/products/1/5236/125121652/%D1%80%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5_%D0%B7%D0%BE%D0%BB%D0%BE%D1%82%D0%BE_%D0%BF%D1%80%D0%BE%D1%81%D0%BC%D0%BE%D1%82%D1%80.jpg')
            else:
                write_msg(event.user_id, bot.new_message(event.text))
            text = 'Text: ' + event.text
            print(text)
            write_msg('225133650', text)
            print("-------------------")
