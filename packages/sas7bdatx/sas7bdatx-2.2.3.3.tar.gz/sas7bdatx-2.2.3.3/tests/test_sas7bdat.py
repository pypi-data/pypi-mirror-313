# !/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from sas7bdat import SAS7BDAT
import tempfile
import os
import datetime


class TestSAS7BDAT(unittest.TestCase):
    def test_read_numbers(self):
        s = SAS7BDAT('tests/data/intvalues.sas7bdat')
        for i, line in enumerate(s):
            if i == 0:
                self.assertEqual(line, ['intvalue'])
            else:
                self.assertEqual(len(line), 1)
                self.assertEqual(line[0], i)
                self.assertEqual(type(line[0]), float)
        self.assertEqual(i, 5)

    def test_read_numbers_skip_header(self):
        s = SAS7BDAT('tests/data/intvalues.sas7bdat', skip_header=True)
        for i, line in enumerate(s):
            self.assertEqual(len(line), 1)
            self.assertEqual(line[0], i + 1)
            self.assertEqual(type(line[0]), float)
        self.assertEqual(i, 4)

    def test_read_floats(self):
        s = SAS7BDAT('tests/data/floatvalues.sas7bdat', skip_header=True)
        for i, line in enumerate(s):
            self.assertEqual(len(line), 1)
            self.assertEqual(line[0], float(i) + 1.0 + float(i) * 0.1)
            self.assertEqual(type(line[0]), float)
        self.assertEqual(i, 4)

    def test_read_characters(self):
        s = SAS7BDAT('tests/data/charactervalues.sas7bdat', skip_header=True)
        characters = 'ABcdE'
        for i, line in enumerate(s):
            self.assertEqual(len(line), 1)
            self.assertEqual(line[0], characters[i])
        self.assertEqual(i, len(characters) - 1)

    def test_read_specialcharacters(self):
        s = SAS7BDAT('tests/data/specialcharactervalues.sas7bdat', skip_header=True)
        characters = u'Äéǿαאا'

        for i, line in enumerate(s):
            self.assertEqual(len(line), 1)
            self.assertEqual(line[0], characters[i])
        self.assertEqual(i, len(characters) - 1)

    def test_read_dates(self):
        s = SAS7BDAT('tests/data/datevalues.sas7bdat', skip_header=True)
        dates = ['1900-01-01', '1950-01-01', '1960-01-01', '1970-01-01', '1980-01-01', '1990-01-01',
                 '2000-01-01', '2010-01-01', '2020-01-01', '2004-02-29', '1999-12-31']

        for i, line in enumerate(s):
            self.assertEqual(len(line), 1)
            self.assertEqual(line[0], datetime.datetime.strptime(dates[i], '%Y-%m-%d').date())
        self.assertEqual(i, len(dates) - 1)

    def test_read_datetimes(self):
        s = SAS7BDAT('tests/data/datetimevalues.sas7bdat', skip_header=True)
        datetimes = ['2000-12-31T00:00:00', '2010-01-01T23:59:22', '2020-02-29T08:12:59']

        for i, line in enumerate(s):
            self.assertEqual(len(line), 1)
            self.assertEqual(line[0], datetime.datetime.strptime(datetimes[i], '%Y-%m-%dT%H:%M:%S'))
        self.assertEqual(i, len(datetimes) - 1)

    def test_read_times(self):
        s = SAS7BDAT('tests/data/timevalues.sas7bdat', skip_header=True)
        datetimes = ['00:00:00', '11:59:01', '12:00:02', '22:05:03', '23:59:04']

        for i, line in enumerate(s):
            self.assertEqual(len(line), 1)
            self.assertEqual(line[0], datetime.datetime.strptime(datetimes[i], '%H:%M:%S').time())
        self.assertEqual(i, len(datetimes) - 1)

    def test_read_mixed_data(self):
        s = SAS7BDAT('tests/data/mixedvalues.sas7bdat', skip_header=True)
        mixed = [
            [1, 0.1, 'abc', datetime.time(hour=0, minute=0), datetime.date(year=1980, month=1, day=1)],
            [2, 0.2, 'def', datetime.time(hour=2, minute=22), datetime.date(year=1990, month=12, day=31)],
            [3, 0.3, 'GHI', datetime.time(hour=23, minute=59), datetime.date(year=2004, month=2, day=29)]
        ]

        for i, line in enumerate(s):
            self.assertEqual(len(line), len(mixed[i]))
            for c, col in enumerate(mixed[i]):
                self.assertEqual(line[c], col)
        self.assertEqual(i, len(mixed) - 1)

    def test_read_mixed_data_compressed_binary(self):
        s = SAS7BDAT('tests/data/mixedvalues_compressed_binary.sas7bdat', skip_header=True)
        mixed = [
            [1, 0.1, 'abc', datetime.time(hour=0, minute=0), datetime.date(year=1980, month=1, day=1)],
            [2, 0.2, 'def', datetime.time(hour=2, minute=22), datetime.date(year=1990, month=12, day=31)],
            [3, 0.3, 'GHI', datetime.time(hour=23, minute=59), datetime.date(year=2004, month=2, day=29)]
        ]

        for i, line in enumerate(s):
            self.assertEqual(len(line), len(mixed[i]))
            for c, col in enumerate(mixed[i]):
                self.assertEqual(line[c], col)
        self.assertEqual(i, len(mixed) - 1)

    def test_read_mixed_data_compressed_yes(self):
        s = SAS7BDAT('tests/data/mixedvalues_compressed_yes.sas7bdat', skip_header=True)
        mixed = [
            [1, 0.1, 'abc', datetime.time(hour=0, minute=0), datetime.date(year=1980, month=1, day=1)],
            [2, 0.2, 'def', datetime.time(hour=2, minute=22), datetime.date(year=1990, month=12, day=31)],
            [3, 0.3, 'GHI', datetime.time(hour=23, minute=59), datetime.date(year=2004, month=2, day=29)]
        ]

        for i, line in enumerate(s):
            self.assertEqual(len(line), len(mixed[i]))
            for c, col in enumerate(mixed[i]):
                self.assertEqual(line[c], col)
        self.assertEqual(i, len(mixed) - 1)

    def test_read_mixed_data_compressed_char(self):
        s = SAS7BDAT('tests/data/mixedvalues_compressed_char.sas7bdat', skip_header=True)
        mixed = [
            [1, 0.1, 'abc', datetime.time(hour=0, minute=0), datetime.date(year=1980, month=1, day=1)],
            [2, 0.2, 'def', datetime.time(hour=2, minute=22), datetime.date(year=1990, month=12, day=31)],
            [3, 0.3, 'GHI', datetime.time(hour=23, minute=59), datetime.date(year=2004, month=2, day=29)]
        ]

        for i, line in enumerate(s):
            self.assertEqual(len(line), len(mixed[i]))
            for c, col in enumerate(mixed[i]):
                self.assertEqual(line[c], col)
        self.assertEqual(i, len(mixed) - 1)

    def test_read_mixed_data_with_empty_cell(self):
        s = SAS7BDAT('tests/data/mixedvalues_empty.sas7bdat', skip_header=True)
        mixed = [
            [1, 0.1, 'abc', datetime.time(hour=0, minute=0), datetime.date(year=1980, month=1, day=1)],
            [2, 0.2, 'def', datetime.time(hour=2, minute=22), datetime.date(year=1990, month=12, day=31)],
            [3, 0.3, 'GHI', datetime.time(hour=23, minute=59), datetime.date(year=2004, month=2, day=29)],
            [4, 0.4, '', datetime.time(hour=00, minute=00), datetime.date(year=2000, month=1, day=1)],
            [5, 0.5, 'MNO', datetime.time(hour=5, minute=55), datetime.date(year=2111, month=11, day=11)],
            [6, None, 'PQR', datetime.time(hour=5, minute=55), datetime.date(year=2111, month=11, day=11)]
        ]

        for i, line in enumerate(s):
            self.assertEqual(len(line), len(mixed[i]))
            for c, col in enumerate(mixed[i]):
                self.assertEqual(line[c], col)
        self.assertEqual(i, len(mixed) - 1)

    def test_context(self):
        with SAS7BDAT('tests/data/mixedvalues_empty.sas7bdat') as s:
            lines1 = [line for line in s.readlines()]
        s = SAS7BDAT('tests/data/mixedvalues_empty.sas7bdat')
        lines2 = [line for line in s.readlines()]
        self.assertEqual(lines1, lines2)

    def test_filehandler(self):
        filename = 'tests/data/mixedvalues_empty.sas7bdat'
        temp = tempfile.NamedTemporaryFile()
        f = open(filename, 'rb')
        s = SAS7BDAT(temp.name, fh=f)
        lines1 = [line for line in s.readlines()]
        f.close()

        s = SAS7BDAT(filename)
        lines2 = [line for line in s.readlines()]
        self.assertEqual(lines1, lines2)
        temp.close()

    def test_filehandler_context(self):
        filename = 'tests/data/mixedvalues_empty.sas7bdat'
        f = open(filename, 'rb')
        self.assertFalse(f.closed)
        temp = tempfile.NamedTemporaryFile()
        with SAS7BDAT(temp.name, fh=f) as s:
            _ = [line for line in s.readlines()]
            self.assertFalse(f.closed)
        self.assertTrue(f.closed)
        temp.close()

    def test_convert_file(self):
        filename = 'tests/data/mixedvalues_empty.sas7bdat'
        s = SAS7BDAT(filename)
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.close()
        success = s.convert_file(temp.name)
        self.assertTrue(success)
        os.unlink(temp.name)

    def test_convert_file_fail(self):
        filename = 'tests/data/mixedvalues_empty.sas7bdat'
        s = SAS7BDAT(filename)
        success = s.convert_file(None)
        self.assertFalse(success)


if __name__ == '__main__':
    unittest.main()
