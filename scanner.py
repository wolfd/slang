import os.path
import codecs

from .token import Token, File

class SlangError(Error):
    def __init__(self, offset: int, reason: str):
        super().__init__(f"Error at: {offset}: {reason}")

class Scanner(object):
    def __init__(self, path: str):
        super().__init__()

        self.filename, self.dirpath = os.path.split(path)

        with codecs.open(path, encoding='utf-8') as fd:
            self.src = fd.read()
        
        self.file = File(
            name=path,
            base=0,
            size=len(self.src),
            lines=[]
        )
        
        self.ch: int = ord(' ')  # single unicode character value
        self.offset: int = 0  # character offset in file
        self.read_offset: int = 0  # reading offset
        self.line_offset: int = 0  # current line offset

    def next(self):
        if self.read_offset < len(self.src):
            self.offset = self.read_offset
            if self.ch == ord('\n'):
                self.line_offset = s.offset
                self.file.lines.append(self.offset)
            
            r = ord(self.src[self.read_offset])

            if r == 0:
                raise SlangError(self.offset, "illegal NUL character")
            
            self.read_offset += 1
            self.ch = r
    
        else:
            self.offset = len(self.src)
            if self.ch == ord('\n'):
                self.line_offset = self.offset
                self.file.lines.append(self.offset)
            
            self.ch = -1  # EOF
    
    def scan_string(self) -> str:
        # '"' open already consumed
        offset = self.offset - 1

        while True:
            ch = self.ch

            if ch == ord('\n') or ch < 0:
                raise SlangError(offset, "string literal not terminated")
                break

            self.next()
            if ch == ord('"'):
                break
            # no escape strings yet

        return self.src[offset:self.offset]
    
    def skip_whitespace(self):
        while is_whitespace(self.ch):
            self.next()

    def scan(self, pos: int, token: Token, literal: str):
        # todo
        pass


def is_letter(ch: int) -> bool:
    return (
        ord('a') <= ch <= ord('z') or
        ord('A') <= ch <= ord('Z') or
        ch == ord('_')
    )

def is_digit(ch: int) -> bool:
    return ord('0') <= ch <= ord('9')

def is_whitespace(ch: int) -> bool:
    if ch == ord(' '):
        return True
    elif ch == ord('\n'):
        return True
    elif ch == ord('\t'):
        return True
    return False