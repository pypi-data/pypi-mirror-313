import os.path
import unittest

from project.package import pp

from . import *
from ..package import pphtml

class Tests(unittest.TestCase):

    html_processor = pphtml.Processor()

    def _infix(self, fn   :str, 
                     infix:str): return infix.join(os.path.splitext(fn))
    def _to_fail(f):
        def g(self, *aa, **kaa):
            try:
                f(self, *aa, **kaa)
                raise AssertionError('expected to fail but passed')
            except: pass
        return g

    def _test(self, p:pp.Processor,fn:str):

        tfn = testfile_path(fn)
        ofn = self._infix(tfn, '-got')
        with open(testfile_path(fn)) as f:

            p.by_name(file_name=tfn, ofile_name=ofn)

        with open(ofn) as of:

            with open(self._infix(tfn, '-expected')) as ef:

                print(f'\nTest: {tfn}', flush=True, end='')
                self.assertEqual(of.read(), ef.read())  

        os.remove(ofn)

    def test_1(self): self._test(pphtml.Processor(), fn='html1.md')
    @_to_fail
    def test_2(self): self._test(pphtml.Processor(), fn='html2.md')
