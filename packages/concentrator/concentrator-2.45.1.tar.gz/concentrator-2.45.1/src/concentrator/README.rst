Плагин взаимодействия с концентратором
==================================================

Обеспечивает взаимодействия с сервисами концентратора.

Для подключения плагина нужно выполнить следующее:

1. Добавить в ``plugins.conf`` concentrator

*Например:*
::

    [plugins]
    plugins = kinder.plugins.notify




2. В общем конфиге садов Kinder.conf должны быть настройки подписи для смэва:

*Например:*
::

    [kinder]
    #мнемоника нашей системы
    SMEV_SYS_MNEMONICS = REGS12345
    #наименование нашей системы
    SMEV_SYS_NAME = Тюменьская область
    #мнемоника ЕПГУ
    SMEV_EPGU_MNEMONIC = RTK001001
    #наименование системы ЕПГУ
    SMEV_EPGU_NAME = РосТелеком
    # Пароль для .pem файла
    SMEV_PRIVKEY_PASS = /tmp/pem.pem
    #путь до pem файла
    SMEV_CERT_AND_KEY = 0000


3. В папку с конфигурационными файлами системы скопировать файл kinder/plugins/concentrator/concentrator.conf.default и переименовать его в concentrator.conf.
   Добавить в него следующие настройки:

*Например:*
::

    [webservice]
    # Код региона, использующийся в смэв сервисах плагина "Концентратор" (16 -Татарстан, 72 -Тюмень)
    SMEV_CONCENTRATOR_REG_CODE =
    # Путь до сервисов концентратора (Полный пусть до wsdl. Например: http://46.61.231.190/ServiceDelivery/ServiceDelivery.wsdl)
    SMEV_CONCENTRATOR_WSDL_URL =
    #tns Для веб сервисов (http://concentrator.gosuslugi.ru/regservicedelivery/smev)
    TNS =
    #настройка добавления xsi:type в запросе и ответе
    ADDXSITYPE = True
    # Отдавать детальную очередь в сервисе
    GET_APPQ_FULL = True
    # Устанавливать тип уведомления по указанным контактным данным
    SET_NOTIFICATION_TYPE = False

4.  В папку с конфигурационными файлами системы скопировать файл kinder/plugins/concentrator/wsfactory_config.xml.default и переименовать в wsfactory_config.xml

В файле прописать:


*Например:*
::

<Param key="certificate_path" valueType="string">/tmp/pem.pem</Param>
<Param key="private_key_path" valueType="string">/tmp/pem.pem</Param>
<Param key="private_key_pass" valueType="string">1111</Param>

Пути до фалов конфигирации в этом файле должны совпадать с аналогичными настройками в kinder.conf, из пункта 2.

Также необходимо продублировать TNS Настройку из 3 пункта в теге Application в атрибуте tns

*Например:*
::

<Application name="RegServiceDelivery" service="ConcentratorService" tns='http://concentrator.gosuslugi.ru/regservicedelivery/smev'>



5. Накатить миграции:

*Например:*
::

    $ python manage.py migrate


Описание менеджмент команд
------------------------------
Команда отправки информации по справочникам на синхронизацию в концентратор

python manage.py send_dicts_to_concentrator -U --size 500

-U - необязательный ключ.
    Указание этого ключа включает отправку информации по справочникам на обновление.
    По умолчанию информация отправляется на добавление
--size -необязательный ключ.
        Вместе с этим ключом нужно указать количество записей,
        которые будут переданы в одном соап-запросе
        при отсылке данных справочника
        'Образование.Организации.ДОО.Региональные.Статистика.ВозрастнаяГруппа'.
        По умолчанию принимает значение 500


Команда удаления исключенных из отображения ДОУ (#EDUKNDG-857)

python manage.py delete_excluded_units_from_concentrator --size 500

--size -необязательный ключ.
        Вместе с этим ключом нужно указать количество записей,
        которые будут переданы в одном соап-запросе
        По умолчанию принимает значение 500
