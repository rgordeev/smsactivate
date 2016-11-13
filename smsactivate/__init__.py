# coding: utf-8
from __future__ import unicode_literals
import requests
import logging

__title__ = 'smsactivate'
__version__ = '0.1'
__author__ = 'Roman Gordeev'
__license__ = 'MIT'

SMS_SERVICE_URLS = {
    # Заказ номера:
    'get-number': 'http://sms-activate.ru/stubs/handler_api.php?api_key=$api_key&action=getNumber&service=$service&forward=$forward&operator=$operator',
    # Запрос количества доступных номеров:
    'get-available-numbers': 'http://sms-activate.ru/stubs/handler_api.php?api_key=$api_key&action=getNumbersStatus',
    # Запрос баланса:
    'get-balance': 'http://sms-activate.ru/stubs/handler_api.php?api_key=$api_key&action=getBalance',
    # Получить состояние активации:
    'get-status': 'http://sms-activate.ru/stubs/handler_api.php?api_key=$api_key&action=getStatus&id=$id',
    # Изменение статуса активации
    'set-status': 'http://sms-activate.ru/stubs/handler_api.php?api_key=$api_key&action=setStatus&status=$status&id=$id&forward=$forward'
}


# $api_key&action=getNumber&service=$service&forward=$forward&operator=$operator
# $api_key - ключ АПИ
# $service - сервис для заказа. По умолчанию равет ot (без привязки к сервису)
# $forward - Необходимо ли выполнить переадресацию?
#     Принимаемые значения - 0 (не выполнять), 1 - (выполнять).
#     (необязательный параметр, по умолчанию равен 0)
# $operator - получить номера определенного оператора
#     (принимаемые значения: mts, beeline, any, где any - любой оператор).
#     Необязательный параметр, по умолчанию равен any
#
# Список доступных сервисов:
#     vk(Вконтакте)
#     ok(Одноклассники)
#     wa(Whatsapp)
#     vi(Viber)
#     tg(Telegram)
#     wb(WeChat)
#     go(Google,youtube,Gmail)
#     av(avito)
#     av(avito
#     +переадресация
#     )
#     fb(facebook)
#     tw(Twitter)
#     ot(Любой другой
#     +переадресация
#     )
#     ub(Uber)
#     qw(Qiwi)
#     gt(Gett)
#     sn(OLX.ua)
#     ig(Instagram)
#     ss(SeoSprint)
#     ym(Open I messenger)
#     ya(Яндекс)
#     ma(Mail.ru)
#     mm(Microsoft)
#     uk(IMO messenger)
#     me(Line messenger)
#     mb(Yahoo)
#     we(Aol)
#     bd(Rambler.ru)
#     kp(Gem4me)
#     dt(КХЛ)
#     fd(GetResponse)
#     ot(Любой другой)
#
# Ответы сервиса:
#     NO_NUMBERS - нет номеров
#     NO_BALANCE - закончился баланс
#     ACCESS_NUMBER:$id:$number - номер выдан ($id - id операции,$number - номер телефона)
#
# Возможные ошибки:
#     BAD_ACTION - некорректное действие
#     BAD_SERVICE - некорректное наименование сервиса
#     BAD_KEY - Неверный API-ключ
#     ERROR_SQL - ошибка SQL-сервера
def get_number(api_key=None, service='ot', forward=0, operator='any', proxies=None, auth=None):
    """
        :param api_key: Ключ API авторизации на сервисе
        :param service: Сервис для заказа. По умолчанию равет ot (без привязки к сервису)
        :param forward: Необходимо ли выполнить переадресацию? Принимаемые значения - 0 (не выполнять), 1 - (выполнять).
            По умолчанию равен 0.
        :param operator: Получить номера определенного оператора
            (принимаемые значения: mts, beeline, any, где any - любой оператор).
            Необязательный параметр, по умолчанию равен any
        :param proxies: адрес прокси сервера
        :param auth: авторизация прокси сервера
        Отправляем запрос на получение номера
        :return: palin text, содержащий номер выделенного сервисом телефона и идентификатор запроса
            Ответы сервиса:
            NO_NUMBERS - нет номеров
            NO_BALANCE - закончился баланс
            ACCESS_NUMBER:$id:$number - номер выдан ($id - id операции,$number - номер телефона)
            BAD_ACTION - некорректное действие
            BAD_SERVICE - некорректное наименование сервиса
            BAD_KEY - Неверный API-ключ
            ERROR_SQL - ошибка SQL-сервера
    """
    url = SMS_SERVICE_URLS.get('get-number')
    url = url.replace('$api_key', api_key)\
        .replace('$service', service)\
        .replace('$forward', str(forward))\
        .replace('$operator', operator)

    try:
        logging.info("Send request to following url %s" % url)
        r = requests.get(url, proxies=proxies, auth=auth, timeout=60)
        if r.status_code == 200:
            logging.info("SMS service respond with: status=%s, text=%s" % (r.status_code, r.text))
            return r.text
        else:
            logging.error("Can not get phone number: status=%s, text=%s" % (r.status_code, r.text))
    except:
        logging.exception("Can not get phone number: unknown exception")


def get_numbers_status(api_key=None, proxies=None, auth=None):
    """
    Запрос количества доступных номеров:
    :param api_key: ключ API авторизации на сервисе
    :param proxies: адрес прокси сервера
    :param auth: авторизация прокси сервера
    :return: Ответ сервиса будет в json формате, пример:
        {"vk_0":32,"ok_0":20,"wa_0":10,"vi_0":29,"tg_0":13,"wb_0":19,"go_0":31,"av_0":0,"av_1":26,"fb_0":23}
        Где до черточки - название сервиса, после обозначение нужно ли включать переадресацию.
        0 - не включать. 1 - включать.
    """
    url = SMS_SERVICE_URLS.get('get-available-numbers')
    url = url.replace('$api_key', api_key)

    try:
        logging.info("Send request to following url %s" % url)
        r = requests.get(url, proxies=proxies, auth=auth, timeout=60)
        if r.status_code == 200:
            logging.info("SMS service response with: status=%s, text=%s" % (r.status_code, r.text))
            return r.json()
        else:
            logging.error("Can not get number statuses: status=%s, text=%s" % (r.status_code, r.text))
    except:
        logging.exception("Can not get number statuses: unknown exception")


def get_balance(api_key=None, proxies=None, auth=None):
    """
    Запрос баланса:
    http://sms-activate.ru/stubs/handler_api.php?api_key=$api_key&action=getBalance
    :param api_key: ключ API авторизации на сервисе
    :param proxies: адрес прокси сервера
    :param auth: авторизация прокси сервера
    :return: ACCESS_BALANCE:$balance (где $balance - баланс на счету)
        Возможные ошибки:
        BAD_KEY - Неверный API-ключ
        ERROR_SQL - ошибка SQL-сервера
    """
    url = SMS_SERVICE_URLS.get('get-balance')
    url = url.replace('$api_key', api_key)

    try:
        logging.info("Send request to following url %s" % url)
        r = requests.get(url, proxies=proxies, auth=auth, timeout=60)
        if r.status_code == 200:
            logging.info("SMS service respond with: status=%s, text=%s" % (r.status_code, r.text))
            return r.text
        else:
            logging.error("Can not get balance: status=%s, text=%s" % (r.status_code, r.text))
    except:
        logging.exception("Can not get balance: unknown exception")


def get_status(api_key=None, request_id=None, proxies=None, auth=None):
    """
    Получить состояние активации:
    http://sms-activate.ru/stubs/handler_api.php?api_key=$api_key&action=getStatus&id=$id
    :param api_key: ключ API авторизации на сервисе
    :param request_id: id активации
    :param proxies: адрес прокси сервера
    :param auth: авторизация прокси сервера
    :return: Ответы сервиса:
        STATUS_WAIT_CODE - ожидание смс
        STATUS_WAIT_RETRY:$lastcode - ожидание уточнения кода (где $lastcode - прошлый, неподошедший код)
        STATUS_WAIT_RESEND - ожидание повторной отправки смс (софт должен нажать повторно выслать смс и выполнить изменение статуса на 6)
        STATUS_CANCEL - активация отменена
        STATUS_OK:$code - код получен (где $code - код активации)
        Возможные ошибки:
        NO_ACTIVATION - id активации не существует
        ERROR_SQL - ошибка SQL-сервера
        BAD_KEY - Неверный API-ключ
        BAD_ACTION - некорректное действие
    """
    url = SMS_SERVICE_URLS.get('get-status')
    url = url.replace('$api_key', api_key).replace('$id', request_id)

    try:
        logging.info("Send request to following url %s" % url)
        r = requests.get(url, proxies=proxies, auth=auth, timeout=60)
        if r.status_code == 200:
            logging.info("SMS service respond with: status=%s, text=%s" % (r.status_code, r.text))
            return r.text
        else:
            logging.error("Can not get request number status: status=%s, text=%s" % (r.status_code, r.text))
    except:
        logging.exception("Can not get request number status: unknown exception")


def set_status(api_key=None, status=None, request_id=None, forward=None, proxies=None, auth=None):
    """
    Изменение статуса активации
    http://sms-activate.ru/stubs/handler_api.php?api_key=$api_key&action=setStatus&status=$status&id=$id&forward=$forward

    :param api_key: ключ API авторизации на сервисе
    :param status: статус активации:
        -1 - отменить активацию
        1 - сообщить о готовности номера (смс на номер отправлено)
        3 - запросить еще один код (бесплатно)
        6 - завершить активацию(если был статус "код получен" - помечает успешно и завершает, если был "подготовка" - удаляет и помечает ошибка, если был статус "ожидает повтора" - переводит активацию в ожидание смс)
        8 - сообщить о том, что номер использован и отменить активацию
    :param request_id: id активации
    :param forward: номер телефона на который нужно выполнить переадресацию (обязательно, только если при getNumber был передан параметр forward=1)
    :param proxies: адрес прокси сервера
    :param auth: авторизация прокси сервера
    :return: Ответы сервиса:
        ACCESS_READY - готовность номера подтверждена
        ACCESS_RETRY_GET - ожидание нового смс
        ACCESS_ACTIVATION - сервис успешно активирован
        ACCESS_CANCEL - активация отменена
        Возможные ошибки:
        ERROR_SQL - ошибка SQL-сервера
        NO_ACTIVATION - id активации не существует
        BAD_SERVICE - некорректное наименование сервиса
        BAD_STATUS - некорректный статус
        BAD_KEY - Неверный API-ключ
        BAD_ACTION - некорректное действие
    """
    url = SMS_SERVICE_URLS.get('set-status')
    url = url.replace('$api_key', api_key)\
        .replace('$status', str(status))\
        .replace('$id', request_id)\
        .replace('$forward', str(forward))

    try:
        logging.info("Send request to following url %s" % url)
        r = requests.get(url, proxies=proxies, auth=auth, timeout=60)
        if r.status_code == 200:
            logging.info("SMS service respond with: status=%s, text=%s" % (r.status_code, r.text))
            return r.text
        else:
            logging.error("Can not change request number status: status=%s, text=%s" % (r.status_code, r.text))
    except:
        logging.exception("Can not change request number status: unknown exception")

