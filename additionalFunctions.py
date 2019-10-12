import random
import time
import datetime


def waiting_tasks(h_from=0, h_to=0, m_from=0, m_to=0, s_from=0, s_to=0, days=0, log=None):
    hours_sleep = random.randrange(h_from, h_to+1)
    minutes_sleep = random.randrange(m_from, m_to+1)
    secs_sleep = random.randrange(s_from, s_to+1)
    timedelta = datetime.timedelta(days=days, hours=hours_sleep,
                                   minutes=minutes_sleep,
                                   seconds=secs_sleep)
    if hours_sleep > 1 or minutes_sleep > 1:
        delay = 30
    else:
        delay = 1
    now = datetime.datetime.now()
    end_time = now + timedelta
    if log:
        log("Продолжение в: " + str(end_time))
    while now < end_time:
        now = datetime.datetime.now()
        time.sleep(delay)


def sleep_between():
    time.sleep(random.randrange(4000, 12000) / 1000)


def is_next_day():
    today = datetime.datetime.now()
    timedelta = datetime.timedelta(days=1)
    tomorrow_day = (today + timedelta).day

    def helper():
        today = datetime.datetime.now()
        today_day = today.day
        return today_day == tomorrow_day
    return helper


class ConsoleLog:

    def __init__(self, queue=False, msg_before=False):
        if queue:
            self.queue = queue
        else:
            self.queue = False
        if msg_before:
            self.msg_before = msg_before
        else:
            self.msg_before = False

    def __call__(self, *args):
        time_now = time.strftime("%H:%M:%S_%d/%m")
        if self.queue:
            if self.msg_before:
                self.queue.put("{0}: [{1}] {2}".format(self.msg_before, time_now, *args))
            else:
                self.queue.put("[{0}] {1}".format(time_now, *args))
        else:
            if self.msg_before:
                print("{0}: [{1}] {2}".format(self.msg_before, time_now, *args))
            else:
                print("[{1}] {2}".format(self.msg_before, time_now, *args))


