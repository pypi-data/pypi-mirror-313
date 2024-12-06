# coding: utf-8

from educommon.ws_log.models import SmevLog
from spyne_smev.client import Client


class SmevClient(Client):
    """
    Перекрываем стандартный клиент spyne_smev'a
    для возможности логирования запросов в SmevLog
    """

    def log_request(self, smev_method, error=None):
        """
        Логирование запросов в SmevLogs
        :param error: Текст ошибки
        :param smev_method: наименование метода смэв
        """
        log_params = dict(
            service_address=self.wsdl.url,
            direction=SmevLog.OUTGOING,
            interaction_type=SmevLog.IS_SMEV,
            method_name=smev_method,
            request=self.last_sent(),
            response=self.last_received()
        )
        if error:
            log_params.update(result=error)
        log = SmevLog(**log_params)
        log.save()
        return log

    def last_sent(self):
        """
        Get last sent I{soap} message.
        :return: The last sent I{soap} message.
        :rtype: unicode
        """
        last_sent = super(SmevClient, self).last_sent()
        return last_sent.plain() if last_sent else u''

    def last_received(self):
        """
        Get last received I{soap} message.
        :return: The last received I{soap} message.
        :rtype: unicode
        """
        last_received = super(SmevClient, self).last_received()
        return last_received.plain() if last_received else u''
