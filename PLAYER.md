# Маршрут игрока

## 1. Клонировать репозиторий

```bash
git clone git@github.com:Saagilat/tes3mp-easy-setup.git
cd tes3mp-easy-setup
```

---

## 2. Установить клиент

Выберите вашу операционную систему:

### Linux

[Инструкция по установке через Proton](docs/player/linux/proton/install.md)

### Windows

> Скоро будет добавлено

### macOS

> Скоро будет добавлено

---

## 3. Настроить шрифты

После первого запуска в папке `openmw-profile` появится файл `settings.cfg`.
Скопируйте в него готовый образец из репозитория:

```bash
cp tools/linux/example-settings.cfg ~/openmw-profile/settings.cfg
```

Если папки `openmw-profile` ещё нет — создайте её вручную:

```bash
mkdir -p ~/openmw-profile
cp tools/linux/example-settings.cfg ~/openmw-profile/settings.cfg
```

> **Примечание:** Вместо `~/openmw-profile` укажите путь к вашей папке OpenMW.
> Linux (Proton): файл лежит рядом с `openmw.cfg`, путь настраивается на шаге 2.

---

## 4. (опционально) Установить локализацию

Выберите язык:

### Русский

```bash
bash tools/linux/localization/russian/install.sh
```

### Другие языки

> Будут добавлены позже

---

## 5. Заполнить tes3mp-client-default.cfg

Откройте файл `tes3mp-client-default.cfg` (рядом с `tes3mp.exe`) и укажите адрес сервера:

```
destinationAddress = ваш-сервер.или-ip
```

Порт по умолчанию: `25565`. Если порт нестандартный, укажите его:

```
destinationPort = 25565
```

---

## 6. Установить утилиту для скачивания модов

Скопируйте и отредактируйте конфиг:

```bash
cp tools/linux/tes3mp-client-update-mods.conf tools/linux/tes3mp-client-update-mods.conf.local
nano tools/linux/tes3mp-client-update-mods.conf.local
```

Укажите пути к вашим файлам:

```
CLIENT_DEFAULT=/путь/к/tes3mp-client-default.cfg
DATA_FILES=/путь/к/Data Files/
OPENMW_CFG=/путь/к/openmw.cfg
```

Запустите синхронизацию модов:

```bash
bash tools/linux/tes3mp-client-update-mods
```

Скрипт скачает моды с сервера, установит их в `Data Files/` и обновит `openmw.cfg`.

---

## 7. Зайти на сервер

1. Запустите `tes3mp.exe` через Steam
2. Введите логин и пароль для регистрации
3. Готово — вы на сервере!