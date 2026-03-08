from __future__ import annotations

from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Generic, List, Optional, Tuple, TypeVar
import re


# ----------------------------
# 1) Money
# ----------------------------

class Money:
    __slots__ = ("_amount", "_currency")

    def __init__(self, amount: Decimal, currency: str) -> None:
        if not isinstance(amount, Decimal):
            raise TypeError("amount must be a Decimal")
        if not isinstance(currency, str) or not currency.strip():
            raise ValueError("currency must be a non-empty string")
        self._amount = amount
        self._currency = currency

    @property
    def amount(self) -> Decimal:
        return self._amount

    @property
    def currency(self) -> str:
        return self._currency

    def _assert_same_currency(self, other: "Money") -> None:
        if not isinstance(other, Money):
            raise TypeError("other must be Money")
        if self.currency != other.currency:
            raise ValueError(f"Currency mismatch: {self.currency} vs {other.currency}")

    def add(self, other: "Money") -> "Money":
        self._assert_same_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def subtract(self, other: "Money") -> "Money":
        self._assert_same_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def multiply(self, factor: int) -> "Money":
        if not isinstance(factor, int):
            raise TypeError("factor must be int")
        return Money(self.amount * Decimal(factor), self.currency)

    def is_negative(self) -> bool:
        return self.amount < 0

    def compare_to(self, other: "Money") -> int:
        self._assert_same_currency(other)
        if self.amount < other.amount:
            return -1
        if self.amount > other.amount:
            return 1
        return 0

    def __repr__(self) -> str:
        return f"Money(amount={self.amount!r}, currency={self.currency!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return False
        return self.amount == other.amount and self.currency == other.currency


# ----------------------------
# 2) PasswordPolicy
# ----------------------------

class PasswordValidationResult:
    __slots__ = ("ok", "errors")

    def __init__(self, ok: bool, errors: Tuple[str, ...]) -> None:
        self.ok = bool(ok)
        self.errors = tuple(errors)

    def __bool__(self) -> bool:
        return self.ok

    def __repr__(self) -> str:
        return f"PasswordValidationResult(ok={self.ok!r}, errors={self.errors!r})"


class PasswordPolicy:
    _special_re = re.compile(r"[^A-Za-z0-9\s]")

    def __init__(
        self,
        min_len: int = 8,
        max_len: int = 16,
        require_upper: bool = True,
        require_digit: bool = True,
        require_special: bool = False,
        forbid_spaces: bool = True,
    ) -> None:
        if not isinstance(min_len, int) or min_len < 1:
            raise ValueError("min_len must be an int >= 1")
        if not isinstance(max_len, int) or max_len < min_len:
            raise ValueError("max_len must be an int >= min_len")

        self.min_len = min_len
        self.max_len = max_len
        self.require_upper = bool(require_upper)
        self.require_digit = bool(require_digit)
        self.require_special = bool(require_special)
        self.forbid_spaces = bool(forbid_spaces)

    def validate(self, pwd: str) -> PasswordValidationResult:
        if not isinstance(pwd, str):
            raise TypeError("pwd must be a string")

        errors: List[str] = []
        n = len(pwd)

        if n < self.min_len:
            errors.append(f"length<{self.min_len}")
        if n > self.max_len:
            errors.append(f"length>{self.max_len}")

        if self.forbid_spaces and any(ch.isspace() for ch in pwd):
            errors.append("contains_space")

        if self.require_upper and not any(ch.isupper() for ch in pwd):
            errors.append("missing_upper")

        if self.require_digit and not any(ch.isdigit() for ch in pwd):
            errors.append("missing_digit")

        if self.require_special and not self._special_re.search(pwd):
            errors.append("missing_special")

        return PasswordValidationResult(ok=(len(errors) == 0), errors=tuple(errors))


# ----------------------------
# 3) DateRange (inclusive)
# ----------------------------

class DateRange:
    __slots__ = ("start", "end")

    def __init__(self, start: date, end: date) -> None:
        if not isinstance(start, date) or not isinstance(end, date):
            raise TypeError("start and end must be datetime.date instances")
        if start > end:
            raise ValueError("start must be <= end")
        self.start = start
        self.end = end

    def contains(self, d: date) -> bool:
        if not isinstance(d, date):
            raise TypeError("d must be a date")
        return self.start <= d <= self.end

    def days_inclusive(self) -> int:
        return (self.end - self.start).days + 1

    def overlaps(self, other: "DateRange") -> bool:
        if not isinstance(other, DateRange):
            raise TypeError("other must be DateRange")
        return not (self.end < other.start or other.end < self.start)

    def intersection(self, other: "DateRange") -> Optional["DateRange"]:
        if not self.overlaps(other):
            return None
        return DateRange(max(self.start, other.start), min(self.end, other.end))

    def __repr__(self) -> str:
        return f"DateRange(start={self.start!r}, end={self.end!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DateRange):
            return False
        return self.start == other.start and self.end == other.end


# ----------------------------
# 4) BankAccount (in-memory ledger)
# ----------------------------

class Transaction:
    __slots__ = ("kind", "amount", "description")

    def __init__(self, kind: str, amount: Decimal, description: str) -> None:
        if kind not in ("deposit", "withdraw"):
            raise ValueError("kind must be 'deposit' or 'withdraw'")
        if not isinstance(amount, Decimal):
            raise TypeError("amount must be a Decimal")
        if not isinstance(description, str):
            raise TypeError("description must be a string")
        self.kind = kind
        self.amount = amount
        self.description = description

    def __repr__(self) -> str:
        return f"Transaction(kind={self.kind!r}, amount={self.amount!r}, description={self.description!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Transaction):
            return False
        return (self.kind, self.amount, self.description) == (other.kind, other.amount, other.description)


class BankAccount:
    def __init__(self, opening_balance: Decimal = Decimal("0")) -> None:
        if not isinstance(opening_balance, Decimal):
            raise TypeError("opening_balance must be a Decimal")
        self._balance: Decimal = opening_balance
        self._transactions: List[Transaction] = []

    def get_balance(self) -> Decimal:
        return self._balance

    def deposit(self, amount: Decimal, description: str = "") -> None:
        self._validate_amount_positive(amount)
        if not isinstance(description, str):
            raise TypeError("description must be a string")
        self._balance += amount
        self._transactions.append(Transaction("deposit", amount, description))

    def withdraw(self, amount: Decimal, description: str = "") -> None:
        self._validate_amount_positive(amount)
        if not isinstance(description, str):
            raise TypeError("description must be a string")
        if amount > self._balance:
            raise ValueError("insufficient_funds")
        self._balance -= amount
        self._transactions.append(Transaction("withdraw", amount, description))

    def get_statement(self) -> Tuple[Transaction, ...]:
        return tuple(self._transactions)

    @staticmethod
    def _validate_amount_positive(amount: Decimal) -> None:
        if not isinstance(amount, Decimal):
            raise TypeError("amount must be a Decimal")
        if amount <= 0:
            raise ValueError("amount must be > 0")


# ----------------------------
# 5) ShoppingCart
# ----------------------------

class CartItem:
    __slots__ = ("sku", "unit_price", "qty")

    def __init__(self, sku: str, unit_price: Decimal, qty: int) -> None:
        if not isinstance(sku, str) or not sku:
            raise ValueError("sku must be a non-empty string")
        if not isinstance(unit_price, Decimal):
            raise TypeError("unit_price must be a Decimal")
        if unit_price < 0:
            raise ValueError("unit_price must be >= 0")
        if not isinstance(qty, int):
            raise TypeError("qty must be int")
        if qty <= 0:
            raise ValueError("qty must be > 0")

        self.sku = sku
        self.unit_price = unit_price
        self.qty = qty

    def __repr__(self) -> str:
        return f"CartItem(sku={self.sku!r}, unit_price={self.unit_price!r}, qty={self.qty!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CartItem):
            return False
        return (self.sku, self.unit_price, self.qty) == (other.sku, other.unit_price, other.qty)


class ShoppingCart:
    def __init__(self, discount_percent: Decimal = Decimal("0")) -> None:
        if not isinstance(discount_percent, Decimal):
            raise TypeError("discount_percent must be a Decimal")
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("discount_percent must be in [0, 100]")
        self._discount_percent = discount_percent
        self._items: Dict[str, CartItem] = {}

    def add_item(self, sku: str, unit_price: Decimal, qty: int = 1) -> None:
        item = CartItem(sku=sku, unit_price=unit_price, qty=qty)
        if sku in self._items:
            existing = self._items[sku]
            # Latest unit_price wins; qty accumulates
            self._items[sku] = CartItem(sku, unit_price, existing.qty + qty)
        else:
            self._items[sku] = item

    def remove_sku(self, sku: str) -> None:
        self._items.pop(sku, None)

    def total_items(self) -> int:
        return sum(i.qty for i in self._items.values())

    def subtotal(self) -> Decimal:
        total = Decimal("0")
        for i in self._items.values():
            total += i.unit_price * Decimal(i.qty)
        return total

    def total(self) -> Decimal:
        sub = self.subtotal()
        factor = (Decimal("100") - self._discount_percent) / Decimal("100")
        total = sub * factor
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def items(self) -> Tuple[CartItem, ...]:
        return tuple(self._items.values())



# ----------------------------
# 6) LRUCache
# ----------------------------

K = TypeVar("K")
V = TypeVar("V")

class LRUCache(Generic[K, V]):
    def __init__(self, capacity: int) -> None:
        if not isinstance(capacity, int):
            raise TypeError("capacity must be int")
        if capacity <= 0:
            raise ValueError("capacity must be > 0")
        self._capacity = capacity
        self._data: Dict[K, V] = {}
        self._recency: List[K] = []  # least-recent at index 0; most-recent at end

    def size(self) -> int:
        return len(self._data)

    def contains_key(self, key: K) -> bool:
        return key in self._data

    def get(self, key: K) -> Optional[V]:
        if key not in self._data:
            return None
        self._touch(key)
        return self._data[key]

    def put(self, key: K, value: V) -> None:
        if key in self._data:
            self._data[key] = value
            self._touch(key)
            return

        if len(self._data) >= self._capacity:
            lru = self._recency.pop(0)
            self._data.pop(lru, None)

        self._data[key] = value
        self._recency.append(key)

    def _touch(self, key: K) -> None:
        try:
            self._recency.remove(key)
        except ValueError:
            pass
        self._recency.append(key)

    def keys_mru_order(self) -> Tuple[K, ...]:
        return tuple(self._recency)


# ----------------------------
# 8) PalindromeChecker
# ----------------------------

class PalindromeChecker:
    def __init__(
        self,
        ignore_case: bool = True,
        ignore_spaces: bool = True,
        ignore_punctuation: bool = True,
    ) -> None:
        self.ignore_case = bool(ignore_case)
        self.ignore_spaces = bool(ignore_spaces)
        self.ignore_punctuation = bool(ignore_punctuation)

    def normalize(self, s: str) -> str:
        if not isinstance(s, str):
            raise TypeError("s must be a string")

        out: List[str] = []
        for ch in s:
            if self.ignore_spaces and ch.isspace():
                continue
            if self.ignore_punctuation and (not ch.isalnum()) and (not ch.isspace()):
                continue
            out.append(ch.lower() if self.ignore_case else ch)
        return "".join(out)

    def is_palindrome(self, s: str) -> bool:
        ns = self.normalize(s)
        return ns == ns[::-1]


