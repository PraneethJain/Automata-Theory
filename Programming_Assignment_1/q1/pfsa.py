import argparse
import pytest
import json


def update(string: str, dictionary: dict):
    if string in dictionary:
        dictionary[string] += 1
    else:
        dictionary.update({string: 1})


def insert(word: str, res: dict[str, dict[str, int]]) -> None:
    if len(word) == 0:
        return

    update(word[0], res["*"])

    prev = word[0]
    cur = prev
    for letter in word[1:]:
        cur += letter
        if prev in res:
            update(cur, res[prev])
        else:
            res.update({prev: {cur: 1}})
        prev = cur

    if prev in res:
        update(prev + "*", res[prev])
    else:
        res.update({prev: {prev + "*": 1}})


def construct(file_str: str) -> dict[str, dict[str, float]]:
    """Takes in the string representing the file and returns pfsa"""
    words = file_str.lower().split()

    res = {"*": {}}
    [insert(word, res) for word in words]

    for key in res:
        s = sum(res[key].values())
        res[key] = {k: v / s for k, v in res[key].items()}

    return res


def main():
    """
    The command for running is `python pfsa.py text.txt`. This will generate
    a file `text.json` which you will be using for generation.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="Name of the text file")
    args = parser.parse_args()

    with open(args.file, "r") as file:
        contents = file.read()
        output = construct(contents)

    name = args.file.split(".")[0]

    with open(f"{name}.json", "w") as file:
        json.dump(output, file)


if __name__ == "__main__":
    main()


STRINGS = ["A cat", "A CAT", "", "A", "A A A A"]
DICTIONARIES = [
    {
        "*": {"a": 0.5, "c": 0.5},
        "a": {"a*": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
    {
        "*": {"a": 0.5, "c": 0.5},
        "a": {"a*": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
    {
        "*": {},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
]


@pytest.mark.parametrize("string, pfsa", list(zip(STRINGS, DICTIONARIES)))
def test_output_match(string, pfsa):
    """
    To test, install `pytest` beforehand in your Python environment.

    Run `pytest pfsa.py` Your code must pass all tests. There are additional
    hidden tests that your code will be tested on during VIVA.
    """
    result = construct(string)
    assert result == pfsa
