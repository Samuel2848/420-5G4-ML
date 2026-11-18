# Repository notes

- Three independent parts (root README only maps them): `apprentissage/` (Pokémon notebooks), `analyse_image/` (Fashion-MNIST CNN notebooks), `agent/` (C++17 CMake library CLI). There is no root build/test/lint command.
- No CI, test targets, pre-commit, lockfile, or lint/typecheck config. Verification is: build `agent/`; execute only the affected notebook(s).

## C++ `agent/`

- Build: `cmake -S agent -B agent/build && cmake --build agent/build` (or documented `cd agent && mkdir build && cd build && cmake .. && make`). Output: `agent/build/bibliotheque`; `agent/build/` is ignored/generated.
- CMake requires >=3.21, C++17, uses `file(GLOB "*.cpp")`; rerun CMake after adding/removing `.cpp` files. Warnings are `-Wall -Wextra -Wpedantic`.
- Run: `./agent/build/bibliotheque -d agent/data` (also `--data-dir`). Paths are relative to the process cwd; without `-d` the app starts with empty filenames and saves fail.
- The CLI reads `data/books.txt` and `data/users.txt` at startup and overwrites both on menu "12" or quit "0"; use a copy of `agent/data/` when testing destructive flows.
- It is a terminal/menu app (French prompts). X11 forwarding in `agent/.devcontainer/` is environment convenience, not a GUI dependency.

## Notebooks

- Notebook cwd matters: all data/model paths are relative to the notebook's own directory. Jupyter/VS Code works; running from repo root via nbconvert needs an explicit cwd.
- `apprentissage/`: tracked data and model, so parts can run standalone. Order: `partie1_2.ipynb` (generates tracked `data/dataset.csv` with a leading index column) -> `partie3_entrainement.ipynb` (writes `modele/modele_pokemon.mod`) -> `partie3_predictions.ipynb`.
- `analyse_image/`: `classification.ipynb` -> `test_model.ipynb`. `analyse_image/datas/` is gitignored and untracked; Fashion-MNIST CSVs must be provided locally. The IDX files there are digit MNIST and unused despite the name.
- Tracked `analyse_image/modele/modele.json` + `modele.weights.h5` let `test_model.ipynb` run without training. Re-running `classification.ipynb` overwrites them with Model A only (not the larger Model B).
- Only `analyse_image/requirements.txt` exists (unpinned, 6 packages); notebooks also use `seaborn`, `joblib`, and Pillow. The checked-in `.venv/` is Windows/ignored; recreate it on Linux. `classification.ipynb` uses `ImageDataGenerator`, which current Keras releases have deprecated/removed; AVIF input needs a Pillow build with AVIF support.

## Environment gotchas

- Workspace opened at repo root uses the minimal root `.devcontainer/` (currently untracked); `.vscode/settings.json` hardcodes `cmake.sourceDirectory` to `/workspaces/420-5G4-ML/agent`. The X11/CMake-3.22.2 devcontainer in `agent/.devcontainer/` applies only when `agent/` itself is the VS Code workspace folder.
- Many tracked files show as modified due to CRLF-only changes (no `.gitattributes`); check real edits with `git diff --ignore-cr-at-eol` before staging.
- Keep French identifiers/messages in the C++ and notebooks; repo docs and code are French.
Verification after writing: re-read AGENTS.md, run git diff -- AGENTS.md, and confirm no other files were changed (especially no line-ending churn).