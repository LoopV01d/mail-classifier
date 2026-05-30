class MailClassifier:
    def __init__(self):
        self.category_dict = {
            'spam': ['ключевые слова'],
            'critical': ['ключевые слова'],
            'access': ['ключевые слова'],
            'hardware': ['ключевые слова'],
            'software': ['ключевые слова'],
            'documents': ['ключевые слова'],
            'tasks': ['ключевые слова'],
            'info': ['ключевые слова']
        }

        # Нужно будет вставить в словарь ключевые слова после финальной обработки категорий

    def classify_mail(self, mail_text):
        mail_text = mail_text.get_full_mail_text()

        for category, keywords in self.category_dict.items():
            for keyword in keywords:
                if keyword in mail_text:
                    return category
                    
        return 'unknown'