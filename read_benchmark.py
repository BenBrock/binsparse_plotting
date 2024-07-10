import re
import numpy as np
import csv

import matplotlib.pyplot as plt
from collections import defaultdict

def plot_sizes(datasets, labels, ordering, fname='out.pdf', title='', x_title='', y_title='', yticks=None):
    fix,ax = plt.subplots()

    dataset_values = [[dataset[matrix] for matrix in ordering] for dataset in datasets]

    markers = ['s', '.', '^', 'o', '+']
    for marker,dataset,label in zip(markers,dataset_values, labels):
        domain = range(len(dataset))
        y_points = dataset
        ax.semilogy(domain, y_points, label=label)

    ax.minorticks_off()

    if yticks != None:
        ax.set_yticks(yticks[0])
        ax.set_yticklabels(yticks[1])

    plt.title(title, fontsize=18)
    plt.xlabel(x_title, fontsize=12)
    plt.ylabel(y_title, fontsize=12)
    plt.rcParams.update({'font.size': 12})
    plt.legend(loc='best')

    plt.tight_layout()
    plt.savefig(fname)

def read_nnz(fname):
    data = {}
    with open(fname, mode='r') as file:
        csvFile = csv.DictReader(file)
        for line in csvFile:
            data[line['dataset']] = int(line['nnz'])
    return data


def read_benchmark_data(file_name):
    matrix_data = defaultdict(lambda: {'runtime': [], 'bandwidth': []})

    for line in open(file_name, 'r'):
        if 'FORPARSER' in line:
            m = re.match('FORPARSER: (.+)', line.strip())

            if m:
                data = m.group(1).split(',')

                m2 = re.match('.+/(.+/.+)\.coo\.bsp\.h5', data[0])
                if m2:
                  matrix = m2.group(1)

                  runtime = float(data[1])
                  bandwidth_gb = float(data[2])

                  matrix_data[matrix]['runtime'].append(runtime)
                  matrix_data[matrix]['bandwidth'].append(bandwidth_gb)

    return matrix_data

def pretty_print_time(size):
    factor = 1

    if size >= 60:
        label = 'm'
        size /= 60
    else:
        if size >= 1:
            label = 's'

        if size < 1:
            size *= 1000
            label = 'ms'

    if int(size) == size:
        size = int(size)

    return '%s %s' % (size, label)

def print_data(matrix_data):
    for matrix in matrix_data.keys():
        runtime = matrix_data[matrix]['runtime']
        bandwidth = matrix_data[matrix]['bandwidth']
        print('%s has runtime %.3f s (SD %.3f, %.3f -> %.3f) and BW %.3f MiB/s (SD %.3f, %.3f -> %.3f)' % (matrix, np.mean(runtime), np.std(runtime), np.min(runtime), np.max(runtime), np.mean(bandwidth)*1024, np.std(bandwidth)*1024, np.min(bandwidth)*1024, np.max(bandwidth)*1024))

def read_and_clean_benchmark_data(file_name):
    matrix_data = read_benchmark_data(file_name)
    return {x: sum(matrix_data[x]['runtime']) for x in matrix_data.keys()};

matrix_nnz = read_nnz('matrix_nnzs.csv')

cutoff = 0
ordering = [x[0] for x in sorted(matrix_nnz.items(), key=lambda x: x[1], reverse=True) if matrix_nnz[x[0]] >= cutoff]

binsparse_coo_gzip1 = read_and_clean_benchmark_data('binsparse_coo_gzip1_read.dat')
binsparse_coo_noz = read_and_clean_benchmark_data('br_coo_noz.71972.out')

datasets = [binsparse_coo_gzip1, binsparse_coo_noz]
labels = ['binsparse_coo_gzip1', 'binsparse_coo_noz']

ytick_data = [0.200, 1, 6, 30, 180, 1080]
ytick_labels = [pretty_print_time(time) for time in ytick_data]

plot_sizes(datasets, labels, ordering, title='SuiteSparse Matrix Collection', y_title='Runtime', x_title='Matrix Index', yticks = (ytick_data, ytick_labels))
