import base64
import io
import os
import zipfile

from lxml import etree

from kinder.core.queue_module.api import prepare_notify_print_context

from lipetsk_specifics.report import GenericPrintReport
from lipetsk_specifics.utils import in_queue_upd
from lipetsk_specifics.utils import reject_upd


class NotificationGenerator:

    IN_QUEUE = 0
    REJECT = 1

    NOTIFICATION_TMP = {
        IN_QUEUE: 'xls/in_queue_notification.xls',
        REJECT: 'xls/reject_notification.xls'
    }

    NOTIFICATION_PARAMS_UPDATER = {
        IN_QUEUE: in_queue_upd,
        REJECT: reject_upd
    }

    def __init__(self, declaration, delegate, profile):

        self.declaration_id = declaration.id
        self.delegate_id = delegate.id

        self.profile = profile

    def generate(self, notification_type=IN_QUEUE):

        variables = prepare_notify_print_context(self, self.profile)
        variables = self.NOTIFICATION_PARAMS_UPDATER.get(
            notification_type
        )(variables, self)

        template = self.NOTIFICATION_TMP.get(notification_type)

        report = GenericPrintReport(["templates", template], vars=variables)
        report.make_report()

        return report.result_name


def _create_archive_declaration(
        file_name, content_type="application/vnd.ms-excel"):
    """Создание xml c описанием приложенного файла.
    :param file_name: Имя файла
    :param content_type: MIME-тип
    :return: (String) Содержимое xml

    """

    archive_description = etree.Element("archiveDescription")
    file_descriptions = etree.SubElement(
        archive_description, "fileDescriptions")
    file_description = etree.SubElement(
        file_descriptions, "fileDescription")

    name = etree.SubElement(file_description, "name")
    name.text = file_name

    content_type_tag = etree.SubElement(file_description, "contentType")
    content_type_tag.text = content_type

    return etree.tostring(archive_description)


def binary_notification_creator(
        declaration, delegate, profile, notification_type):

    # Вся работа должна выполняться с байтовыми строками
    gen = NotificationGenerator(declaration, delegate, profile)

    notification_file_name = gen.generate(notification_type)
    notification_file = io.BytesIO()
    with open(notification_file_name, "rb") as _f:
        notification_file.write(_f.read())

    description_file = io.BytesIO()
    description_file.write(_create_archive_declaration(
        os.path.basename(notification_file_name)))

    mf = io.BytesIO()
    zf = zipfile.ZipFile(mf, mode="w", compression=zipfile.ZIP_DEFLATED)
    zf.writestr("archive-description.xml", description_file.getvalue())
    zf.writestr(os.path.basename(notification_file_name),
                notification_file.getvalue())
    notification_file.close()
    description_file.close()
    zf.close()

    return base64.encodebytes(mf.getvalue())
