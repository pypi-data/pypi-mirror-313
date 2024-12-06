import datetime
import logging

from suds.plugin import MessagePlugin


class UpdateStateSpikeNailPlugin(MessagePlugin):
    """Плагин-костыль для кривого концентратора"""

    def marshalled(self, context):

        method_node = context.envelope.childAtPath(
            "Body/UpdateApplicationStateRequest")

        ns0_prefix, ns0_uri = method_node.resolvePrefix("ns0")
        ns1_prefix, ns1_uri = method_node.resolvePrefix("ns1")

        # Меняем местами. Так требует концентратор. Не знаю зачем
        method_node.addPrefix("ns1", ns0_uri)
        # Жестко зашитый ns, потому как в запросе не используется.
        method_node.addPrefix(
            "cnt", "http://concentrator.gosuslugi.ru/servicedelivery/soap")
        method_node.applyns(("sdSmev", ns1_uri))

        # Проставляем всем кто, под UpdateApplicationState ns ns1.
        # Сейчас там ns0. К слову это одно и тоже.
        for elem in method_node.getChildren():
            elem.walk(lambda this: this.setPrefix("ns1"))

        # Внутри AppData namespace-в быть не должно
        app_data = method_node.childAtPath("MessageData/AppData/")
        for elem in app_data.getChildren():
            elem.setPrefix(None, None)


class FixPrefixPlugin(MessagePlugin):
    """
    Плагин - "Экзоскелет". Фиксит немспейсы в сформированном конверте.
    """

    SERVICE_NAME = ''

    def marshalled(self, context):

        message = context.envelope.childrenAtPath(
            'Body/%s/Message' % self.SERVICE_NAME)[0]
        message_data = context.envelope.childrenAtPath(
            'Body/%s/MessageData' % self.SERVICE_NAME)[0]
        sender = context.envelope.childrenAtPath(
            'Body/%s/Message/Sender' % self.SERVICE_NAME)[0]
        ns = sender.namespace()
        message.setPrefix(*ns)
        message_data.setPrefix(*ns)
        app_data = context.envelope.childrenAtPath(
            'Body/%s/MessageData/AppData' % self.SERVICE_NAME)[0]
        for elem in app_data.getChildren():
            elem.setPrefix(None, None)


class FixPrefixPluginUpdateApplicationState(FixPrefixPlugin):

    SERVICE_NAME = 'UpdateApplicationStateRequest'


class FixPrefixPluginLoadData(FixPrefixPlugin):

    SERVICE_NAME = 'LoadDataRequest'


class LogPlugin(MessagePlugin):

    def marshalled(self, context):
        """
        Логируем текст запроса
        """
        logging.info(u'Sending request to concentrator (%s):\n' % (
            datetime.datetime.strftime(datetime.datetime.now(), '%d.%m.%Y')))

        logging.info(str(context.envelope))

    def received(self, context):
        """
        Логируем текст ответа
        """
        logging.info(u'Get response from concentrator(%s):\n' % (
            datetime.datetime.strftime(datetime.datetime.now(), '%d.%m.%Y')))
        logging.info(str(context.reply))
