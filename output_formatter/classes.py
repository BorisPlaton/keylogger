import threading

from core.events import EventListener


class OutputFormatter(EventListener):

    def __init__(self):
        self.locker = threading.Lock()

    def show_menu(self):
        output_thread = threading.Thread(target=self._output_program_menu, name='OutputThread')
        output_thread.start()

    def _output_program_menu(self):
        with self.locker:
            print('')

    def menu_started(self):
        self.show_menu()

    def time_passed(self):
        pass

    def key_logging_stopped(self):
        print('Time stopped and thus text formatter is showing this message!')
