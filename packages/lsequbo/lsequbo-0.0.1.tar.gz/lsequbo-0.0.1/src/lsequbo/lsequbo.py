#!python3
import argparse
from dataclasses import dataclass, field, replace
from itertools import product
import pathlib
from typing import ClassVar, Self
import numpy as np
from scipy.linalg import lu_factor, lu_solve
import dimod
from . import ising


@dataclass
class Var:
    idx: int
    digit: int = 0
    label: str = "Var"

    nbits: int = field(default=None, repr=False, compare=False)
    default_nbits: ClassVar[int] = 0

    def __post_init__(self):
        if self.nbits is None:
            self.nbits = Var.default_nbits

    def __repr__(self):
        return f'{self.label}({self.idx},digit={self.digit})'

    def __hash__(self):
        return hash(self.astuple)

    @property
    def astuple(self) -> tuple:
        return self.label, self.idx, self.digit

    def __lt__(self, other):
        return self.astuple < other.astuple

    @property
    def aux(self) -> Self:
        """Ancilla Var for corresponding output Var"""
        # TODO: Is this unique?
        return replace(self, label=f'~aux_{self.label}', digit=0)

    def bit(self, digit: int) -> Self:
        """Binary Var for this bit"""
        new_digit = self.digit + digit
        # The d least significant bits are zeroes after multiplication by 2^d
        if new_digit < 0 or new_digit >= self.nbits:
            return '~ZERO'
        return replace(self, digit=new_digit)

    def multiply(self, factor: int) -> Self:
        """Multiply by factor == 2^shift"""
        # TODO Move nbits information to LSE class
        shift = np.log2(factor)
        if not shift.is_integer():
            raise ValueError(f'Cannot multiply Var {self} with factor {factor}')
        # Need extra bit per shift
        nbits = self.nbits + int(shift)
        # Offset digits by shift
        digit = self.digit - int(shift)
        return replace(self, nbits=nbits, digit=digit)


class LSE:
    """
    Linear system of equations.

    Generates QUBO formulations of problem and dumps them to disk.


    TODO Signed encoding for GBE problematic
         Best guess is to fill up variables to maximum width with zeroes.
         All variables would have the same width.

    TODO Precision / rounding
         Problematic without assumptions on x.
         Scale up until Δx ~ 1
            Re-scale such that min(x) = 1.0
            Iteratively multiply by integers until differences are integer
         Or re-scale until max(x) = 1.0
            Then each precision bit halves interval [0, 1].

    TODO Generic GBE creator
         Loses efficiency compared to custom algo
         Keep widths small
    """

    def __init__(self, A: np.ndarray, b: np.ndarray, nbits: int = None):
        self.A = A
        self.b = b
        self.nbits = nbits
        self.signed = False

        self.label = None
        self.gate_based_bqm = None

        Var.default_nbits = nbits

    @property
    def nrows(self) -> int:
        """Number of equations in the LSE"""
        return self.A.shape[0]

    @property
    def ncols(self) -> int:
        """Number of variables in the LSE"""
        return self.A.shape[1]

    @property
    def energy_offset(self) -> int:
        """Energy offset of the BQM"""
        return int(self.b @ self.b)

    @property
    def fixed_row_indices(self) -> list[int]:
        """Trivial rows of LSE (e.g. Dirichlet boundary conditions)"""
        return [idx for idx, row in enumerate(self.A) if np.count_nonzero(row) == 1]

    @property
    def row_indices(self) -> list[int]:
        """Non-trivial rows of LSE"""
        return [idx for idx in range(self.nrows) if idx not in self.fixed_row_indices]

    """Classical solution"""

    @property
    def x(self) -> np.array:
        """Classical solution using LU decomposition"""
        # Perform LU decomposition and solve
        lu, piv = lu_factor(self.A)
        return lu_solve((lu, piv), self.b)

    @property
    def x_bin(self) -> list[str]:
        """Classical solution LSE.x as a bit string representing a binary number"""
        return [np.binary_repr(int(round(solution_var)), width=self.nbits) for solution_var in self.x]

    """Binary Encoding QUBO"""

    @property
    def binary_encoding(self) -> dimod.BinaryQuadraticModel:
        """
        QUBO formulation of LSE.

        Uses conventional method named Binary Encoding (BE).
        """

        def A_binary_repr(multi_index: Var) -> np.ndarray:
            sign = +1
            if self.signed is True and multi_index.digit == multi_index.nbits - 1:
                sign = -1
            return sign * 2 ** multi_index.digit * self.A[:, multi_index.idx]

        # Compute QUBO coefficients
        qubo = {}

        i_multi_indices = [Var(idx, digit) for idx, digit in product(range(self.nrows), range(self.nbits))]
        j_multi_indices = [Var(idx, digit) for idx, digit in product(range(self.ncols), range(self.nbits))]

        for i, j in product(i_multi_indices, j_multi_indices):
            if j == i:
                qubo[i, j] = np.sum(A_binary_repr(i) * (A_binary_repr(i) - 2 * self.b))
            elif j > i:
                qubo[i, j] = np.sum(A_binary_repr(i) * A_binary_repr(j)) * 2  # Factor 2 for lower triangle j < i

        # Init BQM and fix variables
        bqm = dimod.BinaryQuadraticModel.from_qubo(qubo, offset=self.energy_offset)
        bqm.fix_variables(self.fixed_solution_variables)

        return bqm

    def rhs_variables(self, rhs: Var) -> dict:
        """RHS variables b corresponding to row rhs.idx"""
        rhs_variables = {}

        _rhs = self.b[rhs.idx]
        rhs_bit_string = np.binary_repr(int(round(_rhs)), width=rhs.nbits)
        for digit in range(rhs.nbits):
            var = rhs.bit(digit)
            val = rhs_bit_string[rhs.nbits - 1 - digit]
            rhs_variables[var] = int(val)

        return rhs_variables

    @property
    def fixed_solution_variables(self) -> dict:
        """Solution variables x that are fixed since their corresponding row is trivial"""
        fixed_variables = {}

        # Determine trivial rows
        for i in self.fixed_row_indices:
            j = int(np.nonzero(self.A[i])[0][0])

            # Map fixed values to corresponding variables
            _rhs = self.b[i] / self.A[i][j]  # A[i][j] x x[j] = b[i]
            rhs_bit_string = np.binary_repr(int(round(_rhs)), width=self.nbits)
            for digit in range(self.nbits):
                var = Var(j, digit)
                val = rhs_bit_string[self.nbits - 1 - digit]
                fixed_variables[var] = int(val)

        return fixed_variables

    """Gate-Based Encoding QUBO"""

    @property
    def gate_based_encoding(self) -> dimod.BinaryQuadraticModel:
        """
        QUBO formulation of LSE.

        Uses novel method named Gate-Based Encoding (GBE).
        """
        # TODO Implement
        if self.gate_based_bqm is None:
            return self._gate_based_encoding_poisson
        else:
            return self.gate_based_bqm

    @property
    def _gate_based_encoding_poisson(self) -> dimod.BinaryQuadraticModel:
        self.gate_based_bqm = dimod.BinaryQuadraticModel('BINARY')

        for x in self.row_indices:
            a = Var(x - 1)  # .multiply(-1)
            b = Var(x).multiply(2)
            inter = Var(x, label='~inter', nbits=self.nbits+2)
            self.add(inter, a, b)

            a = inter
            b = Var(x + 1)  # .multiply(-1)
            rhs = Var(x, label='rho', nbits=self.nbits+3)
            self.add(rhs, b, a)

            # The bit-0 subtraction is always 0 - a mod 2 = a. Trivial.
            self.gate_based_bqm.contract_variables(inter.bit(0), inter.aux.bit(0))  # carry if and only if inter = 1
            self.gate_based_bqm.contract_variables(Var(x - 1).bit(0), inter.bit(0))  # We do not need intermediary sum

            # Fix charge configuration rho at x
            self.gate_based_bqm.fix_variables(self.rhs_variables(rhs))

        # Fix boundary conditions
        self.gate_based_bqm.fix_variables(self.fixed_solution_variables)
        # Fix placeholder bits that are known to be zero due to multiplications by powers of 2
        self.gate_based_bqm.fix_variable('~ZERO', 0)

        return self.gate_based_bqm

    def add(self, in0: Var, in1: Var, out: Var) -> None:
        bqm = self.gate_based_bqm
        nbits_set = [in0.nbits, in1.nbits, out.nbits]
        nbits = max(nbits_set)
        if out.nbits == nbits:
            aux = out.aux
        else:
            aux = in0.aux

        for d in range(0, 1):
            # No input carry for least significant bit.
            bqm += dimod.generators.halfadder_gate(in0.bit(d), in1.bit(d), out.bit(d), aux.bit(d))
        for d in range(1, nbits - 1):
            # Predecessor carry.bit(d - 1) glues together every digit by being the carry in.
            bqm += dimod.generators.fulladder_gate(in0.bit(d), in1.bit(d), aux.bit(d - 1), out.bit(d), aux.bit(d))
        for d in range(nbits - 1, nbits):
            # The most significant out.bit(nbits - 1) is just the carry.bit(nbits - 2).
            if out.nbits == nbits:
                bqm.relabel_variables({aux.bit(d - 1): out.bit(d)})
            else:
                bqm.relabel_variables({aux.bit(d - 1): in0.bit(d)})
        return

    """Store QUBO models as .ising"""

    def dump(self, path) -> list[str]:
        """Dump QUBO formulations of LSE to .ising"""
        output_dir = pathlib.Path(path) / self.label
        output_dir.mkdir(parents=True, exist_ok=True)

        files = [
            f'{output_dir}/binary_encoding.ising',
            f'{output_dir}/gate_based_encoding.ising'
        ]

        with open(files[0], 'w') as file:
            ising.dump(self.binary_encoding, file)
        with open(files[1], 'w') as file:
            ising.dump(self.gate_based_encoding, file)

        return files

    """Decode response"""

    def decode_sample_bin(self, sample) -> list[str]:
        """Extract solution bit strings from sample returned by D-Wave"""
        # Read back out fixed variables
        all_vars = self.fixed_solution_variables | sample

        # Create sorted array
        keys = sorted(all_vars.keys(), key=lambda x: (x.idx, x.digit), reverse=False)
        values = [all_vars[key] for key in keys]
        array = np.array(values)

        # Reshape with one bit string per row
        matrix = array.reshape(self.ncols, self.nbits)
        ordered_matrix = np.flip(matrix, axis=1)
        bit_strings = ["".join(map(str, row)) for row in ordered_matrix]

        return bit_strings

    def decode_gbe_sample_bin(self, sample) -> list:
        """Extract solution bit strings from sample returned by D-Wave"""
        # Read back out fixed variables
        all_vars = self.fixed_solution_variables | sample

        # Create sorted array
        keys = sorted(all_vars.keys(), reverse=False)
        values = [all_vars[key] for key in keys]
        array = np.array(values[:self.ncols*self.nbits])

        # Reshape with one bit string per row
        matrix = array.reshape(self.ncols, self.nbits)
        ordered_matrix = np.flip(matrix, axis=1)
        bit_strings = ["".join(map(str, row)) for row in ordered_matrix]

        return bit_strings

    def decode_bit_string(self, x):
        if self.signed is True and x[0] == '1':
            return int(x[1:], base=2) - 2 ** (len(x) - 1)
        else:
            return int(x, base=2)

    def decode_sample(self, sample) -> np.array:
        """Extract and decode solutions from sample returned by D-Wave"""
        bit_strings = self.decode_sample_bin(sample)
        integers = [self.decode_bit_string(bit_string) for bit_string in bit_strings]
        return np.array(integers)

    def decode_gbe_sample(self, sample) -> np.array:
        """Extract and decode solutions from sample returned by D-Wave"""
        bit_strings = self.decode_gbe_sample_bin(sample)
        integers = [self.decode_bit_string(bit_string) for bit_string in bit_strings]
        return np.array(integers)

    # Diagnostics

    @staticmethod
    def hamming(x: np.array) -> np.array:
        def _hw(y):
            return np.binary_repr(int(y)).count('1')
        return np.vectorize(_hw)(x)

    @property
    def info(self):
        info = {}

        x = self.x
        info['real'] = np.all(np.isreal(self.A)) and np.all(np.isreal(self.b))

        info['A'] = self.A

        info['A.nrows'] = self.nrows
        info['A.ncols'] = self.ncols

        info['A.square'] = self.nrows == self.ncols
        info['A.symmetric'] = np.allclose(self.A, self.A.T)

        eigenvalues, eigenvectors = np.linalg.eig(self.A)
        info['A.eigenvalues'] = eigenvalues
        info['A.eigenvalues.min'] = np.min(eigenvalues)
        info['A.eigenvalues.max'] = np.max(eigenvalues)

        info['A.positive_semi-definite'] = np.all(eigenvalues >= 0)
        info['A.positive_definite'] = np.all(eigenvalues > 0)

        info['A.determinant'] = np.linalg.det(self.A)

        hamming = self.hamming(self.A)
        info['A.hamming.matrix'] = hamming
        info['A.hamming.weight'] = np.sum(hamming)

        # Classical solution
        info['LU.x'] = x
        info['LU.x.min'] = np.min(x)
        info['LU.x.max'] = np.max(x)

        xfrac, _ = np.modf(x)
        info['LU.x.fractional_part'] = np.abs(xfrac @ xfrac)

        return info


def main(A_file, b_file, nbits):
    A = np.loadtxt(A_file)
    b = np.loadtxt(b_file)
    lse = LSE(A, b, nbits)

    nqubits = lse.ncols * lse.nbits
    label = f'nqubits={nqubits}_nbits={lse.nbits}'
    with open(f'models/lse-{label}.ising', 'w') as file:
        ising.dump(lse.binary_encoding, file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate Ising model and store to .ising")
    parser.add_argument('A', type=str, help="Path to the CSV file for matrix A")
    parser.add_argument('b', type=str, help="Path to the CSV file for vector b")
    parser.add_argument('-b', '--bits', type=int, required=True, help="Number of bits to encode solutions")

    args = parser.parse_args()
    main(args.A, args.b, nbits=args.bits)
