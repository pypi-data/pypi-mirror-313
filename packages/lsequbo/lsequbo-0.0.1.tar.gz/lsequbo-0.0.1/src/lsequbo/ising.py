import csv


DELIMITER = ' '


def dump(data, file):
    bqm = data

    # Enumerate variables and transform QUBO to Ising
    qubitmap = {idx: var for idx, var in enumerate(sorted(bqm.variables, reverse=True))}
    mapping = {var: idx for idx, var in enumerate(sorted(bqm.variables, reverse=True))}
    bqm.relabel_variables(mapping)
    bqm = bqm.spin  # TODO declare new bqm?

    # Write headers
    file.writelines([
        f"# QUBITS {bqm.num_variables}\n",
        f"# offset {bqm.offset}\n",
        f"# qubitmap {qubitmap}\n",
        f"# indices {' '.join(str(idx) for idx, _ in sorted(mapping.items()))}\n"
        f"# variables {' '.join(str(var) for _, var in sorted(mapping.items()))}\n"
        # TODO f"# solutionmask0 ...\n"
    ])

    # Write data
    writer = csv.writer(file, delimiter=DELIMITER, lineterminator='\n')
    for i, bias in bqm.linear.items():
        writer.writerow([i, i, bias])
    for (i, j), bias in bqm.quadratic.items():
        writer.writerow([i, j, bias])

    bqm.relabel_variables(qubitmap)


def load(file):
    headers = {}
    hs = {}
    Js = {}
    reader = csv.reader(file, delimiter=DELIMITER)
    for row in reader:
        if row[0] == '#':
            headers[row[1]] = row[2] if len(row) == 3 else row[2:]
            continue
        i = int(row[0])
        j = int(row[1])
        bias = float(row[2])
        if i == j:
            hs[i] = bias
        else:
            Js[(i, j)] = bias

    return hs, Js, headers
