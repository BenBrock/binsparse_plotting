from plotting import *


def print_data(matrix_data):
    for matrix in matrix_data.keys():
        runtime = matrix_data[matrix]['runtime']
        bandwidth = matrix_data[matrix]['bandwidth']
        print('%s has runtime %.3f s (SD %.3f, %.3f -> %.3f) and BW %.3f MiB/s (SD %.3f, %.3f -> %.3f)' % (matrix, np.mean(runtime), np.std(runtime), np.min(runtime), np.max(runtime), np.mean(bandwidth)*1024, np.std(bandwidth)*1024, np.min(bandwidth)*1024, np.max(bandwidth)*1024))


matrix_nnz = read_nnz('matrix_nnzs.csv')

cutoff = 1000000

# Size of MatrixMarket File
mtx_noz_noaux = read_dataset('mtx_noz_noaux.csv')

mtx_noz_noaux = read_dataset('mtx_noz_noaux.csv')

# Read times for Coo GZIP1
mtx_coo_noz = read_and_clean_benchmark_data('sloth/warm_read/br_mtx_noz.out')
binsparse_coo_noz = read_and_clean_benchmark_data('sloth/warm_read/br_coo_noz.out')
binsparse_coo_gzip1 = read_and_clean_benchmark_data('sloth/warm_read/br_coo_gz1.out')
binsparse_csr_noz = read_and_clean_benchmark_data('sloth/warm_read/br_csr_noz.out')
binsparse_csr_gzip1 = read_and_clean_benchmark_data('sloth/warm_read/br_csr_gz1.out')
mtx_mt = read_and_clean_benchmark_data('sloth/warm_read/br_mtx_noz_multithreaded_warm.out')

binsparse_coo_noz_mt = read_and_clean_benchmark_data('sloth/warm_read_mt/br_coo_noz.out')
binsparse_coo_gzip1_mt = read_and_clean_benchmark_data('sloth/warm_read_mt/br_coo_gz1.out')
binsparse_csr_noz_mt = read_and_clean_benchmark_data('sloth/warm_read_mt/br_csr_noz.out')
binsparse_csr_gzip1_mt = read_and_clean_benchmark_data('sloth/warm_read_mt/br_csr_gz1.out')

# Order by NNZ
# ordering = [x[0] for x in sorted(matrix_nnz.items(), key=lambda x: x[1], reverse=True) if matrix_nnz[x[0]] >= cutoff]

# Order by MTX file size
# ordering = [x[0] for x in sorted(mtx_noz_noaux.items(), key=lambda x: x[1], reverse=True) if matrix_nnz[x[0]] >= cutoff]

# Order by MTX read time
ordering = [x[0] for x in sorted(mtx_coo_noz.items(), key=lambda x: x[1], reverse=True) if matrix_nnz[x[0]] >= cutoff]

datasets = [mtx_coo_noz, binsparse_coo_gzip1, binsparse_csr_gzip1, binsparse_coo_noz, binsparse_csr_noz, mtx_mt, binsparse_coo_gzip1_mt, binsparse_csr_gzip1_mt, binsparse_coo_noz_mt, binsparse_csr_noz_mt]
labels = ['mtx_noz_noaux', 'binsparse_coo_gzip1', 'binsparse_csr_gzip1', 'binsparse_coo_noz', 'binsparse_csr_noz', 'mtx_mt', 'binsparse_coo_gzip1_mt', 'binsparse_csr_gzip1_mt', 'binsparse_coo_noz_mt', 'binsparse_csr_noz_mt']

colors = ['C0', 'C3', 'C4', 'C1', 'C2', 'C5', 'C6', 'C7', 'C8', 'C9']

datasets = datasets[5:]
labels = labels[5:]
colors = colors[5:]

ytick_data = [0.006, 0.03, 0.18, 1, 6, 30, 180]
ytick_data = [0.001, 0.01, 0.1, 1, 10, 100]
ytick_labels = [pretty_print_time(time, True) for time in ytick_data]

xtick_data = [x * 1024 * 1024 for x in [16, 64, 256, 1024, 4096, 16384, 65536]]
xtick_labels = [pretty_print_size(x) for x in xtick_data]

plot_sizes_logx(mtx_noz_noaux, datasets, labels, ordering, title='Parallel Read Times (Warm Cache)', y_title='Runtime', x_title='Matrix Market File Size', yticks = (ytick_data, ytick_labels), xticks = (xtick_data, xtick_labels), colors=colors, fname='out.pdf')

print_speedups(datasets, labels, ordering, mtx_coo_noz)

print_statistics(['sloth/warm_read/br_coo_gz1.out', 'sloth/warm_read/br_coo_noz.out', 'sloth/warm_read/br_csr_gz1.out', 'sloth/warm_read/br_csr_noz.out', 'sloth/warm_read/br_mtx_noz.out', 'sloth/warm_read/br_mtx_noz_multithreaded_warm.out', 'sloth/warm_read_mt/br_coo_noz.out', 'sloth/warm_read_mt/br_coo_gz1.out', 'sloth/warm_read_mt/br_csr_noz.out', 'sloth/warm_read_mt/br_csr_gz1.out'], ordering)
