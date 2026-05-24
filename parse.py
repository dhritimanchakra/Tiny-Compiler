import sys
from lex import *

class Parser:
    def __init__(self,lexer,emitter):
        self.lexer=lexer
        self.emitter=emitter
        self.symbols=set()
        self.labelsDeclared=set()
        self.labelsGotoed = set()
        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()  
    def checkToken(self,kind):
        return kind==self.curToken.kind
    
    def checkPeek(self,kind):
        return kind==self.peekToken.kind
    
    def match(self,kind):
        if not self.checkToken(kind):
            self.abort("Expected "+kind.name+",got "+self.curToken.kind.name)
        self.nextToken()
    def nextToken(self):
        self.curToken=self.peekToken
        self.peekToken=self.lexer.getToken()
    def isComparisonOperator(self):
        return self.checkToken(TokenType.GT) or self.checkToken(TokenType.GTEQ) or self.checkToken(TokenType.LT) or self.checkToken(TokenType.LTEQ) or self.checkToken(TokenType.EQEQ) or self.checkToken(TokenType.NOTEQ)
    def abort(self,message):
        sys.exit("Error"+message)

    def program(self):
        self.emitter.headerLine("#include <stdio.h>")
        self.emitter.headerLine("int main(void){")

        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()
        while not self.checkToken(TokenType.EOF):
            self.statement()

        self.emitter.emitLine("return 0;")
        self.emitter.emitLine("}")
        for label in self.labelsGotoed:
            if label not in self.labelsDeclared:
                self.abort("Attempting to GOTO to undeclared label: " + label)
    def statement(self):
        if self.checkToken(TokenType.PRINT):
            self.nextToken()
            if self.checkToken(TokenType.STRING):
                self.emitter.emitLine("printf(\"" + self.curToken.text + "\\n\");")
                self.nextToken()
            else:
                self.emitter.emit("printf(\"%" + ".2f\\n\", (float)(")
                self.expression()
                self.emitter.emitLine("));")
        elif self.checkToken(TokenType.IF):
            self.nextToken()
            self.emitter.emit("if(")
            self.comparison()

            self.match(TokenType.THEN)
            self.nl()
            self.emitter.emitLine("){")
            while not self.checkToken(TokenType.ENDIF):
                self.statement()

            self.match(TokenType.ENDIF)
            self.emitter.emitLine("}")

        elif self.checkToken(TokenType.WHILE):
            self.nextToken()
            self.