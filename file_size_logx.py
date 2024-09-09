from plotting import *

binsparse_coo_gzip9_aux = read_dataset('binsparse_coo_gzip9_aux.csv')

binsparse_coo_noz_noaux = read_dataset('binsparse_coo_noz_noaux.csv')
binsparse_coo_gzip1_noaux = read_dataset('binsparse_coo_gzip1_noaux.csv')
binsparse_coo_gzip9_noaux = read_dataset('binsparse_coo_gzip9_noaux.csv')

binsparse_csr_gzip9_aux = read_dataset('binsparse_csr_gzip9_aux.csv')

binsparse_csr_noz_noaux = read_dataset('binsparse_csr_noz_noaux.csv')
binsparse_csr_gzip1_noaux = read_dataset('binsparse_csr_gzip1_noaux.csv')
binsparse_csr_gzip9_noaux = read_dataset('binsparse_csr_gzip9_noaux.csv')

mtx_noz_aux = read_dataset('mtx_noz_aux.csv')
mtx_noz_noaux = read_dataset('mtx_noz_noaux.csv')

fmm_noz = read_dataset('fmm_sizes.csv')

matrix_nnz = read_nnz('matrix_nnzs.csv')

cutoff = 1024*1024

# Order by NNZ
# ordering = [x[0] for x in sorted(matrix_nnz.items(), key=lambda x: x[1], reverse=True) if matrix_nnz[x[0]] >= cutoff]

# Order by MTX file size
ordering = [x[0] for x in sorted(mtx_noz_noaux.items(), key=lambda x: x[1], reverse=True) if matrix_nnz[x[0]] >= cutoff]

# This was my old dataset ordering (keeping COO/COOGZ and CSR/CSRGZ consecutive).
# The new legend ordering follows the top-bottom ordering on the plot.
# datasets = [mtx_noz_noaux, binsparse_coo_noz_noaux, binsparse_coo_gzip1_noaux, binsparse_csr_noz_noaux, binsparse_csr_gzip1_noaux]
# labels = ['mtx_noz_noaux', 'binsparse_coo_noz_noaux', 'binsparse_coo_gzip1_noaux', 'binsparse_csr_noz_noaux', 'binsparse_csr_gzip1_noaux']

datasets = [mtx_noz_noaux, binsparse_coo_noz_noaux, binsparse_csr_noz_noaux, binsparse_coo_gzip1_noaux, binsparse_csr_gzip1_noaux]
labels = ['mtx_noz_noaux', 'binsparse_coo_noz_noaux', 'binsparse_csr_noz_noaux', 'binsparse_coo_gzip1_noaux', 'binsparse_csr_gzip1_noaux']

# datasets = [mtx_noz_noaux, binsparse_coo_noz_noaux, binsparse_coo_gzip1_noaux, binsparse_coo_gzip9_noaux]
# labels = ['mtx_noz_noaux', 'binsparse_coo_noz_noaux', 'binsparse_coo_gzip1_noaux', 'binsparse_coo_gzip9_noaux']

ytick_data = [x * 1024 * 1024 for x in [0.25, 1, 4, 16, 64, 256, 1024, 4096, 16384, 65536]]
ytick_labels = [pretty_print_size(x) for x in ytick_data]

xtick_data = [x * 1024 * 1024 for x in [16, 64, 256, 1024, 4096, 16384, 65536]]
xtick_labels = [pretty_print_size(x) for x in xtick_data]

colors = ['C0', 'C1', 'C2', 'C3', 'C4']

plot_sizes_logx(mtx_noz_noaux, datasets, labels, ordering, title='File Size - SuiteSparse Matrix Collection', y_title='File Size (Bytes)', x_title='Matrix Market File Size', yticks = (ytick_data,ytick_labels), xticks = (xtick_data, xtick_labels), colors=colors, fname='out.pdf')

print(ytick_data)
print(ytick_labels)

for matrix in ordering:
    if binsparse_coo_gzip9_aux[matrix] > mtx_noz_aux[matrix]:
        print('%s: %s' % (matrix, pretty_print_size(binsparse_coo_gzip9_aux[matrix] - mtx_noz_aux[matrix])))

print_speedups(datasets, labels, ordering, mtx_noz_noaux)
