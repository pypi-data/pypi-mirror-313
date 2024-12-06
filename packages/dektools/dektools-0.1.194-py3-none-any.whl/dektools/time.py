import time
import datetime
import threading
from zoneinfo import ZoneInfo

TZ_CURRENT = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
TZ_UTC = ZoneInfo('UTC')


def get_tz(tz=None):
    if not tz:
        tz = TZ_CURRENT
    if isinstance(tz, str):
        tz = ZoneInfo(tz)
    return tz


def now(delta=None, tz=None):
    dt = datetime.datetime.now(tz=tz or TZ_CURRENT)
    if delta:
        dt += datetime.timedelta(microseconds=delta)
    return dt


def get_day_index():
    return (datetime.datetime.now(tz=TZ_UTC) - datetime.datetime.fromtimestamp(0, tz=TZ_UTC)).days


class DateTime:
    """
        %Y Year with century as a decimal number(2015)

        %m Month

        %d Day of the month as a zero-padded decimal number(1)

        %I Hour (12-hour clock) as a zero-padded decimal number(01)

        %H Hour (24-hour clock)

        %M Minute as a zero-padded decimal number(33)

        %S Second

        %f microseconds

        %p Locale’s equivalent of either AM or PM(PM)

        %b Month as locale’s abbreviated name(Jun)
    """

    def __init__(self, tz=None):
        self.tz = tz

    def from_str(self, s, fmt=None):
        if fmt is None:
            r = datetime.datetime.fromisoformat(s)
        else:
            r = datetime.datetime.strptime(s, fmt)
        if self.tz:
            r = r.astimezone(self.tz)
        return r

    def to_str(self, obj=None, fmt=None):
        if obj is None:
            obj = datetime.datetime.now()
        if self.tz:
            obj = obj.astimezone(self.tz)
        if fmt is None:
            obj.isoformat()
        else:
            return obj.strftime(fmt)


class Timer:
    def __init__(self, func, interval, count=1):
        self.interval = interval  # seconds
        self.count = 0
        self.limit_count = count  # None for inf
        self.func_set = [func] if func else []
        self.valid = True
        self.stop_event = threading.Event()
        threading.Thread(target=self.__callback).start()

    def _get_interval(self):
        if callable(self.interval):
            return self.interval(self)
        else:
            return self.interval

    def __callback(self):
        now = time.perf_counter()
        next_time = now + self._get_interval()
        while not self.stop_event.wait(next_time - now):
            for func in self.func_set:
                func(self)
            self.count += 1
            if self.limit_count is not None and self.limit_count <= self.count:
                self.end()
            else:
                next_time += self._get_interval()
        self.valid = False

    def add_func(self, func):
        self.func_set.append(func)

    def remove_func(self, func):
        self.func_set.remove(func)
        if not self.func_set:
            self.end()

    def end(self):
        self.stop_event.set()


class TimerInLoop:
    def __init__(self):
        self._id_cursor = 0
        self._records = {}

    def __len__(self):
        return len(self._records)

    def _new_id(self):
        self._id_cursor += 1
        return self._id_cursor

    def set_interval(self, func, interval, count=1):  # seconds
        self._records[self._new_id()] = [func, interval, time.time(), count, 0]

    def clear_interval(self, uid):
        return bool(self._records.pop(uid, None))

    def has_interval(self, uid):
        return uid in self._records

    def find_interval(self, func):
        for uid, record in self._records.items():
            if record[0] is func:
                yield uid

    def peek(self):
        remove = set()
        times = 10 ** 7
        tn = time.time()
        for uid in self._records.keys():
            func, interval, ts, count, index = record = self._records[uid]
            if interval == 0:
                idx = index + 1
            else:
                idx = int((tn - ts) * times) // int(interval * times)
            if idx > index:
                func()
                if count is not None:
                    count -= 1
                    if count <= 0:
                        remove.add(uid)
                        continue
                    else:
                        record[-2] = count
                record[-1] = idx
        for uid in remove:
            self._records.pop(uid, None)
