# Сервис почтовых рассылок
# Курсовая работа по теме Django

## Задание 1 Разработка сервиса

Чтобы удержать текущих клиентов, часто используют вспомогательные, или «прогревающие», 
рассылки для информирования и привлечения клиентов.
Разработать сервис управления рассылками, администрирования и получения статистики.

### Описание задания

1. Реализовать интерфейс заполнения рассылок, то есть CRUD-механизм для управления рассылками.
2. Реализовать скрипт рассылки, который должен работать из командной строки и по расписанию.
3. Добавить настройки конфигурации для периодического запуска задачи.

### Сущности системы
1. Клиент сервиса:
- контактный email,
- ФИО,
- комментарий.
2. Рассылка (настройки):
- время рассылки;
- периодичность: раз в день, раз в неделю, раз в месяц;
- статус рассылки: завершена, создана, запущена.
3. Сообщение для рассылки:
- тема письма,
- тело письма.
4. Логи рассылки:
- дата и время последней попытки;
- статус попытки;
- ответ почтового сервера, если он был.

Создать связи между сущностями. Вы можете расширять модели для сущностей в 
произвольном количестве полей либо добавлять вспомогательные модели.

### Логика работы системы

1. После создания новой рассылки, если текущее время больше времени начала и 
меньше времени окончания, то должны быть выбраны из справочника все клиенты, 
которые указаны в настройках рассылки, и запущена отправка для всех этих клиентов.
2. Если создается рассылка со временем старта в будущем, то отправка должна 
стартовать автоматически по наступлению этого времени без дополнительных действий со стороны 
пользователя системы.
3. По ходу отправки сообщений должна собираться статистика 
(см. описание сущности «сообщение» и «логи» выше) 
по каждому сообщению для последующего формирования отчетов.
4. Внешний сервис, который принимает отправляемые сообщения, может долго обрабатывать запрос, 
отвечать некорректными данными, на какое-то время вообще не принимать запросы. 
Нужна корректная обработка подобных ошибок. Проблемы с внешним сервисом не должны влиять 
на стабильность работы разрабатываемого сервиса рассылок.

#### ‍Рекомендации

Реализовать интерфейс можно с помощью UI kit Bootstrap.
Для работы с периодическими задачами можно использовать либо crontab-задачи в чистом виде, 
либо изучить дополнительно библиотеку: https://pypi.org/project/django-crontab/

‍Периодические задачи — задачи, которые повторяются с определенной частотой, 
задаваемой расписанием.

crontab — классический демон, который используется для периодического выполнения заданий 
в определенное время. Регулярные действия описываются инструкциями, помещенными в файлы 
crontab и в специальные каталоги.

Служба crontab не поддерживается в Windows, но может быть запущена через WSL. 
Поэтому если вы работаете на этой ОС, то решите задачу запуска периодических задач 
с помощью библиотеки apscheduler: https://pypi.org/project/django-apscheduler/.

Подробную информацию, что такое crontab-задачи, найти самостоятельно.

## Задание 2 Доработка сервиса

Сервис по управлению рассылками пользуется популярностью, однако запущенный MVP 
уже не удовлетворяет потребностям бизнеса.

Доработать веб-приложение.
1. Разделить права доступа для различных пользователей.
2. Добавить раздел блога для развития популярности сервиса в интернете.

### Описание задания

1. Расширить модель пользователя для регистрации по почте, а также верификации.
2. Добавить интерфейс для входа, регистрации и подтверждения почтового ящика.
3. Реализовать ограничение доступа к рассылкам для разных пользователей.
4. Реализовать интерфейс менеджера.
5. Создать блог для продвижения сервиса.

Использовать для наследования модель AbstractUser.

### Функционал менеджера

- Может просматривать любые рассылки.
- Может просматривать список пользователей сервиса.
- Может блокировать пользователей сервиса.
- Может отключать рассылки.
- Не может редактировать рассылки.
- Не может управлять списком рассылок.
- Не может изменять рассылки и сообщения.

### Функционал пользователя

Весь функционал дублируется из первой части курсовой работы.
Но теперь нужно следить за тем, чтобы пользователь не мог случайным образом изменить
чужую рассылку и мог работать только со своим списком клиентов и со своим списком рассылок.

### Продвижение

#### Блог

Реализовать приложение для ведения блога. При этом отдельный интерфейс реализовывать
не требуется, но необходимо настроить административную панель для контент-менеджера.

В сущность блога добавить поля:
- заголовок,
- содержимое статьи,
- изображение,
- количество просмотров,
- дата публикации.

#### Главная страница

Реализовать главную страницу в произвольном формате, но обязательно отобразите
следующую информацию:
- количество рассылок всего,
- количество активных рассылок,
- количество уникальных клиентов для рассылок,
- 3 случайные статьи из блога.

#### Кеширование

Для блога и главной страницы самостоятельно выбрать, какие данные необходимо кешировать,
а также каким способом необходимо произвести кеширование.

## Требования к выполнению

1. Интерфейс системы содержит следующие экраны: 
- список рассылок;
- отчет проведенных рассылок отдельно;
- создание рассылки;
- удаление рассылки;
- создание пользователя;
- удаление пользователя;
- редактирование пользователя.
2. Реализована вся требуемую логика работы системы.
3. Интерфейс понятен и соответствует базовым требованиям системы.
4. Все интерфейсы для изменения и создания сущностей, не относящиеся к стандартной админке, реализованы с помощью Django-форм.
5. Все настройки прав доступа реализованы верно.
6. Использованы как минимум два типа кеширования.
7. Решение выложено на GitHub.


### Запуск

WEB приложение по рассылке сообщений по электронной почте (и по номеру телефона).
Необходимо:

- установить зависимости из requirements.txt
- зарегистрироваться на sms.ru (для работы верификации по номеру телефона нужен ключ)
- убрать лишнее в названии .env и вставить соответствующие значения
- python manage.py runserver
- python manage.py csu
- python manage.py runapscheduler
