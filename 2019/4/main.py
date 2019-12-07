def has_double_digits(p: str):
    i = 0
    while i < len(p) - 1:
        if p[i] == p[i+1]:
            return True
        i += 1
    return False


def has_double_digits_2(p: str):
    i = 0
    while i < len(p) - 1:
        if p[i] == p[i+1]:
            if i == 0 or p[i] != p[i-1]:
                if i == len(p) - 2 or p[i] != p[i+2]:
                    return True
        i += 1
    return False


def digits_increase(p: str):
    i = 0
    while i < len(p) - 1:
        if int(p[i]) > int(p[i+1]):
            return False
        i += 1
    return True


def count_valid():
    valid_count = 0
    current = 235741
    while current <= 706948:
        p_str = str(current)
        if has_double_digits_2(p_str) and digits_increase(p_str):
            valid_count += 1
           # print(p_str)
        current += 1

    print("Valid: " + str(valid_count))


count_valid()
