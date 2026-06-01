#!/bin/bash

KEYWORDS_FILE="src/keywords.json"

while true; do
    echo ""
    echo "=== Управление категориями ==="
    echo "1. Показать все категории"
    echo "2. Добавить категорию"
    echo "3. Удалить категорию"
    echo "4. Добавить ключевое слово"
    echo "5. Удалить ключевое слово"
    echo "6. Выход"
    echo ""
    read -p "Выберите действие [1-6]: " choice

    if [ "$choice" = "1" ]; then
        echo ""
        python3 -c "
import json
with open('$KEYWORDS_FILE', encoding='utf-8') as f:
    data = json.load(f)
for cat, words in data['body_keywords'].items():
    print(f'  {cat}: {words}')
"

    elif [ "$choice" = "2" ]; then
        read -p "Название новой категории: " category
        python3 -c "
import json
with open('$KEYWORDS_FILE', encoding='utf-8') as f:
    data = json.load(f)
if '$category' in data['body_keywords']:
    print('Категория уже существует')
else:
    data['body_keywords']['$category'] = []
    data['subject_keywords']['$category'] = []
    with open('$KEYWORDS_FILE', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('Добавлена категория: $category')
"

    elif [ "$choice" = "3" ]; then
        read -p "Категория для удаления: " category
        python3 -c "
import json
with open('$KEYWORDS_FILE', encoding='utf-8') as f:
    data = json.load(f)
if '$category' not in data['body_keywords']:
    print('Категория не найдена')
else:
    del data['body_keywords']['$category']
    data['subject_keywords'].pop('$category', None)
    with open('$KEYWORDS_FILE', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('Удалена категория: $category')
"

    elif [ "$choice" = "4" ]; then
        read -p "Категория: " category
        read -p "Ключевое слово: " keyword
        python3 -c "
import json
with open('$KEYWORDS_FILE', encoding='utf-8') as f:
    data = json.load(f)
if '$category' not in data['body_keywords']:
    print('Категория не найдена')
elif '$keyword' in data['body_keywords']['$category']:
    print('Слово уже есть')
else:
    data['body_keywords']['$category'].append('$keyword')
    with open('$KEYWORDS_FILE', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('Добавлено: $keyword -> $category')
"

    elif [ "$choice" = "5" ]; then
        read -p "Категория: " category
        read -p "Ключевое слово для удаления: " keyword
        python3 -c "
import json
with open('$KEYWORDS_FILE', encoding='utf-8') as f:
    data = json.load(f)
if '$category' not in data['body_keywords']:
    print('Категория не найдена')
elif '$keyword' not in data['body_keywords']['$category']:
    print('Слово не найдено')
else:
    data['body_keywords']['$category'].remove('$keyword')
    with open('$KEYWORDS_FILE', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('Удалено: $keyword из $category')
"

    elif [ "$choice" = "6" ]; then
        echo "Выход"
        exit 0

    else
        echo "Неверный выбор"
    fi

done