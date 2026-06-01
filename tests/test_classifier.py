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

def test_software():
    classifier = MailClassifier()

    mail = MailMessage(
        "Техническая проблема с 1С.txt",
        "Ошибка при запуске 1С",
        "d.sergeev@company.com",
        "Коллеги, добрый день. При попытке запустить 1С программа виснет на этапе загрузки конфигурации. Также вчера выходило уведомление об истечении лицензии. Помогите, пожалуйста, разобраться."
    )

    assert classifier.classify_mail(mail) == "software"


def test_documents():
    classifier = MailClassifier()

    mail = MailMessage(
        "Согласование закрывающих документов.txt",
        "Согласование закрывающих документов",
        "buh@company.com",
        "Добрый день! Направляем вам скан счета-фактуры и акт выполненных работ по договору №123-А от 01.06.2026. Просим проверить данные и прислать подписанный скан до конца дня."
    )

    assert classifier.classify_mail(mail) == "documents"


def test_tasks():
    classifier = MailClassifier()

    mail = MailMessage(
        "Поручение по подготовке отчета.txt",
        "Запрос на подготовку отчета",
        "i.smirnov@company.com",
        "Коллеги, добрый день! Необходимо сделать сводную таблицу по продажам за май. Прошу подготовить данные к завтрашнему утру. Требуется также краткий комментарий по отклонениям от плана."
    )

    assert classifier.classify_mail(mail) == "tasks"


def test_info():
    classifier = MailClassifier()

    mail = MailMessage(
        "Информационное уведомление о работах.txt",
        "Напоминание: плановые работы в офисе",
        "hr@company.com",
        "Уважаемые сотрудники! Информируем вас, что в ближайшую субботу будут проводиться плановые работы по обновлению сети в офисе. Доступ в здание будет ограничен. Спасибо за понимание!"
    )

    assert classifier.classify_mail(mail) == "info"

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
        "  ",
        "e.sokolova@personal.ru",
        "  "
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

def test_register():
    classifier = MailClassifier()

    mail = MailMessage(
        "ДОСТУП.txt",
        "ЗАПРОС НА ПРЕДОСТАВЛЕНИЕ ПРАВ В GITLAB",
        "a.petrov@company.com",
        "ПРИВЕТСТВУЮ! ДЛЯ ВЫПОЛНЕНИЯ ТЕКУЩИХ ЗАДАЧ МНЕ НЕОБХОДИМО ПОЛУЧИТЬ ПРАВА НА ЗАПИСЬ В РЕПОЗИТОРИИ ПРОЕКТА «ALPHA». МОЯ УЧЕТНАЯ ЗАПИСЬ: A.PETROV. ПРОШУ ВЫДАТЬ ДОСТУП В БЛИЖАЙШЕЕ ВРЕМЯ."
    )

    assert classifier.classify_mail(mail) == "access"

def test_mixed_categories():
    classifier = MailClassifier()

    mail = MailMessage(
        "Срочный запрос доступа для устранения аварии.txt",
        "СРОЧНО: Ошибка 500 и запрос прав в GitLab",
        "a.petrov@company.com",
        "Коллеги, добрый день! Ситуация критичная: наш сервер выдает «Ошибка 500», работа сайта полностью остановлена! Мне необходимо срочно проверить логи, но у меня нет прав на запись в репозиторий. Прошу выдать права в GitLab (учетная запись: a.petrov) прямо сейчас, это вопрос аварийного восстановления!"
    )

    assert classifier.classify_mail(mail) == "critical"