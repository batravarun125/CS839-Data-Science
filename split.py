def files():
    n = 0
    while True:
        n += 1
        yield open('data/raw/%d.txt' % n, 'w')


pat = 'URL:'
fs = files()
outfile = next(fs) 
filename = 'data.txt'
with open(filename) as infile:
    for line in infile:
        if pat not in line:
            outfile.write(line)
        else:
            items = line.split(pat)
            outfile.write(items[0])
            for item in items[1:]:
                outfile = next(fs)
                outfile.write(pat + item)
