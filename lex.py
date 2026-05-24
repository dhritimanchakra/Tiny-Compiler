import sys
import enum
class Lexer:    
    def __init__(self,source):
        self.source = source + '\n' 
        self.curChar = ''  
        self.curPos = -1   
        self.nextChar()
    def nextChar(self):
        self.curPos+=1
        if self.curPos>=len(self.source):
            self.curChar='\0'
        else:
            self.curChar=self.source[self.curPos]
    def peek(self):
        if self.curPos+1>=len(self.source):
            return '\0'
        return self.source[self.curPos+1]
    def abort(self,message):
        sys.exit("Lexing error"+message)
    def getToken(self):
        self.skipWhiteSpace()
        self.skipComment()
        token=None
        if self.curChar=="+":
            token=Token(self.curChar,TokenType.PLUS)
        elif self.curChar=="-":
            token=Token(self.curChar,TokenType.MINUS)
        elif self.curChar=="*":
            token=Token(self.charChar,TokenType.ASTERISK)
        elif self.curChar=="/":
            token=Token(self.curChar,TokenType.SLASH)
        elif self.curChar=="=":
            if self.peek()=="=":
                lastChar=self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                token=Token(self.curChar,TokenType.EQ)
        elif self.curChar==">":
            if self.peek()=="=":
                lastChar=self.curChar
                self.nextChar()
                token=Token(lastChar+self.curChar,TokenType.GETQ)
            else:
                token=Token(self.curChar,TokenType.GT)
        elif self.curChar=="<":
            if self.peek()=="=":
                lastChar=self.curChar
                self.nextChar
                token=Token(lastChar+self.curChar,TokenType.LETQ)
            else:
                token=Token(self.curChar,TokenType.LT)
        elif self.curChar == '!':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek())
        elif self.curChar == '\"':
            
            self.nextChar()
            startPos = self.curPos

            while self.curChar != '\"':
               
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                    self.abort("Illegal character in string.")
                self.nextChar()

            tokText = self.source[startPos : self.curPos] # Get the substring.
            token = Token(tokText, TokenType.STRING)
