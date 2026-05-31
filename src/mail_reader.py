import json
from pathlib import Path

from mail_message import MailMessage


class MailReader:
    BINARY_EXTENSIONS = {
        '.bin', '.jpg', '.jpeg', '.png', '.gif',
        '.pdf', '.exe', '.zip', '.rar', '.mp3', '.mp4',
    }
    MAX_FILE_SIZE = 1_000_000

    SUBJECT_PREFIXES = ('subject:', 'тема:', 'tema:')
    SENDER_PREFIXES = ('from:', 'от кого:', 'ot kogo:')
    SKIP_HEADER_PREFIXES = (
        'to:', 'кому:', 'komu:',
        'date:', 'дата:', 'data:',
        'cc:', 'bcc:', 'reply-to:',
    )

    def __init__(self, inbox_path):
        self.inbox_path = Path(inbox_path)

    def read_all(self):
        if not self.inbox_path.exists():
            raise FileNotFoundError(f"Папка не найдена: {self.inbox_path}")
        if not self.inbox_path.is_dir():
            raise NotADirectoryError(f"Не папка: {self.inbox_path}")

        results = []
        for entry in sorted(self.inbox_path.iterdir()):
            if not entry.is_file():
                continue
            if entry.name.startswith('.'):
                continue
            results.append(self.read_one(entry))
        return results

    def read_one(self, path):
        path = Path(path)
        try:
            if path.suffix.lower() in self.BINARY_EXTENSIONS:
                return (path, None, 'бинарный формат файла')

            size = path.stat().st_size
            if size == 0:
                return (path, None, 'пустой файл')
            if size > self.MAX_FILE_SIZE:
                return (path, None, 'файл слишком большой')

            raw_bytes = path.read_bytes()

            if b'\x00' in raw_bytes[:4096]:
                return (path, None, 'двоичные данные в файле')

            text = self.decode_bytes(raw_bytes)
            if text is None:
                return (path, None, 'не удалось декодировать текст')

            if not text.strip():
                return (path, None, 'файл содержит только пробелы')

            if path.suffix.lower() == '.json':
                message = self.parse_json(path, text)
            else:
                message = self.parse_email(path, text)

            return (path, message, None)

        except PermissionError:
            return (path, None, 'нет прав на чтение')
        except OSError as e:
            return (path, None, f'ошибка ОС: {e}')

    def decode_bytes(self, raw_bytes):
        for encoding in ('utf-8', 'cp1251', 'latin-1'):
            try:
                return raw_bytes.decode(encoding)
            except UnicodeDecodeError:
                continue
        return None

    def parse_json(self, path, text):
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            return self.parse_email(path, text)

        if not isinstance(data, dict):
            return self.parse_email(path, text)

        topic = str(data.get('subject') or data.get('topic') or '')
        sender = str(data.get('from') or data.get('sender') or '')
        body = str(data.get('body') or data.get('message') or '')
        return MailMessage(path.name, topic, sender, body)

    def parse_email(self, path, text):
        topic = ''
        sender = ''
        body_lines = []
        in_body = False

        for line in text.splitlines():
            if in_body:
                body_lines.append(line)
                continue

            stripped = line.strip()
            low = stripped.lower()

            if any(low.startswith(p) for p in self.SUBJECT_PREFIXES):
                topic = self.after_colon(stripped)
            elif any(low.startswith(p) for p in self.SENDER_PREFIXES):
                sender = self.after_colon(stripped)
            elif any(low.startswith(p) for p in self.SKIP_HEADER_PREFIXES):
                continue
            elif stripped == '':
                if topic or sender:
                    in_body = True
            else:
                in_body = True
                body_lines.append(line)

        body = '\n'.join(body_lines).strip()
        return MailMessage(path.name, topic, sender, body)

    def after_colon(self, line):
        idx = line.find(':')
        return line[idx + 1:].strip() if idx >= 0 else line.strip()
