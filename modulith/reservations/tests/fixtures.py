from injector import inject


def with_injector(injector):
    def decorator(f):
        f = inject(f)

        def wrapper():
            return injector.call_with_injection(f)

        return wrapper
    return decorator

# injector = Injector([BaseModule(), StubModule()])


# @with_injector(injector)
# def test_foo(session: Session):
#    session is injected!
