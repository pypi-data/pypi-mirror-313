import traceback

from kinder import logger

from .constants import OperationEnumerate


def obj_save_handler(obj, proxy, created):
    """
    При сохранении объекта, отправляем информацию в концентратор
    """
    try:
        proxy().send_obj(obj,
                         OperationEnumerate.ADD if created
                         else OperationEnumerate.UPDATE)
    except Exception:
        logger.error(traceback.format_exc())


def obj_delete_handler(obj, proxy):
    """
    При удалении объекта, отправляем информацию в концентратор
    """
    try:
        proxy().send_obj(obj, OperationEnumerate.DELETE)
    except Exception:
        logger.error(traceback.format_exc())
