from core.datastuctures import Listener


class TextFormatter(Listener):

    def time_passed(self):
        pass

    def time_stopped(self):
        print('Time stopped and thus text formatter is showing this message!')
