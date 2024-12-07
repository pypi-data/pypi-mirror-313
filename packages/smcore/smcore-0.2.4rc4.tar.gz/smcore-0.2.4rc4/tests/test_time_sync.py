import unittest
import datetime
from smcore import SyncTime

test_server = "pool.ntp.org"


class TestSyncTime(unittest.TestCase):
    def test_synchronize(self):
        s = SyncTime()
        s.synchronize(test_server)
        self.assertNotEqual(s.now(), datetime.datetime.now(datetime.timezone.utc))
