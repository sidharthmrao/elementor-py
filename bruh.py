import pickle

single_reference = {
    'A': 'w',
    'W': 'l',
    'E': 'y',
    'F': 'r',
}

double_reference = {
    'A': {
        'A': 'f',
        'W': 'm',
        'E': 'p',
        'F': 'b',
    },
    'W': {
        'W': 'n',
        'E': 't',
        'F': 'd',
    },
    'E': {
        'E': 'c',
        'F': 'j',
    },
    'F': {
        'F': 'g',
    }
}

triple_reference = {
    'A': 'i',
    'W': 'u',
    'E': 'e',
    'F': 'o',
}

quad_reference = {
    'A': 'Y',
    'W': 's',
    'E': 'h',
    'F': 'N',
}

try:
    f = open("saved_elements.pickle", "rb")
    elements = pickle.load(f)
    f.close()
except:
    elements = {
        'A': {
            "root": "A",
            "base": "A",
            "lang": "",
        },
        'W': {
            "root": "W",
            "base": "W",
            "lang": "",
        },
        'E': {
            "root": "E",
            "base": "E",
            "lang": "",
        },
        'F': {
            "root": "F",
            "base": "F",
            "lang": "",
        },
    }


def analyze_syllable(syllable):
    pass

def compile_values(values: list):
    if not all(value in elements.keys() for value in values):
        for value in values:
            if value not in elements.keys():
                print(f"{value} not found, please initialize this item before using it to make another.")
    else:
        values_root = sorted([''.join(elements[values[0]]["root"]), ''.join(elements[values[1]]["root"])])
        if values_root[0] == values_root[1]:
            elements[values]["root"] = values_root[0]+"2"
        else:
            value_0_split = values_root[0].split(")")[-1][:-1]
            value_1_split = values_root[1].split(")")[0][1:]

            value_splits = sorted([value_0_split, value_1_split])

            if len(value_splits[0]+value_splits[1]) <= 4:
                combine_portion = ''.join(value_splits)
                elements[values]["root"] = combine_portion

            else:
                elements[item]["root"] = ["(" + ''.join(elements[value]["root"]) + ")" for value in values]


def print_item(item: str):
    print("___")
    print(elements[item]["root"])
    print('+'.join(elements[item]["base"]))
    print("‾‾‾")


def set_item(item: str, values: list):
    elements[item] = {
        "root": "",
        "base": values,
        "lang": ""
    }

    if len(values) == 1 and values[0] in elements.keys():
        elements[item]["root"] = elements[values[0]]["root"]
    elif all(value in elements.keys() for value in values):
        elements[item]["root"] = ["(" + ''.join(elements[value]["root"]) + ")" for value in values]
    else:
        for value in values:
            if value not in elements.keys():
                print(f"{value} not found, please initialize this item before using it to make another.")

    elements[item]["root"] = sorted(elements[item]["root"])
    elements[item]["base"] = sorted(elements[item]["base"])


while True:
    print(
        "Enter in your query in format 'val=val1+val2' to set a new item or 'val' to get data about an item. Enter 'save' to save and quit.")
    query = input()

    if "=" in query:
        query = query.split("=")

        if len(query) > 2:
            print("Invalid input. Don't use multiple '='.")
            continue

        item = query[0]
        values = query[1]
        values = values.split("+")

        if len(values) > 2:
            print("Invalid input. Only 2 items can be added to make another.")
            continue

        set_item(item, values)

    elif query in elements.keys():
        print_item(query)
    else:
        print("Item not found.")
