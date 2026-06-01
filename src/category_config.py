import json
import re
from pathlib import Path


class ConfigError(Exception):
    pass


class CategoryRule:
    def __init__(self, name, priority, keywords_subject, keywords_body, regex_patterns, case_sensitive):
        self.name = name
        self.priority = priority
        self.case_sensitive = case_sensitive
        self.keywords_subject = self._prepare(keywords_subject)
        self.keywords_body = self._prepare(keywords_body)
        self.regex_patterns = self._compile_regex(regex_patterns)

    def _prepare(self, words):
        if self.case_sensitive:
            return list(words)
        return [w.lower() for w in words]

    def _compile_regex(self, patterns):
        compiled = []
        flags = 0 if self.case_sensitive else re.IGNORECASE
        for pat in patterns:
            try:
                compiled.append(re.compile(pat, flags))
            except re.error as e:
                raise ConfigError(f"Категория '{self.name}', regex '{pat}' невалиден: {e}")
        return compiled

    def matches(self, subject, body):
        subj = subject if self.case_sensitive else subject.lower()
        body_text = body if self.case_sensitive else body.lower()

        for kw in self.keywords_subject:
            if kw in subj:
                return True

        for kw in self.keywords_body:
            if kw in body_text:
                return True

        full = subject + '\n' + body
        for pattern in self.regex_patterns:
            if pattern.search(full):
                return True

        return False


class ConfigLoader:
    REQUIRED_FIELDS = ('name', 'priority')

    @classmethod
    def load(cls, path):
        path = Path(path)
        if not path.exists():
            raise ConfigError(f"Файл конфигурации не найден: {path}")

        try:
            with path.open('r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigError(f"Некорректный JSON в {path}: {e}")
        except OSError as e:
            raise ConfigError(f"Не удалось прочитать {path}: {e}")

        if not isinstance(data, dict):
            raise ConfigError("Корневой элемент конфига должен быть объектом JSON")

        default_category = str(data.get('default_category', 'unknown'))
        case_sensitive = bool(data.get('case_sensitive', False))

        raw_categories = data.get('categories')
        if not isinstance(raw_categories, list) or not raw_categories:
            raise ConfigError("Поле 'categories' должно быть непустым списком")

        rules = []
        seen_names = set()

        for idx, raw in enumerate(raw_categories):
            if not isinstance(raw, dict):
                raise ConfigError(f"Категория #{idx} должна быть объектом")

            for field in cls.REQUIRED_FIELDS:
                if field not in raw:
                    raise ConfigError(f"Категория #{idx} не имеет обязательного поля '{field}'")

            name = str(raw['name']).strip()
            if not name:
                raise ConfigError(f"Категория #{idx} имеет пустое имя")
            if name in seen_names:
                raise ConfigError(f"Категория '{name}' встречается дважды")
            seen_names.add(name)

            try:
                priority = int(raw['priority'])
            except (TypeError, ValueError):
                raise ConfigError(f"Категория '{name}': priority должен быть числом")

            keywords_subject = raw.get('keywords_subject', []) or []
            keywords_body = raw.get('keywords_body', []) or []
            regex_patterns = raw.get('regex_patterns', []) or []

            if not isinstance(keywords_subject, list):
                raise ConfigError(f"Категория '{name}': keywords_subject должен быть списком")
            if not isinstance(keywords_body, list):
                raise ConfigError(f"Категория '{name}': keywords_body должен быть списком")
            if not isinstance(regex_patterns, list):
                raise ConfigError(f"Категория '{name}': regex_patterns должен быть списком")

            if not keywords_subject and not keywords_body and not regex_patterns:
                raise ConfigError(f"Категория '{name}' не содержит ни одного ключевого слова или regex")

            rules.append(CategoryRule(
                name=name,
                priority=priority,
                keywords_subject=keywords_subject,
                keywords_body=keywords_body,
                regex_patterns=regex_patterns,
                case_sensitive=case_sensitive,
            ))

        rules.sort(key=lambda r: r.priority)
        return rules, default_category


class ConfigurableClassifier:
    def __init__(self, config_path):
        self.rules, self.default_category = ConfigLoader.load(config_path)

    def classify_mail(self, mail_message):
        subject = getattr(mail_message, 'topic', '') or ''
        body = getattr(mail_message, 'message', '') or ''

        for rule in self.rules:
            if rule.matches(subject, body):
                return rule.name

        return self.default_category

    def describe_rules(self):
        return [
            {
                'priority': r.priority,
                'name': r.name,
                'subject_keywords': len(r.keywords_subject),
                'body_keywords': len(r.keywords_body),
                'regex_patterns': len(r.regex_patterns),
            }
            for r in self.rules
        ]
