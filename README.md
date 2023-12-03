# Lex and parser

This was a final project that I made for my formal languages class. I created a lexer and parser for a CFG that we were given. The program also supports language interpretation and you can write custom test by creating a `.while` file inside of the test folder and running `parse.py`.

# CFG
```
P -> S ";" P | S
S -> "proc" f "(" L ")" "{" P "}"
    | "if" C "{" P "}" "else" "{" P "}"
    | "while" C "{" P "}"
    | "print" C
    | C
 L -> x "," X | x | Ɛ
 X -> x "," X | x
 C -> E | E "<" E | E "=" E | E ">" E
 E -> T M
 M -> "+" T M | "-" T M | Ɛ
 T -> F N
 N -> "*" F N | "/" F N | Ɛ
 F -> A | A "^" F
 A -> "(" C ")"
    | x ":" "=" C
    | f "(" R ")"
    | x
    | n
 R -> C "," Q | C | Ɛ
 Q -> C "," Q | C
 ```

 # Sample output

 ```
 *** Running tests/factorial.while ***
proc factorial(n){(r:=1.0);while (n<1.0) {(r:=(r*n));(n:=(n-1.0))};print r};factorial(5.0)
120.0

---------------
*** Running tests/fibonacci.while ***
proc fib(n){(i:=1.0);(a:=1.0);(b:=0.0);while (n<i) {(i:=(i+1.0));(a:=(a+b));(b:=(a-b))};a};print fib(12.0)
144.0

---------------
*** Running tests/ifelse.while ***
proc state(x){(y:=(x-3.0));(z:=0.0);if (x<5.0) {if (y=0.0) {(z:=1.0)} else {(z:=2.0)}} else {(z:=3.0)};print z};state(1.0);state(12.0);state(3.0)
2.0
3.0
1.0

---------------
*** Running tests/function.while ***
proc f(n){((1.0+n)+1.0)};(q:=2.0);(m:=1.0);print f(m);print f(q)
3.0
4.0

---------------
*** Running tests/innerProc.while ***
proc outerProc(x){(x:=(x*2.0))}

---------------
 ```