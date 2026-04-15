import csv
import json
import sys
import numpy as np
from sklearn.preprocessing import StandardScaler, MultiLabelBinarizer
from sklearn.neighbors import NearestNeighbors
import umap

CSV_FILE = "docs/wines.csv"
OUTPUT_FILE = "docs/wines_3d.json"

NUMERIC_FIELDS = [
    "alcohol", "price", "visible_depth", "smell_intensity",
    "flavor_intensity", "acidity", "tannins", "body",
    "dryness", "length", "warmth", "rating"
]

BINARY_FIELDS = ["sparkling", "fortified"]

CATEGORICAL_FIELDS = ["country", "region", "grape", "color"]


def load_csv():
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def safe_float(val, default=0.0):
    try:    return float(val)
    except: return default


def safe_int(val, default=0):
    try:    return int(val)
    except: return default


def build_vectors(wines):
    # Numeric features:
    numeric = np.array([
        [safe_float(w.get(f, "")) for f in NUMERIC_FIELDS]
        for w in wines
    ])

    alc_idx = NUMERIC_FIELDS.index("alcohol")
    numeric[:, alc_idx] = numeric[:, alc_idx] / 100.0

    price_idx = NUMERIC_FIELDS.index("price")
    numeric[:, price_idx] = np.log1p(numeric[:, price_idx])

    numeric = StandardScaler().fit_transform(numeric)

    # Binary features:
    binary = np.array([
        [safe_float(w.get(f, "0")) for f in BINARY_FIELDS]
        for w in wines
    ])

    # Multi-label binarize smells and flavors:
    smells  = [w.get("smells", "").split("|")  for w in wines]
    flavors = [w.get("flavors", "").split("|") for w in wines]

    mlb_smells  = MultiLabelBinarizer()
    mlb_flavors = MultiLabelBinarizer()
    smell_matrix  = mlb_smells.fit_transform(smells)
    flavor_matrix = mlb_flavors.fit_transform(flavors)

    # One-hot encode categoricals:
    cat_matrices = []

    for field in CATEGORICAL_FIELDS:
        vals   = [w.get(field, "") for w in wines]
        unique = sorted(set(vals))
        lookup = {v: i for i, v in enumerate(unique)}
        onehot = np.zeros((len(wines), len(unique)))

        for i, v in enumerate(vals): onehot[i, lookup[v]] = 1.0

        cat_matrices.append(onehot)

    return np.hstack([numeric, binary, smell_matrix, flavor_matrix, *cat_matrices])  # type: ignore


def reduce_to_3d(X):
    n_neighbors = max(2, len(X) - 1) if len(X) < 15 else 15

    reducer = umap.UMAP(
        n_components=3,
        n_neighbors=n_neighbors,
        min_dist=0.1,
        metric="euclidean",
        random_state=42
    )
    return reducer.fit_transform(X)


def find_neighbors(X, k=5):
    k = min(k, len(X) - 1)

    if k < 1: return [[] for _ in range(len(X))]

    nn = NearestNeighbors(n_neighbors=k + 1, metric="cosine").fit(X)
    _, indices = nn.kneighbors(X)

    return [row[1:].tolist() for row in indices]


def export(wines, coords, neighbors):
    output = []

    for i, w in enumerate(wines):
        output.append({
            "country":          w.get("country", ""),
            "region":           w.get("region", ""),
            "grape":            w.get("grape", ""),
            "producer":         w.get("producer", ""),
            "vintage":          w.get("vintage", ""),
            "alcohol":          safe_float(w.get("alcohol", "")),
            "price":            safe_float(w.get("price", "")),
            "visible_depth":    safe_float(w.get("visible_depth", "")),
            "color":            w.get("color", ""),
            "sparkling":        safe_int(w.get("sparkling", "0")),
            "fortified":        safe_int(w.get("fortified", "0")),
            "smells":           [s for s in w.get("smells", "").split("|") if s],
            "smell_intensity":  safe_float(w.get("smell_intensity", "")),
            "flavors":          [f for f in w.get("flavors", "").split("|") if f],
            "flavor_intensity": safe_float(w.get("flavor_intensity", "")),
            "acidity":          safe_float(w.get("acidity", "")),
            "tannins":          safe_float(w.get("tannins", "")),
            "body":             safe_float(w.get("body", "")),
            "dryness":          safe_float(w.get("dryness", "")),
            "length":           safe_float(w.get("length", "")),
            "warmth":           safe_float(w.get("warmth", "")),
            "rating":           safe_int(w.get("rating", "")),
            "x": float(coords[i, 0]),
            "y": float(coords[i, 1]),
            "z": float(coords[i, 2]),
            "neighbors": neighbors[i],
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"Exported {len(output)} wines → {OUTPUT_FILE}")


def main():
    wines = load_csv()

    if len(wines) < 3:
        print(f"Need at least 3 wines in {CSV_FILE} (found {len(wines)}).")
        sys.exit(1)

    print(f"Loaded {len(wines)} wines.")

    X = build_vectors(wines)
    print(f"Feature vector dimensionality: {X.shape[1]}")

    coords = reduce_to_3d(X)
    neighbors = find_neighbors(X)
    export(wines, coords, neighbors)


if __name__ == "__main__":
    main()
