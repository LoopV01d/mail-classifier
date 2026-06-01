import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from mail_reader import MailReader
from mail_classification import MailClassifier
from category_config import ConfigurableClassifier, ConfigError

def main():
    parser = argparse.ArgumentParser(description="Сортировщик корпоративной почты")
    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help='Путь к JSON-конфигу категорий (расширение). Без флага — захардкоженные правила.'
    )
    args = parser.parse_args()

    inbox_path = Path(__file__).parent.parent / "inbox"
    output_path = Path(__file__).parent.parent / "output"

    print(f"Читаем письма из: {inbox_path}")

    reader = MailReader(inbox_path)

    if args.config:
        try:
            classifier = ConfigurableClassifier(args.config)
            print(f"Режим: расширение, конфиг {args.config}")
        except ConfigError as e:
            print(f"Ошибка конфига: {e}")
            sys.exit(2)
    else:
        classifier = MailClassifier()
        print("Режим: базовый (захардкоженные правила)")

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

if __name__ == "__main__":
    main()