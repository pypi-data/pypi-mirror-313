from __future__ import annotations

import json
import mimetypes
import urllib
import uuid
import zipfile
from typing import TYPE_CHECKING

from aio_client import configs as aio_client_settings
from django.core.files.base import ContentFile
import magic

from kinder import logger
from kinder.core.declaration.models import Declaration
from kinder.core.declaration.models import DeclarationDoc
from kinder.core.utils.address import ApplicationRequestAddressType
from kinder.core.utils.address import get_full_address
from kinder.core.utils.address import get_gar_code


if TYPE_CHECKING:
    from concentrator.smev3_v321.service_types.kinder_conc import AddressType


_PREF_EXT = {
    '.jpg',
    '.doc',
    '.docx',
    '.pdf',
    '.png',
    '.txt',
    '.odt',
    '.xls',
    '.xlsx',
}


def random_filename(file):
    """Возвращает случайное название файла."""
    # Пытаемся получить расширение из mime-типа
    mime_type = magic.from_buffer(file, mime=True)
    possible_extensions = mimetypes.guess_all_extensions(mime_type)
    extension = ''
    if possible_extensions:
        if len(possible_extensions) == 1:
            extension = possible_extensions[0]
        else:
            for _extension in possible_extensions:
                # Если несколько возможных расширений, отдаём предпочтение 
                # некоторым из них вместо того чтоб брать первое 
                if _extension in _PREF_EXT:
                    extension = _extension
                    break
            else:
                # Если предпочитаемых нет, берём первое
                extension = possible_extensions[0]
                    
    uid = uuid.uuid4().hex
    return f'{uid}{extension}'


def process_attachments(
        attachments: list[str] | str,
        declaration: Declaration,
        approve: bool = True
) -> list[DeclarationDoc]:
    """Обработка прикреплённых файлов.

    :param attachments: Объект с ссылками на вложения
    :param declaration: Заявление
    :param approve: Подтверждены ли вложения

    :return: Список принятых документов
    """

    docs = []

    # маневр на случай если в attachments прийдет JSON обернутый в список
    if isinstance(attachments, list):
        attachments = [json.loads(attachment) for attachment in attachments]
    else:
        attachments = json.loads(attachments)

    # Получение адреса сервера АИО без лишних частей
    base_aio_url = urllib.parse.urljoin(aio_client_settings.AIO_SERVER, '/')

    for attachment in attachments:

        url = attachment[0].strip('/')
        url = urllib.parse.urljoin(base_aio_url, url)
        try:
            name, html = urllib.request.urlretrieve(url)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                logger.error(f'Не удалось получить вложение ({e})')
                continue
            raise

        try:
            with zipfile.ZipFile(name, 'r', zipfile.ZIP_DEFLATED) as (
                    zip_archive):
                for zipped_file_name in zip_archive.namelist():
                    if zipped_file_name.split('.')[-1] == 'xml':
                        continue
                    file = zip_archive.read(zipped_file_name)
                    try:
                        filename = random_filename(file)
                    except Exception:
                        # Костыль, поэтому если не получилось -
                        # не расстраиваемся.
                        filename = f'{uuid.uuid4().hex}.dat'

                    doc = DeclarationDoc.objects.create(
                        file=ContentFile(file, name=filename),
                        name=filename,
                        declaration=declaration,
                        approve=approve)
                    docs.append(doc)
        except zipfile.BadZipFile:
            pass

    return docs


def get_address_place_code(address: AddressType) -> str:
    """Получение значение "Населённый пункт" из ApplicationRequest.

    :param address: Блок адреса из ApplicationRequest

    :return: Код ФИАС для населенного пункта (берется первое корректное
        заполненное поле - населенный пункт, город, район, регион), иначе
        пустая строка.

    :raise: ValueError

    """

    return (
        get_gar_code(address.Place.code) or
        get_gar_code(address.City.code) or
        get_gar_code(address.Area.code) or
        get_gar_code(address.Region.code)
    )


def get_application_request_full_address(address: AddressType) -> str:
    """Формирует полный адрес для ApplicationRequest из GUID остальных полей
    запроса

    :param address: Блок адреса из запроса ApplicationRequest
    :return: Полный адрес в строковом представлении
    """
    place_guid = get_address_place_code(address)
    street_guid = get_gar_code(address.Street.code)
    house_guid = get_gar_code(address.House.code)

    address_type = ApplicationRequestAddressType(
        full_address=address.FullAddress,
        place=place_guid,
        street=street_guid,
        house=house_guid,
        apartment=address.Apartment if address.Apartment else ''
    )
    return get_full_address(address_type)
