import filecmp
import os
import unittest

import m3_xlwt

from .utils import in_tst_dir, in_tst_output_dir


def from_tst_dir(filename):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

class TestMini(unittest.TestCase):
    def test_create_mini_xls(self):
        book = m3_xlwt.Workbook()
        sheet = book.add_sheet('m3_xlwt was here')
        book.save(in_tst_output_dir('mini.xls'))

        self.assertTrue(filecmp.cmp(in_tst_dir('mini.xls'),
                                    in_tst_output_dir('mini.xls'),
                                    shallow=False))
