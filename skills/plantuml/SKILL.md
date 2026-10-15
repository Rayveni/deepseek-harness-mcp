---
name: plantuml
description: >-
  Диаграммы PlantUML по запросу «нарисуй/визуализируй/покажи схему» (нотация не названа): процесс, архитектура, взаимодействие, модель данных, жизненный цикл, сравнение. Предлагай исходник в чате вместе с отрендеренной картинкой, доводи правками, сохраняй .puml и изображение только после подтверждения; также чинит/переоформляет/рендерит существующий .puml.
  Turn a "draw me a diagram" request into PlantUML. Use when the user asks to draw, visualize, or diagram a process, architecture, interaction, data model, lifecycle, or comparison without naming a notation - propose the source in chat with its rendered picture, iterate, and write the .puml plus image to disk only after the user confirms. Also use to fix, restyle, or render an existing .puml file.
---

# Диаграмма → PlantUML

Инструменты MCP `mcp-plantuml`: `puml_check_source`, `puml_render`, `puml_encode`, `puml_list_types`, `puml_skeleton`. Аргументы — в схемах инструментов; здесь только правила.

**Порядок работы:**

1. **Прочитать** запрос, выбрать вариант (§1).
2. **Предложить в чате**: полный исходник в блоке ```plantuml + картинка, отрендеренная MCP (`puml_render`, `output_format=png`), в одном сообщении; одной строкой — вариант и почему, предположение, запасной вариант.
3. **Итерации**: правки → снова `puml_render` → снова исходник + свежая картинка.
4. **Предложить сохранение** (§4) — точные пути, ждать подтверждения.
5. **Сохранить** только после подтверждения: `.puml` (write) + изображение (base64 из `puml_render` → файл), показать картинку, `present` обоих файлов.

Код и картинка — одно ответ. Ничего в рабочую директорию до подтверждения пользователя.

## 1. Выбор варианта

Полная карта, сигналы и скелеты — в [references/diagram-types.md](references/diagram-types.md). Частое:

| Запрос | Вариант |
| --- | --- |
| Как работает пошагово? | Activity (новый синтаксис) |
| Кто кого вызывает, порядок? | Sequence |
| Из чего состоит? | Component |
| Какие состояния? | State |
| Модель данных? | Class / ER |
| Где работает? | Deployment |
| Кто что может? | Use case |
| План? | Gantt / WBS |
| AS IS / TO BE | Component/Activity с `package`+`frame` на сторону |

Одна диаграмма = один вопрос. Проще вариант, несущий смысл. Альтернативы обсуждаются в чате, а не молча записаны в файл.

## 2. Правила исходника

`@startuml/@enduml`, `title`, явные `skinparam`.

- Закрывай кавычки: незакрытая метка `: "текст` молча проглатывает строки до конца.
- Явные алиасы: `component "billing (архив)" as ba1`, далее `ba1`.
- Цвет стрелок по смыслу (`-[#D9534F]->` текущее, `-[#5CB85C,bold]->` целевое) + `legend`.
- `skinparam componentStyle rectangle`, `skinparam shadowing false`, `skinparam backgroundColor #FFFFFF`.
- Метки на языке пользователя, алиасы ASCII.
- Состояния с пробелами/не-ASCII — только через `state "Имя" as alias`.
- ~30+ элементов: разбить по сценариям.

## 3. Проверка и рендер

```
puml_check_source(source=<исходник>)  → синтаксис без файлов
puml_render(source=<исходник>, output_format="png")  → base64 картинки
```

- `puml_render` — один запуск java; синтаксические ошибки вернёт сам (как `SYNTAX ERROR`). Картинка приходит в строке `base64_<fmt>` — декодируй и покажи.
- Ошибка `SYNTAX ERROR` — правь по сообщению, рендерь снова. `RENDER FAILED` — проблема локального рендера (java/jar), не диаграммы; скажи и повтори позже.
- Черновой render — только в scratch (`${TMPDIR:-/tmp}/plantuml-draft/`); финальный save — только в подтверждённый путь.
- Рендер локальный (plantuml.jar внутри MCP-сервера) — исходник не покидает машину. Если картинки нет (java/jar недоступны), скажи явно, выложи проверенный исходник + `puml_encode` URL.

## 4. Сохранение

Предложи точные пути (kebab-case; `.png` для ревью, `.svg` для доков) и остановись. Явно названный в запросе путь — предразрешение. Согласованный исходник сохраняй дословно; PNG рядом; картинку прочитай перед показом; абсолютные пути + `present`. Отказ — исходник + URL в чат.
