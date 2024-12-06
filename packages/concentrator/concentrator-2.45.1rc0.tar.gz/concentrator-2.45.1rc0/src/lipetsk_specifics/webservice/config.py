# coding: utf-8

from yadic.container import Container

from concentrator.models import ChangeSource


config = {
    "UpdateProxy": {
        "__default__": {
            "__realization__": "concentrator."
                               "webservice.proxy.IUpdateApplicationProxy"
        },
        "lipetsk_proxy": {
            "behavior": "lipetsk_behavior",
            "storage": "standard"
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
        "lipetsk_behavior": {
            "__realization__": "lipetsk_specifics."
                               "webservice.proxy.LipetskUpdateProxy"
        },
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
        }
    }
}

cont = Container(config)
