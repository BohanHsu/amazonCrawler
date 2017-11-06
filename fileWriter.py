def writeLinesToFIle(lines, filename):
    f = open(filename, 'w')
    for line in lines:
        f.write(line)

    f.close()
