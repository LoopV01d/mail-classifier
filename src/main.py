import sys
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from mail_reader import MailReader
from mail_classification import MailClassifier

def main():
    inbox_path = Path(__file__).parent.parent / "inbox"
    output_path = Path(__file__).parent.parent / "output"

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

    for path, message, error in results:
        if error:
            errors.append((path.name, error))
            unprocessed_dir = output_path / "unprocessed"
            unprocessed_dir.mkdir(parents=True, exist_ok=True)
            dest = unprocessed_dir / path.name
            if not dest.exists():
                shutil.move(path, dest)
            continue

        category = classifier.classify_mail(message)
        stats[category] = stats.get(category, 0) + 1

        dest_dir = output_path / category
        dest_dir.mkdir(parents=True, exist_ok=True)

        dest = dest_dir / path.name
        if not dest.exists():
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

if __name__ == "__main__":
    main()