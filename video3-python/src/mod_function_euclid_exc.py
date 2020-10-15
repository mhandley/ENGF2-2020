def GCD(a,b):
    """Compute the GCD of two positive int."""
    if not (a > 0 and b > 0): 
        raise ArithmeticError("%s, %s: Must be positive int." % (a,b))
    while (b != 0):
        a, b = b, a % b
    return a

# Test cases for function
def test_euclid(): 
    ax = 42                 # Create test case 
    bx = 30                 # from simple example.
    assert GCD(ax,bx) == 6  # Turn test print, into assert
    assert GCD(bx,ax) == 6

def test_euclid_exc():
    try:
        r = GCD(5, -1)  # tiggers exception.
        assert False    # skip rest of block.
    except ArithmeticError as e:
        # Exec. except block for `Exception'
        assert "Must be positive int." in str(e)  
    except:
        assert False    # skip other blocks.
    finally:
        assert True     # Always execute finally.

import pytest
@pytest.mark.parametrize("test_inputs", 
    [(-1, 10), (10, -5), (-4, -9)])
def test_euclid_exc_raises(test_inputs):
    ax, bx = test_inputs
    with pytest.raises(Exception) as excinfo:
        GCD(ax, bx)  
    assert "Must be positive int." in str(excinfo.value)

import sys
if __name__ == "__main__":
    try:
        # Take the two first command-line args, as integers.
        ax = int(sys.argv[1])
        bx = int(sys.argv[2])
        print(GCD(ax, bx))
    except IndexError:
        print("Euclid requires two arguments.")
    except ValueError:
        print("Euclid requires two integers.")
    except ArithmeticError:
        print("Euclid requires positive integers.")
