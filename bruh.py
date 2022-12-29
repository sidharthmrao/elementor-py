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
    if syllable in "0123456789":
        return syllable
    match len(syllable):
        case 1:
            return single_reference[syllable] + "a"
        case 2:
            return double_reference[syllable[0]][syllable[1]] + "a"
        case 3:
            return double_reference[syllable[0]][syllable[1]] + triple_reference[syllable[2]]
        case _:
            return double_reference[syllable[0]][syllable[1]] + triple_reference[syllable[2]] + quad_reference[
                syllable[3]]


def analyze_root(root):
    if type(root) == str:
        return analyze_syllable(root)
    elif len(root) == 1:
        return analyze_syllable(root[0])
    else:
        a = analyze_root(root[0])
        b = analyze_root(root[1])

        if type(a) == str and a in "0123456789":
            if b[-1] in "aeiou":
                return b + "a"
            elif b[-1] not in "wylr":
                return b[:-1] + "a" + b[-1]
            elif b[-1] == "a":
                return b + "y"
            elif b[-2]+b[-1] == "ay":
                return b[:-1] + "w"
            elif b[-2]+b[-1] == "aw":
                return b[:-1] + "r"
            elif b[-2]+b[-1] == "ar":
                return b[:-1] + "l"
            else:
                return b

        return ''.join([analyze_root(root[0]), analyze_root(root[1])])


def compile_to_string(lis):
    if type(lis) == str:
        return lis
    elif len(lis) == 1:
        return lis[0]

    if type(lis[0]) == str:
        string_1 = lis[0]
    else:
        string_1 = compile_to_string(lis[0])
    if type(lis[1]) == str:
        string_2 = lis[1]
    else:
        string_2 = compile_to_string(lis[1])

    return string_1 + string_2


def compile_to_visual(lis):
    if type(lis) == str:
        return "(" + lis + ")"
    elif len(lis) == 1:
        return "(" + lis[0] + ")"

    return "(" + compile_to_visual(lis[0]) + compile_to_visual(lis[1]) + ")"


def check_b_greater(a, b):
    if type(a) == str and type(b) == str:
        if a in "0123456789":
            return False
        elif b in "0123456789":
            return True
        elif b.startswith(a):
            return True
        elif a.startswith(b):
            return False
        return a > b
    elif type(a) == str:
        if a in "0123456789":
            return False
        return True
    elif type(b) == str:
        if b in "0123456789":
            return True
        return False
    else:
        return check_b_greater(a[0], b[0])


def custom_sort(item: str):
    current = elements[item]["root"]

    if type(current) == str:
        return
    elif len(current) == 1:
        elements[item]["root"] = current[0]
        return

    string_1 = compile_to_string(current[0])
    string_2 = compile_to_string(current[1])

    if check_b_greater(string_1, string_2):
        elements[item]["root"] = [current[1], current[0]]
        elements[item]["base"] = [elements[item]["base"][1], elements[item]["base"][0]]


def print_item(item: str):
    print("___")
    print("ROOT: ", compile_to_visual(elements[item]["root"])[1:-1])
    print("LANG: ", elements[item]["lang"])
    print("BASE: ", '+'.join(elements[item]["base"]))
    print("‾‾‾")


def check_combinable(a, b):
    if a == b and len(compile_to_string(a)) >= 3:
        return True

    if type(a) == str and type(b) == str:
        return len(a) + len(b) <= 4 or (a == b and len(a) >= 3)
    elif type(a) == str:
        return len(a) + len(b[0]) <= 4 or (a == b[0] and len(a) >= 3)
    elif type(b) == str:
        if type(a[1]) == str:
            return len(a[1]) + len(b) <= 4 or (a[1] == b and len(b) >= 3)
        return False
    else:
        return len(a[-1]) + len(b[0]) <= 4 or (a[-1] == b[0] and len(a[-1]) >= 3)


def combined(a, b):
    if a == b and len(compile_to_string(a)) >= 3:
        return ["2", a]
    elif type(a) == str and type(b) == str:
        if a == b and len(a) >= 3:
            return ["2", a]
        return a + b
    elif type(a) == str:
        if a == b[0] and len(a) >= 3:
            return [["2", a], b[1]]
        return [a + b[0], b[1]]
    elif type(b) == str:
        if a[1] == b and len(b) >= 3:
            return [a[0], ["2", b]]
        return [a[0], a[1] + b]
    else:
        if a[1] == b[0] and len(compile_to_string(a[1])) >= 3:
            return [[a[0], ["2", a[1]]], b[1]]
        return [[a[0], a[1] + b[0]], b[1]]


def set_item(item: str, values: list):
    elements[item] = {
        "root": "",
        "base": values,
        "lang": ""
    }

    if len(values) == 1 and values[0] in elements.keys():
        elements[item]["root"] = elements[values[0]]["root"]
    elif all(value in elements.keys() for value in values):
        elements[item]["root"] = [elements[value]["root"] for value in values]

        custom_sort(item)
        current = elements[item]["root"]
        if type(current) != str:
            if len(current) > 1:
                if check_combinable(current[0], current[1]):
                    elements[item]["root"] = combined(current[0], current[1])
            else:
                elements[item]["root"] = current[0]
                elements[item]["base"] = [elements[item]["base"][0]]

    else:
        for value in values:
            if value not in elements.keys():
                print(f"{value} not found, please initialize this item before using it to make another.")

    custom_sort(item)

    elements[item]["lang"] = analyze_root(elements[item]["root"])


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
