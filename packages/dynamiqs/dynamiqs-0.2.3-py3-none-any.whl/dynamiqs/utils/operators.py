from __future__ import annotations

from math import prod

import jax
import jax.numpy as jnp
from jax import Array
from jax.typing import ArrayLike

from .._utils import cdtype
from .quantum_utils import dag, tensor

__all__ = [
    'cnot',
    'create',
    'destroy',
    'displace',
    'eye',
    'hadamard',
    'momentum',
    'number',
    'parity',
    'position',
    'quadrature',
    'rx',
    'ry',
    'rz',
    'sgate',
    'sigmam',
    'sigmap',
    'sigmax',
    'sigmay',
    'sigmaz',
    'squeeze',
    'tgate',
    'toffoli',
    'zero',
]


def eye(*dims: int) -> Array:
    r"""Returns the identity operator.

    If multiple dimensions are provided $\mathtt{dims}=(n_1,\dots,n_N)$, it returns the
    identity operator of the composite Hilbert space of dimension $n=\prod n_k$:
    $$
        I_n = I_{n_1}\otimes\dots\otimes I_{n_N}.
    $$

    Args:
        *dims: Hilbert space dimension of each subsystem.

    Returns:
        _(array of shape (n, n))_ Identity operator, with _n = prod(dims)_.

    Examples:
        Single-mode $I_4$:
        >>> dq.eye(4)
        Array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j]], dtype=complex64)

        Multi-mode $I_2 \otimes I_3$:
        >>> dq.eye(2, 3)
        Array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j]], dtype=complex64)
    """
    dim = prod(dims)
    return jnp.eye(dim, dtype=cdtype())


def zero(*dims: int) -> Array:
    r"""Returns the null operator.

    If multiple dimensions are provided $\mathtt{dims}=(n_1,\dots,n_N)$, it returns the
    null operator of the composite Hilbert space of dimension $n=\prod n_k$:
    $$
        0_n = 0_{n_1}\otimes\dots\otimes 0_{n_N}.
    $$

    Args:
        *dims: Hilbert space dimension of each subsystem.

    Returns:
        _(array of shape (n, n))_ Null operator, with _n = prod(dims)_.

    Examples:
        Single-mode $0_4$:
        >>> dq.zero(4)
        Array([[0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j]], dtype=complex64)

        Multi-mode $0_2 \otimes 0_3$:
        >>> dq.zero(2, 3)
        Array([[0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j]], dtype=complex64)
    """
    dim = prod(dims)
    return jnp.zeros((dim, dim), dtype=cdtype())


def destroy(*dims: int) -> Array | tuple[Array, ...]:
    r"""Returns a bosonic annihilation operator, or a tuple of annihilation operators
    for a multi-mode system.

    If multiple dimensions are provided $\mathtt{dims}=(n_1,\dots,n_N)$, it returns a
    tuple with _len(dims)_ operators $(A_1,\dots,A_N)$, where $A_k$ is the annihilation
    operator acting on the $k$-th subsystem within the composite Hilbert space of
    dimension $n=\prod n_k$:
    $$
        A_k = I_{n_1} \otimes\dots\otimes a_{n_k} \otimes\dots\otimes I_{n_N}.
    $$

    Args:
        *dims: Hilbert space dimension of each mode.

    Returns:
        _(array or tuple of arrays, each of shape (n, n))_ Annihilation operator(s),
            with _n = prod(dims)_.

    Examples:
        Single-mode $a$:
        >>> dq.destroy(4)
        Array([[0.   +0.j, 1.   +0.j, 0.   +0.j, 0.   +0.j],
               [0.   +0.j, 0.   +0.j, 1.414+0.j, 0.   +0.j],
               [0.   +0.j, 0.   +0.j, 0.   +0.j, 1.732+0.j],
               [0.   +0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j]], dtype=complex64)

        Multi-mode $a\otimes I_3$ and $I_2\otimes b$:
        >>> a, b = dq.destroy(2, 3)
        >>> a
        Array([[0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j]], dtype=complex64)
        >>> b
        Array([[0.   +0.j, 1.   +0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j],
               [0.   +0.j, 0.   +0.j, 1.414+0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j],
               [0.   +0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j],
               [0.   +0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j, 1.   +0.j, 0.   +0.j],
               [0.   +0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j, 1.414+0.j],
               [0.   +0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j]],      dtype=complex64)
    """  # noqa: E501
    if len(dims) == 1:
        return _destroy_single(dims[0])

    a = [_destroy_single(dim) for dim in dims]
    Id = [eye(dim) for dim in dims]
    return tuple(
        tensor(*[a[j] if i == j else Id[j] for j in range(len(dims))])
        for i in range(len(dims))
    )


def _destroy_single(dim: int) -> Array:
    """Bosonic annihilation operator."""
    return jnp.diag(jnp.sqrt(jnp.arange(1, stop=dim, dtype=cdtype())), k=1)


def create(*dims: int) -> Array | tuple[Array, ...]:
    r"""Returns a bosonic creation operator, or a tuple of creation operators for a
    multi-mode system.

    If multiple dimensions are provided $\mathtt{dims}=(n_1,\dots,n_N)$, it returns a
    tuple with _len(dims)_ operators $(A_1^\dag,\dots,A_N^\dag)$, where $A_k^\dag$ is
    the creation operator acting on the $k$-th subsystem within the composite Hilbert
    space of dimension $n=\prod n_k$:
    $$
        A_k^\dag = I_{n_1} \otimes\dots\otimes a_{n_k}^\dag \otimes\dots\otimes I_{n_N}.
    $$

    Args:
        *dims: Hilbert space dimension of each mode.

    Returns:
        _(array or tuple of arrays, each of shape (n, n))_ Creation operator(s), with
            _n = prod(dims)_.

    Examples:
        Single-mode $a^\dag$:
        >>> dq.create(4)
        Array([[0.   +0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j],
               [1.   +0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j],
               [0.   +0.j, 1.414+0.j, 0.   +0.j, 0.   +0.j],
               [0.   +0.j, 0.   +0.j, 1.732+0.j, 0.   +0.j]], dtype=complex64)

        Multi-mode $a^\dag\otimes I_3$ and $I_2\otimes b^\dag$:
        >>> adag, bdag = dq.create(2, 3)
        >>> adag
        Array([[0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j]], dtype=complex64)
        >>> bdag
        Array([[0.   +0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j],
               [1.   +0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j],
               [0.   +0.j, 1.414+0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j],
               [0.   +0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j],
               [0.   +0.j, 0.   +0.j, 0.   +0.j, 1.   +0.j, 0.   +0.j, 0.   +0.j],
               [0.   +0.j, 0.   +0.j, 0.   +0.j, 0.   +0.j, 1.414+0.j, 0.   +0.j]],      dtype=complex64)
    """  # noqa: E501
    if len(dims) == 1:
        return _create_single(dims[0])

    adag = [_create_single(dim) for dim in dims]
    Id = [eye(dim) for dim in dims]
    return tuple(
        tensor(*[adag[j] if i == j else Id[j] for j in range(len(dims))])
        for i in range(len(dims))
    )


def _create_single(dim: int) -> Array:
    """Bosonic creation operator."""
    return jnp.diag(jnp.sqrt(jnp.arange(1, stop=dim, dtype=cdtype())), k=-1)


def number(*dims: int) -> Array | tuple[Array, ...]:
    r"""Returns the number operator of a bosonic mode, or a tuple of number operators
    for a multi-mode system.

    For a single mode, it is defined by $N = a^\dag a$, where $a$ and $a^\dag$ are the
    mode annihilation and creation operators, respectively. If multiple dimensions are
    provided $\mathtt{dims}=(n_1,\dots,n_M)$, it returns a tuple with _len(dims)_
    operators $(N_1,\dots,N_M)$, where $N_k$ is the number operator acting on the $k$-th
    subsystem within the composite Hilbert space of dimension $n=\prod n_k$:
    $$
        N_k = I_{n_1} \otimes\dots\otimes a_{n_k}^\dag a_{n_k} \otimes\dots\otimes I_{n_M}.
    $$

    Args:
        *dims: Hilbert space dimension of each mode.

    Returns:
        _(array or tuple of arrays, each of shape (n, n))_ Number operator(s), with
            _n = prod(dims)_.

    Examples:
        Single-mode $a^\dag a$:
        >>> dq.number(4)
        Array([[0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 2.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 3.+0.j]], dtype=complex64)

        Multi-mode $a^\dag a \otimes I_3$ and $I_2\otimes b^\dag b$:
        >>> na, nb = dq.number(2, 3)
        >>> na
        Array([[0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j]], dtype=complex64)
        >>> nb
        Array([[0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 2.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 2.+0.j]], dtype=complex64)
    """  # noqa: E501
    if len(dims) == 1:
        return _number_single(dims[0])

    nums = [_number_single(dim) for dim in dims]
    Id = [eye(dim) for dim in dims]
    return tuple(
        tensor(*[nums[j] if i == j else Id[j] for j in range(len(dims))])
        for i in range(len(dims))
    )


def _number_single(dim: int) -> Array:
    """Bosonic number operator."""
    return jnp.diag(jnp.arange(0, stop=dim, dtype=cdtype()))


def parity(dim: int) -> Array:
    r"""Returns the parity operator of a bosonic mode.

    It is defined by $P = e^{i\pi a^\dag a}$, where $a$ and $a^\dag$ are the
    annihilation and creation operators, respectively.

    Args:
        dim: Dimension of the Hilbert space.

    Returns:
        _(array of shape (dim, dim))_ Parity operator.

    Examples:
        >>> dq.parity(4)
        Array([[ 1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j],
               [ 0.+0.j, -1.+0.j,  0.+0.j,  0.+0.j],
               [ 0.+0.j,  0.+0.j,  1.+0.j,  0.+0.j],
               [ 0.+0.j,  0.+0.j,  0.+0.j, -1.+0.j]], dtype=complex64)
    """
    diag_values = jnp.ones(dim, dtype=cdtype())
    diag_values = diag_values.at[1::2].set(-1)
    return jnp.diag(diag_values)


def displace(dim: int, alpha: ArrayLike) -> Array:
    r"""Returns the displacement operator of complex amplitude $\alpha$.

    It is defined by
    $$
        D(\alpha) = \exp(\alpha a^\dag - \alpha^* a),
    $$
    where $a$ and $a^\dag$ are the annihilation and creation operators, respectively.

    Args:
        dim: Dimension of the Hilbert space.
        alpha _(array_like of shape (...))_: Displacement amplitude.

    Returns:
        _(array of shape (..., dim, dim))_ Displacement operator.

    Examples:
        >>> dq.displace(4, 0.5)
        Array([[ 0.882+0.j, -0.441+0.j,  0.156+0.j, -0.047+0.j],
               [ 0.441+0.j,  0.662+0.j, -0.542+0.j,  0.27 +0.j],
               [ 0.156+0.j,  0.542+0.j,  0.442+0.j, -0.697+0.j],
               [ 0.047+0.j,  0.27 +0.j,  0.697+0.j,  0.662+0.j]], dtype=complex64)
        >>> dq.displace(4, [0.1, 0.2]).shape
        (2, 4, 4)
    """
    alpha = jnp.asarray(alpha, dtype=cdtype())
    alpha = alpha[..., None, None]  # (..., 1, 1)

    a = destroy(dim)  # (n, n)
    return jax.scipy.linalg.expm(alpha * dag(a) - alpha.conj() * a)


def squeeze(dim: int, z: ArrayLike) -> Array:
    r"""Returns the squeezing operator of complex squeezing amplitude $z$.

    It is defined by
    $$
        S(z) = \exp\left(\frac{1}{2}\left(z^* a^2 - z a^{\dag 2}\right)\right),
    $$
    where $a$ and $a^\dag$ are the annihilation and creation operators, respectively.

    Args:
        dim: Dimension of the Hilbert space.
        z _(array_like of shape (...))_: Squeezing amplitude.

    Returns:
        _(array of shape (..., dim, dim))_ Squeezing operator.

    Examples:
        >>> dq.squeeze(4, 0.5)
        Array([[ 0.938+0.j,  0.   +0.j,  0.346+0.j,  0.   +0.j],
               [ 0.   +0.j,  0.818+0.j,  0.   +0.j,  0.575+0.j],
               [-0.346+0.j,  0.   +0.j,  0.938+0.j,  0.   +0.j],
               [ 0.   +0.j, -0.575+0.j,  0.   +0.j,  0.818+0.j]], dtype=complex64)
        >>> dq.squeeze(4, [0.1, 0.2]).shape
        (2, 4, 4)
    """
    z = jnp.asarray(z, dtype=cdtype())
    z = z[..., None, None]  # (..., 1, 1)

    a = destroy(dim)  # (n, n)
    a2 = a @ a
    return jax.scipy.linalg.expm(0.5 * (z.conj() * a2 - z * dag(a2)))


def quadrature(dim: int, phi: float) -> Array:
    r"""Returns the quadrature operator of phase angle $\phi$.

    It is defined by $x_\phi = (e^{i\phi} a^\dag + e^{-i\phi} a) / 2$, where $a$ and
    $a^\dag$ are the annihilation and creation operators respectively.

    Args:
        dim: Dimension of the Hilbert space.
        phi: Phase angle.

    Returns:
        _(array of shape (dim, dim))_ Quadrature operator.

    Examples:
        >>> dq.quadrature(3, 0.0)
        Array([[0.   +0.j, 0.5  +0.j, 0.   +0.j],
               [0.5  +0.j, 0.   +0.j, 0.707+0.j],
               [0.   +0.j, 0.707+0.j, 0.   +0.j]], dtype=complex64)
        >>> dq.quadrature(3, jnp.pi / 2)
        Array([[ 0.+0.j   , -0.-0.5j  ,  0.+0.j   ],
               [-0.+0.5j  ,  0.+0.j   , -0.-0.707j],
               [ 0.+0.j   , -0.+0.707j,  0.+0.j   ]], dtype=complex64)
    """
    a = destroy(dim)
    return 0.5 * (jnp.exp(1j * phi) * dag(a) + jnp.exp(-1j * phi) * a)


def position(dim: int) -> Array:
    r"""Returns the position operator $x = (a^\dag + a) / 2$.

    Args:
        dim: Dimension of the Hilbert space.

    Returns:
        _(array of shape (dim, dim))_ Position operator.

    Examples:
        >>> dq.position(3)
        Array([[0.   +0.j, 0.5  +0.j, 0.   +0.j],
               [0.5  +0.j, 0.   +0.j, 0.707+0.j],
               [0.   +0.j, 0.707+0.j, 0.   +0.j]], dtype=complex64)
    """
    a = destroy(dim)
    return 0.5 * (a + dag(a))


def momentum(dim: int) -> Array:
    r"""Returns the momentum operator $p = i (a^\dag - a) / 2$.

    Args:
        dim: Dimension of the Hilbert space.

    Returns:
        _(array of shape (dim, dim))_ Momentum operator.

    Examples:
        >>> dq.momentum(3)
        Array([[0.+0.j   , 0.-0.5j  , 0.+0.j   ],
               [0.+0.5j  , 0.+0.j   , 0.-0.707j],
               [0.+0.j   , 0.+0.707j, 0.+0.j   ]], dtype=complex64)
    """
    a = destroy(dim)
    return 0.5j * (dag(a) - a)


def sigmax() -> Array:
    r"""Returns the Pauli $\sigma_x$ operator.

    It is defined by $\sigma_x = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$.

    Returns:
        _(array of shape (2, 2))_ Pauli $\sigma_x$ operator.

    Examples:
        >>> dq.sigmax()
        Array([[0.+0.j, 1.+0.j],
               [1.+0.j, 0.+0.j]], dtype=complex64)
    """
    return jnp.array([[0, 1], [1, 0]], dtype=cdtype())


def sigmay() -> Array:
    r"""Returns the Pauli $\sigma_y$ operator.

    It is defined by $\sigma_y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}$.

    Returns:
        _(array of shape (2, 2))_ Pauli $\sigma_y$ operator.

    Examples:
        >>> dq.sigmay()
        Array([[ 0.+0.j, -0.-1.j],
               [ 0.+1.j,  0.+0.j]], dtype=complex64)
    """
    return jnp.array([[0, -1j], [1j, 0]], dtype=cdtype())


def sigmaz() -> Array:
    r"""Returns the Pauli $\sigma_z$ operator.

    It is defined by $\sigma_z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$.

    Returns:
        _(array of shape (2, 2))_ Pauli $\sigma_z$ operator.

    Examples:
        >>> dq.sigmaz()
        Array([[ 1.+0.j,  0.+0.j],
               [ 0.+0.j, -1.+0.j]], dtype=complex64)
    """
    return jnp.array([[1, 0], [0, -1]], dtype=cdtype())


def sigmap() -> Array:
    r"""Returns the Pauli raising operator $\sigma_+$.

    It is defined by $\sigma_+ = \begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}$.

    Returns:
        _(array of shape (2, 2))_ Pauli $\sigma_+$ operator.

    Examples:
        >>> dq.sigmap()
        Array([[0.+0.j, 1.+0.j],
               [0.+0.j, 0.+0.j]], dtype=complex64)
    """
    return jnp.array([[0, 1], [0, 0]], dtype=cdtype())


def sigmam() -> Array:
    r"""Returns the Pauli lowering operator $\sigma_-$.

    It is defined by $\sigma_- = \begin{pmatrix} 0 & 0 \\ 1 & 0 \end{pmatrix}$.

    Returns:
        _(array of shape (2, 2))_ Pauli $\sigma_-$ operator.

    Examples:
        >>> dq.sigmam()
        Array([[0.+0.j, 0.+0.j],
               [1.+0.j, 0.+0.j]], dtype=complex64)
    """
    return jnp.array([[0, 0], [1, 0]], dtype=cdtype())


def hadamard(n: int = 1) -> Array:
    r"""Returns the Hadamard transform on $n$ qubits.

    For a single qubit, it is defined by
    $$
        H = \frac{1}{\sqrt2} \begin{pmatrix}
            1 & 1 \\\\
            1 & -1
        \end{pmatrix}
    $$
    For $n$ qubits, it is defined by the tensor product of Hadamard matrices:
    $$
        H_n = \bigotimes_{k=1}^n H
    $$

    Args:
        n: Number of qubits to act on.

    Returns:
        _(array of shape (2^n, 2^n))_ Hadamard transform operator.

    Examples:
        >>> dq.hadamard()
        Array([[ 0.707+0.j,  0.707+0.j],
               [ 0.707+0.j, -0.707+0.j]], dtype=complex64)
        >>> dq.hadamard(2)
        Array([[ 0.5+0.j,  0.5+0.j,  0.5+0.j,  0.5+0.j],
               [ 0.5+0.j, -0.5+0.j,  0.5+0.j, -0.5+0.j],
               [ 0.5+0.j,  0.5+0.j, -0.5+0.j, -0.5+0.j],
               [ 0.5+0.j, -0.5+0.j, -0.5+0.j,  0.5-0.j]], dtype=complex64)
    """
    H1 = jnp.array([[1, 1], [1, -1]], dtype=cdtype()) / jnp.sqrt(2)
    Hs = jnp.broadcast_to(H1, (n, 2, 2))  # (n, 2, 2)
    return tensor(*Hs)


def rx(theta: ArrayLike) -> Array:
    r"""Returns the $R_x(\theta)$ rotation gate.

    It is defined by
    $$
        R_x(\theta) = \begin{pmatrix}
            \cos(\theta/2)   & -i\sin(\theta/2) \\\\
            -i\sin(\theta/2) & \cos(\theta/2)
        \end{pmatrix}
    $$

    Args:
        theta _(array_like of shape (...))_: Rotation angle $\theta$ in radians.

    Returns:
        _(array of shape (..., 2, 2))_ $R_x(\theta)$ gate.

    Examples:
        >>> dq.rx(jnp.pi)
        Array([[-0.+0.j,  0.-1.j],
               [ 0.-1.j, -0.+0.j]], dtype=complex64)
        >>> dq.rx([0, jnp.pi/4, jnp.pi/3, jnp.pi/2, jnp.pi]).shape
        (5, 2, 2)
    """
    theta = jnp.asarray(theta)
    c = jnp.cos(theta / 2)
    s = jnp.sin(theta / 2)
    rx = jnp.array([[c, -1j * s], [-1j * s, c]], dtype=cdtype())
    return jnp.moveaxis(rx, (0, 1), (-2, -1))


def ry(theta: ArrayLike) -> Array:
    r"""Returns the $R_y(\theta)$ rotation gate.

    It is defined by
    $$
        R_y(\theta) = \begin{pmatrix}
            \cos(\theta/2) & -\sin(\theta/2) \\\\
            \sin(\theta/2) & \cos(\theta/2)
        \end{pmatrix}
    $$

    Args:
        theta _(array_like of shape (...))_: Rotation angle $\theta$ in radians.

    Returns:
        _(array of shape (..., 2, 2))_ $R_y(\theta)$ gate.

    Examples:
        >>> dq.ry(jnp.pi)
        Array([[-0.+0.j, -1.+0.j],
               [ 1.+0.j, -0.+0.j]], dtype=complex64)
        >>> dq.ry([0, jnp.pi/4, jnp.pi/3, jnp.pi/2, jnp.pi]).shape
        (5, 2, 2)
    """
    theta = jnp.asarray(theta)
    c = jnp.cos(theta / 2)
    s = jnp.sin(theta / 2)
    ry = jnp.array([[c, -s], [s, c]], dtype=cdtype())
    return jnp.moveaxis(ry, (0, 1), (-2, -1))


def rz(theta: ArrayLike) -> Array:
    r"""Returns the $R_z(\theta)$ rotation gate.

    It is defined by
    $$
        R_z(\theta) = \begin{pmatrix}
            e^{-i\theta/2} & 0 \\\\
            0              & e^{i\theta/2}
        \end{pmatrix}
    $$

    Args:
        theta _(array_like of shape (...))_: Rotation angle $\theta$ in radians.

    Returns:
        _(array of shape (..., 2, 2))_ $R_z(\theta)$ gate.

    Examples:
        >>> dq.rz(jnp.pi)
        Array([[-0.-1.j,  0.+0.j],
               [ 0.+0.j, -0.+1.j]], dtype=complex64)
        >>> dq.rz([0, jnp.pi/4, jnp.pi/3, jnp.pi/2, jnp.pi]).shape
        (5, 2, 2)
    """
    theta = jnp.asarray(theta)
    zero = jnp.zeros_like(theta)
    rz = jnp.array(
        [[jnp.exp(-1j * theta / 2), zero], [zero, jnp.exp(1j * theta / 2)]],
        dtype=cdtype(),
    )
    return jnp.moveaxis(rz, (0, 1), (-2, -1))


def sgate() -> Array:
    r"""Returns the $\text{S}$ gate.

    It is defined by $\text{S} = \begin{pmatrix} 1 & 0 \\ 0 & i \end{pmatrix}$.

    Returns:
        _(array of shape (2, 2))_ $\text{S}$ gate.

    Examples:
        >>> dq.sgate()
        Array([[1.+0.j, 0.+0.j],
               [0.+0.j, 0.+1.j]], dtype=complex64)
    """
    return jnp.array([[1, 0], [0, 1j]], dtype=cdtype())


def tgate() -> Array:
    r"""Returns the $\text{T}$ gate.

    It is defined by
    $\text{T} = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\frac{\pi}{4}} \end{pmatrix}$.

    Returns:
        _(array of shape (2, 2))_ $\text{T}$ gate.

    Examples:
        >>> dq.tgate()
        Array([[1.   +0.j   , 0.   +0.j   ],
               [0.   +0.j   , 0.707+0.707j]], dtype=complex64)
    """
    return jnp.array([[1, 0], [0, (1 + 1j) / jnp.sqrt(2)]], dtype=cdtype())


def cnot() -> Array:
    r"""Returns the $\text{CNOT}$ gate.

    It is defined by
    $$
        \text{CNOT} = \begin{pmatrix}
            1 & 0 & 0 & 0 \\\\
            0 & 1 & 0 & 0 \\\\
            0 & 0 & 0 & 1 \\\\
            0 & 0 & 1 & 0
        \end{pmatrix}
    $$

    Returns:
        _(array of shape (4, 4))_ $\text{CNOT}$ gate.

    Examples:
        >>> dq.cnot()
        Array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j],
               [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j]], dtype=complex64)
    """
    return jnp.array(
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=cdtype()
    )


def toffoli() -> Array:
    r"""Returns the $\text{Toffoli}$ gate.

    It is defined by
    $$
        \text{Toffoli} = \begin{pmatrix}
            1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\\\
            0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\\\
            0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\\\
            0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\\\
            0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\\\
            0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\\\
            0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 \\\\
            0 & 0 & 0 & 0 & 0 & 0 & 1 & 0
        \end{pmatrix}
    $$

    Returns:
        _(array of shape (8, 8))_ $\text{Toffoli}$ gate.

    Examples:
        >>> dq.toffoli()
        Array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j],
               [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j]],      dtype=complex64)
    """  # noqa: E501
    return jnp.array(
        [
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 0],
        ],
        dtype=cdtype(),
    )
