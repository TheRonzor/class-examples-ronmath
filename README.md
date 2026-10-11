# ronmath

This is an intentionally absurd example meant to mitigate floating-point error.

The point is not the math, and this isn't intended for any real use!

The point is to serve as a clear example of the following concepts for classes in Python:

- Inheritance: `is a` type relationships. For example, `ComplexMatrix` is a type of `Matrix`, therefore it inherits all of the usual properties and methods of `Matrix`, and defines some additional behavior, such as the conjugate transpose (implemented as `.CT`)

- Composition: `has a` type relationships. For example: 
    - `Rational` has as properties two integers (the numerator and denominator) 
    - `Complex` has as properties two `Rational`s (the real and imaginary parts)

- `dunder` methods. The name refers to the fact that they start and end with double underscores. These are special built-in methods you can use to define behavior such as:
    - What it means to compare two instances of a class (equality, less than,  etc.)
    - What it means to perform various operations such as addition (`__add__`) and other arithmetic
    - What happens when we print the object to the screen (defining the `__repr__` and/or `__str__` dunders).
    - and many others. Some of them have default behaviors, and others will raise errors if you do not define them (e.g., in order to compare/sort `Rational` numbers, I have to define the `__eq__` dunder for equality, and the `__lt__` dunder for less than).

