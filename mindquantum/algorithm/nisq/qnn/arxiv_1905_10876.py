# Copyright 2023 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""These ansatz are adpot from arxiv 1906 10876."""
# pylint: disable=too-few-public-methods
from mindquantum.algorithm.nisq._ansatz import Ansatz, single_qubit_gate_layer
from mindquantum.core.circuit import UN
from mindquantum.core.gates import BARRIER, RX, RY, RZ, H, X, Z
from mindquantum.core.parameterresolver import PRGenerator
from mindquantum.utils.type_value_check import (
    _check_input_type,
    _check_int_type,
    _check_value_should_not_less,
)


class Initializer:
    """
    Initialize parameters for ansatz.

    Args:
        n_qubits (int): total qubits number of this ansatz.
        depth (int): depth of ansatz.
        prefix (str): prefix of parameters. Default: ``''``.
        subfix (str): subfix of parameters. Default: ``''``.
    """

    def __init__(self, n_qubits: int, depth: int, prefix: str = '', subfix: str = ''):
        """Initialize parameters."""
        _check_int_type('n_qubits', n_qubits)
        _check_value_should_not_less('n_qubits', 0, n_qubits)
        _check_value_should_not_less('depth', 1, depth)
        _check_int_type('depth', depth)
        _check_input_type('prefix', str, prefix)
        self.n_qubits = n_qubits
        self.depth = depth
        self.pr_gen = PRGenerator(prefix, subfix)


class Ansatz1(Ansatz, Initializer):
    """
    Ansatz 1 implement from arxiv paper.

    Please refers to `Expressibility and entangling capability of parameterized quantum circuits for hybrid
    quantum-classical algorithms <https://arxiv.org/abs/1905.10876>`_.

    Args:
        n_qubits (int): total qubits number of this ansatz.
        depth (int): depth of ansatz.
        prefix (str): prefix of parameters. Default: ``''``.
        subfix (str): subfix of parameters. Default: ``''``.

    Examples:
        >>> from mindquantum.algorithm.nisq import Ansatz1
        >>> Ansatz1(3, 2).circuit
        q0: ──RX(p0)────RZ(p1)─────RX(p6)─────RZ(p7)──
        q1: ──RX(p2)────RZ(p3)─────RX(p8)─────RZ(p9)──
        q2: ──RX(p4)────RZ(p5)────RX(p10)────RZ(p11)──
    """

    def __init__(self, n_qubits: int, depth: int, prefix: str = '', subfix: str = ''):
        """Construct ansatz."""
        Initializer.__init__(self, n_qubits, depth, prefix, subfix)
        Ansatz.__init__(self, 'Ansatz1', n_qubits, depth)

    def _implement(self, depth):  # pylint: disable=arguments-differ
        """Implement of ansatz 1."""
        for _ in range(depth):
            self._circuit += single_qubit_gate_layer(RX, self.n_qubits, pr_gen=self.pr_gen)
            self._circuit += single_qubit_gate_layer(RZ, self.n_qubits, pr_gen=self.pr_gen)
            self._circuit += BARRIER


class Ansatz2(Ansatz, Initializer):
    """
    Ansatz 2 implement from arxiv paper.

    Please refers to `Expressibility and entangling capability of parameterized quantum circuits for hybrid
    quantum-classical algorithms <https://arxiv.org/abs/1905.10876>`_.

    Args:
        n_qubits (int): total qubits number of this ansatz.
        depth (int): depth of ansatz.
        prefix (str): prefix of parameters. Default: ``''``.
        subfix (str): subfix of parameters. Default: ``''``.

    Examples:
        >>> from mindquantum.algorithm.nisq import Ansatz2
        >>> Ansatz2(3, 2).circuit
        q0: ──RX(p0)────RZ(p1)─────────X─────RX(p6)─────RZ(p7)─────────X──
                                       │                               │
        q1: ──RX(p2)────RZ(p3)────X────●─────RX(p8)─────RZ(p9)────X────●──
                                  │                               │
        q2: ──RX(p4)────RZ(p5)────●─────────RX(p10)────RZ(p11)────●───────
    """

    def __init__(self, n_qubits: int, depth: int, prefix: str = '', subfix: str = ''):
        """Construct ansatz."""
        Initializer.__init__(self, n_qubits, depth, prefix, subfix)
        Ansatz.__init__(self, 'Ansatz2', n_qubits, depth)

    def _implement(self, depth):  # pylint: disable=arguments-differ
        """Implement of ansatz 2."""
        for _ in range(depth):
            self._circuit += single_qubit_gate_layer(RX, self.n_qubits, pr_gen=self.pr_gen)
            self._circuit += single_qubit_gate_layer(RZ, self.n_qubits, pr_gen=self.pr_gen)
            for i in range(self.n_qubits - 1):
                self._circuit += X.on(self.n_qubits - 2 - i, self.n_qubits - 1 - i)
            self._circuit += BARRIER


class Ansatz3(Ansatz, Initializer):
    """
    Ansatz 3 implement from arxiv paper.

    Please refers to `Expressibility and entangling capability of parameterized quantum circuits for hybrid
    quantum-classical algorithms <https://arxiv.org/abs/1905.10876>`_.

    Args:
        n_qubits (int): total qubits number of this ansatz.
        depth (int): depth of ansatz.
        prefix (str): prefix of parameters. Default: ``''``.
        subfix (str): subfix of parameters. Default: ``''``.

    Examples:
        >>> from mindquantum.algorithm.nisq import Ansatz3
        >>> Ansatz3(3, 1).circuit
        q0: ──RX(p0)────RZ(p1)──────────────RZ(p7)──
                                              │
        q1: ──RX(p2)────RZ(p3)────RZ(p6)──────●─────
                                    │
        q2: ──RX(p4)────RZ(p5)──────●───────────────
    """

    def __init__(self, n_qubits: int, depth: int, prefix: str = '', subfix: str = ''):
        """Construct ansatz."""
        Initializer.__init__(self, n_qubits, depth, prefix, subfix)
        Ansatz.__init__(self, 'Ansatz3', n_qubits, depth)

    def _implement(self, depth):  # pylint: disable=arguments-differ
        """Implement of ansatz 3."""
        for _ in range(depth):
            self._circuit += single_qubit_gate_layer(RX, self.n_qubits, pr_gen=self.pr_gen)
            self._circuit += single_qubit_gate_layer(RZ, self.n_qubits, pr_gen=self.pr_gen)
            for i in range(self.n_qubits - 1):
                self._circuit += RZ(self.pr_gen.new()).on(self.n_qubits - 2 - i, self.n_qubits - 1 - i)
            self._circuit += BARRIER


class Ansatz4(Ansatz, Initializer):
    """
    Ansatz 4 implement from arxiv paper.

    Please refers to `Expressibility and entangling capability of parameterized quantum circuits for hybrid
    quantum-classical algorithms <https://arxiv.org/abs/1905.10876>`_.

    Args:
        n_qubits (int): total qubits number of this ansatz.
        depth (int): depth of ansatz.
        prefix (str): prefix of parameters. Default: ``''``.
        subfix (str): subfix of parameters. Default: ``''``.

    Examples:
        >>> from mindquantum.algorithm.nisq import Ansatz4
        >>> Ansatz4(3, 1).circuit
        q0: ──RX(p0)────RZ(p1)──────────────RX(p7)──
                                              │
        q1: ──RX(p2)────RZ(p3)────RX(p6)──────●─────
                                    │
        q2: ──RX(p4)────RZ(p5)──────●───────────────
    """

    def __init__(self, n_qubits: int, depth: int, prefix: str = '', subfix: str = ''):
        """Construct ansatz."""
        Initializer.__init__(self, n_qubits, depth, prefix, subfix)
        Ansatz.__init__(self, 'Ansatz4', n_qubits, depth)

    def _implement(self, depth):  # pylint: disable=arguments-differ
        """Implement of ansatz 4."""
        for _ in range(depth):
            self._circuit += single_qubit_gate_layer(RX, self.n_qubits, pr_gen=self.pr_gen)
            self._circuit += single_qubit_gate_layer(RZ, self.n_qubits, pr_gen=self.pr_gen)
            for i in range(self.n_qubits - 1):
                self._circuit += RX(self.pr_gen.new()).on(self.n_qubits - 2 - i, self.n_qubits - 1 - i)
            self._circuit += BARRIER


class Ansatz5(Ansatz, Initializer):
    """
    Ansatz 5 implement from arxiv paper.

    Please refers to `Expressibility and entangling capability of parameterized quantum circuits for hybrid
    quantum-classical algorithms <https://arxiv.org/abs/1905.10876>`_.

    Args:
        n_qubits (int): total qubits number of this ansatz.
        depth (int): depth of ansatz.
        prefix (str): prefix of parameters. Default: ``''``.
        subfix (str): subfix of parameters. Default: ``''``.

    Examples:
        >>> from mindquantum.algorithm.nisq import Ansatz5
        >>> Ansatz5(3, 1).circuit
        q0: ──RX(p0)────RZ(p3)──────────────RZ(p7)──────────────RZ(p9)───────●──────────●───────RX(p12)────RZ(p15)──
                                              │                   │          │          │
        q1: ──RX(p1)────RZ(p4)────RZ(p6)──────┼─────────●─────────●──────────┼───────RZ(p11)────RX(p13)────RZ(p16)──
                                    │         │         │                    │
        q2: ──RX(p2)────RZ(p5)──────●─────────●───────RZ(p8)──────────────RZ(p10)───────────────RX(p14)────RZ(p17)──
    """

    def __init__(self, n_qubits: int, depth: int, prefix: str = '', subfix: str = ''):
        """Construct ansatz."""
        Initializer.__init__(self, n_qubits, depth, prefix, subfix)
        Ansatz.__init__(self, 'Ansatz5', n_qubits, depth)

    def _implement(self, depth):  # pylint: disable=arguments-differ
        """Implement of ansatz 5."""
        for _ in range(depth):
            self._circuit += single_qubit_gate_layer(RX, self.n_qubits, pr_gen=self.pr_gen)
            self._circuit += single_qubit_gate_layer(RZ, self.n_qubits, pr_gen=self.pr_gen)
            for ctrl in range(self.n_qubits)[::-1]:
                for obj in range(self.n_qubits)[::-1]:
                    if obj != ctrl:
                        self._circuit += RZ(self.pr_gen.new()).on(obj, ctrl)
            self._circuit += BARRIER
            self._circuit += single_qubit_gate_layer(RX, self.n_qubits, pr_gen=self.pr_gen)
            self._circuit += single_qubit_gate_layer(RZ, self.n_qubits, pr_gen=self.pr_gen)
            self._circuit += BARRIER


class Ansatz6(Ansatz, Initializer):
    """
    Ansatz 6 implement from arxiv paper.

    Please refers to `Expressibility and entangling capability of parameterized quantum circuits for hybrid
    quantum-classical algorithms <https://arxiv.org/abs/1905.10876>`_.

    Args:
        n_qubits (int): total qubits number of this ansatz.
        depth (int): depth of ansatz.
        prefix (str): prefix of parameters. Default: ``''``.
        subfix (str): subfix of parameters. Default: ``''``.

    Examples:
        >>> from mindquantum.algorithm.nisq import Ansatz6
        >>> Ansatz6(3, 1).circuit
        q0: ──RX(p0)────RZ(p3)──────────────RX(p7)──────────────RX(p9)───────●──────────●───────RX(p12)────RZ(p15)──
                                              │                   │          │          │
        q1: ──RX(p1)────RZ(p4)────RX(p6)──────┼─────────●─────────●──────────┼───────RX(p11)────RX(p13)────RZ(p16)──
                                    │         │         │                    │
        q2: ──RX(p2)────RZ(p5)──────●─────────●───────RX(p8)──────────────RX(p10)───────────────RX(p14)────RZ(p17)──
    """

    def __init__(self, n_qubits: int, depth: int, prefix: str = '', subfix: str = ''):
        """Construct ansatz."""
        Initializer.__init__(self, n_qubits, depth, prefix, subfix)
        Ansatz.__init__(self, 'Ansatz6', n_qubits, depth)

    def _implement(self, depth):  # pylint: disable=arguments-differ
        """Implement of ansatz 6."""
        for _ in range(depth):
            self._circuit += single_qubit_gate_layer(RX, self.n_qubits, pr_gen=self.pr_gen)
            self._circuit += single_qubit_gate_layer(RZ, self.n_qubits, pr_gen=self.pr_gen)
            for ctrl in range(self.n_qubits)[::-1]:
                for obj in range(self.n_qubits)[::-1]:
                    if obj != ctrl:
                        self._circuit += RX(self.pr_gen.new()).on(obj, ctrl)
            self._circuit += BARRIER
            self._circuit += single_qubit_gate_layer(RX, self.n_qubits, pr_gen=self.pr_gen)
            self._circuit += single_qubit_gate_layer(RZ, self.n_qubits, pr_gen=self.pr_gen)
            self._circuit += BARRIER


class Ansatz7(Ansatz, Initializer):
    """
    Ansatz 7 implement from arxiv paper.

    Please refers to `Expressibility and entangling capability of parameterized quantum circuits for hybrid
    quantum-classical algorithms <https://arxiv.org/abs/1905.10876>`_.

    Args:
        n_qubits (int): total qubits number of this ansatz.
        depth (int): depth of ansatz.
        prefix (str): prefix of parameters. Default: ``''``.
        subfix (str): subfix of parameters. Default: ``''``.

    Examples:
        >>> from mindquantum.algorithm.nisq import Ansatz7
        >>> Ansatz7(4, 1).circuit
        q0: ──RX(p0)────RZ(p4)────RZ(p8)────RX(p10)────RZ(p14)─────────────
                                    │
        q1: ──RX(p1)────RZ(p5)──────●───────RX(p11)────RZ(p15)────RZ(p18)──
                                                                     │
        q2: ──RX(p2)────RZ(p6)────RZ(p9)────RX(p12)────RZ(p16)───────●─────
                                    │
        q3: ──RX(p3)────RZ(p7)──────●───────RX(p13)────RZ(p17)─────────────
    """

    def __init__(self, n_qubits: int, depth: int, prefix: str = '', subfix: str = ''):
        """Construct ansatz."""
        Initializer.__init__(self, n_qubits, depth, prefix, subfix)
        Ansatz.__init__(self, 'Ansatz7', n_qubits, depth)

    def _implement(self, depth):  # pylint: disable=arguments-differ
        """Implement of ansatz 7."""
        for _ in range(depth):
            self._circuit += single_qubit_gate_layer(RX, self.n_qubits, pr_gen=self.pr_gen)
            self._circuit += single_qubit_gate_layer(RZ, self.n_qubits, pr_gen=self.pr_gen)
            start = 0
            for i in range(start, self.n_qubits, 2):
                obj = i
                ctrl = obj + 1
                if ctrl >= self.n_qubits:
                    continue
                self._circuit += RZ(self.pr_gen.new()).on(obj, ctrl)
            self._circuit += BARRIER
            self._circuit += single_qubit_gate_layer(RX, self.n_qubits, pr_gen=self.pr_gen)
            self._circuit += single_qubit_gate_layer(RZ, self.n_qubits, pr_gen=self.pr_gen)
            start = 1
            for i in range(start, self.n_qubits, 2):
                obj = i
                ctrl = obj + 1
                if ctrl >= self.n_qubits:
                    continue
                self._circuit += RZ(self.pr_gen.new()).on(obj, ctrl)
            self._circuit += BARRIER


class Ansatz8(Ansatz, Initializer):
    """
    Ansatz 8 implement from arxiv paper.

    Please refers to `Expressibility and entangling capability of parameterized quantum circuits for hybrid
    quantum-classical algorithms <https://arxiv.org/abs/1905.10876>`_.

    Args:
        n_qubits (int): total qubits number of this ansatz.
        depth (int): depth of ansatz.
        prefix (str): prefix of parameters. Default: ``''``.
        subfix (str): subfix of parameters. Default: ``''``.

    Examples:
        >>> from mindquantum.algorithm.nisq import Ansatz8
        >>> Ansatz8(4, 1).circuit
        q0: ──RX(p0)────RZ(p1)────RX(p8)────RX(p10)────RZ(p11)─────────────
                                    │
        q1: ──RX(p2)────RZ(p3)──────●───────RX(p12)────RZ(p13)────RX(p18)──
                                                                     │
        q2: ──RX(p4)────RZ(p5)────RX(p9)────RX(p14)────RZ(p15)───────●─────
                                    │
        q3: ──RX(p6)────RZ(p7)──────●───────RX(p16)────RZ(p17)─────────────
    """

    def __init__(self, n_qubits: int, depth: int, prefix: str = '', subfix: str = ''):
        """Construct ansatz."""
        Initializer.__init__(self, n_qubits, depth, prefix, subfix)
        Ansatz.__init__(self, 'Ansatz8', n_qubits, depth)

    def _implement(self, depth):  # pylint: disable=arguments-differ
        """Implement of ansatz 8."""
        for _ in range(depth):
            self._circuit += single_qubit_gate_layer(RX, self.n_qubits, pr_gen=self.pr_gen)
            self._circuit += single_qubit_gate_layer(RZ, self.n_qubits, pr_gen=self.pr_gen)
            start = 0
            for i in range(start, self.n_qubits, 2):
                obj = i
                ctrl = obj + 1
                if ctrl >= self.n_qubits:
                    continue
                self._circuit += RX(self.pr_gen.new()).on(obj, ctrl)
            self._circuit += BARRIER
            self._circuit += single_qubit_gate_layer(RX, self.n_qubits, pr_gen=self.pr_gen)
            self._circuit += single_qubit_gate_layer(RZ, self.n_qubits, pr_gen=self.pr_gen)
            start = 1
            for i in range(start, self.n_qubits, 2):
                obj = i
                ctrl = obj + 1
                if ctrl >= self.n_qubits:
                    continue
                self._circuit += RX(self.pr_gen.new()).on(obj, ctrl)
            self._circuit += BARRIER


class Ansatz9(Ansatz, Initializer):
    """
    Ansatz 9 implement from arxiv paper.

    Please refers to `Expressibility and entangling capability of parameterized quantum circuits for hybrid
    quantum-classical algorithms <https://arxiv.org/abs/1905.10876>`_.

    Args:
        n_qubits (int): total qubits number of this ansatz.
        depth (int): depth of ansatz.
        prefix (str): prefix of parameters. Default: ``''``.
        subfix (str): subfix of parameters. Default: ``''``.

    Examples:
        >>> from mindquantum.algorithm.nisq import Ansatz9
        >>> Ansatz9(4, 2).circuit
        q0: ──H──────────────Z────RX(p0)────H──────────────Z────RX(p4)──
                             │                             │
        q1: ──H─────────Z────●────RX(p1)────H─────────Z────●────RX(p5)──
                        │                             │
        q2: ──H────Z────●─────────RX(p2)────H────Z────●─────────RX(p6)──
                   │                             │
        q3: ──H────●──────────────RX(p3)────H────●──────────────RX(p7)──
    """

    def __init__(self, n_qubits: int, depth: int, prefix: str = '', subfix: str = ''):
        """Construct ansatz."""
        Initializer.__init__(self, n_qubits, depth, prefix, subfix)
        Ansatz.__init__(self, 'Ansatz9', n_qubits, depth)

    def _implement(self, depth):  # pylint: disable=arguments-differ
        """Implement of ansatz 9."""
        for _ in range(depth):
            self._circuit += UN(H, self.n_qubits)
            for i in range(self.n_qubits - 1)[::-1]:
                self._circuit += Z.on(i, i + 1)
            self._circuit += BARRIER
            self._circuit += single_qubit_gate_layer(RX, self.n_qubits, pr_gen=self.pr_gen)
            self._circuit += BARRIER


class Ansatz10(Ansatz, Initializer):
    """
    Ansatz 10 implement from arxiv paper.

    Please refers to `Expressibility and entangling capability of parameterized quantum circuits for hybrid
    quantum-classical algorithms <https://arxiv.org/abs/1905.10876>`_.

    Args:
        n_qubits (int): total qubits number of this ansatz.
        depth (int): depth of ansatz.
        prefix (str): prefix of parameters. Default: ``''``.
        subfix (str): subfix of parameters. Default: ``''``.

    Examples:
        >>> from mindquantum.algorithm.nisq import Ansatz10
        >>> Ansatz10(4, 2).circuit
        q0: ──RY(p0)──────────────●────Z────RY(p4)──────────────●────Z─────RY(p8)──
                                  │    │                        │    │
        q1: ──RY(p1)─────────●────Z────┼────RY(p5)─────────●────Z────┼─────RY(p9)──
                             │         │                   │         │
        q2: ──RY(p2)────●────Z─────────┼────RY(p6)────●────Z─────────┼────RY(p10)──
                        │              │              │              │
        q3: ──RY(p3)────Z──────────────●────RY(p7)────Z──────────────●────RY(p11)──
    """

    def __init__(self, n_qubits: int, depth: int, prefix: str = '', subfix: str = ''):
        """Construct ansatz."""
        Initializer.__init__(self, n_qubits, depth, prefix, subfix)
        Ansatz.__init__(self, 'Ansatz10', n_qubits, depth)

    def _implement(self, depth):  # pylint: disable=arguments-differ
        """Implement of ansatz 10."""
        self._circuit += single_qubit_gate_layer(RY, self.n_qubits, pr_gen=self.pr_gen)
        for _ in range(depth):
            for i in range(self.n_qubits)[::-1]:
                if self.n_qubits != 1:
                    self._circuit += Z.on(i, (i - 1) % self.n_qubits)
            self._circuit += BARRIER
            self._circuit += single_qubit_gate_layer(RY, self.n_qubits, pr_gen=self.pr_gen)
            self._circuit += BARRIER


class Ansatz11(Ansatz, Initializer):
    """
    Ansatz 11 implement from arxiv paper.

    Please refers to `Expressibility and entangling capability of parameterized quantum circuits for hybrid
    quantum-classical algorithms <https://arxiv.org/abs/1905.10876>`_.

    Args:
        n_qubits (int): total qubits number of this ansatz.
        depth (int): depth of ansatz.
        prefix (str): prefix of parameters. Default: ``''``.
        subfix (str): subfix of parameters. Default: ``''``.

    Examples:
        >>> from mindquantum.algorithm.nisq import Ansatz11
        >>> Ansatz11(4, 1).circuit
        q0: ──RY(p0)────RZ(p1)────X─────────────────────────────
                                  │
        q1: ──RY(p2)────RZ(p3)────●─────RY(p8)─────RZ(p9)────X──
                                                             │
        q2: ──RY(p4)────RZ(p5)────X────RY(p10)────RZ(p11)────●──
                                  │
        q3: ──RY(p6)────RZ(p7)────●─────────────────────────────
    """

    def __init__(self, n_qubits: int, depth: int, prefix: str = '', subfix: str = ''):
        """Construct ansatz."""
        Initializer.__init__(self, n_qubits, depth, prefix, subfix)
        Ansatz.__init__(self, 'Ansatz11', n_qubits, depth)

    def _implement(self, depth):  # pylint: disable=arguments-differ
        """Implement of ansatz 11."""
        for _ in range(depth):
            self._circuit += single_qubit_gate_layer(RY, self.n_qubits, pr_gen=self.pr_gen)
            self._circuit += single_qubit_gate_layer(RZ, self.n_qubits, pr_gen=self.pr_gen)
            start = 0
            for i in range(start, self.n_qubits, 2):
                obj = i
                ctrl = obj + 1
                if ctrl >= self.n_qubits:
                    continue
                self._circuit += X.on(obj, ctrl)
            self._circuit += BARRIER
            self._circuit += single_qubit_gate_layer(RY, 1, self.n_qubits - 1, pr_gen=self.pr_gen)
            self._circuit += single_qubit_gate_layer(RZ, 1, self.n_qubits - 1, pr_gen=self.pr_gen)
            start = 1
            for i in range(start, self.n_qubits, 2):
                obj = i
                ctrl = obj + 1
                if ctrl >= self.n_qubits:
                    continue
                self._circuit += X.on(obj, ctrl)
            self._circuit += BARRIER


class Ansatz12(Ansatz, Initializer):
    """
    Ansatz 12 implement from arxiv paper.

    Please refers to `Expressibility and entangling capability of parameterized quantum circuits for hybrid
    quantum-classical algorithms <https://arxiv.org/abs/1905.10876>`_.

    Args:
        n_qubits (int): total qubits number of this ansatz.
        depth (int): depth of ansatz.
        prefix (str): prefix of parameters. Default: ``''``.
        subfix (str): subfix of parameters. Default: ``''``.

    Examples:
        >>> from mindquantum.algorithm.nisq import Ansatz12
        >>> Ansatz12(4, 1).circuit
        q0: ──RY(p0)────RZ(p1)────Z─────────────────────────────
                                  │
        q1: ──RY(p2)────RZ(p3)────●─────RY(p8)─────RZ(p9)────Z──
                                                             │
        q2: ──RY(p4)────RZ(p5)────Z────RY(p10)────RZ(p11)────●──
                                  │
        q3: ──RY(p6)────RZ(p7)────●─────────────────────────────
    """

    def __init__(self, n_qubits: int, depth: int, prefix: str = '', subfix: str = ''):
        """Construct ansatz."""
        Initializer.__init__(self, n_qubits, depth, prefix, subfix)
        Ansatz.__init__(self, 'Ansatz12', n_qubits, depth)

    def _implement(self, depth):  # pylint: disable=arguments-differ
        """Implement of ansatz 12."""
        for _ in range(depth):
            self._circuit += single_qubit_gate_layer(RY, self.n_qubits, pr_gen=self.pr_gen)
            self._circuit += single_qubit_gate_layer(RZ, self.n_qubits, pr_gen=self.pr_gen)
            start = 0
            for i in range(start, self.n_qubits, 2):
                obj = i
                ctrl = obj + 1
                if ctrl >= self.n_qubits:
                    continue
                self._circuit += Z.on(obj, ctrl)
            self._circuit += BARRIER
            self._circuit += single_qubit_gate_layer(RY, 1, self.n_qubits - 1, pr_gen=self.pr_gen)
            self._circuit += single_qubit_gate_layer(RZ, 1, self.n_qubits - 1, pr_gen=self.pr_gen)
            start = 1
            for i in range(start, self.n_qubits, 2):
                obj = i
                ctrl = obj + 1
                if ctrl >= self.n_qubits:
                    continue
                self._circuit += Z.on(obj, ctrl)
            self._circuit += BARRIER


class Ansatz13(Ansatz, Initializer):
    """
    Ansatz 13 implement from arxiv paper.

    Please refers to `Expressibility and entangling capability of parameterized quantum circuits for hybrid
    quantum-classical algorithms <https://arxiv.org/abs/1905.10876>`_.

    Args:
        n_qubits (int): total qubits number of this ansatz.
        depth (int): depth of ansatz.
        prefix (str): prefix of parameters. Default: ``''``.
        subfix (str): subfix of parameters. Default: ``''``.

    Examples:
        >>> from mindquantum.algorithm.nisq import Ansatz13
        >>> Ansatz13(4, 1).circuit
        q0: ──RY(p0)────RZ(p4)──────────────────────────●────────RY(p8)──────────────────●───────RZ(p14)─────────────
                          │                             │                                │          │
        q1: ──RY(p1)──────┼───────────────────●───────RZ(p7)─────RY(p9)──────────────────┼──────────●───────RZ(p15)──
                          │                   │                                          │                     │
        q2: ──RY(p2)──────┼─────────●───────RZ(p6)──────────────RY(p10)────RZ(p12)───────┼─────────────────────●─────
                          │         │                                         │          │
        q3: ──RY(p3)──────●───────RZ(p5)────────────────────────RY(p11)───────●───────RZ(p13)────────────────────────
    """

    def __init__(self, n_qubits: int, depth: int, prefix: str = '', subfix: str = ''):
        """Construct ansatz."""
        Initializer.__init__(self, n_qubits, depth, prefix, subfix)
        Ansatz.__init__(self, 'Ansatz13', n_qubits, depth)

    def _implement(self, depth):  # pylint: disable=arguments-differ
        """Implement of ansatz 13."""
        for _ in range(depth):
            self._circuit += single_qubit_gate_layer(RY, self.n_qubits, pr_gen=self.pr_gen)
            for ctrl in range(self.n_qubits)[::-1]:
                obj = (ctrl + 1) % self.n_qubits
                if obj != ctrl:
                    self._circuit += RZ(self.pr_gen.new()).on(obj, ctrl)
            self._circuit += BARRIER
            self._circuit += single_qubit_gate_layer(RY, self.n_qubits, pr_gen=self.pr_gen)
            for idx in range(self.n_qubits - 1, 2 * self.n_qubits - 1):
                ctrl = idx % self.n_qubits
                obj = (ctrl - 1) % self.n_qubits
                if obj != ctrl:
                    self._circuit += RZ(self.pr_gen.new()).on(obj, ctrl)
            self._circuit += BARRIER


class Ansatz14(Ansatz, Initializer):
    """
    Ansatz 14 implement from arxiv paper.

    Please refers to `Expressibility and entangling capability of parameterized quantum circuits for hybrid
    quantum-classical algorithms <https://arxiv.org/abs/1905.10876>`_.

    Args:
        n_qubits (int): total qubits number of this ansatz.
        depth (int): depth of ansatz.
        prefix (str): prefix of parameters. Default: ``''``.
        subfix (str): subfix of parameters. Default: ``''``.

    Examples:
        >>> from mindquantum.algorithm.nisq import Ansatz14
        >>> Ansatz14(4, 1).circuit
        q0: ──RY(p0)────RX(p4)──────────────────────────●────────RY(p8)──────────────────●───────RX(p14)─────────────
                          │                             │                                │          │
        q1: ──RY(p1)──────┼───────────────────●───────RX(p7)─────RY(p9)──────────────────┼──────────●───────RX(p15)──
                          │                   │                                          │                     │
        q2: ──RY(p2)──────┼─────────●───────RX(p6)──────────────RY(p10)────RX(p12)───────┼─────────────────────●─────
                          │         │                                         │          │
        q3: ──RY(p3)──────●───────RX(p5)────────────────────────RY(p11)───────●───────RX(p13)────────────────────────
    """

    def __init__(self, n_qubits: int, depth: int, prefix: str = '', subfix: str = ''):
        """Construct ansatz."""
        Initializer.__init__(self, n_qubits, depth, prefix, subfix)
        Ansatz.__init__(self, 'Ansatz14', n_qubits, depth)

    def _implement(self, depth):  # pylint: disable=arguments-differ
        """Implement of ansatz 14."""
        for _ in range(depth):
            self._circuit += single_qubit_gate_layer(RY, self.n_qubits, pr_gen=self.pr_gen)
            for ctrl in range(self.n_qubits)[::-1]:
                obj = (ctrl + 1) % self.n_qubits
                if obj != ctrl:
                    self._circuit += RX(self.pr_gen.new()).on(obj, ctrl)
            self._circuit += BARRIER
            self._circuit += single_qubit_gate_layer(RY, self.n_qubits, pr_gen=self.pr_gen)
            for idx in range(self.n_qubits - 1, 2 * self.n_qubits - 1):
                ctrl = idx % self.n_qubits
                obj = (ctrl - 1) % self.n_qubits
                if obj != ctrl:
                    self._circuit += RX(self.pr_gen.new()).on(obj, ctrl)
            self._circuit += BARRIER


class Ansatz15(Ansatz, Initializer):
    """
    Ansatz 15 implement from arxiv paper.

    Please refers to `Expressibility and entangling capability of parameterized quantum circuits for hybrid
    quantum-classical algorithms <https://arxiv.org/abs/1905.10876>`_.

    Args:
        n_qubits (int): total qubits number of this ansatz.
        depth (int): depth of ansatz.
        prefix (str): prefix of parameters. Default: ``''``.
        subfix (str): subfix of parameters. Default: ``''``.

    Examples:
        >>> from mindquantum.algorithm.nisq import Ansatz15
        >>> Ansatz15(4, 1).circuit
        q0: ──RY(p0)────X──────────────●────RY(p4)─────────●────X───────
                        │              │                   │    │
        q1: ──RY(p1)────┼─────────●────X────RY(p5)─────────┼────●────X──
                        │         │                        │         │
        q2: ──RY(p2)────┼────●────X─────────RY(p6)────X────┼─────────●──
                        │    │                        │    │
        q3: ──RY(p3)────●────X──────────────RY(p7)────●────X────────────
    """

    def __init__(self, n_qubits: int, depth: int, prefix: str = '', subfix: str = ''):
        """Construct ansatz."""
        Initializer.__init__(self, n_qubits, depth, prefix, subfix)
        Ansatz.__init__(self, 'Ansatz15', n_qubits, depth)

    def _implement(self, depth):  # pylint: disable=arguments-differ
        """Implement of ansatz 15."""
        for _ in range(depth):
            self._circuit += single_qubit_gate_layer(RY, self.n_qubits, pr_gen=self.pr_gen)
            for ctrl in range(self.n_qubits)[::-1]:
                obj = (ctrl + 1) % self.n_qubits
                if obj != ctrl:
                    self._circuit += X.on(obj, ctrl)
            self._circuit += BARRIER
            self._circuit += single_qubit_gate_layer(RY, self.n_qubits, pr_gen=self.pr_gen)
            for idx in range(self.n_qubits - 1, 2 * self.n_qubits - 1):
                ctrl = idx % self.n_qubits
                obj = (ctrl - 1) % self.n_qubits
                if obj != ctrl:
                    self._circuit += X.on(obj, ctrl)
            self._circuit += BARRIER


class Ansatz16(Ansatz, Initializer):
    """
    Ansatz 16 implement from arxiv paper.

    Please refers to `Expressibility and entangling capability of parameterized quantum circuits for hybrid
    quantum-classical algorithms <https://arxiv.org/abs/1905.10876>`_.

    Args:
        n_qubits (int): total qubits number of this ansatz.
        depth (int): depth of ansatz.
        prefix (str): prefix of parameters. Default: ``''``.
        subfix (str): subfix of parameters. Default: ``''``.

    Examples:
        >>> from mindquantum.algorithm.nisq import Ansatz16
        >>> Ansatz16(4, 1).circuit
        q0: ──RX(p0)────RZ(p1)────RZ(p8)─────────────
                                    │
        q1: ──RX(p2)────RZ(p3)──────●───────RZ(p10)──
                                               │
        q2: ──RX(p4)────RZ(p5)────RZ(p9)───────●─────
                                    │
        q3: ──RX(p6)────RZ(p7)──────●────────────────
    """

    def __init__(self, n_qubits: int, depth: int, prefix: str = '', subfix: str = ''):
        """Construct ansatz."""
        Initializer.__init__(self, n_qubits, depth, prefix, subfix)
        Ansatz.__init__(self, 'Ansatz16', n_qubits, depth)

    def _implement(self, depth):  # pylint: disable=arguments-differ
        """Implement of ansatz 16."""
        for _ in range(depth):
            self._circuit += single_qubit_gate_layer(RX, self.n_qubits, pr_gen=self.pr_gen)
            self._circuit += single_qubit_gate_layer(RZ, self.n_qubits, pr_gen=self.pr_gen)
            start = 0
            for i in range(start, self.n_qubits, 2):
                obj = i
                ctrl = obj + 1
                if ctrl >= self.n_qubits:
                    continue
                self._circuit += RZ(self.pr_gen.new()).on(obj, ctrl)
            self._circuit += BARRIER
            start = 1
            for i in range(start, self.n_qubits, 2):
                obj = i
                ctrl = obj + 1
                if ctrl >= self.n_qubits:
                    continue
                self._circuit += RZ(self.pr_gen.new()).on(obj, ctrl)
            self._circuit += BARRIER


class Ansatz17(Ansatz, Initializer):
    """
    Ansatz 17 implement from arxiv paper.

    Please refers to `Expressibility and entangling capability of parameterized quantum circuits for hybrid
    quantum-classical algorithms <https://arxiv.org/abs/1905.10876>`_.

    Args:
        n_qubits (int): total qubits number of this ansatz.
        depth (int): depth of ansatz.
        prefix (str): prefix of parameters. Default: ``''``.
        subfix (str): subfix of parameters. Default: ``''``.

    Examples:
        >>> from mindquantum.algorithm.nisq import Ansatz17
        >>> Ansatz17(4, 1).circuit
        q0: ──RX(p0)────RZ(p1)────RX(p8)─────────────
                                    │
        q1: ──RX(p2)────RZ(p3)──────●───────RX(p10)──
                                               │
        q2: ──RX(p4)────RZ(p5)────RX(p9)───────●─────
                                    │
        q3: ──RX(p6)────RZ(p7)──────●────────────────
    """

    def __init__(self, n_qubits: int, depth: int, prefix: str = '', subfix: str = ''):
        """Construct ansatz."""
        Initializer.__init__(self, n_qubits, depth, prefix, subfix)
        Ansatz.__init__(self, 'Ansatz17', n_qubits, depth)

    def _implement(self, depth):  # pylint: disable=arguments-differ
        """Implement of ansatz 17."""
        for _ in range(depth):
            self._circuit += single_qubit_gate_layer(RX, self.n_qubits, pr_gen=self.pr_gen)
            self._circuit += single_qubit_gate_layer(RZ, self.n_qubits, pr_gen=self.pr_gen)
            start = 0
            for i in range(start, self.n_qubits, 2):
                obj = i
                ctrl = obj + 1
                if ctrl >= self.n_qubits:
                    continue
                self._circuit += RX(self.pr_gen.new()).on(obj, ctrl)
            self._circuit += BARRIER
            start = 1
            for i in range(start, self.n_qubits, 2):
                obj = i
                ctrl = obj + 1
                if ctrl >= self.n_qubits:
                    continue
                self._circuit += RX(self.pr_gen.new()).on(obj, ctrl)
            self._circuit += BARRIER


class Ansatz18(Ansatz, Initializer):
    """
    Ansatz 18 implement from arxiv paper.

    Please refers to `Expressibility and entangling capability of parameterized quantum circuits for hybrid
    quantum-classical algorithms <https://arxiv.org/abs/1905.10876>`_.

    Args:
        n_qubits (int): total qubits number of this ansatz.
        depth (int): depth of ansatz.
        prefix (str): prefix of parameters. Default: ``''``.
        subfix (str): subfix of parameters. Default: ``''``.

    Examples:
        >>> from mindquantum.algorithm.nisq import Ansatz18
        >>> Ansatz18(4, 1).circuit
        q0: ──RX(p0)────RZ(p1)────RZ(p8)────────────────────────────●─────
                                    │                               │
        q1: ──RX(p2)────RZ(p3)──────┼────────────────────●───────RZ(p11)──
                                    │                    │
        q2: ──RX(p4)────RZ(p5)──────┼─────────●───────RZ(p10)─────────────
                                    │         │
        q3: ──RX(p6)────RZ(p7)──────●───────RZ(p9)────────────────────────
    """

    def __init__(self, n_qubits: int, depth: int, prefix: str = '', subfix: str = ''):
        """Construct ansatz."""
        Initializer.__init__(self, n_qubits, depth, prefix, subfix)
        Ansatz.__init__(self, 'Ansatz18', n_qubits, depth)

    def _implement(self, depth):  # pylint: disable=arguments-differ
        """Implement of ansatz 18."""
        for _ in range(depth):
            self._circuit += single_qubit_gate_layer(RX, self.n_qubits, pr_gen=self.pr_gen)
            self._circuit += single_qubit_gate_layer(RZ, self.n_qubits, pr_gen=self.pr_gen)
            for ctrl in range(self.n_qubits)[::-1]:
                obj = (ctrl + 1) % self.n_qubits
                if obj != ctrl:
                    self._circuit += RZ(self.pr_gen.new()).on(obj, ctrl)
            self._circuit += BARRIER


class Ansatz19(Ansatz, Initializer):
    """
    Ansatz 19 implement from arxiv paper.

    Please refers to `Expressibility and entangling capability of parameterized quantum circuits for hybrid
    quantum-classical algorithms <https://arxiv.org/abs/1905.10876>`_.

    Args:
        n_qubits (int): total qubits number of this ansatz.
        depth (int): depth of ansatz.
        prefix (str): prefix of parameters. Default: ``''``.
        subfix (str): subfix of parameters. Default: ``''``.

    Examples:
        >>> from mindquantum.algorithm.nisq import Ansatz19
        >>> Ansatz19(4, 1).circuit
        q0: ──RX(p0)────RZ(p1)────RX(p8)────────────────────────────●─────
                                    │                               │
        q1: ──RX(p2)────RZ(p3)──────┼────────────────────●───────RX(p11)──
                                    │                    │
        q2: ──RX(p4)────RZ(p5)──────┼─────────●───────RX(p10)─────────────
                                    │         │
        q3: ──RX(p6)────RZ(p7)──────●───────RX(p9)────────────────────────
    """

    def __init__(self, n_qubits: int, depth: int, prefix: str = '', subfix: str = ''):
        """Construct ansatz."""
        Initializer.__init__(self, n_qubits, depth, prefix, subfix)
        Ansatz.__init__(self, 'Ansatz19', n_qubits, depth)

    def _implement(self, depth):  # pylint: disable=arguments-differ
        """Implement of ansatz 19."""
        for _ in range(depth):
            self._circuit += single_qubit_gate_layer(RX, self.n_qubits, pr_gen=self.pr_gen)
            self._circuit += single_qubit_gate_layer(RZ, self.n_qubits, pr_gen=self.pr_gen)
            for ctrl in range(self.n_qubits)[::-1]:
                obj = (ctrl + 1) % self.n_qubits
                if obj != ctrl:
                    self._circuit += RX(self.pr_gen.new()).on(obj, ctrl)
            self._circuit += BARRIER


__all__ = [
    'Ansatz1',
    'Ansatz2',
    'Ansatz3',
    'Ansatz4',
    'Ansatz5',
    'Ansatz6',
    'Ansatz7',
    'Ansatz8',
    'Ansatz9',
    'Ansatz10',
    'Ansatz11',
    'Ansatz12',
    'Ansatz13',
    'Ansatz14',
    'Ansatz15',
    'Ansatz16',
    'Ansatz17',
    'Ansatz18',
    'Ansatz19',
]
__all__.sort()
