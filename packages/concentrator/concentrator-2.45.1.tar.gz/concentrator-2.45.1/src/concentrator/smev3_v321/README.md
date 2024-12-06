# Плагин "Взаимодействие с концентратором СМЭВ 3 (AIO)"

---

## Описание

Плагин реализует следующие изменения в системе:

* Добавляет сервис `FormDataMessageProcessingService` по обработке запросов \
СМЭВ (AIO) с типом ВС `FormData`;

* Добавляет задачу `FormDataMessageProcessingTask` по обработке запросов \
СМЭВ (AIO) с типом ВС `FormData`. \
Требуется, если необходимо инициировать обработку запросов СМЭВ (AIO) на \
стороне РИС;

* Добавляет обработчик `execute_get_provider_request` сигнала (`get_data_done`) \
для обработки запросов СМЭВ (`GetProviderRequest`) (AIO) в момент выполнения \
асинк. задачи в AIO client по получению их из AIO server;

* Добавлены репозиторий исполнителей сервисов и сами исполнители: \
(`ApplicationRequestExecutor`, `GetApplicationAdmissionRequestExecutor`, \
`GetApplicationQueueRequestExecutor`, `GetApplicationRequestExecutor`, \
`ApplicationOrderInfoRequestExecutor`, `GetApplicationQueueReasonRequestExecutor`, ...);

* Добавляет поля ответа и комментария заявителя в карточку направления;

* Добавляет manage-команду для присвоения заявлениям идентификатора ЕПГУ.

## Зависимости

Плагин имеет следующие зависимости:

* Плагин "Контингент" `kinder.plugins.contingent`.

## Подключение

**Важно: плагин не может быть одновременно подключен с плагином \
`concentrator.smev3`.**

Для подключения плагина необходимо:

1. Добавить в файл `plugins.conf` название плагина `concentrator.smev3_v321`.

    ```text

        [plugins]
        plugins =
            ...
            concentrator,
            kinder.plugins.contingent,
            concentrator.smev3_v321,
            ...

    ```

2. Добавить настройки в файл конфигурации концентратора `concentrator.conf` \
в блок `[webservice]`:

    ```text

        [webservice]
        SMEV3_FORM_DATA_TASK_EVERY_MINUTE = */5
        SMEV3_FORM_DATA_TASK_EVERY_HOUR = *
        SMEV3_FORM_DATA_MESSAGE_TYPE = FormData

        SMEV3_STATUS_CHANGE_TASK_EVERY_MINUTE = */5
        SMEV3_STATUS_CHANGE_TASK_EVERY_HOUR = *

        # URL-префикс к медиа файлам (чаще всего адрес РИС)
        ATTACHMENT_REQUEST_MEDIA_HOST = http://edu-kinder.test
        # Тип сообщений запросов AttachmentRequest
        ATTACHMENT_REQUEST_MESSAGE_TYPE = 'AttachmentRequest'

    ```

3. Накатить миграции для плагина:

    `python manage.py migrate`

4. Установить пакеты для работы latex:

    texlive-latex-base
    texlive-latex-extra
    texlive-fonts-recommended
    texlive-fonts-extra
    texlive-lang-cyrillic
    lmodern

## Ссылки

Задачи:

* [EDUKNDG-11192](https://jira.bars.group/browse/EDUKNDG-11192);
* [EDUKNDG-11350 Реализация хранения комментария в направлениях](https://jira.bars.group/browse/EDUKNDG-11350);
* [EDUKNDG-11432](https://jira.bars.group/browse/EDUKNDG-11432);
* [EDUKNDG-11201](https://jira.bars.group/browse/EDUKNDG-11201);
* [EDUKNDG-11198](https://jira.bars.group/browse/EDUKNDG-11198);
* [EDUKNDG-11200](https://jira.bars.group/browse/EDUKNDG-11200);
* [EDUKNDG-11196](https://jira.bars.group/browse/EDUKNDG-11196);
* [EDUKNDG-11199](https://jira.bars.group/browse/EDUKNDG-11199);
* [EDUKNDG-11448](https://jira.bars.group/browse/EDUKNDG-11448);
* [EDUKNDG-11538](https://jira.bars.group/browse/EDUKNDG-11538);
* [EDUKNDG-11447](https://jira.bars.group/browse/EDUKNDG-11447);
* [Реализация обработки запроса ApplicationAdmissionRequest](https://jira.bars.group/browse/EDUKNDG-11197);
* [Реализация синхронной обработки сообщений СМЭВ (AIO)](https://jira.bars.group/browse/EDUKNDG-13133).

Конфа:

* [Концентратор СМЭВ 3 (доработанный в соответствии с Приказом 1845).](https://conf.bars.group/pages/viewpage.action?pageId=108219268);

* [Интеграция ЭДС с ВС "Приём заявлений, постановка на учёт и зачисление детей в образовательные учреждения, реализующие основную образовательную программу дошкольного образования (детские сады)" версии 3.2.1](https://conf.bars.group/pages/viewpage.action?pageId=121655251#id-%D0%98%D0%BD%D1%82%D0%B5%D0%B3%D1%80%D0%B0%D1%86%D0%B8%D1%8F%D0%AD%D0%94%D0%A1%D1%81%D0%92%D0%A1%22%D0%9F%D1%80%D0%B8%D1%91%D0%BC%D0%B7%D0%B0%D1%8F%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B9,%D0%BF%D0%BE%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%D0%BD%D0%B0%D1%83%D1%87%D1%91%D1%82%D0%B8%D0%B7%D0%B0%D1%87%D0%B8%D1%81%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%D0%B4%D0%B5%D1%82%D0%B5%D0%B9%D0%B2%D0%BE%D0%B1%D1%80%D0%B0%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5%D1%83%D1%87%D1%80%D0%B5%D0%B6%D0%B4%D0%B5%D0%BD%D0%B8%D1%8F,%D1%80%D0%B5%D0%B0%D0%BB%D0%B8%D0%B7%D1%83%D1%8E%D1%89%D0%B8%D0%B5%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D1%83%D1%8E%D0%BE%D0%B1%D1%80%D0%B0%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D1%83%D1%8E%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D1%83%D0%B4%D0%BE%D1%88%D0%BA%D0%BE%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%D0%BE%D0%B1%D1%80%D0%B0%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F(%D0%B4%D0%B5%D1%82%D1%81%D0%BA%D0%B8%D0%B5%D1%81%D0%B0%D0%B4%D1%8B)%22%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D0%B83.2.0-3.4%D0%9E%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%D0%BF%D0%BE%D0%BB%D0%B5%D0%B9%D0%BE%D1%82%D0%B2%D0%B5%D1%82%D0%B0).
