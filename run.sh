#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INBOX="$SCRIPT_DIR/inbox"
OUTPUT="$SCRIPT_DIR/output"
LOG="$SCRIPT_DIR/run.log"

echo "=== mail-classifier ===" | tee "$LOG"
echo "Дата запуска: $(date)" | tee -a "$LOG"

if [ ! -d "$INBOX" ]; then
    echo "Ошибка: папка inbox не найдена" | tee -a "$LOG"
    exit 1
fi

MAIL_COUNT=$(find "$INBOX" -maxdepth 1 -type f ! -name ".*" | wc -l | tr -d ' ')
echo "Писем в inbox: $MAIL_COUNT" | tee -a "$LOG"

if [ "$MAIL_COUNT" -eq 0 ]; then
    echo "Inbox пуст, нечего обрабатывать" | tee -a "$LOG"
    exit 0
fi

mkdir -p "$OUTPUT"

echo "" | tee -a "$LOG"
python3 "$SCRIPT_DIR/src/main.py" 2>&1 | tee -a "$LOG"
EXIT_CODE=${PIPESTATUS[0]}

echo "" | tee -a "$LOG"
if [ $EXIT_CODE -eq 0 ]; then
    echo "Статус: успешно завершено" | tee -a "$LOG"
else
    echo "Статус: завершено с ошибкой (код $EXIT_CODE)" | tee -a "$LOG"
fi

exit $EXIT_CODE