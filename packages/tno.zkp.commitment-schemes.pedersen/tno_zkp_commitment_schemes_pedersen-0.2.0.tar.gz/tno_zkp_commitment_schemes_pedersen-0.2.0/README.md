# TNO PET Lab - Zero-Knowledge Proofs (ZKP) - Commitment Schemes - Pedersen

Implementation of the Pedersen commitment scheme.

### PET Lab

The TNO PET Lab consists of generic software components, procedures, and functionalities developed and maintained on a regular basis to facilitate and aid in the development of PET solutions. The lab is a cross-project initiative allowing us to integrate and reuse previously developed PET functionalities to boost the development of new protocols and solutions.

The package `tno.zkp.commitment_schemes.pedersen` is part of the [TNO Python Toolbox](https://github.com/TNO-PET).

_Limitations in (end-)use: the content of this software package may solely be used for applications that comply with international export control laws._  
_This implementation of cryptographic software has not been audited. Use at your own risk._

## Documentation

Documentation of the `tno.zkp.commitment_schemes.pedersen` package can be found
[here](https://docs.pet.tno.nl/zkp/commitment_schemes/pedersen/0.2.0).

## Install

Easily install the `tno.zkp.commitment_schemes.pedersen` package using `pip`:

```console
$ python -m pip install tno.zkp.commitment_schemes.pedersen
```

_Note:_ If you are cloning the repository and wish to edit the source code, be
sure to install the package in editable mode:

```console
$ python -m pip install -e 'tno.zkp.commitment_schemes.pedersen'
```

If you wish to run the tests you can use:

```console
$ python -m pip install 'tno.zkp.commitment_schemes.pedersen[tests]'
```

_Note:_ A significant performance improvement can be achieved by installing the GMPY2 library.

```console
$ python -m pip install 'tno.zkp.commitment_schemes.pedersen[gmpy]'
```

## Using the Pedersen Zero Knowledge Proof library

**NOTE:** This library is meant to be used in combination with the zero-knowledge proof (ZKP) template library found [here](https://github.com/TNO-ZKP/templates). Preliminaries on the content can also be found here. The Pedersen library is an instance of a ZKP, which uses the functionality from the template. In that sense, it is interchangable with the modulus linear form described in the template. They are both homomorphisms to be used in sigma protocols, though they have different structure. If anything below is unclear, it is highly recommended to read the preliminaries.

The ZKP library is based on Thomas Attema's dissertation Compressed $\Sigma$-protocol Theory, which can be found [here](https://scholarlypublications.universiteitleiden.nl/handle/1887/3619596). Many concepts are taken from it, and there will be references throughout the code to the dissertation. In this README the crucial concepts from the dissertation needed to use this library will be explained in short. If anything is unclear, feel free to raise an issue at the code repository.

## Commitment schemes

A commitment scheme is a cryptograpic protocol that is used when a party has a value they want to commit to now, but only share later.
A commitment scheme consists of two phases: in the _commit phase_, the prover commits to a chosen value and sends a _commitment_ to the verifier. During the _reveal phase_, the prover sends the original value and the verifier checks that the earlier commitment was indeed correct. One can view the functionality similar to the prover putting the value in a box, locking it and giving it to the verifier, and only later giving the key to the verifier to check.
Commitment schemes can for instance be used to fairly flip a coin over text-only communication, where it can make sure neither party cheats by changing their prediction. It can also be used in more complex applications, such as signature schemes, secret sharing or zero-knowledge proofs.

### The Pedersen commitment scheme

The Pedersen commitment scheme is defined as follows. The prover has a secret value $\mathbf{x} \in \mathbb{G}^n$ and reveal information $u \in \mathbb{G}$. They calculate the commitment $P := \psi_n(u, \mathbf{x})$, where the homomorphism $\psi_n$ is defined as

$$ \psi_n(u, \mathbf{x}) := h^u \cdot g_1^{x_1} g_2^{x_2} \cdots g_n^{x_n} $$

where $h, g_1, g_2, \dots, g_n \in \mathbb{G}$.
Then the prover sends $P$ to the verifier who stores it. Only later, when the prover wants to show that they indeed chose $\mathbf{x}$, they send $\mathbf{x}$ to the verifier, who then checks that $\psi(u, \mathbf{x}) = P$.

## Compressing the homomorphism

Splitting the homomorphism $\psi_n$ and the input $(u, \mathbf{x})$ works similarly to the linear form found in [the templates package](https://ci.tno.nl/gitlab/pet/lab/zkp/python-packages/microlibs/templates/-/tree/master/src/tno/zkp/modulus_linear_form?ref_type=heads), but the reveal information needs to be handled correctly as well. We split the input vector $\mathbf{x}$ as follows

```math
\mathbf{x} = (x_1, x_2, \dots, x_n) \\
\mathbf{x_L} = (x_1, x_2, \dots, x_{n/2}) \\
\mathbf{x_R} = (x_{n/2+1}, x_{n/2+2}, \dots, x_n)
```

and similarly the generators $g_1, g_2, \dots, g_n$ of $\psi(\cdot)$.
We also need to 'split' the reveal information $u$ and the generator $h$, but these are numbers rather than vectors.
It turns out that if we simply copy these values to both halves, the verification fails. So instead, we give the halves new reveal information $u_L$ and $u_R$ respectively, leading to the following

```math
 \psi_n(u, \mathbf{x}) := h^u \cdot g_1^{x_1} g_2^{x_2} \cdots g_n^{x_n} \\
 \psi_{n/2}^L(u_L, \mathbf{x}_L) := h^{u_L} \cdot g_1^{x_1} g_2^{x_2} \cdots g_{n/2}^{x_{n/2}}
 \\
 \psi_{n/n}^R(u_R, \mathbf{x}_R) := h^{u_R} \cdot g_{n/2+1}^{x_{n/2+1}} g_{n/2+2}^{x_{n/2+2}} \cdots g_n^{x_n}
```

If we plug general $u_L, u_R$ into the scheme and follow the protocol, at the verification step we get the equation

```math
 h^{u_L+cu+c^2u_R} = \left(h^{c+1}\right)^{(u_L+cu_R)} \\
 \implies u_L+cu+c^2u_R = u_L+c(u_L+u_R)+c^2u_R \\
 \implies u = u_L+u_R
```

Therefore when splitting, we define $u_L:=0, \ u_R:=u$ to ensure correct behavior. This design is followed in the code.

## Creating a Sigma Protocol

To support the creation of a sigma protocol the template classes have been created. The template classes can be split into two categories.

The first category are the classes needed to create a basic sigma protocol. The basic sigma protocol creates a proof of knowledge in a non-interactive way. The `StandardSigmaProtocol` object contains all the information needed for the verification and none of the private information. The object can therefore be shared with the verifier for verification.

The `PedersenVectorCommitmentScheme` is a `Homomorphism` object that can be used with the sigma protocol library.

The easiest way to create a `PedersenVectorCommitmentScheme` is using the `from_security_param`, supplying a key length of 256 bits and generating a vector of length 16 in this case. You can also define the coefficients manually, but you need to supply a large enough safe prime as well.

Generating the proof of knowledge is relatively straight forward. You call the method `generate_proof` with the homomorphism, the secret input and the hash function. The class will handle the process as described in the steps above.

To verify the proof of knowledge you only need to call the `verify` function.

```python
from tno.zkp.commitment_schemes.pedersen import PedersenVectorCommitmentScheme
from tno.zkp.templates.sigma_protocol import StandardSigmaProtocol

homomorphism = PedersenVectorCommitmentScheme.from_security_param(key_length=256, vector_length=16)
secret_input_x = homomorphism.random_input()

proof_of_knowledge = StandardSigmaProtocol.generate_proof(
  homomorphism, secret_input_x, "sha256"
)

# proof of knowledge can now be transferred to the verifier
assert proof_of_knowledge.verify()
```

## Compressing a Sigma Protocol

To compress a proof of knowledge there are some requirements on the homomorphism and the input. The requirements are
enforced using the `CompressibleHomomorphism` and the `CompressibleHomomorphismInput` abstract classes.

> Compressing a proof of knowledge makes the verification of the protocol cheaper. The cost savings occur due to a
> compression mechanism. The compression mechanism is described in detail in the dissertation.

The `PedersenVectorCommitmentScheme` class satisfies the requirements. Therefore, we can use the
previous proof of knowledge for compression.

To apply the compression we need to use a compression mechanism. The compression mechanism from the dissertation has
been implemented in the template. To apply it you need to do the following:

```python
from tno.zkp.templates.compression_mechanism import full_compression

# compress the proof of knowledge as much as possible
compressed_protocol = full_compression(proof_of_knowledge)
assert compressed_protocol.verify()
```

The function `full_compression` reduces the ZKP from length $n$ until it can not be compressed anymore, which is a length of 1. The function used for the compression is called `compression` and is available to the user as well. The `compression` function halves the length of the ZKP.
