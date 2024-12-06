import json
import urllib
import uuid
import zipfile

from django.core.files.base import ContentFile
from django.utils.text import get_valid_filename

from aio_client import configs as aio_client_settings
from kinder.core.declaration.models import DeclarationDoc


def random_filename(original):
    """Возвращает валидное расширение и название файла."""

    file_name, file_extension = (original.rsplit('.', 1) + [''])[:2]

    extension = get_valid_filename(file_extension) or 'dat'
    uid = uuid.uuid4().hex

    return f'{uid}.{extension}'


def process_attachments(attachments, declaration, approve=True):
    """
    Обработка прикреплённых файлов
    """
    docs = []

    # маневр на случай если в attachments прийдет JSON обернутый в список
    if isinstance(attachments, list):
        attachments = attachments[0]

    attachments = json.loads(attachments)
    # Получение адреса сервера АИО без лишних частей
    base_aio_url = urllib.parse.urljoin(aio_client_settings.AIO_SERVER, '/')

    for attachment in attachments:

        url = attachment[0]
        url = urllib.parse.urljoin(base_aio_url, url)
        name, html = urllib.request.urlretrieve(url)

        # TODO сделать нормальную валидацию, а не ловить траем
        try:
            with zipfile.ZipFile(name, "r", zipfile.ZIP_DEFLATED) as zip_archive:
                for zipped_file_name in zip_archive.namelist():
                    if zipped_file_name.split('.')[-1] == 'xml':
                        continue

                    filename = random_filename(zipped_file_name)
                    doc = DeclarationDoc.objects.create(
                        file=ContentFile(
                            zip_archive.read(zipped_file_name),
                            name=zipped_file_name
                        ),
                        name=filename,
                        declaration=declaration,
                        approve=approve
                    )
                    docs.append(doc)
        except zipfile.BadZipFile:
            pass
    
    return docs
