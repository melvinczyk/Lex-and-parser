#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
from syntax import *


def lex(s):
    tokens = []
    current = ""

    for char in s:
        if char.isspace():
            if current:
                tokens.append(current)
                current = ""
        elif char in "+-/*^,:=<{}();":
            if current:
                tokens.append(current)
                current = ""
            tokens.append(char)
        else:
            current += char

    if current:
        tokens.append(current)

    #print(f"Tokens after lexing {tokens}")
    return tokens

def parse(toks):
    index = 0

    # Helper

    def isId(s):
        return re.match(r"[a-zA-Z_]\w*", s) is not None
    
    def isNum(s):
        return re.match(r"\d+(\.\d+)?", s) is not None
    
    def peek(n):
        nonlocal toks, index
        if index + n < len(toks):
            return toks[index + n]
        return None
    
    def expect(s):
        nonlocal toks, index
        token = peek(0)
        if token == s:
            if token is not None:
                index += 1
                return token
            else:
                return ErrorMsg(f"Unexpected end of input. Expected '{s}'")
        else:
            return ValueError(f"Expected '{s}', but got {token}")
        

    # Parsing begins

    def parseP():
        s = parseS()
        while peek(0) == ";":
            expect(";")
            s = SeqStmt(s,parseS())
        return s

    def parseS():
        if peek(0) == "proc":
            expect("proc")
            f = peek(0) 
            if isId(f):
                expect(f)
            else:
                raise ErrorMsg(f"Expected an identifier, but got {f}")
            if peek(0) == "(":
                expect("(")
                params = parseL()
                expect(")")
                expect("{")
                inside = parseP()
                expect("}")
                return ProcStmt(Var(f), params, inside)
            else:
                raise ValueError(f"Expected '(', but got {peek(0)}")

        elif peek(0) == "if":
            expect("if")
            guard = parseC()
            expect("{")
            then = parseP()
            expect("}")
            expect("else")
            expect("{")
            else_inside = parseP()
            expect("}")
            return IfStmt(guard, then, else_inside)

        elif peek(0) == "while":
            expect("while")
            guard = parseC()
            expect("{")
            inside = parseP()
            expect("}")
            return WhileStmt(guard, inside)

        elif peek(0) == "print":
            expect("print")
            rhs = parseC()
            return PrintStmt(rhs)

        else:
            if peek(0) is not None:
                return parseC()
        if peek(0) == ";":
            expect(";")
        return parseC()
    
    def parseL():
        if isId(peek(0)):
            param = Var(expect(peek(0)))
            params = parseX()
            return [param] + params
        return []
    
    def parseX():
        if peek(0) == ",":
            expect(",")
            param = Var(expect(peek(0)))
            params = parseX()
            return [param] + params
        return []
    
    def parseC():
        left = parseE()
        if peek(0) == "<":
            expect("<")
            right = parseE()
            return LessThan(left, right)
        
        elif peek(0) == ">":
            expect(">")
            right = parseE()
            return GreaterThan(left, right)
        
        elif peek(0) == "=":
            expect("=")
            right = parseE()
            return Equal(left, right)
        return left
            
    def parseE():
        term = parseT()
        return parseM(term)
    
    def parseM(left):
        if peek(0) in {"+", "-"}:
            operator = expect(peek(0))
            right = parseT()
            if operator == "+":
                left = Plus(left, right)
            else:
                left = Minus(left,right)
            return parseM(left)
        else:
            return left

    def parseT():
        factor = parseF()
        return parseN(factor)
    
    def parseN(left):
        if peek(0) in {"*", "/"}:
            operator = expect(peek(0))
            right = parseF()
            if operator == "*":
                left = Mult(left, right)
            else:
                left = Div(left,right)
            return parseN(left)
        else:
            return left
    
    def parseF():
        a = parseA()
        if peek(0) == "^":
            expect("^")
            return Expo(a,parseF()) # ditto
        else:
            return a
        
    def parseA():
        if peek(0) == "(":
            expect("(")
            params = parseC()
            expect(")")
            return params
        elif isId(peek(0)):
            identifier = expect(peek(0))
            if peek(0) == ":":
                expect(":")
                expect("=")
                value = parseC()
                return Assign(Var(identifier),value)
            elif peek(0) == "(":
                expect("(")
                arguments = parseR()
                expect(")")
                return Call(Var(identifier), arguments)
            else:
                return Var(identifier)
        elif isNum(peek(0)):
            value = float(expect(peek(0)))
            return Lit(value)
        else:
            return ErrorMsg(f"Unexpected token: {peek(0)}")
        
    def parseR():
        expressions = [parseC()]
        while peek(0) == ",":
            expect(",")
            expressions.append(parseC())
        return expressions
        
    
    ast = parseP()
    if isinstance(ast, ErrorMsg):
        return ast
    return ast

def run_file(path):
    with open(path, "r") as file:
        program = "".join(file.readlines())
        ast = parse(lex(program))
        print(ast)
        print(ast.run())


if __name__ == "__main__":
    dir = "tests"
    files = [f for f in os.listdir(dir) if f.endswith(".while")]

    for f in files:
        path = os.path.join(dir, f)
        print(f"*** Running {path} ***")
        run_file(path)
        print("---------------")