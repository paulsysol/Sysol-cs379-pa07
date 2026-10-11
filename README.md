# PA 7: The Parameter Simulator

Full assignment: `PA_07_The_Parameter_Simulator.md` (course handout; copy it alongside this starter when staging the repository).

## GitHub workflow
Use **Use this template** to create your own repository, clone it, add your
completed prior-stage dependencies, and commit and push your PA 7 work. Submit
the files and evidence listed in the assignment through Blackboard.

## Setup
Paste your own completed `lexer.py`/`parser.py`/`symtable.py`/`frames.py`
in first.
The harness checks these dependencies before the PA 7 cases and gives an
actionable error if the prior-stage placeholders are still present.

## Run
```bash
python test_parameters.py
```
Complete `bind_parameters`, `commit_value_result`, and `Closure` in
`parameters.py` (`Cell`, `evaluate()`, and `FunctionDecl` are already
given). Success Token: prints the literal string
`PARAMETER_BINDING_VERIFIED` once every check passes.

For value-result, `bind_parameters` records destinations at call time and
`commit_value_result` copies final values back at return, left to right in
parameter order. The asymmetric `P(a,a)` test distinguishes this from reference.

## Submit
1. `PA7_Theory.pdf` (or `.md`)
2. `parameters.py`, `lexer.py`, `parser.py`, `symtable.py`, `frames.py`
3. Full `python test_parameters.py` transcript, including swap, asymmetric `P(a,a)`, closure checks, and `PARAMETER_BINDING_VERIFIED`
