"""
Fixtures to use in all test files
"""

import itertools
from collections.abc import Generator

import pytest
import sympy

from tno.mpc.encryption_schemes.utils import pow_mod

from tno.zkp.commitment_schemes.pedersen import PedersenVectorCommitmentScheme


@pytest.fixture(params=[1, 2, 3, 6, 10, 20, 50, 100, 200, 500, 1000])
def pedersen_commitment_scheme_without_input_modulus(
    request: pytest.FixtureRequest,
) -> PedersenVectorCommitmentScheme:
    """
    Generate a PedersenVectorCommitmentScheme of length $n$.
    $n$ is taken from the request parameter.
    The coefficients used are chosen at random. The modulus is a random prime.

    :param request: request with parameters
    :return: PedersenVectorCommitmentScheme of length $n$
    """
    return PedersenVectorCommitmentScheme.from_security_param(256, request.param)


@pytest.fixture(params=[1, 2, 3, 6, 10, 20, 50, 100, 200, 500, 1000])
def pedersen_commitment_scheme_with_input_modulus(
    request: pytest.FixtureRequest,
) -> PedersenVectorCommitmentScheme:
    """
    Generate a PedersenVectorCommitmentScheme of length $n$.
    $n$ is taken from the request parameter.
    The coefficients used are chosen at random. The modulus is a random prime.

    :param request: request with parameters
    :return: PedersenVectorCommitmentScheme of length $n$
    """

    random_prime = sympy.ntheory.generate.randprime(2 ^ 240, 2 ^ 256)  # 25000000)
    return PedersenVectorCommitmentScheme.from_security_param(
        256, request.param, random_prime
    )


@pytest.fixture(params=[1, 2, 3, 6, 10, 20, 50, 100, 200, 500, 1000])
def standard_pedersen_commitment_scheme(
    request: pytest.FixtureRequest,
) -> PedersenVectorCommitmentScheme:
    """
    Generate a predefined PedersenVectorCommitmentScheme of length $n$.
    $n$ is taken from the request parameter.
    The coefficients are given by $(g_1, g_2, ..., g_n) = (1, 2, ..., n), h = n+1$.
    The modulus is a predefined arbitrary 256-bit safe prime.

    :param request: request with parameters
    :return: PedersenVectorCommitmentScheme of length $n$
    """
    n = request.param
    # p and q are both prime, so p is a safe prime
    q = 108441331157832885133713644392386597893576968950776969854890282556827293342081
    p = 2 * q + 1
    generator = get_generators(q, p)
    generator_gs = list(itertools.islice(generator, n))
    generator_h = next(generator)
    return PedersenVectorCommitmentScheme(n, p, q, generator_gs, generator_h)


def get_generators(q: int, p: int) -> Generator[int, None, None]:
    for i in range(0, p):
        if pow_mod(i, q, p) == 1:
            yield i
