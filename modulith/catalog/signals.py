

def simple_signal(*args, **kwargs):
    print('signal disp', args, kwargs)


class ClassBasedHandler:

    def handle_ints_added(self, *args, **kwargs):
        print('cls based signal disp', args, kwargs)


# event_handler = ClassBasedHandler()
