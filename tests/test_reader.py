import sys
from pathlib import Path
sys.path.append("src")
from mail_reader import MailReader

def test_reader_reads_text_file():
    reader = MailReader("tests/test_files")
    file_path = Path("tests/test_files/mail.txt")
    path, message, error = reader.read_one(file_path)

    assert error is None
    assert message.topic == "Запрос доступа"
    assert message.sender == "user@company.com"
    assert "VPN" in message.message


def test_reader_empty_file():
    reader = MailReader("tests/test_files")
    file_path = Path("tests/test_files/empty.txt")
    path, message, error = reader.read_one(file_path)

    assert message is None
    assert error == "пустой файл"


def test_reader_binary_file():
    reader = MailReader("tests/test_files")
    file_path = Path("tests/test_files/file.bin")
    path, message, error = reader.read_one(file_path)

    assert message is None
    assert error == "бинарный формат файла"