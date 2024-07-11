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

matrix_nnz = read_nnz('matrix_nnzs.csv')

cutoff = 1024*1024

print(matrix_nnz)

# Order by NNZ
# ordering = [x[0] for x in sorted(matrix_nnz.items(), key=lambda x: x[1], reverse=True) if matrix_nnz[x[0]] >= cutoff]

# Order by MTX file size
ordering = [x[0] for x in sorted(mtx_noz_noaux.items(), key=lambda x: x[1], reverse=True) if matrix_nnz[x[0]] >= cutoff]

datasets = [mtx_noz_noaux, binsparse_coo_noz_noaux, binsparse_coo_gzip1_noaux, binsparse_csr_noz_noaux, binsparse_csr_gzip1_noaux]
labels = ['mtx_noz_noaux', 'binsparse_coo_noz_noaux', 'binsparse_coo_gzip1_noaux', 'binsparse_csr_noz_noaux', 'binsparse_csr_gzip1_noaux']

# datasets = [mtx_noz_noaux, binsparse_coo_noz_noaux, binsparse_coo_gzip1_noaux, binsparse_coo_gzip9_noaux]
# labels = ['mtx_noz_noaux', 'binsparse_coo_noz_noaux', 'binsparse_coo_gzip1_noaux', 'binsparse_coo_gzip9_noaux']

ytick_data = [1024 * 2**(i*3) for i in range(10)]
ytick_labels = [pretty_print_size(size) for size in ytick_data]

ytick_data = ytick_data[3:]
ytick_labels = ytick_labels[3:]

plot_sizes(datasets, labels, ordering, title='SuiteSparse Matrix Collection', y_title='File Size (Bytes)', x_title='Matrix Index', yticks = (ytick_data,ytick_labels))

print(ytick_data)
print(ytick_labels)

for matrix in ordering:
    if binsparse_coo_gzip9_aux[matrix] > mtx_noz_aux[matrix]:
        print('%s: %s' % (matrix, pretty_print_size(binsparse_coo_gzip9_aux[matrix] - mtx_noz_aux[matrix])))
