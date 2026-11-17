<div align="center">

<img src="https://skillicons.dev/icons?i=python,vscode,html,js,latex,windows&theme=dark" alt="Python, VS Code, HTML, JavaScript, LaTeX and Windows" />

# 🧮 Parsers & SDD Evaluator

### FIRST & FOLLOW · LL(1) and SLR(1) parsers · Syntax-directed definition with a dependency graph

![Python](https://img.shields.io/badge/Python-3.13.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![VS Code](https://img.shields.io/badge/VS%20Code-Editor-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-Visualizer-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![Windows 11](https://img.shields.io/badge/Windows%2011-25H2-0078D4?style=for-the-badge&logo=windows11&logoColor=white)

![Course](https://img.shields.io/badge/SI2002-Formal%20Languages-15107A?style=for-the-badge)
![Book](https://img.shields.io/badge/Dragon%20Book-Ch.%204%20%26%205-BDF2D0?style=for-the-badge&labelColor=15107A)
![Report](https://img.shields.io/badge/Report-informe.pdf-B31B1B?style=for-the-badge&logo=adobeacrobatreader&logoColor=white)

**🎓 EAFIT University · Final Project**

</div>

---

## 🧭 Table of contents

| # | Section |
|:-:|---|
| 1 | [🎓 Project cover page](#cover) |
| 2 | [🛠️ Versions and tools](#versions) |
| 3 | [📖 Project description](#description) |
| 4 | [🧠 Algorithms from the book](#algorithms) |
| 5 | [▶️ How to run it (VS Code and terminal)](#running) |
| 6 | [📥 Items 1 & 2: input and output](#items12) |
| 7 | [🧮 Item 3: the SDD evaluator](#item3) |
| 8 | [🌐 The HTML visualizer (optional)](#html) |
| 9 | [🧪 Step-by-step testing guide](#tests) |
| 10 | [🗂️ What each file does](#files) |
| 11 | [🤖 Use of generative AI](#ai) |
| 12 | [📚 References](#references) |

---

<a id="cover"></a>

## 🎓 1. Project cover page

| | |
|---|---|
| 📝 **Project title** | Final Project: FIRST & FOLLOW, LL(1) and SLR(1) parsers, and SDD evaluation |
| 📚 **Course / class** | SI2002 · Formal Languages |
| 👨‍🏫 **Professor** | Sergio Ramírez Rico |
| 👩‍💻👨‍💻 **Students** | **Simón Santiago Soto Berrio** · **Dilan Acevedo Rivera** |
| 🐍 **Programming language** | Python 3.13.13 |
| 🧰 **Tools** | Visual Studio Code (code) · an HTML page (visualizer) · LaTeX on Overleaf (report) |
| 📄 **Report** | [`informe.pdf`](informe.pdf) (in Spanish) |
| 📖 **Reference** | Aho, Lam, Sethi & Ullman (2006). *Compilers: Principles, Techniques, and Tools*, 2nd ed. |

---

<a id="versions"></a>

## 🛠️ 2. Versions and tools

| Category | Detail |
|---|---|
| 🪟 **Operating system** | Windows 11, version **25H2** |
| 🐍 **Programming language** | **Python 3.13.13** |
| 📦 **Python libraries** | Only the **standard library** (`sys`, `os`, `json`, `pathlib`, `webbrowser`). No `pip install` needed. |
| 🚫 **Parser libraries** | **None.** No parser generators or parsing libraries (as the assignment requires). |
| 💻 **Editor** | Visual Studio Code |
| 🌐 **Visualizer** | Any modern browser (Chrome, Edge, Firefox). Works **offline**: no external libraries. |
| 📝 **Report** | LaTeX, compiled with pdfLaTeX on Overleaf |

---

<a id="description"></a>

## 📖 3. Project description

The project implements three pieces of a compiler front end, following the book:

| Item | What it does | Program |
|:-:|---|:-:|
| 1️⃣ | Computes the **FIRST** and **FOLLOW** sets of any context-free grammar (also with ε-productions). | `main.py` |
| 2️⃣ | Builds an **LL(1)** (top-down) and an **SLR(1)** (bottom-up) parser, decides if the grammar is LL(1), SLR(1), both or neither, and answers `yes`/`no` for each input string. | `main.py` |
| 3️⃣ | Defines our own **SDD** (a prefix calculator) and evaluates it on the parse tree using the **dependency graph** and a **topological order**. Detects circular SDDs. | `sdd_main.py` |
| ✨ | Optional **HTML visualizer**: parse tree, dependency graph and evaluation step by step. | `sdd_main.py --html` |

For every input, `main.py` does this:

1. 📥 **Reads** the grammar (and later the strings) with the exact format of the assignment.
2. 🧮 **Computes** FIRST and FOLLOW.
3. 🧱 **Builds** the LL(1) table and the SLR(1) table (LR(0) automaton + ACTION/GOTO).
4. ⚖️ **Decides** which parsers can be used (looking for conflicts).
5. ✅ **Parses** each string and prints `yes` or `no`.

---

<a id="algorithms"></a>

## 🧠 4. Algorithms from the book

| Part | Book | Our function |
|---|---|---|
| 🔤 FIRST and FOLLOW | Section 4.4.2 | `FirstFollow.calcular_first`, `calcular_follow` |
| ✅ LL(1) condition | Section 4.4.3 (definition) | `TablaLL1.cumple_condicion_ll1` |
| 📋 LL(1) table | Algorithm 4.31 (Fig. 4.17) | `TablaLL1.construir` |
| ⬇️ Predictive parser | Algorithm 4.34 (Fig. 4.20, moves as in Fig. 4.21) | `ParserLL1.analizar` |
| 🔁 CLOSURE / GOTO | Section 4.6.2 (Fig. 4.32) | `AutomataLR0.cerradura`, `ir_a` |
| 🧩 LR(0) automaton | Fig. 4.33 (example Fig. 4.31) | `AutomataLR0.construir_coleccion` |
| 📊 SLR(1) table | Algorithm 4.46 (Fig. 4.37) | `TablaSLR1.construir` |
| ⬆️ LR parser | Algorithm 4.44 (Fig. 4.36, moves as in Fig. 4.38) | `ParserSLR1.analizar` |
| 🕸️ Dependency graph | Section 5.2.1 (Fig. 5.7) | `GrafoDependencias.construir` |
| 🔢 Topological order | Section 5.2.2 | `GrafoDependencias.orden_topologico` |
| 🧮 Evaluation | Section 5.2.2 | `EvaluadorSDD.evaluar` |

> 🌳 **What we added to the book:** both parsers also **build the parse tree** (the book's algorithms only "output" the productions), because Item 3 needs it.

---

<a id="running"></a>

## ▶️ 5. How to run it (VS Code and terminal)

### 5.1 ✅ Requirements

- 🐍 **Python 3** installed (we used **3.13.13**). Check it with `python --version`.
- 📦 **Nothing to compile or install**: Python is interpreted and only the standard library is used.
- 🌐 A **web browser**, only for the optional visualizer.

### 5.2 💻 From Visual Studio Code

1. 📂 Open the **project folder**: `File → Open Folder…` *(open the folder, not a single file, so the paths to `tests/` work).*
2. 🖥️ Open a terminal: `Terminal → New Terminal`.
3. ▶️ Type the commands of the table below.

### 5.3 ⌨️ Commands

| What | Command |
|---|---|
| 🅰️ Items 1 & 2 | `python main.py` |
| 🔤 + FIRST and FOLLOW | `python main.py --sets` |
| 📊 + LL(1) table, LR(0) automaton and SLR(1) table | `python main.py --tables` |
| 👣 + parse step by step | `python main.py --trace` |
| 🅱️ Item 3 (SDD) | `python sdd_main.py` |
| 📘 + attribute table and semantic rules | `python sdd_main.py --info` |
| 🕸️ + edges of the dependency graph | `python sdd_main.py --graph` |
| 🔁 Circular version of the SDD | `python sdd_main.py --circular` |
| 🌐 + HTML visualizer (opens by itself) | `python sdd_main.py --html` |

> 🧩 Options can be combined: `python main.py --sets --tables --trace` · `python sdd_main.py --circular --html`

### 5.4 📄 Reading the input from a file

Instead of typing, you can send one of the files in `tests/` to the program:

```powershell
# Windows PowerShell (VS Code default): pipe the file contents in
Get-Content tests\grammars\example1.txt | python main.py
Get-Content tests\sdd_strings.txt | python sdd_main.py
```

```bash
# CMD, Linux or macOS: input redirection
python main.py < tests/grammars/example1.txt
python sdd_main.py < tests/sdd_strings.txt
```

```powershell
# Windows: if the "python" command does not respond, try the "py" launcher
py main.py
```

> ⚠️ **PowerShell does not support `<`** (it raises an error). There, use `Get-Content file.txt | python main.py`.
> 🐧 On Linux/macOS the command is usually `python3`.

---

<a id="items12"></a>

## 📥 6. Items 1 & 2: input and output

### 6.1 📐 Input format (Section 2.2 of the assignment)

```text
n                        ← number of nonterminals
A -> alt1 alt2 ...       ← n lines, alternatives separated by blanks
...
string 1                 ← strings to parse, one per line
string 2
                         ← an empty line ends the strings
```

| Rule | Meaning |
|---|---|
| 🅢 `S` | Always the **start symbol** |
| 🔠 Uppercase letters | **Nonterminals** |
| 🔡 Any other character | **Terminals** |
| ⭕ `e` | The **empty string ε** (also used to give the empty string as input) |
| 💲 `$` | Reserved: end of the input (the program adds it) |

### 6.2 ⚖️ What the program prints

| The grammar is… | The program prints | Then you type |
|---|---|---|
| ✅✅ **LL(1) and SLR(1)** | `Select a parser (T: for LL(1), B: for SLR(1), Q: quit):` | `T` or `B`, the strings and an empty line (back to the menu). `Q` quits. |
| ✅ **Only LL(1)** | `Grammar is LL(1).` | The strings and an empty line |
| ✅ **Only SLR(1)** | `Grammar is SLR(1).` | The strings and an empty line |
| ❌ **Neither** | `Grammar is neither LL(1) nor SLR(1).` | Nothing: the program ends |

For each string: **`yes`** if it belongs to the language, **`no`** if it does not.

### 6.3 🔍 Annotated example (Example 2 of the assignment)

```text
3                 ← 3 nonterminals
S -> AB           ← S → AB
A -> aA d         ← A → aA | d
B -> bBc e        ← B → bBc | ε
Select a parser (T: for LL(1), B: for SLR(1), Q: quit):
T                 ← use the LL(1) parser
d                 ← string 1
yes
adbc              ← string 2
yes
a                 ← string 3
no
                  ← empty line: back to the menu
Select a parser (T: for LL(1), B: for SLR(1), Q: quit):
Q                 ← quit
```

---

<a id="item3"></a>

## 🧮 7. Item 3: the SDD evaluator

### 7.1 ➕ Our SDD: a prefix calculator

The operator goes **first** and is applied to **all** its arguments, from left to right.

```text
S -> E
E -> O(ER) | 0 | 1 | ... | 9
O -> + | * | -
R -> ,ER | e
```

| Expression | Meaning | Value |
|---|---|:-:|
| `+(1,2)` | 1 + 2 | **3** |
| `-(9,2,3)` | (9 − 2) − 3 | **4** |
| `*(2,-(5,1))` | 2 · (5 − 1) | **8** |
| `5` | a single digit | **5** |

### 7.2 🏷️ Attributes

| Symbol | Attribute | Kind | Meaning |
|:-:|:-:|:-:|---|
| `S` | `val` | 🟣 synthesized | value of the whole expression (**main attribute**) |
| `E` | `val` | 🟣 synthesized | value of the expression |
| `O` | `op` | 🟣 synthesized | the operator: `+`, `*` or `-` |
| `R` | `op` | 🟢 inherited | operator to apply to the remaining arguments |
| `R` | `acc` | 🟢 inherited | result of the arguments to the left |
| `R` | `val` | 🟣 synthesized | result after applying `op` to all the arguments |
| terminals | `lexval` | 🟣 synthesized | the character itself (given by the scanner) |

### 7.3 📜 Semantic rules

| Production | Semantic rules |
|---|---|
| `S → E` | `S.val = E.val` |
| `E → O ( E₁ R )` | `R.op = O.op` · `R.acc = E₁.val` · `E.val = R.val` |
| `E → digit` | `E.val = digit.lexval` |
| `O → + \| * \| -` | `O.op = (operator).lexval` |
| `R → , E R₁` | `R₁.op = R.op` · `R₁.acc = R.acc (R.op) E.val` · `R.val = R₁.val` |
| `R → ε` | `R.val = R.acc` |

> 🏷️ The SDD is **L-attributed** but **not S-attributed** (it has inherited attributes). The evaluator does not rely on that: it uses the general **dependency graph** method, so it works for any non-circular SDD.

### 7.4 ⚙️ How the evaluator works

| Step | What happens | File |
|:-:|---|:-:|
| 1️⃣ | The SDD is stored as **data** (each rule: what it defines, what it uses, the function). | `sdd.py` |
| 2️⃣ | Our **LL(1) parser** from Item 2 parses the string and builds the **parse tree**. | `ll1.py` |
| 3️⃣ | One vertex per attribute of each node; one edge from each attribute used to the one defined. | `evaluator.py` |
| 4️⃣ | A **topological order** is computed. If there is a cycle → *"The SDD is circular"* and it stops. | `evaluator.py` |
| 5️⃣ | The attributes are computed in that order. | `evaluator.py` |

### 7.5 🖥️ What is printed

| Output | Meaning |
|---|---|
| `no` | The string is not in the language |
| `Annotated parse tree:` | Each node (`symbol#number`) with its attribute values |
| `Evaluation order:` | The topological order, with the value and the rule of each attribute |
| `Result: S.val = …` | The value of the main attribute |

---

<a id="html"></a>

## 🌐 8. The HTML visualizer (optional)

`python sdd_main.py --html` creates **`visualizer.html`** in the project folder and **opens it in the browser** (if it does not open, double-click it).

| Part | What it shows |
|---|---|
| 🌳 **Parse tree** | Each node with its attributes: inherited on the left, synthesized on the right |
| 🕸️ **Dependency graph** | Arrows between attributes (edge `u → v` means *v uses u*) |
| 👣 **Step by step** | The evaluation in topological order, with the rule and the values used in each step |
| 📋 **Side panel** | The evaluation order (click a row to jump to that step) and the legend |
| 🔁 **Circular SDD** | The attributes that could not be ordered, in red |

---

<a id="tests"></a>

## 🧪 9. Step-by-step testing guide

One example for each command. Lines marked with `←` are the ones you type.

| # | Command | Example | Expected result |
|:-:|---|---|---|
| 1 | `python main.py` | Example 2 of the assignment | menu · `yes`, `yes`, `no` |
| 2 | `python main.py --sets` | Book Example 4.30 | the FIRST/FOLLOW sets of the book |
| 3 | `python main.py --tables` | Example 2 of the assignment | LL(1) table, LR(0) automaton, SLR(1) table |
| 4 | `python main.py --trace` | Our grammar with `+(1,2)` | the moves of the LL(1) parser |
| 5 | `python sdd_main.py` | `+(1,2)` | annotated tree, order, `S.val = 3` |
| 6 | `python sdd_main.py --info` | — | attribute table and semantic rules |
| 7 | `python sdd_main.py --graph` | `+(1,2)` | the 13 edges of the dependency graph |
| 8 | `python sdd_main.py --circular` | `+(1,2)` | *"The SDD is circular…"* |
| 9 | `python sdd_main.py --html` | `+(1,2)` | the visualizer opens in the browser |

<details>
<summary>1️⃣ <code>python main.py</code> · Example 2 of the assignment</summary>

```text
3                 ←
S -> AB           ←
A -> aA d         ←
B -> bBc e        ←
Select a parser (T: for LL(1), B: for SLR(1), Q: quit):
T                 ←
d                 ←
yes
adbc              ←
yes
a                 ←
no
                  ←  (empty line)
Select a parser (T: for LL(1), B: for SLR(1), Q: quit):
Q                 ←
```
</details>

<details>
<summary>2️⃣ <code>python main.py --sets</code> · Book Example 4.30</summary>

```text
5                 ←
S -> TA           ←
A -> +TA e        ←
T -> FB           ←
B -> *FB e        ←
F -> (S) i        ←
First(A) = {+, e}
First(B) = {*, e}
First(F) = {(, i}
First(S) = {(, i}
First(T) = {(, i}
Follow(A) = {), $}
Follow(B) = {), +, $}
Follow(F) = {), *, +, $}
Follow(S) = {), $}
Follow(T) = {), +, $}
Select a parser (T: for LL(1), B: for SLR(1), Q: quit):
Q                 ←
```

📘 These are exactly the sets of Example 4.30 of the book (E = `S`, E′ = `A`, T′ = `B`, id = `i`).
</details>

<details>
<summary>3️⃣ <code>python main.py --tables</code> · Example 2 of the assignment</summary>

Type the same grammar of exercise 1. Before the menu, the program prints:

```text
LL(1) parsing table M
   | a       | b        | c      | d       | $
---+---------+----------+--------+---------+--------
 A | A -> aA |          |        | A -> d  |
 B |         | B -> bBc | B -> e |         | B -> e
 S | S -> AB |          |        | S -> AB |
```

…followed by the **LR(0) automaton** (states `I0, I1, …` with their items and GOTOs) and the **SLR(1) table** (ACTION and GOTO).
</details>

<details>
<summary>4️⃣ <code>python main.py --trace</code> · Our grammar with <code>+(1,2)</code></summary>

```text
4                                 ←
S -> E                            ←
E -> O(ER) 0 1 2 3 4 5 6 7 8 9    ←
O -> + * -                        ←
R -> ,ER e                        ←
Select a parser (T: for LL(1), B: for SLR(1), Q: quit):
T                                 ←
+(1,2)                            ←
MATCHED  STACK   INPUT    ACTION
         S$      +(1,2)$  output S -> E
         E$      +(1,2)$  output E -> O(ER)
         O(ER)$  +(1,2)$  output O -> +
         +(ER)$  +(1,2)$  match +
+        (ER)$   (1,2)$   match (
+(       ER)$    1,2)$    output E -> 1
+(       1R)$    1,2)$    match 1
+(1      R)$     ,2)$     output R -> ,ER
+(1      ,ER)$   ,2)$     match ,
+(1,     ER)$    2)$      output E -> 2
+(1,     2R)$    2)$      match 2
+(1,2    R)$     )$       output R -> e
+(1,2    )$      )$       match )
+(1,2)   $       $        accept
yes
```

💡 Choosing `B` instead of `T` shows the moves of the SLR(1) parser (STACK, SYMBOLS, INPUT, ACTION).
</details>

<details>
<summary>5️⃣ <code>python sdd_main.py</code> · <code>+(1,2)</code></summary>

```text
+(1,2)            ←
String: +(1,2)
Annotated parse tree:
S#1  {val=3}
    E#2  {val=3}
        O#3  {op=+}
            +#4  {lexval=+}
        (#5  {lexval=(}
        E#6  {val=1}
            1#7  {lexval=1}
        R#8  {acc=1, op=+, val=3}
            ,#9  {lexval=,}
            E#10  {val=2}
                2#11  {lexval=2}
            R#12  {acc=3, op=+, val=3}
                e#13
        )#14  {lexval=)}
Evaluation order:
     1. O#3.op = +    (O.op = +.lexval)
     2. E#6.val = 1    (E.val = digit.lexval)
     3. R#8.acc = 1    (R.acc = E1.val)
     4. R#8.op = +    (R.op = O.op)
     5. E#10.val = 2    (E.val = digit.lexval)
     6. R#12.acc = 3    (R1.acc = R.acc (R.op) E.val)
     7. R#12.op = +    (R1.op = R.op)
     8. R#12.val = 3    (R.val = R.acc)
     9. R#8.val = 3    (R.val = R1.val)
    10. E#2.val = 3    (E.val = R.val)
    11. S#1.val = 3    (S.val = E.val)
Result: S.val = 3
                  ←  (empty line)
```

🧾 It is the same example worked by hand in the report. A string outside the language, like `+(1,2` or `12`, prints `no`.
</details>

<details>
<summary>6️⃣ <code>python sdd_main.py --info</code></summary>

Before asking for strings, the program prints the SDD:

```text
Attributes:
  Symbol    Attr    Kind         Type  Meaning
  S         val     synthesized  int   value of the whole expression (main attribute)
  E         val     synthesized  int   value of the expression E
  O         op      synthesized  char  the operator: '+', '*' or '-'
  R         op      inherited    char  operator to apply to the remaining arguments
  R         acc     inherited    int   result of the arguments to the left of R
  R         val     synthesized  int   result after applying op to all the arguments
  terminal  lexval  synthesized  char  the character itself (given by the scanner)

Semantic rules:
  Production    Semantic rules
  S -> E        S.val = E.val
  E -> O(ER)    R.op = O.op; R.acc = E1.val; E.val = R.val
  E -> 0        E.val = digit.lexval
  ...
  R -> ,ER      R1.op = R.op; R1.acc = R.acc (R.op) E.val; R.val = R1.val
  R -> e        R.val = R.acc
```
</details>

<details>
<summary>7️⃣ <code>python sdd_main.py --graph</code> · <code>+(1,2)</code></summary>

Between the annotated tree and the evaluation order, the program prints the edges:

```text
Dependency graph (edge u -> v means v uses u):
    E#2.val -> S#1.val
    O#3.op -> R#8.op
    +#4.lexval -> O#3.op
    E#6.val -> R#8.acc
    1#7.lexval -> E#6.val
    R#8.acc -> R#12.acc
    R#8.op -> R#12.acc
    R#8.op -> R#12.op
    R#8.val -> E#2.val
    E#10.val -> R#12.acc
    2#11.lexval -> E#10.val
    R#12.acc -> R#12.val
    R#12.val -> R#8.val
```
</details>

<details>
<summary>8️⃣ <code>python sdd_main.py --circular</code> · <code>+(1,2)</code></summary>

```text
+(1,2)            ←
The SDD is circular: the dependency graph has a cycle. These attributes could not be ordered: S#1.val, E#2.val, R#8.acc, R#8.val, R#12.acc, R#12.val
Evaluation stopped.
```

🔁 This version changes `R.acc = E1.val` into `R.acc = E.val`, which creates the cycle
`R#8.acc → R#12.acc → R#12.val → R#8.val → E#2.val → R#8.acc`.
</details>

<details>
<summary>9️⃣ <code>python sdd_main.py --html</code> · <code>+(1,2)</code></summary>

Type `+(1,2)` and an empty line. `visualizer.html` opens in the browser: move through the **11 steps** with **→** and check that the order is the same as in exercise 5.
</details>

---

<a id="files"></a>

## 🗂️ 10. What each file does

### 🌳 Project structure

```text
📁 proyecto-lenguajes-formales/
├── 📄 informe.pdf                ← project report (Spanish)
├── 📝 README.md                  ← this document
│
├── 🐍 main.py                    ← Items 1 & 2: entry point
├── 🐍 grammar.py                 ← grammar, productions, input reading
├── 🐍 first_follow.py            ← Item 1: FIRST and FOLLOW
├── 🐍 ll1.py                     ← Item 2: LL(1) table and parser
├── 🐍 slr1.py                    ← Item 2: LR(0) automaton, SLR(1) table and parser
├── 🐍 parse_tree.py              ← the parse tree (nodes)
│
├── 🐍 sdd_main.py                ← Item 3: entry point
├── 🐍 sdd.py                     ← Item 3: our SDD stored as data
├── 🐍 evaluator.py               ← Item 3: dependency graph and evaluation
├── 🐍 visualizer.py              ← Item 3 (optional): builds the HTML
├── 🌐 visualizer_template.html   ← Item 3 (optional): page template
│
└── 📁 tests/
    ├── 📄 sdd_strings.txt        ← strings for Item 3
    └── 📁 grammars/              ← example inputs for main.py
```

### 📚 Summary of each file

| File | What it does | Main pieces |
|---|---|---|
| 🐍 **`main.py`** | **Coordinates Items 1 & 2.** Reads the grammar, builds both tables, decides the case (LL(1), SLR(1), both, neither) and parses the strings. | `Programa.ejecutar()`, `analizar_cadenas()` |
| 🐍 **`grammar.py`** | Defines **productions** and **grammars**, the augmented grammar, and reads the input. | `Produccion`, `Gramatica`, `aumentada()`, `leer_gramatica()`, `tokenizar()` |
| 🐍 **`first_follow.py`** | **FIRST and FOLLOW** with the rules of Section 4.4.2, repeated until nothing changes. | `FirstFollow`, `first_de_cadena()`, `imprimir()` |
| 🐍 **`ll1.py`** | **LL(1) table** (Alg. 4.31), LL(1) condition and **predictive parser** (Alg. 4.34) that builds the tree. | `TablaLL1`, `ParserLL1` |
| 🐍 **`slr1.py`** | **LR(0) automaton** (CLOSURE, GOTO), **SLR(1) table** (Alg. 4.46) and **LR parser** (Alg. 4.44) that builds the tree. | `AutomataLR0`, `TablaSLR1`, `ParserSLR1` |
| 🐍 **`parse_tree.py`** | The **parse tree**: each node has its symbol, production, children and attributes. | `Nodo`, `hoja_terminal()`, `hoja_epsilon()` |
| 🐍 **`sdd_main.py`** | **Coordinates Item 3.** Validates the SDD, parses each string with our LL(1) parser, evaluates it and prints the result. | `ProgramaSDD.ejecutar()` |
| 🐍 **`sdd.py`** | **Our SDD as data**: grammar, attribute table, semantic rules and the circular version. Also checks that the SDD is well defined. | `crear_sdd()`, `SDD.validar()` |
| 🐍 **`evaluator.py`** | **Dependency graph** (5.2.1), **topological order** (5.2.2) and evaluation. Works for any SDD. | `GrafoDependencias`, `EvaluadorSDD`, `SDDCircular` |
| 🐍 **`visualizer.py`** | Turns the tree, the graph and the order into data and writes `visualizer.html`. | `datos_de_un_caso()`, `escribir_html()` |
| 🌐 **`visualizer_template.html`** | The page (HTML + JavaScript) that draws the tree and the graph and plays the evaluation. | |
| 🌐 **`visualizer.html`** | **Generated automatically** with `--html`. It does not need to be edited. | |

---

<a id="ai"></a>

## 🤖 11. Use of generative AI

We used **Claude** (model **Claude Opus 5.5**, by Anthropic, through [claude.ai](https://claude.ai)) as a support tool:

| | Purpose |
|:-:|---|
| 💻 | **Generate program code**, especially the parts that were hardest for us to program, such as the canonical collection of LR(0) items (`AutomataLR0` in `slr1.py`) and the dependency graph with the topological order (`GrafoDependencias` in `evaluator.py`), because we have little programming experience |
| 🌐 | **Generate the optional HTML visualizer** (`visualizer.py` and `visualizer_template.html`) |
| 🔍 | Review the code against the assignment and find what was missing (for example, the incomplete check in `SDD.validar()`) |
| 🧪 | Test the parsers with more grammars |
| 💡 | Discuss whether our first SDD met rule G3 and propose alternatives (we chose the prefix calculator) |
| 📝 | Review and complete the writing of the report |

---

<a id="references"></a>

## 📚 12. References

- 📕 A. V. Aho, M. S. Lam, R. Sethi and J. D. Ullman. *Compilers: Principles, Techniques, and Tools*, 2nd ed. Addison-Wesley, 2006.
- 📊 S. Ramírez Rico. *Lenguajes Formales y Compiladores: Syntax Analysis* (class slides). Universidad EAFIT, 2025.
- 📄 SI2002 Formal Languages, Final project statement. Universidad EAFIT, October 19, 2026.

---

<div align="center">

**Simón Santiago Soto Berrio** · **Dilan Acevedo Rivera**

🎓 Universidad EAFIT · SI2002 Formal Languages · 2026

</div>
