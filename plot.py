import matplotlib.pyplot as plt
import csv

def plot_sizes(datasets, labels, ordering, fname='out.png', title='', x_title='', y_title='', yticks=None):
    fix,ax = plt.subplots()

    dataset_values = [[dataset[matrix] for matrix in ordering] for dataset in datasets]

    print(dataset_values[1])

    markers = ['s', '.', '^', 'o']
    for marker,dataset,label in zip(markers,dataset_values, labels):
        domain = range(len(dataset))
        y_points = dataset
        ax.semilogy(domain, y_points, label=label, marker=marker, markerfacecolor='white')

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

def read_dataset(fname):
    data = {}
    with open(fname, mode='r') as file:
        csvFile = csv.DictReader(file)
        for lines in csvFile:
            data[lines['dataset']] = int(lines['size_bytes'])
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

    return '%s %s' % (size, label)

binsparse_coo_gzip9_aux = read_dataset('binsparse_coo_gzip9_aux.csv')
mtx_noz_aux = read_dataset('mtx_noz_aux.csv')
mtx_noz_noaux = read_dataset('mtx_noz_noaux.csv')

ordering = [x[0] for x in sorted(mtx_noz_aux.items(), key=lambda x: x[1], reverse=True)]

datasets = [mtx_noz_aux, binsparse_coo_gzip9_aux]
labels = ['mtx_noz_aux', 'binsparse_coo_gzip9_aux']

ytick_data = [1024 * 2**(i*3) for i in range(10)]
ytick_labels = [pretty_print_size(size) for size in ytick_data]

plot_sizes(datasets, labels, ordering, title='SuiteSparse Matrix Collection', y_title='File Size (Bytes)', x_title='Matrix Index', yticks = (ytick_data,ytick_labels))

print(ytick_data)
print(ytick_labels)

for matrix in ordering:
    if binsparse_coo_gzip9_aux[matrix] > mtx_noz_aux[matrix]:
        print('%s: %s' % (matrix, pretty_print_size(binsparse_coo_gzip9_aux[matrix] - mtx_noz_aux[matrix])))
