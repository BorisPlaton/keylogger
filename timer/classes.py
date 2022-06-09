from core.datastuctures import Listener, EventHandler, Event


class Timer(EventHandler, Listener):

    def time_passed(self):
        print("Time is over")

    def time_stopped(self):
        print("Time stopped")
