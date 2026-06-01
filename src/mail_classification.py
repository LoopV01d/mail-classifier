import json
from pathlib import Path

class MailClassifier:
    def __init__(self):
        keywords_path = Path(__file__).parent / "keywords.json"
        with open(keywords_path, encoding="utf-8") as f:
            data = json.load(f)
        self.subject_dict = data["subject_keywords"]
        self.category_dict = data["body_keywords"]

    def classify_mail(self, mail_message):
        subject = mail_message.topic.lower()
        text = mail_message.get_full_mail_text().lower()

        for category, keywords in self.subject_dict.items():
            for keyword in keywords:
                if keyword in subject:
                    return category

        for category, keywords in self.category_dict.items():
            for keyword in keywords:
                if keyword in text:
                    return category

        return 'unknown'