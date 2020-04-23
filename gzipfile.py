import gzip


with open('jikefeng.txt', 'r') as f:
    with gzip.open('jikefeng.txt.gz', 'wt') as fh:
        for i in range(10000000):
            fh.write(f.readline())
