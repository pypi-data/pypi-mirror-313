"""
File to test the output of the Pedersen scheme
"""

from __future__ import annotations

import random

import pytest

from tno.mpc.encryption_schemes.utils import pow_mod

from tno.zkp.commitment_schemes.pedersen import PedersenCommitment


@pytest.fixture(
    name="pedersen_output", params=[1, 2, 3, 6, 10, 20, 50, 100, 200, 500, 1000]
)
def fixture_pedersen_output(request: pytest.FixtureRequest) -> PedersenCommitment:
    """
    Create a Pedersen output with given value.
    The modulus is a predefined arbitrary 256-bit safe prime.

    :param request: pytest fixture request with parameter for the value of the output
    :return: PedersenCommitment with the given value
    """
    value = request.param
    q = 108441331157832885133713644392386597893576968950776969854890282556827293342081
    p = 2 * q + 1
    return PedersenCommitment(value, p)


def test_pedersen_output_addition(pedersen_output: PedersenCommitment) -> None:
    """
    Addition of two Pedersen output results in a new Pedersen output with the result having
    value equal to the sum of the values modulo the modulus, where the modulus is the same.

    :param pedersen_output: PedersenCommitment with a value and a modulus
    """
    value = pedersen_output.value
    modulus = pedersen_output.modulus
    random_value = random.randint(0, modulus)
    random_pedersen_output = PedersenCommitment(random_value, modulus)
    result = pedersen_output + random_pedersen_output
    assert result.value == (value * random_value) % modulus


def test_pedersen_output_different_modulus(pedersen_output: PedersenCommitment) -> None:
    """
    If the modulus of two Pedersen outputs are different during addition an exception is expected.

    :param pedersen_output: PedersenCommitment with a value and a modulus
    """
    value = pedersen_output.value
    modulus = pedersen_output.modulus
    new_pedersen_output = PedersenCommitment(value, modulus + 1)
    with pytest.raises(TypeError) as excp:
        pedersen_output + new_pedersen_output
        assert (
            str(excp.value)
            == "The modulus must be the same between the Pedersen commitments"
        )


def test_pedersen_output_multiplication(pedersen_output: PedersenCommitment) -> None:
    """
    Multiplication of a Pedersen output and a constant results in a new Pedersen output
    with the result having value equal to the multiplication of the value
    and the constant modulo the modulus, where the modulus is the same.

    :param pedersen_output: PedersenCommitment with a value and a modulus
    """
    value = pedersen_output.value
    modulus = pedersen_output.modulus
    random_value = random.randint(0, modulus)
    result = pedersen_output * random_value
    assert result.value == pow_mod(value, random_value, modulus)


def test_pedersen_output_equality(pedersen_output: PedersenCommitment) -> None:
    """
    Check if two Pedersen outputs are determined to be equal if they have
    the same value and modulus. If they are not the same the equality should fail.

    :param pedersen_output: PedersenCommitment with a value and a modulus
    """
    value = pedersen_output.value
    modulus = pedersen_output.modulus
    assert PedersenCommitment(value, modulus) == pedersen_output
    assert PedersenCommitment(value, modulus + 1) != pedersen_output
    assert PedersenCommitment(value + 1, modulus) != pedersen_output
