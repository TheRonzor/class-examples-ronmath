from __future__ import annotations

'''
The world's most ridiculous attempt at
solving floating-point error.

This is not for serious use!
'''

class Rational:
    '''
    A Rational has a numerator and denominator, both integers, and stored separately.

    Conversion to float only occurs on an actual call to float().
    '''

    # Rational.reduce() will occasioanlly be called as a lazy
    # attempt to avoid integers becoming too large. Nothing
    # can be done about large coprimes!
    MAX_OPS = 8
    MAX_BITS = 128

    def __init__(self,
                 n: int,
                 d: int,
                 ops: int = 0
                 ):
        if d == 0:
            raise ZeroDivisionError('Denominator cannot be zero.')

        self.n = n
        self.d = d
        self.ops = ops

        if self.d < 0:
            self.n *= -1
            self.d *= -1

        if self.n == 0:
            self.d = 1
            self.ops = 0

        self.check_reduce()
        return

    def __repr__(self) -> str:
        return f'{self.n}/{self.d}'

    def __add__(self, other) -> Rational:
        n = self.n*other.d + self.d*other.n
        d = self.d*other.d
        ops = self.ops + other.ops + 1
        return Rational(n, d, ops)

    def __sub__(self, other) -> Rational:
        n = self.n*other.d - self.d*other.n
        d = self.d*other.d
        ops = self.ops + other.ops + 1
        return Rational(n, d, ops)

    def __mul__(self, other) -> Rational:
        n = self.n*other.n
        d = self.d*other.d
        ops = self.ops + other.ops + 1
        return Rational(n, d, ops)

    def __truediv__(self, other) -> Rational:
        n = self.n*other.d
        d = self.d*other.n
        ops = self.ops + other.ops + 1
        return Rational(n, d, ops)

    def __neg__(self) -> Rational:
        return Rational(-self.n, self.d, self.ops)

    def __float__(self) -> float:
        # Do the division as last as possible.
        return self.n/self.d

    def __lt__(self, other) -> bool:
        return self.n*other.d < self.d*other.n

    def __eq__(self, other) -> bool:
        return self.n*other.d == self.d*other.n

    @staticmethod
    def gcd(x: int, y: int) -> int:
        if y == 0:
            return abs(x)
        return Rational.gcd(y, x % y)

    def check_reduce(self) -> None:
        too_many_ops = self.ops >= Rational.MAX_OPS
        too_many_bits = (
            self.n.bit_length() > Rational.MAX_BITS
            or self.d.bit_length() > Rational.MAX_BITS
        )
        if too_many_ops or too_many_bits:
            self.reduce()

    def reduce(self) -> None:
        g = Rational.gcd(self.n, self.d)
        self.n = self.n//g
        self.d = self.d//g
        self.ops = 0
        return None

    # Class methods are bound to the class itself,
    # i.e. they do not require an instance and automatically
    # receive the class definition itself.
    @classmethod
    def zero(cls) -> Rational:
        return cls(0, 1)

    @classmethod
    def one(cls) -> Rational:
        return cls(1, 1)

    # Static methods can be called independently
    # of an instance. They do not receive the class
    # definition, and they do not require a reference
    # to self.
    @staticmethod
    def _is_integer_text(text: str) -> bool:
        if text.startswith(('+', '-')):
            text = text[1:]
        return bool(text) and text.isdigit()

    @classmethod
    def from_string(cls, text: str) -> Rational:
        if not isinstance(text, str):
            raise ValueError('Rational text must be a string.')

        value = ''.join(text.split())
        if not value:
            raise ValueError('Rational text cannot be empty.')

        if '/' in value:
            if value.count('/') != 1:
                raise ValueError(f'Invalid rational value: {text!r}.')

            numerator_text, denominator_text = value.split('/')
            valid_numerator = cls._is_integer_text(numerator_text)
            valid_denominator = (
                bool(denominator_text) and denominator_text.isdigit()
            )
            if not valid_numerator or not valid_denominator:
                raise ValueError(f'Invalid rational value: {text!r}.')

            n = int(numerator_text)
            d = int(denominator_text)
            return cls(n, d)

        if '.' in value:
            if value.count('.') != 1:
                raise ValueError(f'Invalid decimal value: {text!r}.')

            sign = 1
            unsigned_value = value
            if unsigned_value.startswith(('+', '-')):
                if unsigned_value[0] == '-':
                    sign = -1
                unsigned_value = unsigned_value[1:]

            whole, decimal = unsigned_value.split('.')
            valid_whole = not whole or whole.isdigit()
            valid_decimal = not decimal or decimal.isdigit()
            if not (whole or decimal) or not valid_whole or not valid_decimal:
                raise ValueError(f'Invalid decimal value: {text!r}.')

            digits = (whole or '0') + decimal
            n = sign*int(digits)
            d = 10**len(decimal)
            return cls(n, d)

        if not cls._is_integer_text(value):
            raise ValueError(f'Invalid integer value: {text!r}.')
        return cls(int(value), 1)


class Complex:
    '''
    A Complex number with Rational real and imaginary parts.
    '''
    def __init__(self,
                 real: Rational,
                 imag: Rational
                 ):
        self.real = real
        self.imag = imag
        return

    def __repr__(self) -> str:
        return f'{self.real} + {self.imag}i'.replace('+ -', '- ')

    def __add__(self, other) -> Complex:
        real = self.real + other.real
        imag = self.imag + other.imag
        return Complex(real, imag)

    def __sub__(self, other) -> Complex:
        real = self.real - other.real
        imag = self.imag - other.imag
        return Complex(real, imag)

    def __mul__(self, other) -> Complex:
        real = self.real*other.real - self.imag*other.imag
        imag = self.real*other.imag + self.imag*other.real
        return Complex(real, imag)

    def __truediv__(self, other) -> Complex:
        denominator = other.real*other.real + other.imag*other.imag
        real = (self.real*other.real + self.imag*other.imag) / denominator
        imag = (self.imag*other.real - self.real*other.imag) / denominator
        return Complex(real, imag)

    def __neg__(self) -> Complex:
        return Complex(-self.real, -self.imag)

    def conjugate(self) -> Complex:
        real = Rational(self.real.n, self.real.d, self.real.ops)
        imag = -self.imag
        return Complex(real, imag)

    def __eq__(self, other) -> bool:
        return (self.real == other.real) and (self.imag == other.imag)

    def reduce(self) -> None:
        self.real.reduce()
        self.imag.reduce()
        return None

    @classmethod
    def zero(cls) -> Complex:
        return cls(Rational.zero(), Rational.zero())

    @classmethod
    def one(cls) -> Complex:
        return cls(Rational.one(), Rational.zero())

    @classmethod
    def from_string(cls, text: str) -> Complex:
        if not isinstance(text, str):
            raise ValueError('Complex text must be a string.')

        value = ''.join(text.split())
        if not value:
            raise ValueError('Complex text cannot be empty.')

        if 'i' not in value:
            real = Rational.from_string(value)
            return cls(real, Rational.zero())

        if value.count('i') != 1 or not value.endswith('i'):
            raise ValueError(f'Invalid complex value: {text!r}.')

        value = value[:-1]
        separator_indexes = []
        for index in range(1, len(value)):
            if value[index] in '+-':
                separator_indexes.append(index)

        if len(separator_indexes) > 1:
            raise ValueError(f'Invalid complex value: {text!r}.')

        if separator_indexes:
            separator = separator_indexes[0]
            real_text = value[:separator]
            imag_text = value[separator:]
            real = Rational.from_string(real_text)
        else:
            imag_text = value
            real = Rational.zero()

        if imag_text in ('', '+'):
            imag = Rational.one()
        elif imag_text == '-':
            imag = -Rational.one()
        else:
            imag = Rational.from_string(imag_text)

        return cls(real, imag)


class Matrix:
    DEFAULT_SCALAR_TYPE = Rational

    def __init__(self, data: list[list]):
        if not data or not all(isinstance(row, list) for row in data):
            raise ValueError('Data must be a nonempty list of lists.')

        n_cols = len(data[0])
        if n_cols == 0 or any(len(row) != n_cols for row in data):
            raise ValueError('Matrix must be rectangular and nonempty.')

        self.data = [row.copy() for row in data]
        self.n_rows = len(data)
        self.n_cols = n_cols
        return

    def reduce(self) -> None:
        for row in self.data:
            for value in row:
                value.reduce()
        return None

    def __repr__(self) -> str:
        return '\n'.join(str(row) for row in self.data)

    def __add__(self, other) -> Matrix:
        if self.shape != other.shape:
            raise ValueError('Matrix dimensions must match.')

        data = []
        for i in range(self.n_rows):
            row = []
            for j in range(self.n_cols):
                row.append(self.data[i][j] + other.data[i][j])
            data.append(row)

        return type(self)(data)

    def __sub__(self, other) -> Matrix:
        if self.shape != other.shape:
            raise ValueError('Matrix dimensions must match.')

        data = []
        for i in range(self.n_rows):
            row = []
            for j in range(self.n_cols):
                row.append(self.data[i][j] - other.data[i][j])
            data.append(row)

        return type(self)(data)

    def __matmul__(self, other) -> Matrix:
        if self.n_cols != other.n_rows:
            raise ValueError('Incompatible matrix dimensions.')

        data = []
        scalar_type = type(self.data[0][0])

        for i in range(self.n_rows):
            row = []
            for j in range(other.n_cols):
                total = scalar_type.zero()
                for k in range(self.n_cols):
                    total += self.data[i][k] * other.data[k][j]
                row.append(total)
            data.append(row)

        return type(self)(data)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Matrix) or self.shape != other.shape:
            return False

        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if self.data[i][j] != other.data[i][j]:
                    return False
        return True

    @property
    def shape(self) -> tuple[int, int]:
        return (self.n_rows, self.n_cols)

    @property
    def T(self) -> Matrix:
        data = []
        for j in range(self.n_cols):
            row = []
            for i in range(self.n_rows):
                row.append(self.data[i][j])
            data.append(row)
        return type(self)(data)

    @classmethod
    def zero(cls,
             n_rows: int,
             n_cols: int,
             scalar_type=None
             ) -> Matrix:
        if n_rows <= 0 or n_cols <= 0:
            raise ValueError('Matrix dimensions must be positive.')
        if scalar_type is None:
            scalar_type = cls.DEFAULT_SCALAR_TYPE

        data = []
        for _ in range(n_rows):
            row = []
            for _ in range(n_cols):
                row.append(scalar_type.zero())
            data.append(row)
        return cls(data)

    @classmethod
    def identity(cls, n: int, scalar_type=None) -> Matrix:
        if n <= 0:
            raise ValueError('Matrix dimensions must be positive.')
        if scalar_type is None:
            scalar_type = cls.DEFAULT_SCALAR_TYPE

        data = []
        for i in range(n):
            row = []
            for j in range(n):
                if i == j:
                    row.append(scalar_type.one())
                else:
                    row.append(scalar_type.zero())
            data.append(row)
        return cls(data)


class ComplexMatrix(Matrix):
    DEFAULT_SCALAR_TYPE = Complex

    def __init__(self, data: list[list]):
        super().__init__(data)
        for row in self.data:
            for value in row:
                if not isinstance(value, Complex):
                    raise ValueError('ComplexMatrix entries must be Complex.')
        return

    @property
    def CT(self) -> ComplexMatrix:
        data = []
        for j in range(self.n_cols):
            row = []
            for i in range(self.n_rows):
                row.append(self.data[i][j].conjugate())
            data.append(row)
        return type(self)(data)

    def reduce(self) -> None:
        for row in self.data:
            for value in row:
                value.reduce()
        return None
