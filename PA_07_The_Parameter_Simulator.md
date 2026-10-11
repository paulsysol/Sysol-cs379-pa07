# PA 7: The Parameter Simulator
## CS 379: Programming Languages (Fall 2026)

**Starter repository (GitHub template):** [https://github.com/cwillpinto/cs379-pa07-parameter-simulator](https://github.com/cwillpinto/cs379-pa07-parameter-simulator)

### 🔧 Pipeline Context
This is the **argument-binding stage** of the USILang pipeline. It consumes the `ActivationRecord`/`CallStack` model from PA 6 — every call already gets a frame with locals, parameters, and links — and fills in exactly *how* arguments get copied (or not) into that frame's parameter slots. It also introduces **closures**, functions that carry their defining environment with them. The resulting call/closure mechanism becomes the dispatch target PA 8's VTable engine invokes next week.

**Schedule:** Tuesday, October 6 is Fall Break. The Thursday, October 8 session supports this complete 100-point Project-Oriented Assignment. Due Monday, October 12, 2026 at 11:59 PM Central.

**Verification question:** For each binding mode, identify who owns the writable cell, when the caller can observe a change, and which test would expose an incorrect implementation. Python's sharing of a mutable list object is a separate object-aliasing example; it is not itself USILang pass-by-reference.

---

### Part A: The Specification (50 Points)
**Instructions:** Answer the following in a separate document (PDF or Markdown).

1. **Three Modes, One Function:**
   Given the USILang function `swap(a, b) { let t = a; a = b; b = t; }` called as `swap(x, y)` where `x = 1` and `y = 2` beforehand, trace the values of `x` and `y` **in the caller's scope** after the call returns, under each of these binding modes:
   - Pass-by-value
   - Pass-by-reference
   - Pass-by-value-result
   Show the intermediate state of the callee's activation record (from PA 6) for each mode, not just the final answer.

2. **Asymmetric Aliasing:**
   Let `P(x, y) { x = x + 1; y = y + 1; }` and call `P(a, a)` with caller `a = 10`. Trace each assignment under pass-by-reference and pass-by-value-result. For value-result, copy back at return in parameter order, `x` then `y`. Explain why the final caller values are 12 and 11. A symmetric `swap(a,a)` leaves `a` unchanged in both modes and does not demonstrate the difference.

3. **Closures and Capture:**
   Consider building three closures inside a loop:
   ```
   let makers = [];
   for (i = 0; i < 3; i = i + 1) {
       makers.push(func() { return i; });
   }
   ```
   If each closure captures the **environment**, not a snapshot of `i`'s value at creation time, what do all three closures return when called after the loop finishes? Explain why, referencing the static link concept from PA 6. Then describe the minimal change to USILang's `for` semantics (not the closure mechanism) that would make each closure capture a *different* value of `i`, the way `let`-per-iteration works in JavaScript.

---

### Part B: The Implementation (50 Points)
**Instructions:** Implement parameter-mode binding and closures in `parameters.py`, extending the function-call evaluator from PA 6.

**Requirements:**
1. Implement the binder:
   ```python
   def bind_parameters(param_specs: list[tuple[str, str]], arg_nodes: list, caller_env, callee_record) -> None:
       # param_specs: [("a", "value"), ("b", "reference"), ...]
       ...
   ```
   `bind_parameters` must populate `callee_record.locals_env` (the PA 6 `Environment`) according to each parameter's declared mode:
   - `"value"`: copy the evaluated argument; later mutation inside the callee must not affect the caller.
   - `"reference"`: bind the callee's parameter name directly to the caller's variable slot, so writes inside the callee are visible in the caller immediately.
   - `"value-result"`: copy the value in on call, and copy the (possibly mutated) local value back out to the caller's variable **only when the function returns** — not on every intermediate write.
   - Record value-result destinations at call time and use `commit_value_result(callee_record, caller_env)` after the body. Copy back left to right in parameter declaration order.
2. Represent each function parameter's annotation in `param_specs` (for example, `[('a', 'reference'), ('b', 'reference')]` for `func swap(ref a, ref b)`). Unannotated parameters default to `value`. The supplied parser does not implement function-call syntax; the Python harness drives this interface directly.
3. Implement `Closure`:
   ```python
   class Closure:
       def __init__(self, declaration, defining_env):
           ...
       def call(self, args, caller_env):
           ...
   ```
   `Closure.call` must create the new callee `Environment` as a child of `defining_env` (the environment captured at closure-creation time), **not** a child of `caller_env`. This is what makes lexical scoping and correct closure capture work together with the static link from PA 6.
4. **Aliasing Safety:** your implementation must reproduce the asymmetric `P(a,a)` divergence from Part A. The harness checks both modes and the defined copy-back order.

**Dependency preflight:** Before running the harness, replace the placeholder `lexer.py`, `parser.py`, `symtable.py`, and `frames.py` with your completed prior-stage files. The harness checks these dependencies and reports a setup failure before the PA 7 tests if they remain incomplete.

**Verification:** Run `python test_parameters.py`. The harness checks `swap` under all three modes, asymmetric `P(a,a)`, and closure capture. If value-mode isolates the caller, reference-mode mutates it, value-result mode defers the ordered write-back to return time, and each closure resolves through its captured `defining_env`, the script prints:
```
PARAMETER_BINDING_VERIFIED
```

---

### 🚀 Submission
1. `PA7_Theory.pdf` (or `.md`) — Part A answers.
2. `parameters.py`, `lexer.py`, `parser.py`, `symtable.py`, and `frames.py` — your implementation and completed dependencies.
3. The full `python test_parameters.py` transcript, including the mode, asymmetric `P(a,a)`, and closure checks, ending with the **`PARAMETER_BINDING_VERIFIED`** Success Token.

### Grading Rubric (100 Points)

| Criterion | Points | Evidence |
| :--- | ---: | :--- |
| Three-mode `swap` trace | 20 | Caller and callee states under value, reference, and value-result. |
| Asymmetric `P(a,a)` trace | 20 | Assignment-by-assignment reasoning and left-to-right copy-back; final values 12 and 11. |
| Closure explanation | 10 | Captured environment, static link, and per-iteration-cell alternative. |
| Parameter binder | 25 | Correct private `Cell`, shared caller `Cell`, and recorded value-result destinations. |
| Ordered copy-back | 10 | Final callee values copied to caller at return, in parameter order. |
| Closure implementation | 10 | New call environment is a child of `defining_env`; free names resolve lexically. |
| Reproducible verification | 5 | Completed PA6 dependencies, full test transcript, and Success Token. |
