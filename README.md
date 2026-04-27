MiniLang Compiler

1. Descriere
  Acest proiect reprezinta un compilator simplificat pentru un limbaj numit MiniLang. Scopul lui este sa demonstreze etapele principale ale compilarii: analiza lexicala, sintactica, semantica, generare de cod intermediar, optimizare si generare de cod final.


2. Structura proiectului

- lexer.py – analiza lexicala (transforma textul in tokeni)
- parser.py – analiza sintactica (construieste AST)
- ast_nodes.py – definitiile nodurilor AST
- semantic.py – analiza semantica (verifica tipuri si variabile)
- ir.py – generare cod intermediar (TAC)
- optimizer.py – optimizare cod
- codegen.py – generare cod C
- main.py – ruleaza intreg compilatorul



3. Cum functioneaza

Fluxul compilatorului este:
- Codul MiniLang este citit din fisier (program.min)
- Lexerul genereaza tokeni
- Parserul construieste AST
- Analizorul semantic verifica programul
- Se genereaza cod intermediar (TAC)
- Codul este optimizat
- Se genereaza cod C
- GCC compileaza codul C in executabil `.exe`


4. Cum rulezi proiectul

- Ruleaza compilatorul
powershell
& "C:\Users\Ariana\AppData\Local\Programs\Python\Python313\python.exe" main.py

- Ruleaza programul generat
powershell
.\output\program.exe


5. Fisiere generate

In folderul output vei gasi:
- tokens.txt – lista de tokeni
- ast.txt – arborele AST
- tac.txt – cod intermediar\
- tac_optimized.txt – cod optimizat
- output.c – cod C generat
- program.exe – executabilul final


6. Exemplu
int x;
float y;
bool ok;

x = 10;
y = x * 2 + 5.5;
ok = true;

if (y > 20 && ok) {
    print(y);
}

while (x < 15) {
    x = x + 1;
}



7. Tehnologii folosite

- Python – pentru implementarea compilatorului
- GCC – pentru generarea executabilului


8. Observatii

- Lexerul este implementat manual (similar unui DFA)
- Parserul este de tip recursive descent
- Codul intermediar este de tip TAC (Three Address Code)
- Codul final este generat in C si compilat cu GCC
