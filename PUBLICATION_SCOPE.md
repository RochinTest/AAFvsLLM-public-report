# Граница публичной публикации

Этот репозиторий создан из новой чистой истории и содержит только материалы,
прошедшие отдельный просмотр перед публикацией. Это исследовательское досье,
а не поставка работающей системы.

## Включено

- исходная идея, цели и архитектурная гипотеза;
- хронология Memory Core, retained V3, кризиса доказательств и закрытия;
- статус основных гипотез и причины их пересмотра;
- обезличенные evidence-capsules с измеренными строками и хешами;
- небольшой автономный verifier только для открытых evidence-capsules;
- порядок ручного запроса отдельных очищенных материалов.

Публичные проверочные материалы доступны напрямую:

- [verifier](verify_public_evidence.py);
- [manifest](evidence/public/manifest.json);
- [V3 integrity capsule](evidence/public/v3_integrity.json);
- [conflict characterization capsule](evidence/public/conflict_characterization.json);
- [plasticity/economics capsule](evidence/public/three_questions.json);
- [nonexpressibility capsule](evidence/public/nonexpressibility.json);
- [evidence ledger](docs/EVIDENCE_LEDGER.md).

GitHub может скрывать часть файлов корня и вложенных каталогов за кнопкой
**View all files**. Отсутствие файла на первом экране не означает, что он не
опубликован; ссылки выше ведут к фактическим объектам в ветке `main`.

## Исключено

- весь исходный код работающей системы;
- исходники и конфигурация сервера;
- реализация Turbo-памяти и связанные модели;
- retained-компоненты, реестры и snapshots;
- runtime-сессии, prompts, caches и telemetry;
- сырые run-artifacts, screenshots и архивы;
- старые commits, branches, tags, pull requests и reflogs;
- абсолютные пути и сведения о локальной машине;
- сторонний код с неустановленными условиями распространения.

Публичный verifier не содержит runtime, модели, маршрутизации, specialist-
программ или скрытого доступа к приватному архиву. Исходный приватный архив не
изменён и не является частью этой публикации.

Подробнее: [что можно запросить](REQUEST_ONLY_MATERIALS.md) и
[как подать запрос](CODE_ACCESS.md).
