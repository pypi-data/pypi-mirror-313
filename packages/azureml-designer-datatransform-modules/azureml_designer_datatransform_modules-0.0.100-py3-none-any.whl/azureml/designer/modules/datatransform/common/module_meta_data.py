class ModuleMetaData:
    def __init__(self, id: str = None, name: str = None, category: str = None, description: str = None):
        self._id = id
        self._name = name
        self._category = category
        self._description = description

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    @property
    def description(self):
        return self._description
