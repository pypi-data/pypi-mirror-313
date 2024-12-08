def iterate_ranges(ranges: list[tuple[int, int]]) -> list[int]:
    values = [r[0] for r in ranges]
    while True:
        yield values.copy()
        values[-1] += 1
        i = len(values) - 1
        while values[i] >= ranges[i][1]:
            if i == 0:
                return
            values[i] = ranges[i][0]
            values[i - 1] += 1
            i -= 1

def iterate_same_range(iter_range: tuple[int, int], amount: int) -> list[int]:
    return iterate_ranges([iter_range] * amount)

def iterate_numeral(base: int, amount: int) -> list[int]:
    return iterate_same_range((0, base), amount)

def bin_iter(amount: int) -> list[int]:
    return iterate_numeral(2, amount)

def ter_iter(amount: int) -> list[int]:
    return iterate_numeral(3, amount)

def dec_iter(amount: int) -> list[int]:
    return iterate_numeral(10, amount)
