import abc
import argparse
import dataclasses
import io
import os
import os.path
import re
import sys
import typing

class Writer(abc.ABC):

    @abc.abstractmethod
    def write     (self,part:str) -> None: pass

    def writeline (self,line:str):
        
        self.write(f'{line}\n')

    def writelines(self,lines:list[str]) -> None: 
        
        for line in lines:

            self.writeline(line)

class BufferWriter(Writer):

    def __init__(self):

        self._parts:list[str] = list()
        self._whole:str       = ''

    @typing.override
    def write(self,part:str):

        self._parts.append(part)

    def build(self):

        if self._parts:

            self._whole = ''.join((self._whole, *self._parts,))
            self._parts.clear()
            
        return self._whole

@dataclasses.dataclass
class ProcessingInstruction:

    abort_if:typing.Callable[[str],bool]
    pattern :str
    capture :typing.Callable[[re.Match],str]
    descape :typing.Callable[[str],str]
    repl    :typing.Callable[[str],bool]

    def __post_init__(self):

        if self.abort_if is None: 
           self.abort_if = lambda fcontent: False

class Processor:

    def __init__(self, pis:typing.Iterable[ProcessingInstruction]):

        self._pis = pis

    def __call__(self, file_getter :typing.Callable[[],io.TextIOWrapper],
                       ofile_getter:typing.Callable[[],io.TextIOWrapper]|None=None,
                       working_dir :str                                 |None=None):

        pis = self._pis
        f   = file_getter()
        raw = f.read()
        f.close()
        
        def generated(expr:str) -> str:

            pp = BufferWriter()
            original_wd = os.path.abspath(os.getcwd())
            os.chdir(working_dir)
            try:

                sys.path.append(os.getcwd())
                exec(expr.replace('\\/', '/'), {
                    
                    **globals(),
                    'write'     :pp.write,
                    'writeline' :pp.writeline,
                    'writelines':pp.writelines,
                
                })
                sys.path.pop()
            
            finally:

                os.chdir(original_wd)
            
            return pp.build()

        in_process = raw
        pis_done:list[ProcessingInstruction] = list()
        for pi in pis:

            if pi.abort_if(raw): 
                
                continue

            def replf(m:re.Match[str]):

                return (lambda input: pi.repl(generated(pi.descape(input)),m))(pi.capture(m))

            in_process = re.sub(pattern=pi.pattern, 
                                repl   =replf, 
                                string =in_process, 
                                flags  =re.DOTALL)
            pis_done.append(pi)

        of = ofile_getter()
        of.write(in_process)
        of.close()        
        return pis_done

    def by_name (self, file_name :str,
                       encoding  :str|None=None,
                       ofile_name:str|None=None):
        
        opener = lambda fn,mode='r': (lambda: open(fn, mode=mode, encoding=encoding))
        return self.__call__(file_getter =opener(file_name),
                             ofile_getter=opener(ofile_name if ofile_name is not None else \
                                                 file_name, mode='w'),
                             working_dir =os.path.split(os.path.abspath(file_name))[0])

def main(pp:Processor, 
         ap:argparse.ArgumentParser):

    class A:

        FILE_PATH        = 'f'
        ENCODING         = 'enc'
        OUTPUT_FILE_PATH = 'fo'

    ap.add_argument(f'{A.FILE_PATH}',
                    help   ='file path (input)')
    ap.add_argument(f'--{A.ENCODING}',
                    help   ='file encoding')
    ap.add_argument(f'--{A.OUTPUT_FILE_PATH}',
                    help   ='file path (output)\nIf omitted, the input file is processed in-place.')
    get = ap.parse_args().__getattribute__
    pp.by_name(file_name =get(A.FILE_PATH),
               encoding  =get(A.ENCODING),
               ofile_name=get(A.OUTPUT_FILE_PATH))

def simple_argparser(lang:str):

    return argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                   description   =f'pre-processor for {lang} files')

def main_simple(pp  :Processor,
                lang:str): main(pp, simple_argparser(lang))
