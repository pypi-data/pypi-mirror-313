# coding: utf-8

from yadic.container import Container

from ..models import ChangeSource


config = {
    "UpdateProxy": {
        "__default__": {
            "__realization__": "concentrator."
                               "webservice.proxy.IUpdateApplicationProxy"
        },
        "default": {
            "behavior": "standard",
            "storage": "standard"
        },
        "for_new_application": {
            "behavior": "new_application_behavior",
            "storage": "new_application_storage"
        },
        "reset": {
            "behavior": "reset",
            "storage": "standard"
        }
    },
    "behavior": {
        "__default__": {
            "__type__": "static",
            "__realization__": "concentrator."
                               "webservice.proxy.UpdateProxy"
        },
        "standard": {},
        "new_application_behavior": {},
        "reset": {
            "__realization__": "concentrator."
                               "webservice.proxy.ResetDeclarationProxy"
        }
    },
    "storage": {
        "__default__": {
            "__realization__": "concentrator."
                               "change.StorageHelper"
        },
        "standard": {
            "$source": ChangeSource.UPDATE_APPLICATION,
        },
        "new_application_storage": {
            "$source": ChangeSource.NEW_APPLICATION
        }
    }
}

cont = Container(config)
