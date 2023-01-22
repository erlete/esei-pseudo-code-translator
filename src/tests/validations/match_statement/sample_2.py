def main():
    x = 2
    match x:
        case 1: print("x is 1")
        case 2: print("x is 2")
        case 3: print("x is 3")
        case 4: print("x is 4")

        case _: print("x is not 1, 2, 3, 4")

    x = - 1
    match x:
        case 1: print("x is 1")
        case 2: print("x is 2")
        case 3: print("x is 3")
        case 4: print("x is 4")

        case _: print("x is not 1, 2, 3, 4")


main()
