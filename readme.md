# Wine Space

A 3D visualization of personal tasting notes. This project maps 70 wines tasted in and outside class into a navigable scatter plot. Each wine is encoded across 22 categories, then projected into three-dimensions so wines that ***taste alike*** end up ***near each other**.*

> One important note is that there is no rhyme or reason to the 3 axes you can navigate. That is, each represents a compression of several dimensions at once.
> Site at: [zythiq.github.io/wines-project/](https://zythiq.github.io/wines-project/)

## How It Works

Each wine is described by a mix of fields that get merged into a single high-dimensional feature vector:

- **Multi-label fields:** Smells and flavors are stored as pipe-separated strings in the CSV and binarized with `MultiLabelBinarizer`, so two wines sharing "cherry | leather" actually pull toward each other numerically.
- **12 numeric fields:** Acidity, tannins, body, dryness, length, warmth, smell/flavor intensity, visible depth, ABV, price, and personal rating.
- **4 one-hot categoricals:** Country, region, grape variety, and visual color.
- **1 binary field:** Sparkling or not.

### Dimensional Reduction

The full feature matrix gets fed into **UMAP** (`umap-learn`) targeting 3 components with euclidean distance and `min_dist=0.1`. This is what positions wines in the scatter plot. Proximity is genuine taste/profile similarity, not just one field like grape or country.

* A separate **k-nearest neighbors** pass (cosine similarity, `k=5`) records the 5 closest wines per point as neighbor edges, which get drawn as lines in the visualization.

### Frontend

Two view modes, switchable via the *Flat view* toggle:

- **3D cloud** (default)**:** **Three.js** point cloud. Each dot is a wine floating in taste-space; the closer two dots, the more alike they drink.
  - Orbit by dragging, scroll to zoom, and hover any dot to see its full tasting card. Toggle *Show edges* to draw lines to each wine's 5 nearest neighbors, *My top* to glow my personal highest-rated grape varieties (computed obviously), and the spin button to pause/play auto-rotation.
- **Flat graph:** A **Canvas 2D** force-directed layout. Nodes initialize from the UMAP x/y coordinates and then run a repulsion + spring-attraction simulation. It's the same taste-space relationships as the cloud but flattened and spread out for easier reading. Node size even scales with how often that grape appears in the dataset.
  - Drag nodes to rearrange, scroll to zoom, and right-click any node to pin its tooltip.

Points can be colored by country, grape, region, visual color (mapped to actual hex values like `#9b111e` for ruby), sparkling, price, body, acidity, tannins, dryness, or personal rating. Neighbor edges recolor to match whenever you switch the color-by scheme.

## Specifics

- **Scripting:** `Python`, `csv`, `json`, `numpy`, `scikit-learn`, `umap-learn`, `prompt_toolkit`
- **Frontend:** `HTML`, `CSS`, `JS`, `Three.js`
- **Hosting:** `GitHub Pages`

Created for the **HSPT-160** final project (Spring 2025–26) under the *Technology* track. Let me know if you like ;)
