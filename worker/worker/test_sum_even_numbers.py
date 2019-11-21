from tasks import sum_even_numbers


def test_sum_even_numbers():
    assert sum_even_numbers(bytes("10 5 20 3 2 14 7 8", "utf-8")) == 54
