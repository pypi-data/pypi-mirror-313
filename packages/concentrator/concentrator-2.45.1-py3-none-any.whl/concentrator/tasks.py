# coding: utf-8

from kinder import celery_app
from kinder.core.async_tasks.tasks import AsyncTask
from kinder.core.declaration.models import Declaration
from kinder.settings import logger

from concentrator.webservice.service import send_update_application_state


class SendUpdateApplicationState(AsyncTask):
    """Отправка информации о смене статуса в концентратор."""

    description = u'Отправка информации о смене статуса в концентратор'

    def process(self, declaration_id, is_auto, commentary, log_id,
            desired_date_changed, auto_archive=True, *args, **kwargs):
        """

        :param declaration_id: id заявления
        :param is_auto: авто-смена статуса при применении изменений из ЕПГУ
        :param commentary: комментарий пользователя при применение,
        либо отмене изменений
        :param commentary: комментарий
        :param log_id: идентификатор записи в логе о смене статуса заявления
        :param desired_date_changed: Признак изменения желаемой даты
        :param auto_archive: Присваивать ли архивный статус при авто-смене
        :return:

        """
        try:
            declaration = Declaration.objects.get(id=declaration_id)
        except Declaration.DoesNotExist:
            declaration = None

        smev_log = send_update_application_state(
            declaration,
            is_auto=is_auto,
            commentary=commentary,
            log_id=log_id,
            auto_archive=auto_archive,
            desired_date_changed=desired_date_changed)

        if smev_log is not None:
            values = {}
            if not smev_log.result:
                progress = u'Успешно'
            else:
                progress = u'Завершено с ошибками'
                values[u'Ошибка'] = smev_log.result

            self.set_progress(progress=progress, values=values)

        return self.state

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        super().on_failure(exc, task_id, args, kwargs, einfo)
        logger.error(str(exc))


celery_app.register_task(SendUpdateApplicationState)
