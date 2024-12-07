"""
Test cases for the compression mechanism of the Pedersen protocol.
"""

import re

import pytest

from tno.zkp.templates import StandardSigmaProtocol, compression, full_compression

from tno.zkp.commitment_schemes.pedersen import PedersenVectorCommitmentScheme


def test_compressing_pedersen_protocol_without_input_modulus(
    pedersen_commitment_scheme_without_input_modulus: PedersenVectorCommitmentScheme,
) -> None:
    """
    Test case for compression of the Pedersen protocol.

    :param pedersen_commitment_scheme_without_input_modulus: Scheme used to test the sigma protocol
    """
    scheme = pedersen_commitment_scheme_without_input_modulus
    random_input = scheme.random_input()
    sigma_protocol = StandardSigmaProtocol.generate_proof(
        scheme, random_input, "sha256"
    )
    assert sigma_protocol.verify()

    if scheme.input_size == 1:
        # input size less or equal to 1 throws an exception
        expected_message = (
            "Sigma protocol can not be compressed, input size is less or equal to "
            "1 (1)"
        )
        with pytest.raises(ValueError, match=re.escape(expected_message)):
            compression(sigma_protocol)
        return

    homomorphism_size = sigma_protocol.homomorphism.input_size
    compressed = compression(sigma_protocol)
    assert compressed.homomorphism.input_size < homomorphism_size
    homomorphism_size = compressed.homomorphism.input_size
    assert compressed.verify()

    while compressed.homomorphism.input_size > 1:
        compressed = compression(compressed)
        assert compressed.homomorphism.input_size < homomorphism_size
        homomorphism_size = compressed.homomorphism.input_size
        assert compressed.verify()

    assert compressed.homomorphism.input_size == 1


def test_fully_compressing_pedersen_protocol_without_input_modulus(
    pedersen_commitment_scheme_without_input_modulus: PedersenVectorCommitmentScheme,
) -> None:
    """
    Test case for full compression of the Pedersen protocol.

    :param pedersen_commitment_scheme_without_input_modulus: Scheme used to test the sigma protocol
    """
    scheme = pedersen_commitment_scheme_without_input_modulus
    random_input = scheme.random_input()
    sigma_protocol = StandardSigmaProtocol.generate_proof(
        scheme, random_input, "sha256"
    )
    assert sigma_protocol.verify()

    if scheme.input_size == 1:
        # input size less or equal to 1 throws an exception
        expected_message = (
            "Sigma protocol can not be compressed, input size is less or equal to "
            "1 (1)"
        )
        with pytest.raises(ValueError, match=re.escape(expected_message)):
            full_compression(sigma_protocol)
        return

    compressed = full_compression(sigma_protocol)
    assert compressed.homomorphism.input_size == 1
    assert compressed.verify()


def test_compressing_pedersen_protocol_with_input_modulus(
    pedersen_commitment_scheme_with_input_modulus: PedersenVectorCommitmentScheme,
) -> None:
    """
    Test case for compression of the Pedersen protocol.

    :param pedersen_commitment_scheme_with_input_modulus: Scheme used to test the sigma protocol
    """
    scheme = pedersen_commitment_scheme_with_input_modulus
    random_input = scheme.random_input()
    sigma_protocol = StandardSigmaProtocol.generate_proof(
        scheme, random_input, "sha256"
    )
    assert sigma_protocol.verify()

    if scheme.input_size == 1:
        # input size less or equal to 1 throws an exception
        expected_message = (
            "Sigma protocol can not be compressed, input size is less or equal to "
            "1 (1)"
        )
        with pytest.raises(ValueError, match=re.escape(expected_message)):
            compression(sigma_protocol)
        return

    homomorphism_size = sigma_protocol.homomorphism.input_size
    compressed = compression(sigma_protocol)
    assert compressed.homomorphism.input_size < homomorphism_size
    homomorphism_size = compressed.homomorphism.input_size
    assert compressed.verify()

    while compressed.homomorphism.input_size > 1:
        compressed = compression(compressed)
        assert compressed.homomorphism.input_size < homomorphism_size
        homomorphism_size = compressed.homomorphism.input_size
        assert compressed.verify()

    assert compressed.homomorphism.input_size == 1


def test_fully_compressing_pedersen_protocol_with_input_modulus(
    pedersen_commitment_scheme_with_input_modulus: PedersenVectorCommitmentScheme,
) -> None:
    """
    Test case for full compression of the Pedersen protocol.

    :param pedersen_commitment_scheme_with_input_modulus: Scheme used to test the sigma protocol
    """
    scheme = pedersen_commitment_scheme_with_input_modulus
    random_input = scheme.random_input()
    sigma_protocol = StandardSigmaProtocol.generate_proof(
        scheme, random_input, "sha256"
    )
    assert sigma_protocol.verify()

    if scheme.input_size == 1:
        # input size less or equal to 1 throws an exception
        expected_message = (
            "Sigma protocol can not be compressed, input size is less or equal to "
            "1 (1)"
        )
        with pytest.raises(ValueError, match=re.escape(expected_message)):
            full_compression(sigma_protocol)
        return

    compressed = full_compression(sigma_protocol)
    assert compressed.homomorphism.input_size == 1
    assert compressed.verify()
