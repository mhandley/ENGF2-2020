def test():
    b = 1
    c = 0
    try:
        a = b/c
        print(a)
    except NameError as e:
        print("here1:", e)
    except ZeroDivisionError as e:
        print("here2:", e)
        return
    finally:
        print("here3")
    print("here4")

test()
