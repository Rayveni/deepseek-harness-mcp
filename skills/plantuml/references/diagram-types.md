# Варианты PlantUML — выбор и скелеты

Читать при непонятном вопросе запроса. Один основной вариант; метки на языке пользователя.

## Порядок выбора

1. Что меняется во времени? → Activity, Sequence, State, Timing.
2. Что существует в покое? → Component, Deployment, Class/ER, Use case.
3. Ни то ни другое (план, декомпозиция, сравнение)? → Gantt/WBS, Mindmap, двухстороннее сравнение.
4. Неясно? Самый дешёвый вариант + альтернатива одной строкой.

«Что читатель сделает с картинкой?» — отладка → sequence, ревью дизайна → component, управление → activity/сравнение.

## Activity (новый синтаксис) — процесс, шаги

Сигналы: процесс, алгоритм, шаги, сценарий, workflow, BPMN, ветвления.

```plantuml
@startuml
title Обработка заявки
start
:Получить заявку;
if (Данные полные?) then (да)
  :Проверить лимит;
  fork
    :Списать резерв;
  fork again
    :Уведомить клиента;
  end fork
  :Отправить в биллинг;
else (нет)
  :Запросить недостающее;
  stop
endif
stop
@enduml
```

Полезное: `|Отдел|` — дорожки; `partition "Этап" { ... }`; `detach` — терминал без заливки.

## Sequence — взаимодействие, порядок вызовов

Сигналы: обмен, API, запросы, интеграция, вызовы, handshake, retries, timeouts.

```plantuml
@startuml
title Выгрузка отчёта
actor Клиент
participant "front" as fe
participant "ПД API" as api
database "Платформа данных" as pd
Клиент -> fe : запросить отчёт
fe -> api : POST /export
activate api
api -> pd : запрос данных
pd --> api : набор данных
alt успех
  api --> fe : 200 + ссылка
else таймаут
  api --> fe : 504
end
deactivate api
@enduml
```

Полезное: `++`/`--` вместо activate/deactivate; `alt/opt/loop/par`; `autonumber`; `== Этап ==`.

## Component — архитектура, сервисы

Сигналы: архитектура, из чего состоит, сервисы, модули, интеграции, зависимости.

```plantuml
@startuml
title Целевая архитектура
skinparam componentStyle rectangle
package "Домен платежей" {
  component "payments" as pay
  component "реконсиляция" as rec #E1B12C
  interface "API" as api
}
component "Платформа данных" as pd
pay -[#5CB85C]-> pd : метрика
rec -[#5CB85C]-> pd
pd -[#5CB85C,bold]-> api
@enduml
```

Полезное: `package`/`frame`/`rectangle` — границы; `#E1B12C` — новое в целевом состоянии; стрелки — сообщение, коробки — существительные.

## Deployment — окружения, ноды

Сигналы: окружения, ноды, кластеры, развёртывание, инфраструктура, prod/dev, Kubernetes.

```plantuml
@startuml
title Prod-контур
node "k8s cluster" {
  node "namespace: payments" {
    artifact "payments-api" as api
    database "PostgreSQL" as db
  }
}
cloud "S3" as s3
api --> db
api --> s3 : выгрузки
@enduml
```

Полезное: `node`, `cloud`, `database`, `artifact`, `storage`; вкладывание нод — реальное содержание; протоколы и порты на стрелках.

## Class / ER — модель данных, схема БД

Сигналы: модель данных, сущности, таблицы, поля, связи, БД, домен, cardinality.

```plantuml
@startuml
title Модель счёта
entity "billing_account" as acc {
  * id : uuid <<PK>>
  --
  * client_id : uuid <<FK>>
  balance : numeric
}
entity "payment" as pay {
  * id : uuid <<PK>>
  * account_id : uuid <<FK>>
  amount : numeric
}
acc ||--o{ pay : "имеет"
@enduml
```

Полезное: `entity` — ER (crow's-foot), `class` — UML-классы; `*` — обязательно, `--` — разделитель, `<<PK>>`; только нужные атрибуты.

## State — жизненный цикл, статусы

Сигналы: статус, состояния, жизненный цикл, переходы, state machine, retry.

```plantuml
@startuml
title Жизненный цикл платежа
state "Создан" as created
state "В обработке" as processing
state "Успех" as done
state "Ошибка" as failed
[*] --> created
created --> processing : отправлен
processing --> done : подтверждён
processing --> failed : отказ
failed --> processing : повтор
done --> [*]
@enduml
```

Полезное: `state "имя" as alias { ... }` — составные; `[*]` — начальное/конечное; переходы подписаны событиями. Имена состояний с пробелами/не-ASCII — только через `as`, иначе сервер откажет.

## Use case — роли и возможности

Сигналы: роли, акторы, кто что может, возможности, требования.

```plantuml
@startuml
left to right direction
actor Клиент as c
actor "Оператор" as op
rectangle "Личный кабинет" {
  usecase "Смотреть баланс" as uc1
  usecase "Оспорить платёж" as uc2
}
c --> uc1
op --> uc2
@enduml
```

## Gantt / WBS — планы и декомпозиция

Сигналы: сроки, этапы, план, дорожная карта, декомпозиция, work breakdown.

```plantuml
@startgantt
title План миграции
Project starts 2026-01-12
[Аудит данных] lasts 10 days
[Перенос] lasts 20 days
[Перенос] starts at [Аудит данных]'s end
[Приёмка] lasts 5 days
[Приёмка] starts at [Перенос]'s end
@endgantt
```

Полезное: `@startwbs` с `*` — дерево; `@startmindmap` — брейншторм; только когда время/иерархия и есть ответ.

## AS IS / TO BE — сравнение

Сигналы: AS IS / TO BE, было / стало, сравнить, до и после.

```plantuml
@startuml
title Сравнение: AS IS vs TO BE
package "Вариант 1" #F9F9F9 {
  frame "AS IS" #FFF0F0 {
    component "billing" as b1
    component "архив" as a1
    b1 -[#D9534F]-> a1 : "перенос руками"
  }
  frame "TO BE" #F0FFF0 {
    component "billing" as b2
    component "архив" as a2 #E1B12C
    component "front" as f2 #E1B12C
    b2 -[#5CB85C]-> a2 : "перенос"
    a2 -[#5CB85C,bold]-> f2 : "API"
  }
}
legend bottom
  |= Цвет |= Значение |
  |<#D9534F>| AS IS |
  |<#5CB85C>| TO BE |
  |<#E1B12C>| Новый компонент |
endlegend
@enduml
```

Полезное: обе стороны — один вариант и одни имена; >2 вариантов или >15 элементов на сторону — отдельная диаграмма на вариант.

## Прочие

`timing` — сигналы во времени, `object` — снимок экземпляра, `json`/`yaml` — структура payload, `salt` — wireframes, `nwdiag` — сети. Только когда запрос называет потребность.

## Важно

PlantUML терпит нестрогий синтаксис — незакрытая метка может молча проглотить строки. Всегда рендерь (минимум `puml_check_source`) перед выдачей; читай картинку при длинных не-ASCII метках. Диаграмма попадает на диск пользователя только после подтверждения сохранения.
