# План: Рефакторинг импорта/экспорта — разделение стадий

## Мотивация
Текущая архитектура смешивает доставку архива и его развёртывание.
Нужно разделить:
1. **Stage 1 — Валидация и хранение** (принять архив, проверить, сохранить)
2. **Stage 2 — Развёртывание** (остановить сервер, бэкап, накат, запуск)

---

## Моды

### Формат архива (без изменений)
```
mods.tar.gz
├── plugins/
│   ├── mod1.esp
│   ├── mod2.omwaddon
│   └── requiredDataFiles.json
└── scripts/
    └── test.lua
```

### Доставка (`tes3mp-easy-export-mods`)
- [ ] 0) Пользователь запускает клиент
- [ ] 1) Пакет модов + валидация CRC32 (как сейчас)
- [ ] 2) SCP на сервер в `/tes3mp-easy/import-mods/`
- [ ] 3) SSH `bash scripts/import_mods.sh` — приём и валидация
- [ ] 4) SSH `bash scripts/deploy_mods.sh --latest` — развёртывание последнего архива

### Приём и валидация (`import_mods.sh`)
- [ ] 1) Проверяет архив на целостность (CRC32 из requiredDataFiles.json)
- [ ] 2) Если ок — перемещает в `import-mods/validated/<timestamp>-mods.tar.gz`
- [ ] 3) Если нет — удаляет, пишет ошибку
- [ ] 4) Сервер **НЕ останавливает**

### Развёртывание (`deploy_mods.sh`)
Принимает аргумент — имя архива (или `--latest`).

- [ ] 1) Останавливает TES3MP
- [ ] 2) Проверить, нужно ли бэкапить текущие моды:
       - Если `backups/current_mods_deployed.txt` существует и
         архив с указанным в нём именем есть в `validated/` → бэкап НЕ нужен
       - Иначе → сделать бэкап текущих модов через `package_mods_and_scripts`
         и записать имя нового архива в `current_mods_deployed.txt`
- [ ] 3) Очистить `server/data/` от модов:
       - Удалить всё из `server/data/` кроме `player/`, `cell/`, `requiredDataFiles.json`
- [ ] 4) Распаковать выбранный архив модов в `server/data/`
- [ ] 5) Копирует плагины из `server/data/` обратно в `plugins/` (для HTTP-дистрибуции)
- [ ] 6) Генерирует `customScripts.lua`
- [ ] 7) Копирует `requiredDataFiles.json` в `server/data/` (если ещё не там)
- [ ] 8) Создаёт `mods.tar.gz` для nginx
- [ ] 9) Запускает TES3MP

### Восстановление бэкапа (restore)
- [ ] Админ может выбрать бэкап из `backups/` и накатить его вместо последнего архива
- [ ] `bash deploy_mods.sh --backup <backup_file>` — то же самое, но вместо архива берёт бэкап

---

## Игроки

### Формат архива
```
players.tar.gz
├── player/
│   └── AccountName1.json
└── requiredDataFiles.json   (для отладки)
```

### Доставка + применение (`tes3mp-easy-export-players`)
- [ ] 0) Клиент пакует игроков
- [ ] 1) SCP на сервер
- [ ] 2) SSH `bash import_players.sh`

### import_players.sh
- [ ] 1) Бэкап текущих игроков
- [ ] 2) Останавливает TES3MP (чтобы данные на диске были консистентны)
- [ ] 3) Очищает папку `player/` (удалить всё содержимое)
- [ ] 4) Распаковывает архив поверх данных
- [ ] 5) Запускает TES3MP
- [ ] 6) Очищает import-players/

### restore игроков с сервера
- [ ] `bash restore_players.sh` — показывает список бэкапов, позволяет выбрать
- [ ] Останавливает сервер, накатывает, запускает

---

## Мир (ячейки)

### Формат архива
```
cells.tar.gz
├── cell/
│   └── -1_-2.json
└── requiredDataFiles.json   (для отладки)
```

### Доставка + применение (`tes3mp-easy-export-cells`)
- [ ] 0) Клиент пакует ячейки
- [ ] 1) SCP на сервер
- [ ] 2) SSH `bash import_cells.sh`

### import_cells.sh
- [ ] 1) Бэкап текущих ячеек
- [ ] 2) Останавливает TES3MP
- [ ] 3) Очищает папку `cell/` (удалить всё содержимое)
- [ ] 4) Распаковывает архив поверх данных
- [ ] 5) Запускает TES3MP
- [ ] 6) Очищает import-cells/

### restore мира с сервера
- [ ] `bash restore_cells.sh` — показывает список бэкапов, позволяет выбрать
- [ ] Останавливает сервер, накатывает, запускает

---

## requiredDataFiles.json в world/players

- [ ] `package_players()` — добавить requiredDataFiles.json в архив
- [ ] `package_cells()` — добавить requiredDataFiles.json в архив
- [ ] На сервере при импорте сохранять файл (но не обрабатывать)
- [ ] Нужно только для отладки (админ видит, на какой сборке были эти данные)

---

## clean_data.tar.gz

Отложено. Нужно сначала изучить, что реально лежит в `server/data/` на свежеустановленном сервере.
Возможно, clean_data не нужен — достаточно просто удалять всё, кроме player/ и cell/.

---

## Очерёдность (что делать в первую очередь)

1. `package.sh` — добавить requiredDataFiles.json в players/cells архивы
2. `import_cells.sh` — очищать папку cell/ перед распаковкой
3. `import_players.sh` — добавляем остановку сервера + очистку папки player/
4. `import_mods.sh` — разделить на import (приём/валидация) + deploy (развёртывание)
5. Создать `deploy_mods.sh` с логикой бэкапа по current_mods_deployed.txt
6. Создать `restore_players.sh`, `restore_cells.sh`, `restore_mods.sh`
7. `tes3mp-easy-export-mods` — изменить под новую архитектуру