# Материалы, доступные по запросу

Публичный репозиторий уже содержит достаточные данные, чтобы понять ход
исследования и пересчитать его главные открытые выводы. Более глубокие
материалы выдаются не доступом к исходному архиву, а отдельными очищенными
пакетами.

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
