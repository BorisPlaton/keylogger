from core.datastuctures import Listener


class OutputFormatter(Listener):

    def time_passed(self):
        pass

    def key_logging_stopped(self):
        print('Time stopped and thus text formatter is showing this message!')
