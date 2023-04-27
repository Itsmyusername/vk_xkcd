# Публикация комиксов

Программа скачивает рандомный комикс xkcd и публикует его в группе ВК.

## Окружение

### Как установить

Python3 должен быть уже установлен. Также установите зависимости:

```bash
pip install -r requirements.txt
```

Для работы скрипта нужна регистрация на ВК, необходимо создать группу для постинга, приложение ВК https://vk.com/dev.
Для созданного приложения необходимо получить client_id на странице настроек приложения. 
Далее необходимо получить персональный access_token путем перехода по ссылке:
```
https://oauth.vk.com/authorize?client_id={client_id_приложения}&display=page&scope=groups,photos,wall,notify,stats&response_type=token&v=5.103&
```
Так же нужно получить id вашей группы ВК - http://regvk.com/id/
После регистрации создайте текстовый файл .env, в который запишите следующее:
```
GROUP_ID=id_вашей_группы
VK_TOKEN=ваш_access_token
```

## Запуск

Для запуска в консоли:

```bash

$ python main.py

```