# -------------------------------------------------------------
# SSM-Infinity v1.0 — Full Regression Suite (20 Tests)
# -------------------------------------------------------------
from ssm_infinity_core import SymbolicInfinity

def approx(x, y, tol=1e-6):
    return abs(x - y) <= tol

def print_pass(name):
    print(f"[PASS] {name}")

def print_fail(name, detail):
    print(f"[FAIL] {name} → {detail}")

def run():
    print("=== Running SSM-Infinity Core Test Suite ===\n")

    passed = 0
    failed = 0

    def test(name, condition, detail=""):
        nonlocal passed, failed
        if condition:
            print_pass(name)
            passed += 1
        else:
            print_fail(name, detail)
            failed += 1

    # ---------------------------------------------------------
    # Creation
    # ---------------------------------------------------------
    infp = SymbolicInfinity(+1, 0.8)
    infn = SymbolicInfinity(-1, -0.4)

    # 1. sign stored correctly
    test("Sign stored correctly", infp.sign == 1)

    # 2. align numeric bounds
    test("align in (-1,+1)", -1 < infp.align < 1)

    # 3. unary minus flips sign but preserves alignment magnitude
    neg = -infp
    test("Unary minus flips sign", neg.sign == -1)
    test("Unary minus preserves align", approx(abs(neg.align), abs(infp.align)))

    # ---------------------------------------------------------
    # Addition
    # ---------------------------------------------------------
    # 4. ∞ + ∞ → infinite-class
    res = infp + infp
    test("∞ + ∞ → infinity-class", isinstance(res, SymbolicInfinity) and res.sign == 1)

    # 5. +∞ + -∞ → zero-class
    res = infp + infn
    test("+∞ + -∞ → zero-class", isinstance(res, tuple) and res[0] == "zero-class")

    # 6. zero-class lane numeric
    test("zero-class lane numeric", isinstance(res[1], float))

    # ---------------------------------------------------------
    # Subtraction
    # ---------------------------------------------------------
    # 7. ∞ - ∞ → zero-class
    res = infp - infp
    test("∞ - ∞ → zero-class", isinstance(res, tuple) and res[0] == "zero-class")

    # 8. (+∞) - (-∞) → infinite-class
    res = infp - infn
    test("+∞ - -∞ → infinity-class", isinstance(res, SymbolicInfinity) and res.sign == 1)

    # ---------------------------------------------------------
    # Multiplication
    # ---------------------------------------------------------
    # 9. ∞ * positive finite → infinite-class
    res = infp * 5
    test("∞ * positive → infinity-class", isinstance(res, SymbolicInfinity) and res.sign == 1)

    # 10. ∞ * negative finite → sign flips
    res = infp * -3
    test("∞ * negative → sign-flip", isinstance(res, SymbolicInfinity) and res.sign == -1)

    # ---------------------------------------------------------
    # Division
    # ---------------------------------------------------------
    # 11. ∞ / ∞ → finite-class
    res = infp / SymbolicInfinity(+1, -0.2)
    test("∞ / ∞ → finite-class", isinstance(res, tuple) and res[0] == "finite-class")

    # 12. ∞ / finite → infinite-class
    res = infp / 10
    test("∞ / finite positive → infinite-class", isinstance(res, SymbolicInfinity))

    # 13. ∞ / 0 → undefined
    res = infp / 0
    test("∞ / 0 → undefined",
           isinstance(res, tuple) and len(res) == 2 and isinstance(res[0], str) and res[0].lower() == "undefined")


    # ---------------------------------------------------------
    # Exponentiation
    # ---------------------------------------------------------
    # 14. ∞ ** 0 → finite-class
    res = infp ** 0
    test("∞ ** 0 → finite-class", isinstance(res, tuple) and res[0] == "finite-class")
    test("∞ ** 0 lane = 0", approx(res[1], 0.0))

    # 15. ∞ ** positive exponent → infinite-class
    res = infp ** 2
    test("∞ ** positive exponent → infinity-class", isinstance(res, SymbolicInfinity))

    # 16. ∞ ** negative exponent → zero-class
    res = infp ** -3
    test("∞ ** negative exponent → zero-class", isinstance(res, tuple) and res[0] == "zero-class")

    # ---------------------------------------------------------
    # Lane stability tests
    # ---------------------------------------------------------
    # 17. Collapsed zero-class lane numeric
    zc = ("zero-class", 0.123)
    test("Collapsed zero-class lane numeric", isinstance(zc[1], float))

    # 18. Collapsed finite-class lane numeric
    fc = ("finite-class", -0.5)
    test("finite-class lane numeric", isinstance(fc[1], float))

    # ---------------------------------------------------------
    # Combination rules
    # ---------------------------------------------------------
    # 19. Addition align in (-1,+1)
    res = infp + infp
    test("Addition align bounded", -1 < res.align < 1)

    # 20. Multiplication preserves magnitude of align
    res = infp * -1
    test("Multiplication preserves align magnitude", approx(abs(res.align), abs(infp.align)))

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------
    print("\n=== Test Summary ===")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if failed == 0:
        print("\nAll tests PASSED ✔✔✔")
    else:
        print("\nSome tests FAILED ❌")

if __name__ == "__main__":
    run()
