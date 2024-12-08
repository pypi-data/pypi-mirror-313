from numba import jit, TypingError

from exceptions import (
    EuclideanAlgorithmValueError, EuclideanAlgorithmLengthError
)


@jit(fastmath=True, cache=True)
def euclidean_algorithm_calculating(num1: int, num2: int
                            ) -> int | float | EuclideanAlgorithmValueError:
    if num1 <= 0 or num2 <= 0:
        raise EuclideanAlgorithmValueError
    elif num2 % num1 == 0 or num1 % num2 == 0:
        return num1 if num1 < num2 else num2

    while True:
        if num1 > num2:
            while num1 > num2:
                num1 -= num2
        elif num2 > num1:
            while num2 > num1:
                num2 -= num1

        if num1 == num2:
            return num1


def euclidean_algorithm(num1: int, num2: int
                            ) -> int | float | EuclideanAlgorithmLengthError:
    try:
        euclidean_algorithm_calculating(num1=num1, num2=num2)
    except TypingError:
        raise EuclideanAlgorithmLengthError
    else:
        return euclidean_algorithm_calculating(num1=num1, num2=num2)
