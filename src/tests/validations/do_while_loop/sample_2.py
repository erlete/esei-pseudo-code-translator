def main():
    x = 0
    y = 0
    x = x + 1
    y = y + 1
    print(x, y)
    while y < 10:
        y = y + 1
        print(x, y)
    while x < 10:
        print(x)

    while x < 10:
        x = x + 1
        y = y + 1
        print(x, y)
        while y < 10:
            y = y + 1
            print(x, y)
        while x < 10:
            print(x)


main()
