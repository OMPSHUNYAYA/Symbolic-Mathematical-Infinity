# Getting Started — SSM-Infinity v1.0

Directional Infinity. Zero-Class Collapse. Finite-Class Ratio.  
A deterministic, alignment-preserving model of infinity.

---

Welcome to **SSM-Infinity**, a practical, fully testable, fully deterministic symbolic engine that introduces structure, direction, and alignment to the mathematical treatment of infinity.

This quickstart guide helps you:

- Run the SSM-Infinity engine  
- Understand `<infinity, alignment>` pairs  
- See symbolic outcomes such as zero-class and finite-class  
- Run the full regression test suite  
- Extend the model safely  

Everything works offline, requires no installation beyond Python, and is completely deterministic.

---

## **1. What SSM-Infinity Solves**

Classical mathematics cannot meaningfully handle:

```
∞ - ∞
∞ / ∞
∞ * negative
directional collapse of infinities
limit-dependent outcomes
```

These become undefined, indeterminate, or ambiguous.

**SSM-Infinity** makes them lawful by introducing:

### **Directional infinity**
```
<+∞, a>
<-∞, a>
```

### **Three symbolic outcome classes**
- infinite-class  
- zero-class  
- finite-class  

### **Lane-carrying infinity**
Every infinity has structural posture:

```
a in (-1, +1)
```

This enables deterministic, reproducible results.

---

## **2. Files You Need**

Place the following two files in a folder:

```
ssm_infinity_core.py
test_ssm_infinity_core.py
```

(You may name the folder anything, e.g., `INFINITY/`.)

These provide:

- **Core Engine** — directional infinity with all operators  
- **Test Suite** — 22 regression tests, all passing  

---

## **3. Run the Core Demo**

Open CMD/Terminal inside your folder and run:

```
python ssm_infinity_core.py
```

If everything is correct, you will see output similar to:

```
=== SSM-Infinity Core Engine Demo v1.0 ===

Plus Infinity: <+∞, +0.8000>
Minus Infinity: <-∞, -0.4000>
Unary minus: <-∞, +0.8000>

[1] ∞ + ∞   → infinite-class <+∞, +0.5721>
[2] ∞ + -∞  → zero-class (lane +0.325227)
[3] ∞ - ∞   → zero-class (lane +0.420204)
[4] ∞ * 5   → infinite-class <+∞, +0.8000>
[5] ∞ * -3  → infinite-class <-∞, +0.8000>
[6] ∞ / ∞   → finite-class (lane +0.714286)
[7] ∞ / 10  → infinite-class <+∞, +0.8000>
[8] ∞ / 0   → undefined
[9] ∞ ** 0  → finite-class (lane +0)
[10] ∞ ** 2 → infinite-class <+∞, +0.8000>
[11] ∞ ** -3 → zero-class (lane +0)

=== End of Core Demo ===
```

---

## **4. Running the Full Test Suite**

To verify the engine:

```
python test_ssm_infinity_core.py
```

Expected:

```
All tests PASSED ✔✔✔
```

This confirms all 22 regressions are deterministic and stable.

---

## **5. Understanding Core Results**

### **5.1 Infinite-class**
Returned when the result remains infinite:

```
("infinite-class", SymbolicInfinity(sign, align))
```

Examples:

```
∞ + ∞
∞ * 5
∞ ** positive
```

---

### **5.2 Zero-class**
Returned when infinities collapse symmetrically:

```
("zero-class", lane)
```

Examples:

```
∞ - ∞
+∞ + -∞
∞ ** negative
```

Zero-class means the infinities balance, producing a stable, zero-like symbolic state with alignment metadata.

---

### **5.3 Finite-class**
Returned when infinities cancel proportionally:

```
("finite-class", lane)
```

Examples:

```
∞ / ∞
∞ ** 0
```

Finite-class in v1.0 returns **lane**, not a numeric value.

---

### **5.4 Undefined**
Zero denominators produce a symbolic undefined:

```
("undefined", None)
```

This keeps undefined behavior explicit and structured.

---

## **6. Creating Your Own Infinity Objects**

```
from ssm_infinity_core import SymbolicInfinity

x = SymbolicInfinity(+1, 0.8)   # <+∞, +0.8>
y = SymbolicInfinity(-1, -0.4)  # <-∞, -0.4>
```

Supported operators:

```
+
-
*
/
**
unary -
```

All produce symbolic, class-safe outcomes.

---

## **7. Extending the Engine Safely**

You may add:

- new operators  
- symbolic rules  
- mappings to real-world infinite processes  

**Follow three safety principles:**

1. Keep all lanes inside `(-1, +1)`  
2. Preserve the class structure  
3. Do not convert infinite-class or zero-class into raw numbers  

This ensures mathematical consistency.

---

## **8. Mathematical Foundations (Why Hyperbolic Functions?)**

SSM-Infinity uses rapidity-based merging of alignment lanes:

```
u = atanh(a)
u_out = (u1 + u2) / 2
a_out = tanh(u_out)
```

Reasons for this design:

- Keeps lane strictly inside `(-1, +1)`  
- Prevents alignment “explosion”  
- Mirrors relativistic velocity addition  
- Provides reversibility and smoothness  
- Integrates cleanly with the entire SSM ecosystem  

This is the minimal, safe, and coherent algebra for infinite-domain alignment.

---

## **9. Summary**

You now have:

- A complete symbolic infinity engine  
- Directional infinities `<∞, a>`  
- Zero-class, finite-class, infinite-class rules  
- Full exponentiation behavior  
- Deterministic, testable outcomes  
- A 22-test regression suite  
- Hyperbolic-alignment merging model  

This is a **lawful, deterministic, alignment-preserving** infinity algebra for mathematics, physics, AI reasoning, and symbolic modeling.

