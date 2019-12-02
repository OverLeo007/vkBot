import requests
import bs4


class VkBot:

    def __init__(self, user_id):
        # print(' создан экземпляр')
        self._USER_ID = user_id
        self._USERNAME = self.get_user_name(user_id)

        self._COMMANDS = ["ПРИВЕТ", "ВРЕМЯ", "ПОКА", 'РАСПИСАНИЕ']

    def get_user_name(self, user_id):
        request = requests.get("https://vk.com/id" + str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")

        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])

        return tuple(user_name.split())

    def _get_time(self):
        request = requests.get("https://my-calend.ru/date-and-time-today")
        b = bs4.BeautifulSoup(request.text, "html.parser")
        # time = 0
        return self._clean_all_tag_from_str(str(b.select(".page")[0].findAll("h2")[1]))



    @staticmethod
    def _clean_all_tag_from_str(string_line):
        # print('>>', string_line)
        """
        Очистка строки stringLine от тэгов и их содержимых
        :param string_line: Очищаемая строка
        :return: очищенная строка
        """
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
        # print('>>', result)
        return result

    def new_message(self, message):

        # Привет
        if message.upper() == self._COMMANDS[0]:
            return "Ну здарова пешка Переваловой"

        # Время
        elif message.upper() == self._COMMANDS[1]:
            return 'Время по мск: ' + self._get_time().split()[1]

        # Пока
        elif message.upper() == self._COMMANDS[2]:
            return f"Ну пока, {self._USERNAME[0]}"
        elif message.upper() == self._COMMANDS[3]:
            return f"Хочешь расписание? А подожди пока я это напишу!"

        else:
            return 'каво? /'
