APPLICATION_ORDER_INFO_REQUEST = 'ApplicationOrderInfoRequest'

APPLICATION_ORDER_INFO_REQUEST_SUCCESS_COMMENT = (
    'Данные заявления переданы в Личный кабинет портала госуслуг')
APPLICATION_ORDER_INFO_REQUEST_ERROR_COMMENT = (
    'Заявление по указанным параметрам не найдено')

DECLARATION_ERROR_COMMENT = (
    'Передача данных заявления невозможна, так как в заявлении не заполнены')
APPLICATION_ORDER_INFO_REQUEST_DELEGATE_ERROR_COMMENT = (
    f'{DECLARATION_ERROR_COMMENT} сведения о заявителе')
APPLICATION_ORDER_INFO_REQUEST_CHILD_DATA_ERROR_COMMENT = (
    f'{DECLARATION_ERROR_COMMENT} данные ребенка:')
APPLICATION_ORDER_INFO_REQUEST_DELEGATE_DATA_ERROR_COMMENT = (
    f'{DECLARATION_ERROR_COMMENT} данные заявителя:')

SUBSCRIPTION_UNAVAILABLE_COMMENT = (
    'Не предусмотрена возможность подписаться на информирование по заявлению, '
    'поданному через ЕПГУ. Актуальную информацию о статусе заявления '
    'можно отслеживать в личном кабинете на ЕПГУ.'
 )