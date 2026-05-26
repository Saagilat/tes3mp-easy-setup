# Admin Mods Upload

Скрипт для загрузки модов на сервер TES3MP.

## Файлы

- `tes3mp-mods-upload` — скрипт для отправки модов на сервер
- `tes3mp-mods-upload.conf` — пример конфигурации

## Как настроить

### 1. Отредактируйте конфиг

```bash
nano admin/linux/utilities/tes3mp-mods-upload.conf
```

### 2. Настройте SSH alias (чтобы работало `ssh tes3mp-server`)

Добавьте в `~/.ssh/config`:

```
Host tes3mp-server
    HostName 192.168.1.100       # IP-адрес вашего сервера
    User your_user               # Имя пользователя на сервере
    Port 22                      # Порт SSH (стандартный 22)
    IdentityFile ~/.ssh/id_rsa   # Путь к SSH-ключу (опционально)
```

Если нужно использовать SSH-ключ (рекомендуется), сгенерируйте его и скопируйте на сервер:

```bash
ssh-keygen -t ed25519 -C "tes3mp-admin"   # создать ключ
ssh-copy-id tes3mp-server                   # скопировать ключ на сервер
```

### 3. Запустите скрипт

```bash
./admin/linux/utilities/tes3mp-mods-upload
```

Скрипт синхронизирует вашу локальную папку модов с сервером и запустит `update_mods.sh`.

## Зависимости

- `bash`, `rsync`, `ssh`

## Переменные конфига

| Переменная  | Описание                           | Пример                     |
|-------------|------------------------------------|----------------------------|
| `SSH_HOST`  | SSH-хост (алиас или user@ip)       | `tes3mp-server`            |
| `MODS_DIR`  | Путь к локальной папке с модами    | `/home/user/tes3mp-mods`   |