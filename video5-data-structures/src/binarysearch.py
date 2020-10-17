def test_is_in():
    assert not is_in_bisect([], 4)
    assert is_in_bisect([1], 1)
    assert is_in_bisect([1,2,3], 3)
    assert is_in_bisect([1,2,3], 2)
    assert is_in_bisect([1,2,3], 1)
    assert is_in_bisect([1,2,3,4], 4)
    assert is_in_bisect([1,2,3,4], 3)
    assert is_in_bisect([1,2,3,4], 2)
    assert is_in_bisect([1,2,3,4], 1)
    assert is_in_bisect([1,2,2,2,3], 2)
    assert not is_in_bisect([1,2,3,3,3,10], 4)

def is_in_bisect(lst, val):
    """ Resturns True if val is within the sorted list lst. """
    if len(lst) == 0:
        return False
    start = 0          # start of search range
    end = len(lst)     # end of search range
    while end - start > 1:
        middle = (start + end) // 2
        if val >= lst[middle]:
            start = middle
        else:
            end = middle
    return lst[start] == val 
        
def test_is_in_tikz():
    array = [1,1,2,5,5,10,10,11,17,17,100,110,112,117]
    assert is_in_bisect_tikz(array, 17, r"assets/binarysearch.tex")

def is_in_bisect_tikz(seq, val,pic_name):
    """ Resturns True if val is within the sorted sequence seq. """

    f = open(pic_name, "w")
    node_names = ["n%s" % i for i in range(len(seq)+1)]

    f.write(r"\begin{tikzpicture}")
    f.write("\n")
    for i, name in enumerate(node_names):
        if i == 0:
            f.write(r"\node (%s) {%s};" % (name, seq[i]))
            f.write("\n")
            f.write(r"\draw (%s.north west) rectangle (%s.south east);" % (name,name))
            f.write("\n")
        elif i < len(seq):
            f.write(r"\node [right=0.1cm of %s] (%s) {%s};" % (node_names[i-1], name, seq[i]))
            f.write("\n")
            f.write(r"\draw (%s.north west) rectangle (%s.south east);" % (name,name))
            f.write("\n")
        else:
            f.write(r"\node [right=0.1cm of %s] (%s) {};" % (node_names[i-1], name))
            f.write("\n")
            f.write(r"\draw (%s.north west) rectangle (%s.south east);" % (name,name))
            f.write("\n")

    range_start = 0
    range_end = len(seq)
    diff = range_end - range_start

    num = 1

    f.write(r"\node<%s> [above=0.2cm of %s] (s%s) {s};" % (num, node_names[range_start], num))
    f.write(r"\node<%s> [above=0.2cm of %s] (e%s) {e};" % (num, node_names[range_end], num))
    f.write(r"\draw<%s> [->] (s%s) -- (%s);" % (num, num, node_names[range_start]))
    f.write(r"\draw<%s> [->] (e%s) -- (%s);" % (num, num, node_names[range_end]))
    num += 1 


    while (diff > 1):
        f.write(r"\node<%s> [above=0.2cm of %s] (s%s) {s};" % (num, node_names[range_start], num))
        f.write(r"\node<%s> [above=0.2cm of %s] (e%s) {e};" % (num, node_names[range_end], num))
        f.write(r"\draw<%s> [->] (s%s) -- (%s);" % (num, num, node_names[range_start]))
        f.write(r"\draw<%s> [->] (e%s) -- (%s);" % (num, num, node_names[range_end]))

        range_mid = (range_start + range_end) // 2
        if seq[range_mid] <= val:
            range_start = range_mid
        else:
            range_end = range_mid

        f.write(r"\node<%s> [above=0.2cm of %s] (m%s) {m};" % (num, node_names[range_mid], num))
        f.write(r"\draw<%s> [->] (m%s) -- (%s);" % (num, num, node_names[range_mid]))

        num += 1 

        assert diff > (range_end - range_start) # Ensure progress
        diff = range_end - range_start

    f.write(r"\node<%s> [above=0.2cm of %s] (s%s) {s};" % (num, node_names[range_start], num))
    f.write(r"\node<%s> [above=0.2cm of %s] (e%s) {e};" % (num, node_names[range_end], num))
    f.write(r"\draw<%s> [->] (s%s) -- (%s);" % (num, num, node_names[range_start]))
    f.write(r"\draw<%s> [->] (e%s) -- (%s);" % (num, num, node_names[range_end]))


    f.write(r"\end{tikzpicture}")
    f.write("\n")
    f.close()


    if len(seq)>0 and seq[range_start] == val:
        return True

    return False

