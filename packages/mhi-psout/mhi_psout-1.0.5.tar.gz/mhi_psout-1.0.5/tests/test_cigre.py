import unittest
import os, sys, datetime, os
import warnings
import pytest

import mhi.psout

with warnings.catch_warnings(action='ignore', category=DeprecationWarning):
    import matplotlib.pyplot as plt

from pathlib import Path

class TestPSOutCigre(unittest.TestCase):

    def setUp(self):
        self.parent = Path(__file__).parent
        self.path = self.parent.parent / "test-data" / "Cigre.psout"

    def test_cigre_variables(self):
        with mhi.psout.File(self.path) as file:
            self.assertEqual(file.variables(), {})

    def test_cigre_runs(self):
        with mhi.psout.File(self.path) as file:
            self.assertEqual(file.num_runs, 1)

    def test_cigre_path(self):
        with mhi.psout.File(self.path) as file:
            self.assertIsInstance(file.path, Path)
            self.assertEqual(file.path, self.path)

    def test_psout_path_str(self):
        path_str = str(self.path)
        with mhi.psout.File(path_str) as file:
            self.assertIsInstance(file.path, str)
            self.assertEqual(file.path, path_str)

    def test_psout_datetime(self):
        with mhi.psout.File(self.path) as file:
            self.assertEqual(type(file.created), datetime.datetime)
            self.assertEqual(type(file.modified), datetime.datetime)

    def test_psout_roots(self):
        with mhi.psout.File(self.path) as file:
            root = file.root
            call = root.call(0)
            root2 = call.parent
            self.assertEqual(root, root2)

    def test_psout_calls_same(self):
        with mhi.psout.File(self.path) as file:
            root = file.root
            call1 = root.call(0)
            call2 = root.call(0)
            self.assertEqual(call1, call2)

    @pytest.mark.filterwarnings("ignore:datetime.datetime.utcfromtimestamp")
    def test_psout_image(self):

        import matplotlib.pyplot as plt

        with mhi.psout.File(self.path) as file:

            ac_voltage = file.call("Root/Main/AC Voltage/0")
            run = file.run(0)

            for call in ac_voltage.calls():
                trace = run.trace(call)
                time = trace.domain
                plt.plot(time.data, trace.data, label=trace['Description'])

            plt.xlabel(time['Unit'])
            plt.ylabel(trace['Unit'])
            plt.legend()
            plt.savefig(self.parent / 'ac_voltage.png')

        self.assertTrue((self.parent / 'ac_voltage.png').is_file())

    def test_psout_zero_trace(self):
        with mhi.psout.File(self.path) as file:

            run = file.run(0)
            t = run.trace(57)

            self.assertEqual(t.size, 0)
            self.assertEqual(t.datatype, float)
            data = t.data
            self.assertEqual(len(data), 0)


if __name__ == '__main__':
    unittest.main()
