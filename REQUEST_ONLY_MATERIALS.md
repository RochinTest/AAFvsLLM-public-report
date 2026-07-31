# Материалы, доступные по запросу

Публичный репозиторий уже содержит данные, достаточные для понимания хода
исследования и пересчёта **опубликованных открытых выводов**. Это не означает,
что опубликованы полный runtime, все raw witnesses или весь исторический архив.
Более глубокие материалы выдаются не доступом к исходному архиву, а отдельными
очищенными пакетами.

## Что уже открыто

- [автономный verifier](verify_public_evidence.py);
- [SHA-256 manifest](evidence/public/manifest.json);
- [целостность retained V3](evidence/public/v3_integrity.json);
- [характеризация конфликтов](evidence/public/conflict_characterization.json);
- [пластичность и экономика](evidence/public/three_questions.json);
- [проверка невыразимости](evidence/public/nonexpressibility.json);
- [описание открытых evidence-capsules](evidence/README.md);
- [реестр утверждений и ограничений](docs/EVIDENCE_LEDGER.md).

Команда локального пересчёта:

```bash
python3 verify_public_evidence.py
```

Публичный verifier пересчитывает только раскрытые данные. Он не доказывает
полную воспроизводимость закрытого runtime и не заменяет независимую внешнюю
репликацию.

## Пакеты по запросу

| ID пакета | Возможное содержимое | Не входит |
|---|---|---|
| `AAF-CORE-SANITIZED` | архитектурное ядро, основные контракты и минимальная dependency closure | shell/server, Turbo-память, сессии, старая история |
| `RETAINED-V3-REPRO` | выбранные компоненты V3, manifest, verifier и обезличенные cases | authority records, локальные пути, рабочие журналы |
| `CONFLICT-WITNESSES` | raw cases конфликтного court и независимый пересчёт | server logs, process/environment dumps, личные данные |
| `PLASTICITY-WITNESS` | выбранные cases, tensor-метрики, checkpoint fingerprints и harness | модели или данные с неясными правами |
| `SYNTHESIS-FALSIFICATION` | AST, пространство кандидатов, controls и verifier | unrelated runtime/source tree |

Каждый пакет перед выдачей получает собственный manifest, проверку лицензий,
удаление локальных путей и персональных данных. Совпадение имени пакета с
материалом приватного архива не означает автоматической доступности всего
каталога.

## Не выдаётся стандартным запросом

- исходники и конфигурация сервера;
- Turbo-память, связанные модели и удалённые model caches;
- runtime-сессии, prompts, telemetry и operator journals;
- старые branches, tags, pull requests, Git metadata и reflogs;
- authority secrets, write-guard credentials и необработанные process traces;
- сторонний код и архивы с неустановленными правами распространения.

[Подать запрос](https://github.com/RochinTest/AAFvsLLM-public-report/issues/new?template=code-access.yml)
