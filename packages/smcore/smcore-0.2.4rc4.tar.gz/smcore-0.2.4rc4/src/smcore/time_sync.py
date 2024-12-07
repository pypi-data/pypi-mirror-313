import ntplib
import datetime


class SyncTime:
    def __init__(self):
        self.offset = datetime.timedelta(seconds=0)

    def synchronize(self, serv: str):
        print("synchronizing to", serv)
        c = ntplib.NTPClient()
        resp = c.request(serv)
        self.offset = datetime.timedelta(seconds=resp.offset)
        print(f"time: {self.now()} (offset: {self.offset})")

    def now(self):
        curr_local_time = datetime.datetime.now(datetime.timezone.utc)
        return curr_local_time + self.offset
