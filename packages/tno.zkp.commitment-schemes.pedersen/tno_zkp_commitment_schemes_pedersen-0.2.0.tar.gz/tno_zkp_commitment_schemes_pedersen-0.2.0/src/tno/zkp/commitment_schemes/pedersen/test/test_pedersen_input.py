"""
File to test the input of the Pedersen scheme
"""

from __future__ import annotations

import pytest

from tno.zkp.commitment_schemes.pedersen import (
    PedersenCommitmentInput,
    PedersenVectorCommitmentScheme,
)


@pytest.fixture(
    name="pedersen_input", params=[1, 2, 3, 6, 10, 20, 50, 100, 200, 500, 1000]
)
def fixture_pedersen_input(request: pytest.FixtureRequest) -> PedersenCommitmentInput:
    """
    Create a Pedersen input of length n with values 1...n and reveal information n+1

    :param request: pytest fixture request with parameter for the length of the input
    :return: PedersenCommitmentInput of length n with values 1...n and reveal information n+1
    """
    n = request.param
    vector_input = list(range(1, n + 1))
    reveal_information = n + 1
    scheme = PedersenVectorCommitmentScheme.from_security_param(256, request.param)
    return PedersenCommitmentInput(vector_input, reveal_information, scheme)


def test_pedersen_input_addition(pedersen_input: PedersenCommitmentInput) -> None:
    """
    Addition of two Pedersen inputs results in a new Pedersen input
    where the values as well as the reveal informations are added pairwise.

    :param pedersen_input: PedersenCommitmentInput of length n of 1...n and reveal information n+1
    """
    result = pedersen_input + pedersen_input
    for i, z_i in enumerate(result.input_vector):
        assert z_i == pedersen_input.input_vector[i] + pedersen_input.input_vector[i]
    assert (
        result.reveal_information
        == pedersen_input.reveal_information + pedersen_input.reveal_information
    )


def test_pedersen_input_multiplication(pedersen_input: PedersenCommitmentInput) -> None:
    """
    Multiplication of a Pedersen input and a constant results in a new Pedersen input
    where the values as well as the reveal information are multiplied pairwise.

    :param pedersen_input: PedersenCommitmentInput of length n of 1...n and reveal information n+1
    """
    result = pedersen_input * 3
    for i, z_i in enumerate(result.input_vector):
        assert z_i == pedersen_input.input_vector[i] * 3
    assert result.reveal_information == pedersen_input.reveal_information * 3
