"""
Test cases for the Pedersen protocol.
"""

from tno.zkp.templates import StandardSigmaProtocol

from tno.zkp.commitment_schemes.pedersen import PedersenVectorCommitmentScheme


def test_basic_sigma_protocol_without_input_modulus(
    pedersen_commitment_scheme_without_input_modulus: PedersenVectorCommitmentScheme,
) -> None:
    """
    Test case to check the basic sigma protocol.

    :param pedersen_commitment_scheme_without_input_modulus: The Pedersen scheme
        used to test the sigma protocol
    """
    scheme = pedersen_commitment_scheme_without_input_modulus
    random_input = scheme.random_input()
    sigma_protocol = StandardSigmaProtocol.generate_proof(
        scheme, random_input, "sha256"
    )
    assert sigma_protocol.verify()


def test_basic_sigma_protocol_with_input_modulus(
    pedersen_commitment_scheme_with_input_modulus: PedersenVectorCommitmentScheme,
) -> None:
    """
    Test case to check the basic sigma protocol.

    :param pedersen_commitment_scheme_with_input_modulus: The Pedersen scheme
        used to test the sigma protocol
    """
    scheme = pedersen_commitment_scheme_with_input_modulus
    random_input = scheme.random_input()
    sigma_protocol = StandardSigmaProtocol.generate_proof(
        scheme, random_input, "sha256"
    )
    assert sigma_protocol.verify()
