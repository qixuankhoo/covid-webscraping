import difflib

f_map = {}
g_map = {}

#with open("Louisiana/data/2020-6-20/st_tammany.txt") as f, open("Louisiana/data/2020-07-14/st_tammany.txt") as g:
#with open("test/thing1.txt") as f, open("test/thing2.txt") as g:
with open("test/black_hawk_06_23.txt") as f, open("test/black_hawk_07_14.txt") as g:
#with open("test/test1.txt") as f, open("test/test2.txt") as g:
    flines = f.readlines()
    glines = g.readlines()

    for i, line in enumerate(flines):
        stripped_line = line.lstrip().rstrip()
        if len(stripped_line) > 4:
            f_map[stripped_line] = 1
    for i, line in enumerate(glines):
        stripped_line = line.lstrip().rstrip()
        if len(stripped_line) > 4:
            g_map[stripped_line] = 1
    

    
    with open("test/out1.txt", "w") as fout, open("test/out2.txt", "w") as gout:
        fout.write(str(f_map))
        gout.write(str(g_map))

    for line in f_map.keys():
        if line not in g_map:
            print("\n\n- " + line)
    
    for line in g_map.keys():
        if line not in f_map:
            print("\n\n+ " + line)
        
'''

#with open("Louisiana/data/2020-6-20/st_tammany.txt") as f, open("Louisiana/data/2020-07-14/st_tammany.txt") as g:
#with open("test/thing1.txt") as f, open("test/thing2.txt") as g:
with open("test/black_hawk_06_23.txt") as f, open("test/black_hawk_07_14.txt") as g:
#with open("test/test1.txt") as f, open("test/test2.txt") as g:
    flines = f.readlines()
    glines = g.readlines()

    for i, line in enumerate(flines):
        flines[i] = line.lstrip().rstrip()
    for i, line in enumerate(glines):
        glines[i] = line.lstrip().rstrip()

    flines = [x for x in flines if len(x) > 4]
    glines = [x for x in glines if len(x) > 4]
    
    with open("test/out1.txt", "w") as fout, open("test/out2.txt", "w") as gout:
        fout.write(str(flines))
        gout.write(str(glines))

    d = difflib.Differ()
    diffs = d.compare(flines, glines)
    for diff in diffs:
        if diff[0] == '+' or diff[0] == '-':
            print("\n\n" + diff)
'''