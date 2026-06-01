import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from mail_reader import MailReader
from mail_classification import MailClassifier

def main():
    inbox_path = Path(__file__).parent.parent / "inbox"
    output_path = Path(__file__).parent.parent / "output"
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Читаем письма из: {inbox_path}")

    reader = MailReader(inbox_path)
    classifier = MailClassifier()

    try:
        results = reader.read_all()
    except (FileNotFoundError, NotADirectoryError) as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

    stats = {}
    errors = []
    log_lines = []

    for path, message, error in results:
        if error:
            errors.append((path.name, error))
            log_lines.append(f"{path.name} -> skipped: {error}")
            continue

        category = classifier.classify_mail(message)
        stats[category] = stats.get(category, 0) + 1
        log_lines.append(f"{path.name} -> {category}")

        dest_dir = output_path / category
        dest_dir.mkdir(parents=True, exist_ok=True)

        dest = dest_dir / path.name
        if not dest.exists():
            import shutil
            shutil.move(path, dest)

    print("\n=== Результаты классификации ===")
    for category, count in sorted(stats.items()):
        print(f"  {category}: {count} писем")

    if errors:
        print(f"\n=== Пропущено файлов: {len(errors)} ===")
        for name, reason in errors:
            print(f"  {name}: {reason}")

    total = sum(stats.values())
    print(f"\nВсего обработано: {total} писем")

    log_path = output_path / "processing.log"
    log_text = "\n".join(log_lines)
    log_path.write_text(log_text, encoding="utf-8")

    print(f"Лог обработки сохранён в файл: {log_path}")

if __name__ == "__main__":
    main()