import json


class DataBase:
    def __init__(self):
        with open('data/i18n_fr.json', 'r', encoding="utf8") as file:
            self._i18n = json.load(file)
        with open('data/item.json', 'r', encoding="utf8") as file:
            self._items = json.load(file)
        with open('data/itemType.json', 'r', encoding="utf8") as file:
            self._itemType = json.load(file)
        with open('data/protocolId.json', 'r', encoding="utf8") as file:
            self._protocolId = json.load(file)
        return

    def getTypeName(self, id):
        if str(id) in self._itemType:
            return self.getI18n(self._itemType[str(id)]["nameId"])
        else:
            return f"[{id}] (not found)"

    def getItemName(self, id):
        if str(id) in self._items:
            return self.getI18n(self._items[str(id)]["nameId"])
        else:
            return f"[{id}] nameId not found"

    def getI18n(self, id):
        if str(id) in self._i18n:
            return self._i18n[str(id)]["value"]
        else:
            return f"[{id}] (not found)"
