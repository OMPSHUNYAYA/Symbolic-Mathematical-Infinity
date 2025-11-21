# ============================================================
# SSM-Infinity Core Engine v1.0
# Monolithic Version (Option-C)
# ============================================================

import math

# ============================================================
# SECTION 1 — Global Constants & Safe Helpers
# ============================================================

EPS = 1e-12

def clamp_lane(a):
    """Clamp lane safely within (-1,+1)."""
    return max(min(a, 1 - EPS), -1 + EPS)

def safe_atanh(a):
    a = clamp_lane(a)
    return math.atanh(a)

def safe_tanh(u):
    return math.tanh(u)


# ============================================================
# SECTION 2 — Lane Combination Logic
# ============================================================

def combine_align(a1, a2):
    """
    Combine alignment lanes using rapidity semantics.
    u = atanh(a)
    u_out = (u1 + u2) / 2
    a_out = tanh(u_out)
    """
    u1 = safe_atanh(a1)
    u2 = safe_atanh(a2)
    return safe_tanh((u1 + u2) / 2)


def combine_align_diff(a1, a2):
    """
    For directional ratios (e.g., ∞ / ∞),
    we use atanh(a1) - atanh(a2).
    """
    u1 = safe_atanh(a1)
    u2 = safe_atanh(a2)
    return safe_tanh(u1 - u2)


# ============================================================
# SECTION 3 — Type Helpers & Collapse Parity
# ============================================================

def phi(value_with_lane):
    """
    Collapse parity: phi((m,a)) = m
    Used for structured classes.
    """
    if isinstance(value_with_lane, tuple):
        m, _ = value_with_lane
        return m
    raise ValueError("phi expects a structured tuple.")

def is_infinity(x):
    return isinstance(x, SymbolicInfinity)

def is_zero_class(x):
    return isinstance(x, tuple) and x[0] == "zero-class"

def is_finite_class(x):
    return isinstance(x, tuple) and x[0] == "finite-class"

def is_undefined(x):
    return isinstance(x, tuple) and x[0] == "undefined"

def is_finite_number(x):
    return isinstance(x, (int, float)) and math.isfinite(x)


# ============================================================
# SECTION 4 — SymbolicInfinity Class (Extended)
# ============================================================

class SymbolicInfinity:
    """
    Represents directional infinity <±∞, a> with alignment lane a in (-1,+1).
    sign = +1 for +∞, -1 for -∞.
    """

    def __init__(self, sign, align=0.0):
        if sign not in (+1, -1):
            raise ValueError("sign must be +1 or -1.")

        self.sign = sign
        self.align = clamp_lane(align)

    # Pretty representation
    def pretty(self):
        s = "+∞" if self.sign > 0 else "-∞"
        return f"<{s}, {self.align:+.4f}>"

    def __repr__(self):
        return f"SymbolicInfinity(sign={self.sign}, align={self.align:+.4f})"

    # Unary minus
    def __neg__(self):
        return SymbolicInfinity(-self.sign, self.align)

    # ----------------------------------
    # Core Infinity Algebra (+, -, *, /)
    # ----------------------------------

    def __add__(self, other):
        # ∞ + ∞
        if is_infinity(other):
            if self.sign == other.sign:
                # Same-direction infinities → infinity-class
                a = combine_align(self.align, other.align)
                return SymbolicInfinity(self.sign, a)
            else:
                # Opposing infinities → zero-class
                a = combine_align(self.align, other.align)
                return ("zero-class", a)

        # ∞ + finite → ∞
        if is_finite_number(other):
            return SymbolicInfinity(self.sign, self.align)

        return ("undefined", None)

    def __sub__(self, other):
        # ∞ - ∞ === ∞ + (-∞)
        if is_infinity(other):
            if self.sign != other.sign:
                # +∞ - (-∞) = +∞, etc
                a = combine_align(self.align, -other.align)
                return SymbolicInfinity(self.sign, a)
            else:
                # +∞ - +∞ → zero-class
                a = combine_align(self.align, -other.align)
                return ("zero-class", a)

        # ∞ - finite = ∞
        if is_finite_number(other):
            return SymbolicInfinity(self.sign, self.align)

        return ("undefined", None)

    def __mul__(self, other):
        # ∞ * finite
        if is_finite_number(other):
            if other == 0:
                return ("zero-class", 0.0)
            out_sign = self.sign * (1 if other > 0 else -1)
            return SymbolicInfinity(out_sign, self.align)

        # ∞ * ∞
        if is_infinity(other):
            out_sign = self.sign * other.sign
            a = combine_align(self.align, other.align)
            return SymbolicInfinity(out_sign, a)

        return ("undefined", None)

    def __truediv__(self, other):
        # ∞ / finite
        if is_finite_number(other):
            if other == 0:
                return ("undefined", None)
            out_sign = self.sign * (1 if other > 0 else -1)
            return SymbolicInfinity(out_sign, self.align)

        # ∞ / ∞ → finite-class (ratio)
        if is_infinity(other):
            a = combine_align_diff(self.align, other.align)
            return ("finite-class", a)

        return ("undefined", None)

    # ----------------------------------
    # Minimal Safe Exponentiation
    # ----------------------------------

    def __pow__(self, other):
        """
        Minimal safe exponentiation rules:
        1) ∞ ** positive finite → ∞ (same direction)
        2) ∞ ** 0 → finite-class 1 (neutral lane)
        3) ∞ ** negative finite → zero-class collapse
        4) finite ** ∞ handled in expression evaluator
        """
        if is_finite_number(other):

            # rule: ∞ ** 0 = 1 (finite-class)
            if other == 0:
                return ("finite-class", 0.0)

            # ∞ ** positive finite = ∞
            if other > 0:
                return SymbolicInfinity(self.sign, self.align)

            # ∞ ** negative finite → zero-class
            if other < 0:
                return ("zero-class", 0.0)

        return ("undefined", None)


# ============================================================
# SECTION 5 — Mixed-Type Algebra Helpers
# ============================================================

def format_result(result):
    """
    Pretty-format structured outputs.
    """
    if is_infinity(result):
        return f"infinite-class {result.pretty()}"
    if is_zero_class(result):
        return f"zero-class (lane {result[1]:+.6f})"
    if is_finite_class(result):
        return f"finite-class (lane {result[1]:+.6f})"
    if is_undefined(result):
        return "undefined"
    return f"raw: {result!r}"


# ============================================================
# SECTION 6 — Expression Evaluator (Minimal v1.0)
# ============================================================

def eval_expr(expr):
    """
    Very limited evaluator:
    Accepts expressions like:
        ("inf", +1, 0.4) + 3
        p + m / p2
    Only supports SymbolicInfinity and Python numbers.
    """
    # For v1.0, assume user directly calls operators
    return expr


# ============================================================
# SECTION 7 — Demo Suite
# ============================================================

def run_demo():
    print("=== SSM-Infinity Core Engine Demo v1.0 ===\n")

    p  = SymbolicInfinity(+1, +0.80)
    m  = SymbolicInfinity(-1, -0.40)
    p2 = SymbolicInfinity(+1, +0.20)

    print("Plus Infinity:", p.pretty())
    print("Minus Infinity:", m.pretty())
    print("Unary minus:", (-p).pretty(), "\n")

    print("[1] ∞ + ∞ →", format_result(p + p2))
    print("[2] +∞ + -∞ →", format_result(p + m))
    print("[3] ∞ - ∞ →", format_result(p - p2))
    print("[4] ∞ * 5 →", format_result(p * 5))
    print("[5] ∞ * -3 →", format_result(p * -3))
    print("[6] ∞ / ∞ →", format_result(p / p2))
    print("[7] ∞ / 10 →", format_result(p / 10))
    print("[8] ∞ / 0 →", format_result(p / 0))
    print("[9] ∞ ** 0 →", format_result(p ** 0))
    print("[10] ∞ ** 2 →", format_result(p ** 2))
    print("[11] ∞ ** -3 →", format_result(p ** -3))

    print("\n=== End of Core Demo ===")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    run_demo()
