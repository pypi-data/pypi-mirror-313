"""
File to test the functionality of the Pedersen scheme.
Note that standard_pedersen_commitment_scheme is a predefined scheme
with generators $(g_1, g_2, ..., g_n) = (1, 2, ..., n), h = n+1$
and a predefined arbitrary 256-bit safe prime as its modulus.
"""

from __future__ import annotations

import itertools
from functools import reduce
from math import ceil

import pytest

from tno.zkp.commitment_schemes.pedersen import (
    PedersenCommitmentInput,
    PedersenVectorCommitmentScheme,
)


def factorial(n: int) -> int:
    """
    Helper function to calculate the factorial
    n! = n * (n-1) * ... * 1

    :param n: The nonnegative integer input
    :raises ValueError: If n is negative
    :return: n!, the factorial of n
    """
    if n < 0:
        raise ValueError("n must be a nonnegative integer")
    r = 1
    for i in range(1, n + 1):
        r *= i
    return r


def test_pedersen(
    standard_pedersen_commitment_scheme: PedersenVectorCommitmentScheme,
) -> None:
    """
    Check if the Pedersen scheme returns the expected result. The expected result is
    the product of all generators for an input of all ones.

    :param standard_pedersen_commitment_scheme: PedersenVectorCommitmentScheme with fixed p and q
    """
    scheme = standard_pedersen_commitment_scheme
    n = scheme.input_size
    modulus = scheme.modulus
    ones_input = [1 for _ in range(n)]
    reveal_information = 1
    pedersen_input = PedersenCommitmentInput(ones_input, reveal_information, scheme)
    result = scheme.evaluate(pedersen_input)
    generators = scheme.generator_gs + [scheme.generator_h]
    expected_result = reduce(lambda acc, y: (acc * y) % modulus, generators)
    assert result.value == expected_result


def test_adding_forms_together(
    standard_pedersen_commitment_scheme: PedersenVectorCommitmentScheme,
) -> None:
    """
    Check if two Pedersen schemes are added correctly by adding the Pedersen scheme to itself.
    The addition of the two Pedersen schemes results in a new Pedersen scheme with
    generators squared. The expected results will be the multiplication of the squared generators.

    :param standard_pedersen_commitment_scheme: PedersenVectorCommitmentScheme with fixed p and q
    """
    scheme = standard_pedersen_commitment_scheme
    generators = scheme.generator_gs + [scheme.generator_h]
    generators_squared = map(lambda x: x**2, generators)
    modulus = scheme.modulus
    expected_result = reduce(lambda acc, y: (acc * y) % modulus, generators_squared)

    scheme = scheme + scheme
    n = scheme.input_size
    ones_input = [1 for _ in range(n)]
    reveal_information = 1
    pedersen_input = PedersenCommitmentInput(ones_input, reveal_information, scheme)
    result = scheme.evaluate(pedersen_input)
    assert result.value == expected_result


@pytest.mark.parametrize("constant", list(range(1, 10)))
def test_multiply_form_with_constant_together(
    standard_pedersen_commitment_scheme: PedersenVectorCommitmentScheme, constant: int
) -> None:
    """
    Check if a Pedersen scheme multiplies with a constant correctly.
    The multiplication results in a new Pedersen scheme with
    generators to the power of the constant. The expected result will be the new
    generators multiplied together.

    :param standard_pedersen_commitment_scheme: PedersenVectorCommitmentScheme with fixed p and q
    :param constant: Multiplication factor for the Pedersen scheme
    """
    scheme = standard_pedersen_commitment_scheme
    generators = scheme.generator_gs + [scheme.generator_h]
    modulus = scheme.modulus
    generators_power = map(lambda x: pow(x, constant, modulus), generators)
    expected_result = reduce(lambda acc, y: (acc * y) % modulus, generators_power)

    scheme = scheme * constant
    n = scheme.input_size
    ones_input = [1 for _ in range(n)]
    reveal_information = 1
    pedersen_input = PedersenCommitmentInput(ones_input, reveal_information, scheme)
    result = scheme.evaluate(pedersen_input)
    assert result.value == expected_result


def test_splitting_form(
    standard_pedersen_commitment_scheme: PedersenVectorCommitmentScheme,
) -> None:
    """
    Split a Pedersen scheme in two halves. The left half will be prepended
    with a 1 coefficient if the length of the Pedersen scheme is odd.

    :param standard_pedersen_commitment_scheme: PedersenVectorCommitmentScheme with fixed p and q
    """
    scheme = standard_pedersen_commitment_scheme
    n = scheme.input_size
    modulus = scheme.modulus
    left_half, right_half = scheme.split_in_half()

    ones_input = [1 for _ in range(ceil(n / 2))]
    reveal_information = 1

    pedersen_input_right = PedersenCommitmentInput(
        ones_input, reveal_information, scheme
    )
    pedersen_input_left = PedersenCommitmentInput(
        ones_input, reveal_information, scheme
    )

    # check the right result
    right_result = right_half.evaluate(pedersen_input_right)
    start = n // 2
    right_generators = list(itertools.islice(scheme.generator_gs, int(start), None)) + [
        scheme.generator_h
    ]
    # g_(n/2)*g_(n/2)+1*...*g_n*h
    right_expected_result = reduce(lambda acc, y: (acc * y) % modulus, right_generators)
    assert right_result.value == right_expected_result

    # check the left result
    left_result = left_half.evaluate(pedersen_input_left)
    end = n // 2
    left_generators = list(itertools.islice(scheme.generator_gs, int(end))) + [
        scheme.generator_h
    ]
    # g_1*g_2*...*g_(n/2)*h
    left_expected_result = reduce(lambda acc, y: (acc * y) % modulus, left_generators)
    assert left_result.value == left_expected_result


def test_equality(
    standard_pedersen_commitment_scheme: PedersenVectorCommitmentScheme,
) -> None:
    """
    Check if two Pedersen schemes are determined to be equal if they have the same
    generators and modulus. If they are not the same the equality should fail.

    :param standard_pedersen_commitment_scheme: PedersenVectorCommitmentScheme with fixed p and q
    """
    scheme = standard_pedersen_commitment_scheme
    n = scheme.input_size
    modulus = scheme.modulus
    input_modulus = scheme.input_modulus
    generator_gs = scheme.generator_gs
    generator_h = scheme.generator_h

    # same generators and modulus
    new_generator_gs = [*generator_gs]
    new_generator_h = generator_h
    new_scheme = PedersenVectorCommitmentScheme(
        n, modulus, input_modulus, new_generator_gs, new_generator_h
    )
    assert new_scheme == scheme

    # different modulus
    new_scheme = PedersenVectorCommitmentScheme(
        n, modulus + 1, input_modulus, generator_gs, generator_h
    )
    assert new_scheme != scheme

    # different generators
    new_generator_gs = list(range(2, n + 2))
    new_generator_h = n + 2
    new_scheme = PedersenVectorCommitmentScheme(
        n, modulus, input_modulus, new_generator_gs, new_generator_h
    )
    assert new_scheme != scheme
