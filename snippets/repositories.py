

class TransactionalRepo:

    def __enter__(self):
        print('transaction start')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('transtaction end')

    def find(self):
        pass

    def save(self, entity):
        pass


with TransactionalRepo() as repo:
    stuff = repo.find()

    stuff.do_more()

    repo.save(stuff)
