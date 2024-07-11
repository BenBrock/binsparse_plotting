from plotting import *


def print_data(matrix_data):
    for matrix in matrix_data.keys():
        runtime = matrix_data[matrix]['runtime']
        bandwidth = matrix_data[matrix]['bandwidth']
        print('%s has runtime %.3f s (SD %.3f, %.3f -> %.3f) and BW %.3f MiB/s (SD %.3f, %.3f -> %.3f)' % (matrix, np.mean(runtime), np.std(runtime), np.min(runtime), np.max(runtime), np.mean(bandwidth)*1024, np.std(bandwidth)*1024, np.min(bandwidth)*1024, np.max(bandwidth)*1024))


matrix_nnz = read_nnz('matrix_nnzs.csv')

cutoff = 1000000

mtx_noz_noaux = read_dataset('mtx_noz_noaux.csv')

binsparse_coo_gzip1 = read_and_clean_benchmark_data('binsparse_coo_gzip1_read.dat')
binsparse_coo_noz = read_and_clean_benchmark_data('br_coo_noz.71972.out')
mtx_coo_noz = read_and_clean_benchmark_data('br_mtx_noz.73384.out')

# Order by NNZ
# ordering = [x[0] for x in sorted(matrix_nnz.items(), key=lambda x: x[1], reverse=True) if matrix_nnz[x[0]] >= cutoff]

# Order by MTX file size
# ordering = [x[0] for x in sorted(mtx_noz_noaux.items(), key=lambda x: x[1], reverse=True) if matrix_nnz[x[0]] >= cutoff]

# Order by MTX read time
ordering = [x[0] for x in sorted(mtx_coo_noz.items(), key=lambda x: x[1], reverse=True) if matrix_nnz[x[0]] >= cutoff]

datasets = [binsparse_coo_gzip1, binsparse_coo_noz, mtx_coo_noz]
labels = ['binsparse_coo_gzip1', 'binsparse_coo_noz', 'mtx_coo_noz']

ytick_data = [0.200, 1, 6, 30, 180, 1080]
ytick_labels = [pretty_print_time(time) for time in ytick_data]

plot_sizes(datasets, labels, ordering, title='SuiteSparse Matrix Collection', y_title='Runtime', x_title='Matrix Index', yticks = (ytick_data, ytick_labels))

print_speedups(datasets, labels, ordering, mtx_coo_noz)