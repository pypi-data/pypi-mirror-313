"""
File containing the Pedersen commitment scheme
"""

from __future__ import annotations

import logging
import math
from random import randrange

import sympy

from tno.mpc.encryption_schemes.utils import USE_GMPY2, mod_inv, pow_mod, randprime
from tno.zkp.templates import CompressibleHomomorphism
from tno.zkp.templates.homomorphism import (
    HomomorphismInput,
    SupportsMultiplicationAndAddition,
)

if USE_GMPY2:
    import gmpy2

logger = logging.getLogger(__name__)


class PedersenCommitmentInput(HomomorphismInput[int]):
    """
    Input for the Pedersen homomorphism. Can be split into two (almost) equal parts.
    When split in half, the right half keeps the original reveal information, while
    the left half gets assigned reveal information 0.
    """

    def split_in_half(self) -> tuple[PedersenCommitmentInput, PedersenCommitmentInput]:
        """
        Split the input vector into two halves.
        If the length is odd, a 0 is first prepended to make the length even.
        The right half keeps the original reveal information, while
        the left half gets assigned reveal information 0.

        :return: Tuple of commitment inputs representing the left and right half respectively.
        """
        vector = self.input_vector

        # if the vector has odd length, prepend a zero
        if len(vector) % 2 == 1:
            vector = [0] + vector

        left = vector[: len(vector) // 2]
        right = vector[len(vector) // 2 :]

        # reveal information is only added to the right hand side
        left_reveal_information = 0
        right_reveal_information = self.reveal_information

        return PedersenCommitmentInput(
            left, left_reveal_information, self._scheme
        ), PedersenCommitmentInput(right, right_reveal_information, self._scheme)

    @property
    def input_vector(self) -> list[int]:
        """
        The input vector that contains the preimage.

        :return: The input vector
        """
        return self._input_vector

    @property
    def reveal_information(self) -> int:
        """
        The reveal information to open the commitment.

        :return: The reveal information corresponding to this input
        """
        return self._reveal_information

    def __add__(self, other: object) -> PedersenCommitmentInput:
        if isinstance(other, int):
            vector_update = [(other + x) for x in self.input_vector]
            reveal_information = self.reveal_information + other
            return PedersenCommitmentInput(
                vector_update, reveal_information, self._scheme
            )
        if isinstance(other, PedersenCommitmentInput):
            if other._scheme != self._scheme:
                raise ValueError(
                    "Can not add two commitment inputs of different schemes"
                )
            vector_update = [
                (x + y) for x, y in zip(self.input_vector, other.input_vector)
            ]
            reveal_information = self.reveal_information + other.reveal_information
            return PedersenCommitmentInput(
                vector_update, reveal_information, self._scheme
            )

        raise TypeError(f"Can not add type {type(other)} with PedersenCommitmentInput")

    def __mul__(self, other: object) -> PedersenCommitmentInput:
        if not isinstance(other, int):
            raise ValueError("Can not multiply by something other than an integer")
        vector_update = [(other * x) for x in self.input_vector]
        reveal_information = self.reveal_information * other
        return PedersenCommitmentInput(vector_update, reveal_information, self._scheme)

    __rmul__ = __mul__

    def __init__(
        self,
        vector_input: list[int],
        reveal_information: int,
        scheme: PedersenVectorCommitmentScheme,
    ):
        self._input_vector = vector_input
        self._reveal_information = reveal_information
        self._scheme = scheme

    def __str__(self) -> str:
        return (
            f"Vector input is: {self._input_vector}\n"
            f"Reveal information is: {self._reveal_information}"
        )


class PedersenCommitment(SupportsMultiplicationAndAddition):
    """
    Output for Pedersen scheme. A separate class in which all additions and multiplications
    are performed under the specified modulus.
    """

    def __init__(self, value: int, modulus: int):
        super().__init__()
        self.value = value
        self._modulus = modulus

    @property
    def modulus(self) -> int:
        """
        The modulus under which all operations are performed.

        :return: The modulus
        """
        return self._modulus

    def __neg__(self) -> PedersenCommitment:
        return PedersenCommitment(mod_inv(self.value, self.modulus), self.modulus)

    def __add__(self, other: object) -> PedersenCommitment:
        if not isinstance(other, PedersenCommitment):
            raise TypeError("Expected a Pedersen commitment")
        if self.modulus != other.modulus:
            raise TypeError(
                "The modulus must be the same between the Pedersen commitments"
            )
        return PedersenCommitment(
            (self.value * other.value) % self.modulus, self.modulus
        )

    def __mul__(self, other: object) -> PedersenCommitment:
        if not isinstance(other, int):
            raise TypeError("Expected an integer")

        self_value = self.value
        if other < 0:
            other = -other
            self_value = mod_inv(self_value, self.modulus)

        return PedersenCommitment(
            pow_mod(self_value, other, self.modulus), self.modulus
        )

    __rmul__ = __mul__

    def __str__(self) -> str:
        return str(self.value)

    def to_bytes(self) -> bytes:
        """
        Creates a bytes object containing the Pedersen commitment value.

        :return: A bytes object of the commitment
        """
        length = int(math.ceil(self.value.bit_length() / 8))
        return int(self.value).to_bytes(length=length, byteorder="big")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PedersenCommitment):
            return False
        return self.value == other.value and self.modulus == other.modulus

    def __hash__(self) -> int:
        return hash((self.value, self.modulus))


class PedersenVectorCommitmentScheme(
    CompressibleHomomorphism[int, PedersenCommitment, int]
):
    """
    A Pedersen scheme which operates on a group. The Pedersen scheme evaluates the result
    as $h^u g_1^{x_1} g_2^{x_2} ... g_n^{x^n}$, where $x$ is the vector input of length $n$,
    $u$ is the reveal information and the $g_i$ and $h$ are generators.
    The Pedersen scheme can also be split into two halves. If the length is odd a 1 is prepended to
    make the Pedersen scheme of even length.
    When split in half, the generators $g_i$ are split, and both halves keep the same generator $h$.
    """

    def split_in_half(
        self,
    ) -> tuple[PedersenVectorCommitmentScheme, PedersenVectorCommitmentScheme]:
        """
        Split the generators of the Pedersen scheme into two halves.
        If the length is odd, a 1 is first prepended to make the length even.
        Both halves keep the same generator $h$.

        :return: Tuple of commitment schemes representing the left and right half respectively.
        """
        generators = self.generator_gs
        # if the homomorphism has odd length, prepend a 1
        if len(generators) % 2 == 1:
            one = gmpy2.mpz(1) if USE_GMPY2 else 1
            generators = [one] + generators

        new_input_size = len(generators) // 2
        left_generators = generators[:new_input_size]
        right_generators = generators[new_input_size:]
        left_scheme = PedersenVectorCommitmentScheme(
            new_input_size,
            self.modulus,
            self.input_modulus,
            left_generators,
            self.generator_h,
        )
        right_scheme = PedersenVectorCommitmentScheme(
            new_input_size,
            self.modulus,
            self.input_modulus,
            right_generators,
            self.generator_h,
        )
        return left_scheme, right_scheme

    def __mul__(self, other: object) -> PedersenVectorCommitmentScheme:
        if not isinstance(other, int):
            raise TypeError(
                f"Can not multiply with anything other than a number, current type is {type(other)}."
            )
        new_gs = [pow_mod(g, other, self.modulus) for g in self.generator_gs]
        new_h = pow_mod(self.generator_h, other, self.modulus)
        return PedersenVectorCommitmentScheme(
            self.input_size,
            self.modulus,
            self.input_modulus,
            new_gs,
            new_h,
        )

    def __add__(self, other: object) -> PedersenVectorCommitmentScheme:
        if not isinstance(other, PedersenVectorCommitmentScheme):
            raise TypeError(
                f"Can not add with anything other than a Pedersen vector commitment scheme, "
                f"current type is {type(other)}."
            )
        if other.input_size != self.input_size:
            raise ValueError(
                f"Can only add two scheme of the same size "
                f"Can only add two scheme of the same size, "
                f"current sizes are {self.input_size} and {other.input_size}."
            )

        if other.input_modulus != self.input_modulus:
            raise ValueError("Both schemes must use the same modulus")

        new_gs = [
            g_other * g_self
            for g_self, g_other in zip(self.generator_gs, other.generator_gs)
        ]
        new_h = other.generator_h * self.generator_h
        return PedersenVectorCommitmentScheme(
            self.input_size,
            self.modulus,
            self.input_modulus,
            new_gs,
            new_h,
        )

    @property
    def input_size(self) -> int:
        """
        The length any input vector should have.
        This is equal to the number of generators in the Pedersen scheme.

        :return: The input size
        """
        return self._input_length

    def __init__(
        self,
        vector_length: int,
        modulus: int,
        input_modulus: int,
        generator_gs: list[int],
        generator_h: int,
    ):
        self._input_length = vector_length
        self._modulus = modulus
        self.input_modulus = input_modulus
        self.generator_gs = generator_gs
        self.generator_h = generator_h

    @classmethod
    def from_security_param(
        cls,
        key_length: int,
        vector_length: int = 1,
        input_modulus: int | None = None,
    ) -> PedersenVectorCommitmentScheme:
        """
        Create a Pedersen commitment scheme using the security parameters provided.

        :param key_length: The length of the key in bits
        :param vector_length: The length of the input vector on which the scheme can be applied
        :param input_modulus: The modulus for the input elements in the input vector.
            If not given the value modulus is the modulus of the generated prime.
        :return: A Pedersen commitment scheme with the provided parameters
        """
        # Check whether input_modulus is prime
        if input_modulus is not None:
            assert sympy.isprime(input_modulus)
            value_mod_bit_len = input_modulus.bit_length()
            leftover_bit_len = key_length - value_mod_bit_len
        else:
            leftover_bit_len = key_length
        logger.debug("Initializing the key")
        success = False

        # Generate safe prime p. If value modulus is given, we need p-1 to have
        # value modulus as a divisor as well. This is to ensure that we have a
        # subgroup of that order in the multiplicative group Z_p^*.
        i = q = p = 0
        while not success:
            q = randprime(2 ** (leftover_bit_len - 1), 2**leftover_bit_len - 1)
            p = 2 * q * input_modulus + 1 if input_modulus else 2 * q + 1
            success = sympy.isprime(p)
            i = i + 1
            if i % 1000 == 0:
                logger.debug("round %d", i)
        # If no input_modulus is given, we will work in the subgroup of prime order q.

        generator_gs = []

        for i in range(vector_length):
            generator_gs.append(cls.get_prime_subgroup_generator(p, q, input_modulus))
        generator_h = cls.get_prime_subgroup_generator(p, q, input_modulus)

        if not input_modulus:
            input_modulus = q

        return cls(vector_length, p, input_modulus, generator_gs, generator_h)

    @staticmethod
    def get_prime_subgroup_generator(p: int, q: int, input_modulus: int | None) -> int:
        """
        Given a finite multiplicative group and a prime, sample a random nontrivial
        element (which is also a generator) of the prime order subgroup. Based on the
        fact that all nontrivial elements of a prime order group have that prime as order.

        :param group order: Order of the group
        :param prime: Prime number
        :return: A randomly generated nontrivial element of prime order subgroup
        """
        factors = {2, q, input_modulus} if input_modulus else {2, q}
        attempt = randrange(2, p - 1)
        resolved = False
        while not resolved:
            resolved = True
            attempt = randrange(2, p - 1)
            for factor in factors:
                power = pow_mod(attempt, int((p - 1) / factor), p)
                if power == 1:
                    resolved = False
                    break
        generator = (
            pow_mod(attempt, 2 * q, p)
            if input_modulus is not None and input_modulus != q
            else pow_mod(attempt, 2, p)
        )

        return generator

    def evaluate(
        self, homomorphism_input: HomomorphismInput[int]
    ) -> PedersenCommitment:
        """
        Apply the Pedersen scheme to the homomorphism input.
        The result is $h^u g_1^{x_1} g_2^{x_2} ... g_n^{x^n}$,
        where $x$ is the vector input of length $n$, $u$ is the reveal information
        and the $g_i$ and $h$ are generators.

        :param homomorphism_input: The input for the Pedersen scheme
        :return: PedersenCommitment representing the result of the input applied to the homomorphism
        :raise ValueError: When the input length is not of the expected input size
        :raise TypeError: When the input is not a `PedersenCommitmentInput`
        """
        if not isinstance(homomorphism_input, PedersenCommitmentInput):
            raise TypeError(
                f"Different input type is given than expected. Expected `PedersenCommitmentInput`, got {type(homomorphism_input)}."
            )

        randomness = pow_mod(
            self.generator_h, homomorphism_input.reveal_information, self._modulus
        )
        logger.debug(
            f"reveal information: {homomorphism_input.reveal_information}\n"
            f"randomness: {randomness}\n"
            f"input vector: {homomorphism_input.input_vector}"
        )
        commitment = randomness
        if len(homomorphism_input.input_vector) != self.input_size:
            raise ValueError(
                f"Input is not of the correct length got length "
                f"{len(homomorphism_input.input_vector)} expected "
                f"{self.input_size}"
            )

        for generator, value in zip(self.generator_gs, homomorphism_input.input_vector):
            commitment = (
                commitment * pow_mod(generator, value, self._modulus)
            ) % self._modulus
        logger.debug(f"evaluation result: {commitment}")
        return PedersenCommitment(commitment, self.modulus)

    def random_input(self) -> PedersenCommitmentInput:
        """
        Generate a random input that can be used in the Pedersen scheme.

        :return: a random PedersenCommitmentInput
        """
        random_vector = [
            randrange(0, self.input_modulus) for _ in range(self.input_size)
        ]
        random_reveal_information = randrange(0, self.input_modulus)
        return PedersenCommitmentInput(random_vector, random_reveal_information, self)

    def output_to_bytes(self, output: PedersenCommitment) -> bytes:
        """
        Create a bytes object of a Pedersen output.
        Is used to create a hash of a Pedersen commitment,
        which is used as a challenge to make the protocol non-interactive.

        :param output: A Pedersen commitment
        :return: A bytes object of the output
        """
        return output.to_bytes()

    def challenge_from_bytes(self, hash_bytes: bytes) -> int:
        """
        Create a challenge from a bytes object.
        The bytes object is generated as a hash of a previous Pedersen commitment.
        This challenge is used to make the protocol non-interactive.

        :param hash_bytes: A bytes object created by a hash function
        :return: A challenge to use in the sigma protocol
        """
        return int(int.from_bytes(hash_bytes, "big") % self.modulus)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PedersenVectorCommitmentScheme):
            return False
        return (
            self.generator_gs == other.generator_gs
            and self.generator_gs == other.generator_gs
            and self.modulus == other.modulus
        )

    def __hash__(self) -> int:
        return hash((self.generator_gs, self.generator_h, self.modulus))

    @property
    def modulus(self) -> int:
        """
        Modulus of the group used during the pedersen commitment scheme.

        :return: The modulus
        """
        return self._modulus
