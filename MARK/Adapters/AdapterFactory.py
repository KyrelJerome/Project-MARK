
from Adapters import JSON_ADAPTER_ID

import AdaptersConsts
class AdapterFactory:

    @staticmethod
    def getAdapter(adapter_id: str):
        if id == JSON_ADAPTER_ID:
            return None # TODO Implement our first adapter
        else:
            raise AdapterNameError("Invalid adapter defined for use,\
                please ensure an adapter constant is defined and implemented")

class AdapterNameError(Exception):
    pass
