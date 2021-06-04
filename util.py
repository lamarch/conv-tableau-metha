import threading


class AdvancedThread(threading.Thread):
    def __init__(self, on_quit, *_args, **_kwargs) -> None:
        super().__init__(*_args, **_kwargs)

        self.on_quit = on_quit

        self.stop_event = threading.Event()
        self.stop_event.clear()

    def run(self):
        super().run()
        self.on_quit()

    def stop(self):
        self.stop_event.set()

    def stopped(self):
        return self.stop_event.is_set()


class SimpleRedirector(object):
    def __init__(self, command) -> None:
        self.command = command

    def write(self, data):
        self.command(data)

    def flush():
        pass
