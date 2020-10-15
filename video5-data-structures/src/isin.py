def test_is_in():
    assert is_in([1,2,3], 3)
    assert not is_in([1,2,3], 4)

def is_in(lst, target):
    for value in lst:
        if value == target:
            return True
    return False

