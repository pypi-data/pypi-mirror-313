import os.path

def testfile_path(fn:str): return os.path.join(os.path.split(__file__)[0], 'files', fn)
