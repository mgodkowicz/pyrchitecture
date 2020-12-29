class Repository:
    def get(self):
        pass

    def save(self, obj):
        pass


class ORMRepository(Repository):
    pass


class InMemoryRepository(Repository):
    def get(self):
        return {'a': 1}
