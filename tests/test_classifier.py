import pytest
from src.mail_message import MailMessage
from src.mail_classification import MailClassifier

def test_spam():
    classifier = MailClassifier()

    mail = MailMessage(
        "Уведомление о выигрыше.txt",
        "Ваш уникальный выигрыш ждет!",
        "support@offers-promo.ru",
        "Здравствуйте! Поздравляем, вы стали победителем нашего розыгрыша. Ваша банковская карта выбрана для получения приза. Чтобы забрать выигрыш, перейдите по ссылке в личном кабинете. Спешите, предложение ограничено!"
    )

    assert classifier.classify_mail(mail) == "spam"

def test_critical():
    classifier = MailClassifier()

    mail = MailMessage(
        "Оповещение об аварии сервера.txt",
        "Авария на основном сервере",
        "sysadmin@company.com",
        "Коллеги, добрый день. В данный момент лежит основной сервер базы данных. Работа всех подразделений остановлена. Специалисты уже работают над устранением. Просим не перезагружать рабочие станции до особого распоряжения."
    )

    assert classifier.classify_mail(mail) == "critical"

def test_access():
    classifier = MailClassifier()

    mail = MailMessage(
        "Запрос прав доступа.txt",
        "Запрос на предоставление прав в GitLab",
        "a.petrov@company.com",
        "Приветствую! Для выполнения текущих задач мне необходимо получить права на запись в репозитории проекта «Alpha». Моя учетная запись: a.petrov. Прошу выдать доступ в ближайшее время."
    )

    assert classifier.classify_mail(mail) == "access"

def test_hardware():
    classifier = MailClassifier()

    mail = MailMessage(
        "Заявка на ремонт ноутбука.txt",
        "Не включается ноутбук",
        "m.ivanova@company.com",
        "Добрый день! Мой рабочий ноутбук сегодня утром перестал включаться (не реагирует на кнопку питания). Подскажите, к кому обратиться для диагностики или ремонта устройства?"
    )

    assert classifier.classify_mail(mail) == "hardware"

def test_unknown_no_matches():
    classifier = MailClassifier()

    mail = MailMessage(
        "Общая встреча за чашкой кофе.txt",
        "Есть время поболтать?",
        "e.sokolova@personal.ru",
        "Привет! Давно не виделись. Я тут обнаружила интересную статью про книги, которую мы обсуждали на прошлой неделе, и подумала, что тебе она тоже понравится. Если будет время на этой неделе, давай сходим в кофейню за углом и просто пообщаемся, без всяких рабочих вопросов. Дай знать, когда тебе будет удобно!"
    )

    assert classifier.classify_mail(mail) == "unknown"

def test_unknown_empty():
    classifier = MailClassifier()

    mail = MailMessage(
        "Общая встреча за чашкой кофе.txt",
        "Есть время поболтать?",
        "e.sokolova@personal.ru",
        " "
    )

    assert classifier.classify_mail(mail) == "unknown"

def test_unknown_wrong_format():
    classifier = MailClassifier()

    mail = MailMessage(
        "Общая встреча за чашкой кофе.svg",
        "Есть время поболтать?",
        "e.sokolova@personal.ru",
        "Привет! Давно не виделись. Я тут обнаружила интересную статью про книги, которую мы обсуждали на прошлой неделе, и подумала, что тебе она тоже понравится. Если будет время на этой неделе, давай сходим в кофейню за углом и просто пообщаемся, без всяких рабочих вопросов. Дай знать, когда тебе будет удобно!"
    )

    assert classifier.classify_mail(mail) == "unknown"