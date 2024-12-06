# YooKassa API Python Client Library

[![Build Status](https://travis-ci.org/yoomoney/yookassa-sdk-python.svg?branch=master)](https://travis-ci.org/yoomoney/yookassa-sdk-python)
[![Latest Stable Version](https://img.shields.io/pypi/v/yookassa.svg)](https://pypi.org/project/yookassa/)
[![Total Downloads](https://img.shields.io/pypi/dm/yookassa.svg)](https://pypi.org/project/yookassa/)
[![License](https://img.shields.io/pypi/l/yookassa.svg)](https://git.yoomoney.ru/projects/SDK/repos/yookassa-sdk-python)

Russian | [English](README.en.md)

Клиент для работы с платежами по [API ЮKassa](https://yookassa.ru/developers/api)
Подходит тем, у кого способ подключения к ЮKassa называется API.

## Особенности

* Версия 3.x поддерживает Python >=3.7. Для работы на более ранних версиях Python используйте версии yookassa 2.x
* Изменение структуры каталогов/файлов затронуло часть импортов пакетов. При переходе с версии yookassa 2.x проверьте импорты в вашем проекте:
  * `yookassa.domain.models.airline` → `yookassa.domain.models.payment_data.request.airline`
  * `yookassa.domain.models.authorization_details` → `yookassa.domain.models.payment_data.response.authorization_details`
  * `yookassa.domain.models.receipt_customer` → `yookassa.domain.models.receipt_data.receipt_customer`
  * `yookassa.domain.models.receipt_item` → `yookassa.domain.models.receipt_data.receipt_item`
  * `yookassa.domain.models.receipt_item_supplier` → `yookassa.domain.models.receipt_data.receipt_item_supplier`
  * `yookassa.domain.models.recipient` → `yookassa.domain.models.payment_data.recipient`
  * `yookassa.domain.models.refund_source` → `yookassa.domain.models.refund_data.refund_source`
* `Settings.get_account_settings()` теперь возвращает объект `Me`. Для поддержки совместимости, к полям объекта можно обращаться как к массиву - `me.account_id = me['account_id']`
* Поле `me.fiscalization_enabled` устарело, но пока поддерживается. Вместо него добавлен объект `me.fiscalization`.

## Требования

1. Python >=3.7
2. pip

## Установка
### C помощью pip

1. Установите pip.
2. В консоли выполните команду
```bash
pip install --upgrade yookassa
```

### С помощью easy_install
1. Установите easy_install.
2. В консоли выполните команду
```bash
easy_install --upgrade yookassa
```

## Начало работы

1. Импортируйте модуль
```python
import yookassa
```
2. Установите данные для конфигурации
```python
from yookassa import Configuration

Configuration.configure('<Идентификатор магазина>', '<Секретный ключ>')
```

или

```python
from yookassa import Configuration

Configuration.account_id = '<Идентификатор магазина>'
Configuration.secret_key = '<Секретный ключ>'
```

или через oauth

```python
from yookassa import Configuration

Configuration.configure_auth_token('<Oauth Token>')
```

Если вы согласны участвовать в развитии SDK, вы можете передать данные о вашем фреймворке, cms или модуле:
```python
from yookassa import Configuration
from yookassa.domain.common.user_agent import Version

Configuration.configure('<Идентификатор магазина>', '<Секретный ключ>')
Configuration.configure_user_agent(
    framework=Version('Django', '2.2.3'),
    cms=Version('Wagtail', '2.6.2'),
    module=Version('Y.CMS', '0.0.1')
)
```

3. Вызовите нужный метод API. [Подробнее в документации к API ЮKassa](https://yookassa.ru/developers/api)

## Примеры использования SDK

#### [Настройки SDK API ЮKassa](./docs/examples/01-configuration.md)
* [Аутентификация](./docs/examples/01-configuration.md#Аутентификация)
* [Статистические данные об используемом окружении](./docs/examples/01-configuration.md#Статистические-данные-об-используемом-окружении)
* [Получение информации о магазине](./docs/examples/01-configuration.md#Получение-информации-о-магазине)
* [Работа с Webhook](./docs/examples/01-configuration.md#Работа-с-Webhook)
* [Входящие уведомления](./docs/examples/01-configuration.md#Входящие-уведомления)

#### [Работа с платежами](./docs/examples/02-payments.md)
* [Запрос на создание платежа](./docs/examples/02-payments.md#Запрос-на-создание-платежа)
* [Запрос на создание платежа через билдер](./docs/examples/02-payments.md#Запрос-на-создание-платежа-через-билдер)
* [Запрос на частичное подтверждение платежа](./docs/examples/02-payments.md#Запрос-на-частичное-подтверждение-платежа)
* [Запрос на отмену незавершенного платежа](./docs/examples/02-payments.md#Запрос-на-отмену-незавершенного-платежа)
* [Получить информацию о платеже](./docs/examples/02-payments.md#Получить-информацию-о-платеже)
* [Получить список платежей с фильтрацией](./docs/examples/02-payments.md#Получить-список-платежей-с-фильтрацией)

#### [Работа с возвратами](./docs/examples/03-refunds.md)
* [Запрос на создание возврата](./docs/examples/03-refunds.md#Запрос-на-создание-возврата)
* [Запрос на создание возврата через билдер](./docs/examples/03-refunds.md#Запрос-на-создание-возврата-через-билдер)
* [Получить информацию о возврате](./docs/examples/03-refunds.md#Получить-информацию-о-возврате)
* [Получить список возвратов с фильтрацией](./docs/examples/03-refunds.md#Получить-список-возвратов-с-фильтрацией)

#### [Работа с чеками](./docs/examples/04-receipts.md)
* [Запрос на создание чека](./docs/examples/04-receipts.md#Запрос-на-создание-чека)
* [Запрос на создание чека через билдер](./docs/examples/04-receipts.md#Запрос-на-создание-чека-через-билдер)
* [Получить информацию о чеке](./docs/examples/04-receipts.md#Получить-информацию-о-чеке)
* [Получить список чеков с фильтрацией](./docs/examples/04-receipts.md#Получить-список-чеков-с-фильтрацией)

#### [Работа со сделками](./docs/examples/05-deals.md)
* [Запрос на создание сделки](./docs/examples/05-deals.md#Запрос-на-создание-сделки)
* [Запрос на создание сделки через билдер](./docs/examples/05-deals.md#Запрос-на-создание-сделки-через-билдер)
* [Запрос на создание платежа с привязкой к сделке](./docs/examples/05-deals.md#Запрос-на-создание-платежа-с-привязкой-к-сделке)
* [Получить информацию о сделке](./docs/examples/05-deals.md#Получить-информацию-о-сделке)
* [Получить список сделок с фильтрацией](./docs/examples/05-deals.md#Получить-список-сделок-с-фильтрацией)

### [Работа с выплатами](./docs/examples/06-payouts.md)
* [Запрос на выплату продавцу](./docs/examples/06-payouts.md#Запрос-на-выплату-продавцу)
  * [Проведение выплаты на банковскую карту](./docs/examples/06-payouts.md#Проведение-выплаты-на-банковскую-карту)
  * [Проведение выплаты в кошелек ЮMoney](./docs/examples/06-payouts.md#Проведение-выплаты-в-кошелек-юmoney)
  * [Проведение выплаты через СБП](./docs/examples/06-payouts.md#Проведение-выплаты-через-сбп)
  * [Выплаты самозанятым](./docs/examples/06-payouts.md#Выплаты-самозанятым)
  * [Проведение выплаты по безопасной сделке](./docs/examples/06-payouts.md#Проведение-выплаты-по-безопасной-сделке)
* [Получить информацию о выплате](./docs/examples/06-payouts.md#Получить-информацию-о-выплате)

### [Работа с самозанятыми](./docs/examples/07-self-employed.md)
* [Запрос на создание самозанятого](./docs/examples/07-self-employed.md#Запрос-на-создание-самозанятого)
* [Получить информацию о самозанятом](./docs/examples/07-self-employed.md#Получить-информацию-о-самозанятом)

### [Работа с персональными данными](./docs/examples/08-personal-data.md)
* [Создание персональных данных](./docs/examples/08-personal-data.md#Создание-персональных-данных)
* [Получить информацию о персональных данных](./docs/examples/08-personal-data.md#Получить-информацию-о-персональных-данных)

#### [Работа со списком участников СБП](./docs/examples/09-sbp-banks.md)
* [Получить список участников СБП](./docs/examples/09-sbp-banks.md#Получить-список-участников-СБП)

#### [Работа со счетами](./docs/examples/10-invoices.md)
* [Запрос на создание счета](./docs/examples/10-invoices.md#Запрос-на-создание-счета)
* [Запрос на создание счета через билдер](./docs/examples/10-invoices.md#Запрос-на-создание-счета-через-билдер)
* [Получить информацию о счете](./docs/examples/10-invoices.md#Получить-информацию-о-счете)
