import csv
import os

try:
    from prompt_toolkit import prompt as pt_prompt
    from prompt_toolkit.completion import WordCompleter
    HAS_PT = True

except ImportError:
    HAS_PT = False


CSV_FILE = r"C:\Users\zvanh\Downloads\Classwork\25-26\Spring\HSPT-160\wines-project\docs\wines.csv"

FIELDS = [
    "country", "region", "grape", "producer", "vintage",
    "alcohol", "price", "visible_depth", "color", "sparkling", "smells", "smell_intensity",
    "flavors", "flavor_intensity", "acidity", "tannins", "body", "dryness",
    "length", "warmth", "rating"
]

SCALE_STEPS   = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
RATING_VALUES = [-2, 0, 1, 2]

COUNTRIES = [
    "Argentina", "Australia", "Austria", "Chile", "China", "France",
    "Georgia", "Germany", "Greece", "Hungary", "Israel", "Italy",
    "Lebanon", "New Zealand", "Portugal", "South Africa", "Spain",
    "United States", "Uruguay",
]

REGIONS = [
    "Alsace", "Barossa Valley", "Bordeaux", "Burgundy", "Champagne",
    "Chianti", "Columbia Valley", "Douro Valley", "Finger Lakes",
    "Loire Valley", "Marlborough", "Mendoza", "Mosel", "Napa Valley",
    "Oregon", "Piedmont", "Rheingau", "Rhône Valley", "Rioja",
    "Sonoma", "Stellenbosch", "Tuscany", "Wachau", "Willamette Valley",
]

GRAPES = [
    "Albariño", "Barbera", "Cabernet Franc", "Cabernet Sauvignon",
    "Carménère", "Chardonnay", "Chenin Blanc", "Gamay", "Gewürztraminer",
    "Grenache", "Grüner Veltliner", "Malbec", "Marsanne", "Merlot",
    "Mourvèdre", "Muscat", "Nebbiolo", "Petit Verdot", "Petite Sirah",
    "Pinot Blanc", "Pinot Gris", "Pinot Noir", "Pinotage", "Primitivo",
    "Riesling", "Sangiovese", "Sauvignon Blanc", "Sémillon", "Syrah",
    "Tempranillo", "Torrontés", "Touriga Nacional", "Trebbiano",
    "Verdejo", "Vermentino", "Viognier", "Zinfandel",
]

COLORS = [
    "water white", "pale straw", "straw", "golden straw", "gold",
    "deep gold", "amber", "pale salmon", "salmon", "pink",
    "copper", "pale ruby", "ruby", "deep ruby", "garnet",
    "purple", "deep purple", "brick red", "tawny", "brown",
]

SMELL_FLAVOR_VOCAB = [
    "almond", "apple", "apricot", "banana", "blackberry", "blackcurrant",
    "blueberry", "butter", "caramel", "cassis", "cedar", "cherry",
    "chocolate", "cinnamon", "citrus", "clove", "cocoa", "coconut",
    "coffee", "cranberry", "cream", "earth", "elderflower", "eucalyptus",
    "fig", "flint", "ginger", "gooseberry", "grapefruit", "grass",
    "green apple", "green pepper", "hay", "hazelnut", "herbs", "honey",
    "jam", "jasmine", "lavender", "leather", "lemon", "licorice",
    "lime", "lychee", "mango", "melon", "mineral", "mint", "mushroom",
    "nutmeg", "oak", "olive", "orange", "passion fruit", "peach",
    "pear", "pepper", "petrol", "pine", "plum", "prune", "raisin",
    "raspberry", "rose", "sage", "smoke", "spice", "stone fruit",
    "strawberry", "tar", "thyme", "tobacco", "toast", "toffee",
    "tropical fruit", "truffle", "vanilla", "violet", "walnut", "wood",
]


def load_wines():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_wines(wines):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(wines)


def _input(prompt_text, completer_words=None):
    """
    Wraps prompt_toolkit for tab-completion when available, falls back to input().
    """
    if HAS_PT and completer_words:
        completer = WordCompleter(completer_words, ignore_case=True, sentence=True) # type: ignore
        return pt_prompt(f"  {prompt_text}: ", completer=completer).strip() # type: ignore
    
    return input(f"  {prompt_text}: ").strip()


def ask_yes_no(label, default=False):
    default_str = "y" if default else "n"
    while True:
        raw = input(f"  {label} [y/n] [{default_str}]: ").strip().lower()
        if not raw:
            return "1" if default else "0"
        
        if raw in ("y", "yes"):
            return "1"
        
        if raw in ("n", "no"):
            return "0"
        
        print("    Please enter y or n.")


def ask_str(label, default=None, completions=None):
    show = f" [{default}]" if default else ""
    val = _input(f"{label}{show}", completions)
    return val if val else default


def ask_int(label, default=None, choices=None):
    show = f" [{default}]" if default is not None else ""

    while True:
        raw = input(f"  {label}{show}: ").strip()
        if not raw: return default

        try:
            n = int(raw)

            if choices and n not in choices:
                print(f"    Must be one of {choices}. Try again.")
                continue

            return n
        
        except ValueError:
            print(f"    Not a valid integer. Try again.")


def ask_float(label, default=None, lo=None, hi=None):
    show = f" [{default}]" if default is not None else ""

    while True:
        raw = input(f"  {label}{show}: ").strip()
        if not raw: return default

        try:
            n = float(raw)

            if lo is not None and n < lo:
                print(f"    Must be >= {lo}. Try again.")
                continue

            if hi is not None and n > hi:
                print(f"    Must be <= {hi}. Try again.")
                continue

            return n
        
        except ValueError:
            print(f"    Not a valid number. Try again.")


def ask_scale(label, default=None):
    show = f" [{default}]" if default is not None else ""

    while True:
        raw = input(f"  {label} {SCALE_STEPS}{show}: ").strip()
        if not raw: return default

        try:
            val = float(raw)

            if val not in SCALE_STEPS:
                print(f"    Must be one of {SCALE_STEPS}. Try again.")
                continue

            return val
        
        except ValueError:
            print(f"    Not a valid number. Try again.")


def ask_list(label, default=None, completions=None):
    """
    Comma-separated list. Each item gets tab-completion individually.
    """
    show = f" [{default}]" if default else ""

    if HAS_PT and completions:
        completer = WordCompleter(completions, ignore_case=True) # type: ignore
        raw = pt_prompt(f"  {label} (comma-separated){show}: ", completer=completer).strip() # type: ignore

    else:
        raw = input(f"  {label} (comma-separated){show}: ").strip()

    if not raw: return default
    items = [s.strip() for s in raw.split(",") if s.strip()]
    return "|".join(items) if items else default


def prompt_wine(defaults=None):
    d = defaults or {}

    def d_str(key):
        return d.get(key) or None

    def d_num(key):
        val = d.get(key)
        if val is None or val == "":
            return None
        
        try:    return float(val)
        except: return None

    def d_int(key):
        val = d.get(key)
        if val is None or val == "":
            return None
        
        try:    return int(val)
        except: return None

    # Build completions from existing wines + built-in lists
    wines = load_wines()
    countries_ext   = sorted(set(COUNTRIES   + [w["country"]  for w in wines if w.get("country")]))
    regions_ext     = sorted(set(REGIONS     + [w["region"]   for w in wines if w.get("region")]))
    grapes_ext      = sorted(set(GRAPES      + [w["grape"]    for w in wines if w.get("grape")]))
    colors_ext      = sorted(set(COLORS      + [w["color"]    for w in wines if w.get("color")]))
    producers_ext   = sorted(set(              [w["producer"]  for w in wines if w.get("producer")]))
    smells_flavs    = sorted(set(SMELL_FLAVOR_VOCAB
        + [t for w in wines for t in (w.get("smells", "") + "|" + w.get("flavors", "")).split("|") if t]
    ))

    wine = {}
    wine["producer"]         = ask_str("Producer", d_str("producer"), producers_ext)
    wine["country"]          = ask_str("Country", d_str("country"), countries_ext)
    wine["region"]           = ask_str("Region", d_str("region"), regions_ext)
    wine["vintage"]          = ask_int("Vintage", d_int("vintage"))
    wine["grape"]            = ask_str("Grape", d_str("grape"), grapes_ext)
    wine["alcohol"]          = ask_float("Alcohol %", d_num("alcohol"), lo=0, hi=100)
    wine["price"]            = ask_float("Price $", d_num("price"), lo=0)
    wine["visible_depth"]    = ask_scale("Depth", d_num("visible_depth"))
    wine["color"]            = ask_str("Color", d_str("color"), colors_ext)
    wine["sparkling"]        = ask_yes_no("Sparkling?", default=False)
    wine["smells"]           = ask_list("Smells", d_str("smells"), smells_flavs)
    wine["smell_intensity"]  = ask_scale("Smell intensity", d_num("smell_intensity"))
    wine["flavors"]          = ask_list("Flavors", d_str("flavors"), smells_flavs)
    wine["flavor_intensity"] = ask_scale("Flavor intensity", d_num("flavor_intensity"))
    wine["acidity"]          = ask_scale("Acidity", d_num("acidity"))
    wine["tannins"]          = ask_scale("Tannins", d_num("tannins"))
    wine["body"]             = ask_scale("Body", d_num("body"))
    wine["dryness"]          = ask_scale("Dryness", d_num("dryness"))
    wine["length"]           = ask_scale("Length", d_num("length"))
    wine["warmth"]           = ask_scale("Warmth", d_num("warmth"))
    wine["rating"]           = ask_int("Rating {-2, 0, 1, 2}", d_int("rating"), RATING_VALUES)

    # Normalize to strings for CSV:
    for k, v in wine.items(): wine[k] = str(v) if v is not None else ""
    return wine


def display_name(w):
    parts = [w.get("grape", ""), w.get("region", ""), w.get("country", "")]
    parts = [p for p in parts if p]
    label = ", ".join(parts) if parts else "(unnamed)"
    vintage = w.get("vintage", "")

    return f"{label} ({vintage})" if vintage else label


def list_wines(wines):
    if not wines:
        print("\n  No wines in database.\n")
        return

    print()

    for i, w in enumerate(wines):
        print(f"  [{i}] {display_name(w)}")

    print()


def add_wine(wines):
    print("\n  Add a new wine (press Enter to leave blank):\n")

    try: wine = prompt_wine()
    except KeyboardInterrupt:
        print("\n  Aborted.\n")
        return

    wines.append(wine)
    save_wines(wines)
    print(f"\n  Added \"{display_name(wine)}\".\n")


def edit_wine(wines):
    list_wines(wines)
    if not wines: return

    try:
        idx = int(input("  Index to edit: ").strip())
        if not (0 <= idx < len(wines)): raise ValueError()

    except (ValueError, KeyboardInterrupt):
        print("\n  Aborted.\n")
        return

    print(f"\n  Editing \"{display_name(wines[idx])}\" (press Enter to keep current value):\n")

    try: wine = prompt_wine(defaults=wines[idx])
    except KeyboardInterrupt:
        print("\n  Aborted.\n")
        return

    wines[idx] = wine
    save_wines(wines)
    print(f"\n  Updated \"{display_name(wine)}\".\n")


def remove_wine(wines):
    list_wines(wines)
    if not wines: return

    try:
        idx = int(input("  Index to remove: ").strip())
        if not (0 <= idx < len(wines)): raise ValueError()

    except (ValueError, KeyboardInterrupt):
        print("\n  Aborted.\n")
        return

    removed = wines.pop(idx)
    save_wines(wines)
    print(f"\n  Removed \"{display_name(removed)}\".\n")


def main():
    wines = load_wines()
    actions = {"l": list_wines, "a": add_wine, "e": edit_wine, "r": remove_wine}

    print("\n  Wine Database")
    print("  ─────────────")
    print("  [l]ist [a]dd [e]dit [r]emove [q]uit\n")

    while True:
        cmd = input("  > ").strip().lower()
        if cmd == "q": break

        if cmd in actions:
            actions[cmd](wines)
            if cmd != "l": wines = load_wines()

        else:
            print("  Unknown command.\n")


if __name__ == "__main__":
    main()
