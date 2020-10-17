def test_isin():
    isin_bisect = isin_recursive
    assert isin_bisect([1,2,3], 3)
    assert isin_bisect([1,2,3], 2)
    assert isin_bisect([1,2,3], 1)
    assert isin_bisect([1,2,2,2,3], 2)
    assert not isin_bisect([1,2,3,3,3,10], 4)

        
def isin_recursive(seq, val, start=0, end=None):
    end = end if end is not None else len(seq)

    if not end - start > 1:
        return len(seq)>0 and (seq[start] == val)

    mid = (start + end) // 2
    if seq[mid] <= val:
        return isin_recursive(seq, val, mid, end)
    else:
        return isin_recursive(seq, val, start, mid)
        