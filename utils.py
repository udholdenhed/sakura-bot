import nltk

from shared_vars import cities


def match(array: dict, city: str) -> list:
    res = []
    for i in array:
        if len(city) > 4:
            smooth = 0.2
        else:
            smooth = 0.51
        if nltk.edit_distance(city, i["city"]) / len(i["city"]) < smooth:
            res.append(i)
    return res


def find_city(city):
    result = binary_search(cities, city)
    if result is None:
        result = match(cities, city)
    return result


def binary_search(array: dict, target: str) -> str:
    start = 0
    end = len(array) - 1

    while start <= end:
        middle = (start + end) // 2
        midpoint = array[middle]["city"]
        if midpoint > target:
            end = middle - 1
        elif midpoint < target:
            start = middle + 1
        else:
            return midpoint
