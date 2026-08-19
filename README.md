# Build Your Own Git

[![shipthatcode — Build Your Own Git](https://api.shipthatcode.com/cert/e23e2b38e98c9e540da6c150abd64560.svg)](https://shipthatcode.com/courses/build-git)

My working repo for [Build Your Own Git](https://shipthatcode.com/courses/build-git) on [shipthatcode.com](https://shipthatcode.com) — built lesson by lesson in my own editor.

## What you need

- **git** and a terminal (macOS/Linux: the built-in one; Windows: see below)
- Python 3 (`python3 --version` should work)
- any editor you like — VS Code, Vim, JetBrains, anything

### On Windows

Use **WSL** if you can: run `wsl --install` in an admin PowerShell once, then do everything (git, editing, `./run_tests.sh`) inside the Ubuntu terminal — it behaves exactly like the grader.

[Git Bash](https://git-scm.com/downloads) (installs with git) also runs `./run_tests.sh`. One caveat: native Windows compilers and runtimes write Windows line endings (`\r\n`), so on byte-exact tests you can see local FAILs where the diff looks identical — your logic is fine, the invisible line endings differ. If that happens, trust **Check my solution** on the lesson page (graded on Linux), or switch to WSL.

## Getting started (one-time setup)

1. Unzip this download and open the folder in your editor.
2. Create a new **empty, public** repo at [github.com/new](https://github.com/new) — leave "Add a README" and ".gitignore" **unchecked** (this folder already has both).
3. In your terminal, inside the unzipped folder, push it to GitHub:

   ```sh
   git init
   git add .
   git commit -m "start Build Your Own Git"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
   git push -u origin main
   ```

4. Paste your repo link on the [course page](https://shipthatcode.com/courses/build-git) ("Work in your own editor" → **Link repo**). Done — you never do this again.

## The lesson loop

1. Read the lesson on shipthatcode, write your code in `main.py` here.
2. Test locally against **the lesson you're on**: `./run_tests.sh 01`, `./run_tests.sh 02`, and so on. On Windows, run this inside Git Bash. (A bare `./run_tests.sh` runs every lesson's tests, which is only useful on courses where one program answers all of them — see below.)
3. When it passes: `git add -A && git commit -m "lesson 01" && git push`
4. Hit **Check my solution** on the lesson page — shipthatcode pulls this repo and grades it against the full suite, including hidden tests.

## Project structure

The project keeps the lesson entry point small and puts reusable Git ideas in
the `pygit/` package. A lesson can import the code it needs instead of putting
all the code in one file.

```text
.
├── main.py
├── pygit/
│   ├── __init__.py
│   ├── objects.py
│   ├── store.py
│   ├── cat_file.py
│   ├── pack_header.py
│   └── tree.py
├── tests/
├── run_tests.sh
├── README.md
└── .shipthatcode.json
```

### Root files

- `main.py` — the small entry point used by the current lesson. It is kept
   empty between lessons so the reusable code stays in `pygit/`.
- `run_tests.sh` — runs the public tests for one lesson or for the whole set.
- `README.md` — project notes, setup instructions, and this structure guide.
- `.shipthatcode.json` — tells the course grader how to run the repository.

### The `pygit/` package

- `__init__.py` — marks `pygit` as a Python package.
- `objects.py` — shared Git object helpers.
   - `hash_object` builds the Git object header and returns its SHA-1 hash.
   - `parse_object` checks and splits a serialized object.
   - `get_object_path` builds the path used by a loose Git object.
- `store.py` — an early in-memory object store.
   - `MemoryStore` keeps objects by SHA-1.
   - Its methods write, read, check, and process simple store commands.
   - `run_simulator` connects the store to standard input and output.
- `cat_file.py` — the reusable model for `git cat-file` queries.
   - `CatFileStore` stores objects and handles `-e`, `-t`, `-s`, and `-p`.
   - `run_cat_file` processes the lesson input and returns its output.
- `pack_header.py` — packfile header parsing.
   - `parse_pack_header` validates the 12-byte header and reads its version and
      object count.
   - `run_pack_headers` handles hexadecimal input lines.
- `tree.py` — tree object creation.
   - `build_tree_body` sorts entries and creates the binary tree body.
   - `hash_tree` hashes that body as a Git tree object.
   - `run_tree_hash` reads the lesson format and returns the tree hash.

### The `tests/` folder

Each numbered folder contains public input files for one lesson. The tests are
useful examples of the input and output formats, but the reusable implementation
belongs in `pygit/`.

### One lesson at a time

Each lesson states its own input and output format, and **most lessons are a separate exercise rather than a bigger version of the last one**. Two lessons can be handed the same input line and correctly want different output — a tokenizer prints `[ls] [-la]`, while the next lesson, which receives already-tokenized input, prints `ls -la`. No single program can satisfy both, and it isn't supposed to.

So treat `main.py` as the file for the lesson you're grading: when you move on, change what it does. Nothing is lost — every earlier lesson is in your git history (`git log`, `git show`), and shipthatcode remembers each lesson you passed, so a lesson stays completed even after you replace the code that passed it. If you'd rather keep the code visible, copy it aside first (`cp main.py solutions/01-<lesson>.py`) — extra files are ignored by the grader.

When a lesson genuinely does build on the previous one, its own text says so and its tests will pass with the earlier behaviour still in place.

## If the course gets updated

Courses improve over time — exercises get added, tests get fixed. If the [course page](https://shipthatcode.com/courses/build-git) says your starter is out of date: download a fresh zip, **delete this repo's `tests/` folder entirely**, copy in the fresh `tests/` and `.shipthatcode.json`, and keep your own code exactly as it is. (Don't merge test folders — lesson numbering can shift between versions.) Lessons you've already completed stay completed either way.

<sub>Repo topic suggestion: `shipthatcode` · Starter generated by [shipthatcode.com](https://shipthatcode.com)</sub>
