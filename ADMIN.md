# Маршрут администратора

## 1. Клонировать репозиторий

```bash
git clone git@github.com:Saagilat/tes3mp-easy-setup.git
cd tes3mp-easy-setup
```

---

## 2. Установить сервер

Запустите скрипт установки на вашем сервере (VPS):

```bash
curl -fsSL https://raw.githubusercontent.com/Saagilat/tes3mp-easy-setup/master/server_setup/scripts/install.sh | bash
```

Или скачайте и запустите вручную:

```bash
wget https://raw.githubusercontent.com/Saagilat/tes3mp-easy-setup/master/server_setup/scripts/install.sh
sudo bash install.sh
```

Скрипт установит Docker, скачает TES3MP сервер, настроит конфиги и запустит контейнер.

---

## 3. Настроить SSH-доступ и алиас

Чтобы отправлять моды на сервер одной командой, настройте SSH-ключ:

```bash
ssh-keygen -t ed25519
ssh-copy-id root@ваш-сервер.или-ip
```

Проверьте подключение:

```bash
ssh root@ваш-сервер.или-ip
```

Добавьте алиас в `~/.bashrc` или `~/.bash_aliases`:

```bash
alias tes3mp-easy-имя-сервера='bash ~/tes3mp-easy-setup/tools/linux/tes3mp-server-update-mods'
```

Примените изменения:

```bash
source ~/.bashrc
```

---

## 4. Выгрузить моды

Отредактируйте конфиг синхронизации:

```bash
nano tools/linux/tes3mp-server-update-mods.conf
```

Укажите сервер и локальные папки с модами:

```
SSH_HOST=root@ваш-сервер.или-ip
PLUGINS_DIR=/путь/к/вашим/plugins
SERVER_SCRIPTS_DIR=/путь/к/вашим/server-scripts
```

Поместите файлы модов (`.esp`/`.esm`/`.omwaddon`) в папку `PLUGINS_DIR`,
а Lua-скрипты — в папку `SERVER_SCRIPTS_DIR`.

Запустите синхронизацию:

```bash
tes3mp-easy-имя-сервера
```

Скрипт скопирует все файлы на сервер и перезапустит контейнер.

---

## 5. Создать аккаунт администратора

1. **Зайдите в игру** через клиент TES3MP на вашем сервере
2. **Зарегистрируйтесь** — введите любой логин и пароль (первый зарегистрированный аккаунт получит ранг ServerOwner)
3. **Выйдите из игры**
4. **Остановите сервер:**

   ```bash
   ssh root@ваш-сервер.или-ip "cd /tes3mp-easy && docker compose down"
   ```

5. **Откройте файл игрока** и измените `staffRank`:

   ```bash
   ssh root@ваш-сервер.или-ip "nano /tes3mp-easy/container-data/server/data/player/<accountName>.json"
   ```

   Найдите секцию `settings` и установите нужный ранг:

   ```json
   "settings": {
       "staffRank": 3,
       ...
   }
   ```

   | Код | Ранг |
   |-----|------|
   | `0` | Обычный игрок |
   | `1` | Модератор |
   | `2` | Администратор |
   | `3` | Владелец сервера (ServerOwner) |

6. **Запустите сервер:**

   ```bash
   ssh root@ваш-сервер.или-ip "cd /tes3mp-easy && docker compose up -d"
   ```

Готово — теперь вы администратор сервера.