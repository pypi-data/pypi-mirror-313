# Схeма ../templates/xsd/event.xsd

GenerateDSNamespaceDefs = {
    'EventServiceRequestType':
        'xmlns:ns="http://epgu.gosuslugi.ru/lk/order/event/3.1.1"',
}

GenerateDSNamespaceTypePrefixes = {
    # nsprefix_ для типа statusCodeType
    'statusCodeType': 'ns',
    'statusCodeType_orgCode': 'ns',
    'statusCodeType_techCode': 'ns',

    # nsprefix_ для типа OrderStatusEventType
    'OrderStatusEventType': 'ns',
    'OrderStatusEventType_statusCode': 'ns',
    'OrderStatusEventType_cancelAllowed': 'ns',
    'OrderStatusEventType_sendMessageAllowed': 'ns',

    # nsprefix_ для типа PaymentType
    'PaymentType': 'ns',
    'PaymentType_source': 'ns',
    'PaymentType_uin': 'ns',
    'PaymentType_description': 'ns',

    # nsprefix_ для типа PaymentStatusEventType
    'PaymentStatusEventType': 'ns',
    'PaymentStatusEventType_status': 'ns',
    'PaymentStatusEventType_payment': 'ns',

    # nsprefix_ для типа InfoEventType
    'InfoEventType': 'ns',
    'InfoEventType_code': 'ns',

    # nsprefix_ для типа TextMessageEventType
    'TextMessageEventType': 'ns',

    # nsprefix_ для типа organizationDataType
    'organizationDataType': 'ns',
    'organizationDataType_organizationId': 'ns',
    'organizationDataType_areaId': 'ns',

    # nsprefix_ для типа equeueInvitationType
    'equeueInvitationType': 'ns',
    'equeueInvitationType_organizationData': 'ns',
    'equeueInvitationType_startDate': 'ns',
    'equeueInvitationType_endDate': 'ns',

    # nsprefix_ для типа equeueClosedType
    'equeueClosedType': 'ns',

    # nsprefix_ для типа EqueueEventType
    'EqueueEventType': 'ns',
    'EqueueEventType_equeueInvitation': 'ns',
    'EqueueEventType_equeueClosed': 'ns',

    # nsprefix_ для типа EventType
    'EventType': 'ns',
    'EventType_orderStatusEvent': 'ns',
    'EventType_paymentStatusEvent': 'ns',
    'EventType_infoEvent': 'ns',
    'EventType_textMessageEvent': 'ns',
    'EventType_equeueEvent': 'ns',

    # nsprefix_ для типа EventServiceRequestType
    'EventServiceRequestType': 'ns',
    'EventServiceRequestType_env': 'ns',
    'EventServiceRequestType_orderId': 'ns',
    'EventServiceRequestType_eventDate': 'ns',
    'EventServiceRequestType_eventComment': 'ns',
    'EventServiceRequestType_eventAuthor': 'ns',
    'EventServiceRequestType_event': 'ns',

    # nsprefix_ для типа EventServiceResponseType
    'EventServiceResponseType': 'ns',
    'EventServiceResponseType_code': 'ns',
    'EventServiceResponseType_message': 'ns',
}
