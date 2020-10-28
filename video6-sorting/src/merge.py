
def mergesort(lst, compare):
    # sort lst
    if len(lst)<=1:
        return lst
    pivot = len(lst) // 2
    lst1 = mergesort(lst[:pivot], compare)
    lst2 = mergesort(lst[pivot:], compare)
    return merge(lst1, lst2, compare)

def merge(lst1, lst2, compare):
    # merge two sorted lists
    merged_list = []
    index1 = 0
    index2 = 0
    len1 = len(lst1)
    len2 = len(lst2)

    while index1 < len1 or index2 < len2:
        if index2 == len2 or \
           (index1 < len1 and compare(lst1[index1], lst2[index2])):
            merged_list.append(lst1[index1])
            index1 += 1
        else:
            merged_list.append(lst2[index2])
            index2 += 1

    return merged_list

# def test_mergesort():
#     assert(mergesort([]) == [])
#     assert(mergesort([1]) == [1])
#     assert(mergesort([1,2,3,4]) == [1,2,3,4])
#     assert(mergesort([4,3,2,1]) == [1,2,3,4])
#     assert(mergesort([5,4,3,2,1]) == [1,2,3,4,5])                

def cmp_str(s1, s2):
    return s1.lower() < s2.lower()

def test_sortstr():
    assert(mergesort(["abc"], cmp_str) == ["abc"])
    assert(mergesort(["BA", "aa", "bbbb", "a"], cmp_str) == \
           ["a", "aa", "BA", "bbbb"])
    assert(mergesort(["BAAAAA", "aa", "bbbb", "a"], \
                     lambda x, y: len(x) < len(y)) == \
           ["a", "aa", "bbbb", "BAAAAA"])
    
