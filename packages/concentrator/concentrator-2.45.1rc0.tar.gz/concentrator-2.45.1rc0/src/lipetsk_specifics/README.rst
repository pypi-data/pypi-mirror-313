Плагин взаимодействия с концентратором
==================================================

Обеспечивает взаимодействия с сервисами концентратора.
Перекрыты грид льгот, формы добавления и редактирования льготы.
Перекрыты следующие методы концентратора:
    NewApplicationRequest
    GetApplicationRequest
    UpdateApplicationRequest
    CheckDeclarationDOU

Для подключения плагина нужно выполнить следующее:

1. Добавить в ``plugins.conf`` lipetsk_specifics после concentrator, порядок ВАЖЕН!

*Например:*
::

    [plugins]
    ...
    concentrator,
    lipetsk_specifics,
    ...

Если версия продукта >= 2.26.0, необходимо также подключить плагин
::
    kinder.plugins.privilege_attributes,

2. В папку с конфигурационными файлами системы скопировать файл kinder/plugins/lipetsk_specifics/wsfactory_config.xml.default и переименовать его в wsfactory_config.xml.
В файле прописать:


*Например:*
::

<Param key="certificate_path" valueType="string">/tmp/pem.pem</Param>
<Param key="private_key_path" valueType="string">/tmp/pem.pem</Param>
<Param key="private_key_pass" valueType="string">1111</Param>


Указать TNS теге Application в атрибуте tns

*Например:*
::

<Application name="RegServiceDelivery" service="ConcentratorService" tns='http://concentrator.gosuslugi.ru/regservicedelivery/smev'>


3. Накатить миграции:

*Например:*
::

    $ python manage.py migrate
