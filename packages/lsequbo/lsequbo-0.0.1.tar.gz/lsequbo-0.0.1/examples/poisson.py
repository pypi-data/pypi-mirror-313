import argparse
import numpy as np
import dimod
import dwave.system
import lsequbo


class Poisson:

    def __init__(self, L: int = None):
        self.L = L
        self._b = None

    @property
    def A(self):
        # Discrete Laplace operator
        A = 2 * np.eye(self.L)
        A -= np.eye(self.L, k=-1) + np.eye(self.L, k=1)

        # Dirichlet boundary conditions
        for x in self.boundary:
            A[x] = 0
            A[x][x] = 1

        return A.astype(int)

    @property
    def b(self) -> np.ndarray:
        if self._b is None:
            return self.b_one_sided_bias
        else:
            return self._b

    @property
    def b_one_sided_bias(self) -> np.ndarray:
        self._b = np.zeros(self.L)
        self._b[-1] = self.L - 1
        return self._b

    @property
    def b_two_sided_bias(self) -> np.ndarray:
        self._b = np.zeros(self.L)
        self._b[0] = - np.floor(self.L / 2)
        self._b[-1] = np.ceil(self.L / 2 - 1)
        return self._b

    @property
    def b_point_charge(self) -> np.ndarray:
        c = (self.L - 1) // 2
        self._b = np.zeros(self.L)
        self._b[c] = 1
        self._b[-1 - c] = 1
        return self._b

    @property
    def boundary(self) -> list:
        return [0, self.L - 1]

    @staticmethod
    def gate_based_encoding(lse) -> dimod.BinaryQuadraticModel:
        Var = lsequbo.Var
        lse.gate_based_bqm = dimod.BinaryQuadraticModel('BINARY')
        bqm = lse.gate_based_bqm

        for x in lse.row_indices:
            # Sum intermediary Var can at most double
            sum_ = Var(x, label='~sum', nbits=lse.nbits+1)  # (requires 1 extra bit)
            lse.add(Var(x - 1), Var(x + 1), sum_)

            phi = Var(x)
            # Result can quadruple
            rho = Var(x, label='rho', nbits=lse.nbits+2)  # (2 extra bits). With unsigned only 1 extra.
            lse.add(rho, sum_, phi.multiply(2))

            # The bit-0 subtraction is always 0 - sum(0) mod 2 = sum(0). Trivial.
            bqm.contract_variables(rho.bit(0), sum_.bit(0))  # We do not need intermediary sum(0) bit.
            bqm.contract_variables(rho.bit(0), rho.aux.bit(0))

            # Fix charge configuration rho at x
            bqm.fix_variables(lse.rhs_variables(rho))

        # Fix boundary conditions
        bqm.fix_variables(lse.fixed_solution_variables)
        # Fix placeholder bits that are known to be zero due to multiplications by powers of 2
        bqm.fix_variable('~ZERO', 0)

        return bqm


def main(L, nbits, path, region):

    num_reads = 5000
    # Initialize LSE
    model = Poisson(L)

    # Encode problem to QUBO
    lse = lsequbo.LSE(A=model.A, b=model.b, nbits=nbits)
    lse.label = f'poisson_L={L}_nbits={nbits}'
    print('-----------------------')
    print(f'| {lse.label} |')
    print('-----------------------')
    # Poisson.gate_based_encoding(lse)
    lse.dump(path)

    # Solve
    sampler = dwave.system.DWaveSampler(region=region)

    # Embeddings
    composite = dwave.system.AutoEmbeddingComposite(sampler)

    # Send to D-Wave
    response_be = composite.sample(lse.binary_encoding, num_reads=num_reads)
    response_gbe = composite.sample(lse.gate_based_encoding, num_reads=num_reads)
    print()

    # Decode solution
    print('Binary Encoding')
    print('---------------')
    print('Energy =', response_be.first.energy)
    print('num_occurrences =', response_be.first.num_occurrences)
    print('num_reads =', num_reads)
    print('Success rate =', response_be.first.num_occurrences / num_reads)
    print()
    x_be = lse.decode_sample(response_be.first.sample)

    print('Gate-Based Encoding')
    print('-------------------')
    print('Energy =', response_gbe.first.energy)
    num_success = np.sum([record.num_occurrences for record in response_gbe.lowest().data()])
    print('num_success =', num_success)
    print('num_reads =', num_reads)
    print('Success rate =', num_success / num_reads)
    print()
    x_gbe = lse.decode_gbe_sample(response_gbe.first.sample)

    print('LU decomposition, x = ', lse.x)
    print('BE x = ', x_be)
    print('BE diff. =', np.sum(np.abs(x_be - lse.x)))
    # print('BE diff. =', (x_be - lse.x) @ (x_be - lse.x))
    print('GBE x = ', x_gbe)
    print('BE diff. =', np.sum(np.abs(x_gbe - lse.x)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate Poisson model, encode to QUBO and solve on D-Wave")
    parser.add_argument('L', type=int, help="Length of model")
    parser.add_argument('-b', '--bits', type=int, required=False, default=4,
                        help="Number of bits to encode solutions")
    parser.add_argument('-o', '--out', type=str, required=False, default=None,
                        help="Path to store Ising file and response")
    parser.add_argument('-r', '--region', type=str, required=False, default='eu-central-1',
                        help="Region to select D-Wave QPU")

    args = parser.parse_args()
    main(args.L, nbits=args.bits, path=args.out, region=args.region)
