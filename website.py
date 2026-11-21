from flask import Flask, request
from support.parser import parse_equation

from tests.helpers.balance import check_is_balanced

from src.solver import balance_equation
from src.elements import get_all_atoms

app = Flask(__name__)

UPPER = 1
LOWER = 2
NUMBER = 3

DIG_TO_SUBSCRIPT = {"0": "\u2080", "1": "\u2081",
                    "2": "\u2082", "3": "\u2083",
                    "4": "\u2084", "5": "\u2085",
                    "6": "\u2086", "7": "\u2087",
                    "8": "\u2088", "9": "\u2089"}


HEADER = "<h1 style='margin-top: 100px; margin-bottom: 10px; text-align: center; color: purple'>Chemical Equation Balancer</h1><style>li { margin-left: -25px; }</style>"
FORM = '''
<form action="/input" method="post" style='text-align: center'> 
  <input
    id="reactants"
    name="reactants" 
    placeholder="H2 + O2" 
    style="width: 200px"
  >
  &rarr;
  <input 
    id="products"
    placeholder="H2O"
    name="products"
    style="width: 200px"
  >
  &nbsp;&nbsp;&nbsp;&nbsp;
  <input type="submit" value="Balance">
</form>
<hr>
'''
HISTORY_HEADER = "<h3 style='margin-top: 100px; margin-bottom: 10px; text-align: center; color: black'>History:</h3><style>li { margin-left: -25px; }</style>"

history: list[str] = []


def page(msg: str) -> str:
    result: str = HEADER + FORM

    is_new_msg: bool = msg and msg not in history

    if is_new_msg:
        result += f"<p style='text-align: center'>{msg}</p>"

    if msg or history:
        result += "<hr>"
    
    result += HISTORY_HEADER
    result += "<ul style='list-style-position: inside;'>"
    for element in history:
        result += f"<li style='text-align: center'>{element}</li>"
    result += "</ul>"
    if msg or history:
        result += "<br><br>"

    if is_new_msg:
        history.append(msg)

    return result


def error(msg, r, p):
    reactsd: str = display_side(r)
    prodsd: str = display_side(p)
    return page(
        f"<b style='color: #E30B5D;'>{reactsd} &rarr; {prodsd}</b> " + msg
    )


def letter_type(x: str):
    if len(x) == 0:
        return None
    else:
        x = x[0]
    if x.isupper():
        return UPPER
    elif x.islower():
        return LOWER
    elif x.isnumeric():
        return NUMBER


def split(element):
    element = list(element)
    if not element:
        return []
    partial = element.pop(0)
    prev_type = letter_type(partial)
    result = []
    while element or partial:
        next_type = letter_type(element)
        if not next_type or next_type == UPPER or\
           (prev_type != NUMBER and next_type == NUMBER):
            result.append(partial)
            partial = ""
        if element:
            partial += element.pop(0)
        prev_type = next_type
    return result


def display(element):
    element = split(element)
    result = ""
    for i in element:
        if letter_type(i) != NUMBER:
            result += f"{i}"
        else:
            result += f"<sub>{i}</sub>"
    return result


def display_side(sidestr: str, sol=None):
    side: list[str] = sidestr.replace(" ", "").split("+")
    for i in range(len(side)):
        side[i] = display(side[i])
        if sol and sol[i] != 1:
            side[i] = str(sol[i]) + side[i]
    return " + ".join(side)


def digits_to_subscript(input_side: str) -> str:
    data = ""
    for character in input_side:
        if character.isdigit():
            data += DIG_TO_SUBSCRIPT[character]
        else:
            data += character
    return data


@app.route("/input", methods=['POST'])
def balance():
    reactant_form_input: str = request.form['reactants']
    product_form_input: str = request.form['products']
    reactant_form_data: str = digits_to_subscript(reactant_form_input)
    product_form_data: str = digits_to_subscript(product_form_input)

    eqn = reactant_form_data + " \u2192 " + product_form_data
    reacts, prods = parse_equation(eqn, False)
    reacts_dictify, prods_dictify = parse_equation(eqn, True)
    if reacts_dictify == prods_dictify:
        return page(f"The balanced equation is <b style=\"color: blue;\">{reactant_form_data} &rarr; {product_form_data}</b>.")
    atoms1 = get_all_atoms(reacts_dictify)
    atoms2 = get_all_atoms(prods_dictify)
    if not atoms1 or set(atoms1) != set(atoms2):
        return error(
            "is not a valid chemical equation.",
            reactant_form_data,
            product_form_data
        )

    sol = balance_equation(eqn)
    invalid = False
    if sol:
        try:
            check_is_balanced(eqn, sol)
        except AssertionError:
            invalid = True

    if invalid or not sol or float('inf') in sol or float('nan') in sol:
        return error(
            "does not have a valid solution.",
            reactant_form_data,
            product_form_data
        )

    react_str: str = " + ".join([(str(sol[x])
                                if sol[x] != 1 else "") + x for x in reacts])
    prod_str: str = " + ".join([(str(sol[x]) if sol[x] !=
                                 1 else "") + x for x in prods])

    return page(f"The balanced equation is <b style=\"color: blue;\">{react_str} &rarr; {prod_str}</b>.")


@app.route("/")
def homepage():
    return page("")


app.run(host='0.0.0.0', port=1024, debug=True)
