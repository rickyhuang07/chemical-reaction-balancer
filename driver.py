from config import MY_FUNCTIONS
import reference
import sys
import importlib
import importlib.util

try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "ensurepip"])
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", 'requests'])
finally:
    import requests


EVERYTHING: list[tuple[str, int]] = [
    ('elements.get_all_atoms', 3),
    ('elements.molar_mass', 3),
    ('elements.grams_to_mols', 2),
    ('solver.make_atom_vector', 4),
    ('solver.make_compound_matrix', 3),
    ('solver.make_dummy_equation', 3),
    ('solver.make_system_of_equations', 3),
    ('solver.scale_solution', 4),
    ('solver.make_dictionary_solution', 3),
    ('solver.balance_equation', 3),
    ('matrix_operations.negate_matrix', 3),
    ('matrix_operations.transpose_matrix', 4),
    ('matrix_operations.pivot_matrix', 5),
    ('matrix_operations.scale_matrix', 5),
    ('matrix_operations.ref', 5),
    ('matrix_operations.back_substitute', 5),
    ('matrix_operations.gaussian_elimination', 3),
    ('limiting.ratio', 2),
    ('limiting.limiting_reactant', 2),
    ('chemical_yield.theoretical_yield', 2),
]


ALL_FUNCTIONS = set([x[0] for x in EVERYTHING])
REFERENCE_FUNCTIONS = ALL_FUNCTIONS - set(MY_FUNCTIONS)
assert set(MY_FUNCTIONS) - ALL_FUNCTIONS == set()
assert set(MY_FUNCTIONS) | REFERENCE_FUNCTIONS == ALL_FUNCTIONS


def get(x):
    version = ''.join(sys.version.split(" ")[0].split(".")[:-1])
    result = requests.get(
        f'https://gitlab.caltech.edu/blank/project05/-/raw/master/pyc/{x}.cpython-{version}.pyc')
    with open(f'reference/{x}.pyc', 'wb') as f:
        f.write(result.content)


cnt = 0

def load(x):
    global cnt
    try:
        spec = importlib.util.spec_from_file_location(x, f"reference/{x}.pyc")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except FileNotFoundError:
        if cnt == 0:
            cnt += 1
            get(x)
            return load(x)
        cnt = 0
        return None
    cnt = 0
    return mod


def driver_import(f):
    global reference
    if f.startswith('elements'):
        reference.elements = load("elements")
        import src.elements
    if f.startswith('matrix_operations'):
        reference.matrix_operations = load("matrix_operations")
        import src.matrix_operations
    if f.startswith('solver'):
        reference.solver = load("solver")
        import src.solver
    if f.startswith('limiting'):
        import src.limiting
        reference.limiting = load("limiting")
    if f.startswith('chemical_yield'):
        reference.chemical_yield = load("chemical_yield")
        import src.chemical_yield

    assert f in ALL_FUNCTIONS, f
    package, func = f.split(".")
    return getattr(getattr(src if f in MY_FUNCTIONS else reference, package), func)


def driver_import_reference(f):
    global reference
    if f.startswith('elements'):
        reference.elements = load("elements")
    if f.startswith('matrix_operations'):
        reference.matrix_operations = load("matrix_operations")
    if f.startswith('solver'):
        reference.solver = load("solver")
    if f.startswith('limiting'):
        reference.limiting = load("limiting")
    if f.startswith('chemical_yield'):
        reference.chemical_yield = load("chemical_yield")

    assert f in ALL_FUNCTIONS, f
    package, func = f.split(".")
    return getattr(getattr(reference, package), func)


def provide_reference_impl(func):
    """Wrapper allowing a function to use the reference implementation.

    Provides the reference implementation from the driver if func is not in config.MY_FUNCTIONS.
    """
    module_name = func.__module__.split(".")[-1]
    func_id = module_name + '.' + func.__name__
    def with_reference(*args, **kwargs):
        if func_id in MY_FUNCTIONS:
            return func(*args, **kwargs)
        else:
            ref_func = driver_import_reference(func_id)
            return ref_func(*args, **kwargs)
    return with_reference
