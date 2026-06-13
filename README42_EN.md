*This project was created as part of the 42 curriculum by alebaron, rruiz*

# Pacman: Recreating a legendary video game using Python

## Description

**Pac‑man** is a video game created by Tōru Iwatani in 1980. After 46 years, this arcade game remains iconic and is an essential piece of video game history. Today, it's our turn to develop it.

Key objectives of this project:

- **Game creation**: Learn how to build a video game using modern technologies.
- **Reuse of others' work**: Use other students' work to generate our maze.
- **Project management**: Learn to manage a complex group project.

[Link to Itch.io page](https://alebaron.itch.io/pac-mon)


## Instructions

```bash
# Clone the project
git clone https://github.com/alizealebaron/pac_man.git
cd pac-man

# Install dependencies
uv sync
# Or using the Makefile
make install
```

### Makefile commands

```bash
# Install dependencies and create a virtual environment
make install

# Run the program
make run

# Check and report strict linting errors
make lint-strict

# Check and report linting errors
make lint

# Clean files created by Python
make clean

# Launch a debug test environment
make debug
```

### Basic execution

```bash
# Use default files
uv run python pac-man.py [/path/to/config]
# Or with the Makefile
make run
```

## Configuration

This section describes the JSON configuration file structure used by the game, the expected keys, their constraints and default values.

- **Configuration file**: None by default; the game will use predefined defaults if not provided.
- **Format**: JSON.

### Available keys

- **`highscore_filename`** (str): Name of the highscore save file. Default is "highscores.json". Must be a non-empty string.
- **`level`** (list[object]): List of level configurations. Each element is a level object with fields:
  - **`id`** (int): Level identifier (>= 1).
  - **`width`** (int): Maze width (>= 2, <= 500).
  - **`height`** (int): Maze height (>= 2, <= 500).
  The `level` field must contain at least one valid level.
- **`lives`** (int): Number of player lives. Default 3. Constraints: >= 1, <= 1000.
- **`points_per_pacgum`** (int): Points for a normal pacgum. Default 10. Constraints: >= 1, <= 1000.
- **`points_per_super_pacgum`** (int): Points for a super pacgum. Default 50. Constraints: >= 1, <= 1000.
- **`points_per_ghost`** (int): Points for eating a ghost. Default 100. Constraints: >= 1, <= 1000.
- **`level_max_time`** (int): Maximum time to complete a level (seconds). Default 90. Constraints: >= 1, <= 3600.
- **`seed`** (int or null): Seed for random generation. Default 42.

### Behavior on invalid values

Validation is performed by the `ConfigModel` ([src/models/configmodel.py](src/models/configmodel.py)).

Invalid values are replaced by their defaults and a warning is printed to standard error.

For the `level` key, invalid entries are ignored (with a warning). If no valid level configuration is found, the model's default value is used.

### Minimal configuration file

```json
{
    "highscore_filename": "highscores.json",
    "level": [{"id":1,"width":6,"height":6}],
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "level_max_time": 90,
    "seed": 24
}
```

## Highscore

The highscore system is intentionally simple and easy to modify: scores are stored in a JSON file whose name is defined by the `highscore_filename` configuration key (default `highscores.json`).

### Technical behavior

On startup, the game loads the score list from the file via the `retrieve_score_from_json()` method in `src/pacmanManager.py`, which converts each entry into a `Score` object.

When the player chooses to save their score (victory screen), a `Score` object is created and appended to the list (`win_view.save_without_name` or through the name entry UI). The whole list is then written back to the JSON file by `update_json_score()`.

The scoreboard display (in the `victory view`) sorts the list by descending `score` and shows the top 9 results. The `menu view` shows the top 3 scores and the `scoreboard` view displays the top 30 scores.

### Entry format and constraints

- Each score is an object with fields:
  - `name` (str): Player name — validated by `Score` (length 1–10) and sanitized in the view (disallowed characters removed).
  - `score` (int): Numeric score (>= 0).
  - `pokemon` (str): Associated Pokémon name (non-empty string).

### Example score entries

```json
[
    {"name": "Alizéa", "score": 1, "pokemon": "Ducklett"},
    {"name": "Rémy", "score": 12, "pokemon": "Mawile"}
]
```

## Maze Generation

The project includes a maze generator taken from another student's project (`src/mazegenerator/mazegenerator.py`). Since this feature was not implemented from scratch, we used the `a_maze_ing` package provided by 42 central. This package produces a grid of cells (an integer matrix encoding walls) and also computes a shortest path between the entry and exit, which helps with element placement and movement logic.

### How it works and parameters

- `MazeGenerator` is instantiated with: `size=(width, height)`, `perfect` (bool), `entry_cell`, `exit_cell`, and `seed`. If `seed > 0`, generation is deterministic via `random.seed(seed)`; otherwise a random seed is used.

- After initialization, `generate()` builds the matrix, optionally adds a central "42" pattern if the size allows, generates walls via recursive exploration, and computes the `shortest_path`.

### Integration with levels

In `src/models/levelModel.py`, each `Level` creates its `MazeGenerator` with `MazeGenerator((width, height), seed=(num_level + seed))`. The provided seed combines the level number and the global seed (from the configuration), producing reproducible but varying mazes per level.

## Implementation

To ship a complete project without implementing everything ourselves, we used several Python packages that simplified development:

- **`arcade`**: main 2D rendering and UI library. All views (`game_view`, `menu_view`, `scoreboard_view`, etc.), input handling, audio playback, and sprite rendering rely on `arcade` and `arcade.gui`.
- **`pydantic`**: data validation and serialization for models (`ConfigModel`, `Score`, `PokemonModel`, `EnemyDataModel`, ...). Ensures constraints (types, bounds, lengths) when loading from JSON.
- **`argparse`** (stdlib): command-line argument parsing (notably for passing a custom config file).
- **`Pillow (PIL)`**: used for some image manipulation in `src/view/maze_renderer.py` (texture preparation/combination).
- **`pyinstaller`**: packaging tool (create standalone executables to distribute the game without a Python environment).
- **`flake8`** and **`mypy`**: help maintain code quality; not required to run the game but mandatory for project validation.

## General Software Architecture

The project follows a simple modular MVC (Model — View — Controller) architecture. Below is an overview of the main modules and relationships:

- **Model (`src/models`)**: contains data classes and pure business logic:
  - `ConfigModel`, `LevelConfig`: validation and representation of game configuration.
  - `Score`: representation of a scoreboard entry.
  - `PlayerModel`, `Level`, `EnemyModel`, `PokemonModel`, etc.: states and rules related to game entities.
- **View (`src/view`)**: all graphical interfaces and rendering logic:
  - `main_window.py`, `menu_view.py`, `game_view.py`, `scoreboard_view.py`, `save_score/*` and other views. They consume models and trigger actions via the manager/controller.
  - `maze_renderer.py` handles visual rendering of the maze from generator data.
- **Controller / Manager (`src/pacmanManager.py`, `src/managers/*`)**:
  orchestrates game logic, updates models and triggers view changes:
  - `PacmanManager` loads the configuration, creates levels and the player, manages the scoreboard and instantiates managers (enemies, collectibles, etc.).
  - Specific managers (`enemy_manager.py`, `collectible_manager.py`) handle local logic (AI, collisions, spawning).
- **Generation / utilities (`src/mazegenerator`, `src/parsing`)**:
  - `MazeGenerator` produces the mazes used by `Level`.
  - `parsing/config_loader.py` and `parsing/arg_parser.py` handle loading and validating configurations.

### Startup logic

- The game starts, `PacmanManager` loads the `ConfigModel` via `ConfigLoader`.
- `PacmanManager` creates `Level` instances (which construct `MazeGenerator`s) and instantiates `PlayerModel` and managers.
- Views query `PacmanManager` for current state and render models. User actions are forwarded to the manager, which updates models and, if needed, changes the view.

### UML Illustration (MVC)

![Architecture UML](project_management/uml/light_UML.png)

## Project Management

To ease onboarding for this project, which included many tasks and features, we maintained a backlog. A backlog is a prioritized list of features to implement and improvements to make. We split each feature into smaller tasks. This provided a clear overall vision for the project. We also listed improvements and bugs found during development.

### Project documents

You can find the management documents in the `project_management/` folder. This includes:

```
project_management/
├── backlog/
    └── backlof_Pacman.xlsx    # Excel file with our backlog prior to project completion
├── sketch/
    ├── gameover_sketch.webp   # Initial sketch for the gameover view
    ├── mainmenu_sketch.webp   # Initial sketch for the menu view
    └── win_sketch.webp        # Initial sketch for the victory view
└── uml/
    ├── light_UML.png          # Simplified UML diagram for the project
    └── logique_findejeu.webp  # Diagram of end-of-game logic
```

### Role distribution

**Alebaron**:
- UI implementation
- Score system implementation
- Cheats and settings management
- Writing the quiz questions
- Docstring verification
- README writing

**Rruiz**:
- Configuration loading
- Maze generation
- Player movement
- Enemy movement
- Bug fixes
- Flake8 and mypy compliance

## Resources

### Pacman documentation

- [Pac‑man - Wikipedia](https://fr.wikipedia.org/wiki/Pac-Man)
- [Free pacman (game)](https://freepacman.org/)
- [Pac‑Man ghost AI visualized](https://www.reddit.com/r/interestingasfuck/comments/cdph0r/pacman_ghost_ai_visualized/?tl=fr)

### Python library documentation

- [The Python Arcade Library](https://api.arcade.academy/en/3.3.3/index.html)
- [Mypy documentation](https://mypy.readthedocs.io/en/stable/)
- [Pydantic documentation](https://pydantic.dev/docs/validation/latest/get-started/)
- [Pyinstaller Manual](https://pyinstaller.org/en/stable/)
- [Python argparse Module](https://docs.python.org/3/library/argparse.html)
- [Python assert Keyword](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement)

### Pokémon assets / sprites

- [Pokémon Mystery Dungeon sprites](https://sprites.pmdcollab.org/)
- [Pokémon Mystery Dungeon assets](https://www.spriters-resource.com/nintendo_switch/pokemonmysterydungeonrescueteamdx/)
- [Pokémon Mystery Dungeon music](https://youtu.be/w7TP5d5mUMw?si=hrDAKu1_mXS0yPxW)

### Use of AI

- Debugging assistance
- Arcade-related explanations
- Simplifying rendering calculations
- Rewriting and translating text (README)
- Generating part of the docstrings
- Fixing mypy errors

### Credits

- **Pokémon animations & icons**: CHUNSOFT, Emmuffin, G~, FrivolousAqua, baronessfaron, chime, anomalocaris, Uni, Emboarger, Angels-Snack, Morei, ShyStarryRain, Ichor, Frostdrop1, Caitemis, JFain, NickOnimura, NeroIntruder

- **Music**: Keisuke Ito, composer for "Pokémon Mystery Dungeon: Rescue Team DX"

- **Background and assets**: Nintendo, The Pokémon Company, Game Freak, CHUNSOFT.

### Disclaimer

This game is a fangame created for an academic project. Pokémon and Pokémon Mystery Dungeon are the property of Nintendo, Game Freak, Creatures and The Pokémon Company. Please support the official works.

---

**Last modified**: 13 June 2026
**Contact:** alebaron@student.42lehavre.fr / rruiz@student.42lehavre.fr
