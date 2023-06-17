"""
В данном модуле написаны вспомогательные функции.
"""

import string
import random
import re


MONTHS = {
    "января": 1,
    "февраля": 2,
    "марта": 3,
    "апреля": 4,
    "мая": 5,
    "июня": 6,
    "июля": 7,
    "августа": 8,
    "сентября": 9,
    "октября": 10,
    "ноября": 11,
    "декабря": 12
}


def random_tag() -> str:
    """
    Генерирует случайный тег для запроса (для runner'а).

    :return: сгенерированный тег.
    """
    return "".join(random.choice(string.digits + string.ascii_lowercase) for _ in range(10))


def parse_wait_time(response: str) -> int:
    """
    Парсит ответ FunPay на запрос о поднятии лотов.

    :param response: текст ответа.

    :return: Примерное время ожидание до следующего поднятия лотов (в секундах).
    """
    if response == "Подождите секунду.":
        return 2
    elif response == "Подождите минуту.":
        return 60
    elif response == "Подождите час.":
        return 3600
    elif "сек" in response:
        response = response.split()
        return int(response[1])
    elif "мин" in response:
        response = response.split()
        # ["Подождите", "n", "минут."]
        return (int(response[1])-1) * 60
    elif "час" in response:
        response = response.split()
        return (int(response[1])) * 3600
    else:
        return 10


class RegularExpressions(object):
    """
    В данном классе хранятся скомпилированные регулярные выражения, описывающие системные сообщения FunPay и прочие
    элементы текстов.
    Класс является singleton'ом.
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            setattr(cls, "instance", super(RegularExpressions, cls).__new__(cls))
        return getattr(cls, "instance")

    def __init__(self):
        self.ORDER_PURCHASED = re.compile(r"Покупатель [a-zA-Z0-9]+ оплатил заказ #[A-Z0-9]{8}\.")
        """
        Скомпилированное регулярное выражение, описывающее сообщение об оплате заказа.
        Лучше всего использовать вместе с MessageTypesRes.ORDER_PURCHASED2
        """

        self.ORDER_PURCHASED2 = re.compile(r"[a-zA-Z0-9]+, не забудьте потом нажать кнопку "
                                           r"«Подтвердить выполнение заказа»\.")
        """
        Скомпилированное регулярное выражение, описывающее сообщение об оплате заказа (2).
        Лучше всего использовать вместе с MessageTypesRes.ORDER_PURCHASED
        """

        self.ORDER_CONFIRMED = re.compile(r"Покупатель [a-zA-Z0-9]+ подтвердил успешное выполнение "
                                          r"заказа #[A-Z0-9]{8} и отправил деньги продавцу [a-zA-Z0-9]+\.")
        """
        Скомпилированное регулярное выражение, описывающее сообщение о подтверждении выполнения заказа.
        """

        self.NEW_FEEDBACK = re.compile(r"Покупатель [a-zA-Z0-9]+ написал отзыв к заказу #[A-Z0-9]{8}\.")
        """
        Скомпилированное регулярное выражение, описывающее сообщение о новом отзыве.
        """

        self.FEEDBACK_CHANGED = re.compile(r"Покупатель [a-zA-Z0-9]+ изменил отзыв к заказу #[A-Z0-9]{8}\.")
        """
        Скомпилированное регулярное выражение, описывающее сообщение об изменении отзыва.
        """

        self.FEEDBACK_DELETED = re.compile(r"Покупатель [a-zA-Z0-9]+ удалил отзыв к заказу #[A-Z0-9]{8}\.")
        """
        Скомпилированное регулярное выражение, описывающее сообщение об удалении отзыва.
        """

        self.NEW_FEEDBACK_ANSWER = re.compile(r"Продавец [a-zA-Z0-9]+ ответил на отзыв к заказу #[A-Z0-9]{8}\.")
        """
        Скомпилированное регулярное выражение, описывающее сообщение о новом ответе на отзыв.
        """

        self.FEEDBACK_ANSWER_CHANGED = re.compile(r"Продавец [a-zA-Z0-9]+ изменил ответ на отзыв к "
                                                  r"заказу #[A-Z0-9]{8}\.")
        """
        Скомпилированное регулярное выражение, описывающее сообщение об изменении ответа на отзыв.
        """

        self.FEEDBACK_ANSWER_DELETED = re.compile(r"Продавец [a-zA-Z0-9]+ удалил ответ на отзыв к заказу "
                                                  r"#[A-Z0-9]{8}\.")
        """
        Скомпилированное регулярное выражение, описывающее сообщение об удалении ответа на отзыв.
        """

        self.ORDER_REOPENED = re.compile(r"Заказ #[A-Z0-9]{8} открыт повторно\.")
        """
        Скомпилированное регулярное выражение, описывающее сообщение о повтором открытии заказа.
        """

        self.REFUND = re.compile(r"Продавец [a-zA-Z0-9]+ вернул деньги покупателю [a-zA-Z0-9]+ "
                                 r"по заказу #[A-Z0-9]{8}\.")
        """
        Скомпилированное регулярное выражение, описывающее сообщение о возврате денежных средств.
        """

        self.PARTIAL_REFUND = re.compile(r"Часть средств по заказу #[A-Z0-9]{8} возвращена покупателю\.")
        """
        Скомпилированное регулярное выражение, описывающее сообщение частичном о возврате денежных средств.
        """

        self.ORDER_CONFIRMED_BY_ADMIN = re.compile(r"Администратор [a-zA-Z0-9]+ подтвердил успешное выполнение "
                                                   r"заказа #[A-Z0-9]{8} и отправил деньги продавцу [a-zA-Z0-9]+\.")
        """
        Скомпилированное регулярное выражение, описывающее сообщение о подтверждении выполнения заказа администратором.
        """

        self.ORDER_ID = re.compile(r"#[A-Z0-9]{8}")
        """
        Скомпилированное регулярное выражение, описывающее ID заказа.
        """

        self.ORDER_DATE = re.compile(r"\d{1,2} [а-я]+, \d{1,2}:\d{1,2}")
        """
        Скомпилированное регулярное выражение, описывающее дату заказа в формате <ДД месяца, ЧЧ:ММ>.
        """

        self.FULL_ORDER_DATE = re.compile(r"\d{1,2} [а-я]+ \d{4}, \d{1,2}:\d{1,2}")
        """
        Скомпилированное регулярное выражение, описывающее дату заказа в формате <ДД месяца ГГГГ, ЧЧ:ММ>.
        """

        self.DISCORD = "Вы можете перейти в Discord. " \
                       "Внимание: общение за пределами сервера FunPay считается нарушением правил."
        """
        Точный текст сообщения о предложении перехода в Discord.
        """

        self.PRODUCTS_AMOUNT = re.compile(r"\d+ шт\.")
        """
        Скомпилированное регулярное выражение, описывающее запись кол-ва товаров в заказе.
        """
