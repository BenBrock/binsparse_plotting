import matplotlib.pyplot as plt
import csv
import re

import numpy as np
from statistics import geometric_mean

from collections import defaultdict

import os
import json

relabel = {}
relabel['mtx_noz_noaux'] = '.mtx'
relabel['binsparse_coo_noz_noaux'] = '.coo.bsp'
relabel['binsparse_coo_gzip1_noaux'] = '.coo.bsp.gz'
relabel['binsparse_csr_noz_noaux'] = '.csr.bsp'
relabel['binsparse_csr_gzip1_noaux'] = '.csr.bsp.gz'

relabel['binsparse_coo_noz'] = '.coo.bsp'
relabel['binsparse_coo_gzip1'] = '.coo.bsp.gz'
relabel['binsparse_csr_noz'] = '.csr.bsp'
relabel['binsparse_csr_gzip1'] = '.csr.bsp.gz'

relabel['fmm_noz'] = '.fmm.mtx'

relabel['mtx_mt'] = '.mtx (P)'

relabel['binsparse_coo_noz_mt'] = '.coo.bsp (P)'
relabel['binsparse_coo_gzip1_mt'] = '.coo.bsp.gz (P)'
relabel['binsparse_csr_noz_mt'] = '.csr.bsp (P)'
relabel['binsparse_csr_gzip1_mt'] = '.csr.bsp.gz (P)'

relabel['tensor_tns'] = '.tns (T)'
relabel['tensor_coo_bsp_gz9'] = '.coo.bsp.gz9 (T)'
relabel['tensor_csf_bsp_gz9'] = '.csf.bsp.gz9 (T)'

def plot_sizes_logx(matrix_sizes, datasets, labels, ordering, fname='out.png', title='', x_title='', y_title='', yticks=None, xticks=None, colors=None, style='scatter', tensor_data=None):
    plt.style.use('tableau-colorblind10')
    fix,ax = plt.subplots()

    dataset_values = [[dataset[matrix] for matrix in ordering] for dataset in datasets]

    domain_values = [matrix_sizes[matrix] for matrix in ordering]

    ax.set_yscale('log')
    ax.set_xscale('log')

    if colors == None:
        colors = [None for d in datasets]

    markers = [None for d in datasets]

    for marker,dataset,label,color in zip(markers,dataset_values, labels, colors):
        domain = domain_values
        y_points = dataset

        if style == 'line':
            ax.semilogy(domain, y_points, label=relabel[label], color=color)
        elif style == 'scatter':
            ax.scatter(domain, y_points, label=relabel[label], s=2, color=color, alpha=0.9)
        else:
            print('Style must be either line or scatter')
            assert(False)

    if tensor_data != None:
        (tensor_sizes,tensor_datasets,tensor_labels,tensor_ordering,tensor_colors) = tensor_data

        tensor_domain_values = [tensor_sizes[tensor] for tensor in tensor_ordering]

        tensor_markers = [None for d in tensor_datasets]

        tensor_dataset_values = [[dataset[tensor] for tensor in tensor_ordering] for dataset in tensor_datasets]

        for marker,dataset,label,color in zip(tensor_markers,tensor_dataset_values,tensor_labels,tensor_colors):
            domain = tensor_domain_values
            y_points = dataset

            if style == 'line':
                ax.semilogy(domain, y_points, label=relabel[label], color=color)
            elif style == 'scatter':
                ax.scatter(domain, y_points, label=relabel[label], s=2, color=color, alpha=0.9)
            else:
                print('Style must be either line or scatter')
                assert(False)

    ax.minorticks_off()


    if yticks != None:
        ax.set_yticks(yticks[0])
        ax.set_yticklabels(yticks[1])

    if xticks != None:
        ax.set_xticks(xticks[0])
        ax.set_xticklabels(xticks[1])

    plt.title(title, fontsize=18)
    plt.xlabel(x_title, fontsize=12)
    plt.ylabel(y_title, fontsize=12)
    plt.rcParams.update({'font.size': 12})
    legend = plt.legend(loc='best')

    for handle in legend.legend_handles:
        handle._sizes = [20];

    plt.tight_layout()
    import os
    filename, file_extension = os.path.splitext(fname)
    if file_extension == '.png':
        plt.savefig(fname, dpi=200)
    else:
        plt.savefig(fname)

def plot_sizes(datasets, labels, ordering, fname='out.png', title='', x_title='', y_title='', yticks=None, style='scatter'):
    fix,ax = plt.subplots()

    dataset_values = [[dataset[matrix] for matrix in ordering] for dataset in datasets]

    ax.set_yscale('log')

    markers = ['s', '.', '^', 'o', '+']
    for marker,dataset,label in zip(markers,dataset_values, labels):
        domain = range(len(dataset))
        y_points = dataset

        if style == 'line':
            ax.semilogy(domain, y_points, label=label)
        elif style == 'scatter':
            ax.scatter(domain, y_points, label=label, s=0.5)
        else:
            print('Style must be either line or scatter')
            assert(False)

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
    import os
    filename, file_extension = os.path.splitext(fname)
    if file_extension == '.png':
        plt.savefig(fname, dpi=400)
    else:
        plt.savefig(fname)


def read_dataset(fname):
    data = {}
    with open(fname, mode='r') as file:
        csvFile = csv.DictReader(file)
        for line in csvFile:
            data[line['dataset']] = int(line['size_bytes'])
    return data

def read_nnz(fname):
    data = {}
    with open(fname, mode='r') as file:
        csvFile = csv.DictReader(file)
        for line in csvFile:
            data[line['dataset']] = int(line['nnz'])
    return data

def pretty_print_size(size):
    factor = 1
    while size / 1024.0 >= 1:
        factor *= 1024;
        size /= 1024

    if factor == 1:
        label = 'B'
    elif factor == 1024:
        label = 'KiB'
    elif factor == 1024*1024:
        label = 'MiB'
    elif factor == 1024*1024*1024:
        label = 'GiB'
    elif factor == 1024*1024*1024*1024:
        label = 'TiB'
    else:
        assert(False)

    if int(size) == size:
        size = int(size)

    return '%s %s' % (size, label)


def pretty_print_time(size, only_seconds=False):
    factor = 1

    if not only_seconds and size >= 60:
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

    if type(size) == float:
        return '%.1f %s' % (size, label)

    return '%s %s' % (size, label)

def read_benchmark_data(file_name):
    matrix_data = defaultdict(lambda: {'runtime': [], 'bandwidth': []})

    for line in open(file_name, 'r'):
        if 'FORPARSER' in line:
            m = re.match('FORPARSER: (.+)', line.strip())

            if m:
                data = m.group(1).split(',')

                m2 = re.match('.+/(.+/.+?)\..+', data[0])
                if m2:
                  matrix = m2.group(1)

                  runtime = float(data[1])
                  bandwidth_gb = float(data[2])

                  matrix_data[matrix]['runtime'].append(runtime)
                  matrix_data[matrix]['bandwidth'].append(bandwidth_gb)
                else:
                    print('%s not matched...' % (data[0]))

    return matrix_data

def read_and_clean_benchmark_data(file_name):
    matrix_data = read_benchmark_data(file_name)
    return {x: np.mean(matrix_data[x]['runtime']) for x in matrix_data.keys()};

def read_and_clean_tensor_data(directory, prefix=None):
    dataset = {}
    for i in range(1, 30):
        file_name = prefix + "_%s.json" % (i,) if prefix != None else "%s.json" % (i,)
        file_name = directory + '/' + file_name
        file_exists = os.path.exists(file_name) and os.path.isfile(file_name)

        if file_exists:
            try:
                with open(file_name, "r") as f:
                    data = json.load(f)

                    runtime = np.mean(data['times'][10:])

                    m = re.match('tensors/(.+?)\..+', data['filename'])
                    label = m.group(1)

                    dataset[label] = runtime
            except:
                pass
    return dataset

def print_speedups(datasets, labels, ordering, baseline):
    speedups = {}
    for label in labels:
        speedups[label] = []

    for matrix in ordering:
        for dataset,label in zip(datasets,labels):
            speedups[label].append(baseline[matrix] / dataset[matrix])
            # if baseline[matrix] < dataset[matrix]:
            #     print('%s is slower.' % (matrix))

    for label in labels:
        mean_speedup = geometric_mean(speedups[label])
        max_speedup = np.max(speedups[label])
        min_speedup = np.min(speedups[label])

        print('%s has a mean speedup of %.3fx, max speedup of %.3fx, and min speedup of %.3fx\n' % (label, mean_speedup, max_speedup, min_speedup,))

def print_statistics(files, ordering):
    for file in files:
        matrix_data = read_benchmark_data(file)

        coefficients_of_variance = []
        high_cv_matrices = []

        for matrix in ordering:
            variance = np.var(matrix_data[matrix]['runtime'])
            mean = np.mean(matrix_data[matrix]['runtime'])

            stdev = np.sqrt(variance)

            cv = stdev / mean

            if cv >= 1:
              high_cv_matrices.append((matrix, cv))

            coefficients_of_variance.append(cv)

        if len(high_cv_matrices) > 0:
            print('%s has high variance matrices:' % (file,))
            for matrix,cv in sorted(high_cv_matrices, key=lambda x: x[1]):
                print('%s: %.2lf' % (matrix,cv))

        print('%s has average CV of %.2f, min CV of %.2f, max CV of %.2f' % (file, np.mean(coefficients_of_variance), np.min(coefficients_of_variance), np.max(coefficients_of_variance)))

