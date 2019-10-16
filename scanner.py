import os.path
import codecs

import token

class SlangError(Exception):
    def __init__(self, offset: int, reason: str):
        super().__init__(f"Error at: {offset}: {reason}")

class Scanner(object):
    def __init__(self, path: str):
        super().__init__()

        self.filename, self.dirpath = os.path.split(path)

        with codecs.open(path, encoding='utf-8') as fd:
            self.src = fd.read()
        
        self.file = token.File(
            name=path,
            base=0,
            size=len(self.src),
            lines=[]
        )

        self.ch: int = ord(' ')  # single unicode character value
        self.offset: int = 0  # character offset in file
        self.read_offset: int = 0  # reading offset
        self.line_offset: int = 0  # current line offset
    
    def peek(self) -> int:
        if self.read_offset < len(self.src):
            return ord(self.src[self.read_offset])
        return 0  # EOF

    def next(self):
        if self.read_offset < len(self.src):
            self.offset = self.read_offset
            if self.ch == ord('\n'):
                self.line_offset = self.offset
                self.file.lines.append(self.offset)

            read_char = ord(self.src[self.read_offset])

            if read_char == 0:
                raise SlangError(self.offset, "illegal NUL character")
            
            self.read_offset += 1
            self.ch = read_char
    
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
    
    def scan_identifier(self) -> str:
        offset = self.offset
        while is_letter(self.ch) or is_digit(self.ch):
            self.next()

        return self.src[offset:self.offset]
    
    def scan_number(self) -> (token.Token, str):
        offset = self.offset
        seen_decimal_point = False
        while is_digit(self.ch) or self.ch == ord('.'):
            if self.ch == ord('.'):
                if seen_decimal_point:
                    raise SlangError(self.offset, "cannot have two decimal points in a number")
                seen_decimal_point = True
            self.next()

        if seen_decimal_point:
            found_token = token.Token.FLOAT
        else:
            found_token = token.Token.INTEGER
        
        return found_token, self.src[offset:self.offset]
    
    def skip_whitespace(self):
        while is_whitespace(self.ch):
            self.next()

    def scan(self) -> (int, token.Token, str):  # pos, token, literal
        self.skip_whitespace()

        pos = self.offset
        tok = None
        literal = None

        ch = self.ch
        if is_letter(ch):
            literal = self.scan_identifier()
            tok = token.lookup(literal)
        elif is_digit(ch) or ch == ord(".") and is_digit(self.peek()):
            tok, literal = self.scan_number()
        else:
            self.next()

            if ch == ord('\n'):  # newline forcibly ends any expression/statement
                return pos, token.Token.EOL, '\n'
            elif ch == ord('"'):
                tok = token.Token.STRING
                literal = self.scan_string()
            elif ch == ord('{'):
                tok = token.Token.LBRACKET
            elif ch == ord('}'):
                tok = token.Token.RBRACKET
            else:
                tok = token.Token.ILLEGAL
                literal = chr(ch)

        if literal is None:
            literal = chr(ch)

        return pos, tok, literal


def is_letter(ch: int) -> bool:
    return (
        ord('a') <= ch <= ord('z') or
        ord('A') <= ch <= ord('Z') or
        ch == ord('_')
    )

def is_digit(ch: int) -> bool:
    return ord('0') <= ch <= ord('9')

def is_whitespace(ch: int) -> bool:
    # newlines are not considered whitespace, as they are EOL
    if ch == ord(' '):
        return True
    elif ch == ord('\t'):
        return True
    return False

if __name__ == "__main__":
    my_scanner = Scanner("main.sl")
    while my_scanner.offset < my_scanner.file.size:
        print(my_scanner.scan())
