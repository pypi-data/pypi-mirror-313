import glob
import os

from kinder.core.declaration.tests.factory_declaration import DeclarationF
from kinder.core.helpers import recursive_getattr


def copy_from(declaration, fields=None):
    """Создает полный дубликат заявления."""

    params = {}
    for field in fields:
        params[field.replace('.', '__')] = (
            recursive_getattr(declaration, field.replace('.', '__')))
    return DeclarationF.create(**params)


def examples(current_dir, name=None):
    """Генератор файлов примеров.
    :param current_dir: путь до папки содержащей директорию current_dir
    :param name: имя файлаб по умолчанию отдаем 1.xml
    """
    name = name or '1.xml'
    examples_folder = os.path.join(current_dir, 'examples')
    files = glob.glob('{}/*.xml'.format(examples_folder))
    for file_path in files:
        if name in file_path:
            with open(file_path, 'r') as f:
                yield f.read()
