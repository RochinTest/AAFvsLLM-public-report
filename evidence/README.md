# Открытые evidence-capsules

Здесь находятся небольшие обезличенные наборы, достаточные для пересчёта
главных чисел публичного отчёта. Это не копии всего приватного `runs`-дерева и
не runtime системы.

| Файл | Что пересчитывается |
|---|---|
| [`public/v3_integrity.json`](public/v3_integrity.json) | число компонентов, размеры/хеши, manifest и guard mismatches |
| [`public/conflict_characterization.json`](public/conflict_characterization.json) | 35 normal-runtime строк, число conflict leaks и controls |
| [`public/three_questions.json`](public/three_questions.json) | held-out delta, tensor changes и economics accounting |
| [`public/nonexpressibility.json`](public/nonexpressibility.json) | принадлежность 24 AST известному fixed-chain пространству |
| [`public/manifest.json`](public/manifest.json) | SHA-256 четырёх evidence-capsules |

Запуск:

```bash
python3 verify_public_evidence.py
```

Verifier сначала сверяет четыре капсулы с manifest, затем заново получает
производные значения из строк и чисел. Итоговое слово `supported` или
`not_supported`, записанное внутри JSON, не используется как самостоятельное
доказательство.

## Граница воспроизводимости

Публичный набор позволяет проверить арифметику, структуру и внутреннюю
согласованность решающих выводов. Он не позволяет заново собрать AAF runtime
или повторить процессы без request-only пакетов. Такая граница обозначается в
каждом документе, а не скрывается за словом «sealed».

Per-case строки открыты для conflict characterization, plasticity и
fixed-chain targets. Исторический court V3, три изолированных repair-candidate
court и manifest/registry byte comparison представлены только как явно
помеченные агрегаты приватного аудита.

Полные raw cases и harness доступны только после отдельной очистки:
[перечень request-only пакетов](../REQUEST_ONLY_MATERIALS.md).
