#!/usr/bin/env python3
"""
Terminal-based Wordle Clone
===========================
A fully-featured Wordle game with ANSI colors, stats tracking,
typing effects, themed modes, and a beautiful terminal UI.

Usage:
    python wordle.py [--wordfile FILEPATH] [--length N]

Requirements:
    Python 3.7+  (no external packages needed)
"""

import random
import sys
import os
import time
import json
from pathlib import Path
from typing import List, Tuple, Optional

# ─── ANSI helpers ──────────────────────────────────────────────────────────────

GREEN  = "\033[42;30m"   # green background, black text
YELLOW = "\033[43;30m"   # yellow background, black text
GREY   = "\033[100;37m"  # dark-grey background, white text
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
CYAN   = "\033[36m"
RED    = "\033[31m"
MAGENTA = "\033[35m"

EMOJI_MAP = {"green": "🟩", "yellow": "🟨", "grey": "⬜"}
COLOR_MAP = {"green": GREEN, "yellow": YELLOW, "grey": GREY}

STATS_FILE = Path(__file__).parent / ".wordle_stats.json"

# ─── Themed word lists ─────────────────────────────────────────────────────────

FANTASY_WORDS = [
    "magic", "dragon", "sword", "quest", "spell", "dwarf", "elfin", "rogue",
    "troll", "demon", "witch", "fairy", "giant", "ghost", "beast", "curse",
    "flame", "storm", "blade", "crown", "realm", "tower", "scout", "grave",
    "crypt", "charm", "staff", "steal", "sneak", "armor", "guild", "jewel",
    "forge", "manor", "titan", "raven", "blood", "stone", "frost", "shade",
    "mirth", "dread", "valor", "vigor", "wrath", "fiend", "siege", "noble",
    "lunge", "kneel", "grail", "haunt", "talon", "venom", "reign", "exile",
    "omega", "chaos", "abyss", "glyph", "elven", "oaken", "fable", "power",
    "royal", "night", "light", "dream", "world", "mount", "siren", "skull",
    "lunar", "solar", "elder", "coven", "druid", "cloak", "golem", "hydra",
    "joust", "lance", "brawl", "potion", "trove", "vault", "haven", "blaze",
]

TECH_WORDS = [
    "cloud", "cyber", "pixel", "bytes", "cache", "debug", "float", "stack",
    "array", "class", "queue", "model", "table", "query", "index", "linux",
    "patch", "build", "clone", "drive", "input", "mouse", "logic", "email",
    "virus", "frame", "login", "token", "route", "crash", "flash", "power",
    "print", "scope", "shift", "shell", "yield", "throw", "parse", "fetch",
    "async", "trait", "tuple", "union", "proxy", "regex", "codec", "fiber",
    "modem", "codec", "diode", "relay", "reset", "block", "chain", "crypt",
    "merge", "branch", "react", "swift", "rusty", "razor", "azure", "batch",
    "match", "watch", "event", "timer", "value", "error", "panic", "abort",
    "ports", "nodes", "graph", "depth", "width", "color", "audio", "video",
]

FOOD_WORDS = [
    "pizza", "bread", "steak", "salad", "cream", "sugar", "pasta", "apple",
    "grape", "lemon", "mango", "peach", "melon", "berry", "olive", "onion",
    "basil", "thyme", "clove", "honey", "flour", "yeast", "sauce", "gravy",
    "broth", "curry", "roast", "grill", "steam", "poach", "saute", "toast",
    "bagel", "donut", "crepe", "scone", "fudge", "candy", "tarte", "mousse",
    "cocoa", "mocha", "latte", "juice", "cider", "feast", "diner", "lunch",
    "snack", "treat", "spice", "aroma", "flavor", "taste", "sweet", "tangy",
    "crisp", "chewy", "smoky", "zesty", "minty", "nutty", "fruit", "grain",
    "wheat", "maize", "beans", "liver", "trout", "squid", "prawn", "clams",
    "bacon", "chili", "nacho", "taco", "ramen", "sushi", "briny", "filet",
]

SPORTS_WORDS = [
    "score", "match", "field", "coach", "track", "serve", "pitch", "catch",
    "throw", "swing", "rally", "draft", "round", "medal", "court", "arena",
    "vault", "squad", "bench", "block", "point", "bonus", "homer", "brawl",
    "clash", "drive", "guard", "steal", "ditch", "blitz", "sweep", "extra",
    "final", "relay", "hurry", "chase", "spark", "blaze", "flame", "vigor",
    "forte", "sport", "racer", "rider", "yacht", "canoe", "kayak", "climb",
    "skate", "spike", "smash", "volley", "punch", "boxer", "rugby", "jockey",
    "goalie", "diver", "fencer", "timer", "clock", "start", "goal", "fault",
    "power", "speed", "agile", "quick", "swift", "fleet", "jumps", "darts",
    "chess", "lance", "press", "drill", "train", "focus", "pride", "title",
]

# Curated 150-word Normal list — every word has handcrafted hints below.
NORMAL_WORDS = [
    "apple", "beach", "brain", "bread", "chair", "cloud", "clock", "crown",
    "dance", "earth", "flame", "ghost", "glass", "grape", "heart", "honey",
    "horse", "house", "knife", "lemon", "light", "lions", "money", "mouse",
    "music", "night", "ocean", "paint", "paper", "phone", "piano", "pizza",
    "plane", "queen", "river", "robot", "rocky", "sheep", "sleep", "smile",
    "snake", "snowy", "stone", "sugar", "sword", "table", "tiger", "train",
    "water", "zebra",
    # Expansion to 150
    "angel", "arrow", "actor", "album", "anvil", "badge", "bench", "blink",
    "bloom", "brick", "broom", "candy", "cabin", "cliff", "coral", "crane",
    "diary", "diver", "drone", "eagle", "ember", "enemy", "fable", "fence",
    "field", "flock", "frost", "globe", "grain", "guard", "haven", "honor",
    "image", "ivory", "jelly", "judge", "karma", "kayak", "knock", "lance",
    "latch", "lever", "magic", "mango", "march", "medal", "mirth", "mocha",
    "novel", "north", "olive", "onion", "organ", "pearl", "petal", "pixel",
    "pluck", "porch", "prism", "quiet", "quill", "raven", "razor", "relic",
    "rifle", "robin", "salsa", "scarf", "scorn", "scout", "shore", "skull",
    "spice", "spine", "stage", "steam", "stork", "swarm", "tango", "tarot",
    "thorn", "tooth", "torch", "tower", "trace", "trout", "vault", "vinyl",
    "vivid", "voter", "waltz", "wheat", "whirl", "weave", "witch", "wreck",
    "yacht", "yield", "youth", "zesty",
]
# Trim/normalize to ensure exactly 5-letter words
NORMAL_WORDS = [w for w in NORMAL_WORDS if len(w) == 5]

GAME_MODES = {
    "1": ("Normal",  NORMAL_WORDS),
    "2": ("Fantasy", FANTASY_WORDS),
    "3": ("Tech",    TECH_WORDS),
    "4": ("Food",    FOOD_WORDS),
    "5": ("Sports",  SPORTS_WORDS),
}

# ─── Word handling ─────────────────────────────────────────────────────────────

def load_words(filepath: str, length: int = 5) -> List[str]:
    """Load words of the given length from a text file (one word per line)."""
    path = Path(filepath)
    if not path.exists():
        print(f"{RED}Error: word file '{filepath}' not found.{RESET}")
        sys.exit(1)
    words = [
        w.strip().lower()
        for w in path.read_text().splitlines()
        if w.strip().isalpha() and len(w.strip()) == length
    ]
    if not words:
        print(f"{RED}Error: no {length}-letter words found in '{filepath}'.{RESET}")
        sys.exit(1)
    return words


def get_easy_words(words: List[str]) -> List[str]:
    """Return the easiest third of words ranked by common letter frequency."""
    freq = {}
    for w in words:
        for ch in set(w):
            freq[ch] = freq.get(ch, 0) + 1
    scored = sorted(words, key=lambda w: sum(freq.get(c, 0) for c in set(w)), reverse=True)
    n = max(len(scored) // 3, 1)
    return scored[:n]


def choose_word(words: List[str]) -> str:
    """Pick a random word from the list."""
    return random.choice(words)

# ─── Game logic ────────────────────────────────────────────────────────────────

def validate_guess(guess: str, word_length: int, valid_words: List[str]) -> Optional[str]:
    """Return an error message if the guess is invalid, else None."""
    if len(guess) != word_length:
        return f"Please enter exactly {word_length} letters."
    if not guess.isalpha():
        return "Only alphabetic characters are allowed."
    if guess not in valid_words:
        return "Not in word list. Try another word."
    return None


def get_feedback(guess: str, secret: str) -> List[str]:
    """
    Return per-letter feedback: 'green', 'yellow', or 'grey'.
    Handles duplicate letters correctly.
    """
    result = ["grey"] * len(guess)
    secret_chars = list(secret)

    # First pass — greens
    for i, (g, s) in enumerate(zip(guess, secret)):
        if g == s:
            result[i] = "green"
            secret_chars[i] = None

    # Second pass — yellows
    for i, g in enumerate(guess):
        if result[i] == "green":
            continue
        if g in secret_chars:
            result[i] = "yellow"
            secret_chars[secret_chars.index(g)] = None

    return result

# ─── Display ───────────────────────────────────────────────────────────────────

def slow_print(text: str, delay: float = 0.03) -> None:
    """Print text with a typewriter animation."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


# Keep backward-compatible alias
typing_effect = slow_print


def render_row(guess: str, feedback: List[str], use_emoji: bool = False) -> str:
    """Render a single guess row with colors or emoji."""
    cells = []
    for ch, fb in zip(guess.upper(), feedback):
        if use_emoji:
            cells.append(f"{EMOJI_MAP[fb]} {ch}")
        else:
            cells.append(f"{COLOR_MAP[fb]} {ch} {RESET}")
    return "  ".join(cells)


def display_board(
    guesses: List[Tuple[str, List[str]]],
    max_attempts: int,
    word_length: int,
) -> None:
    """Print the full board grid."""
    print()
    for guess, feedback in guesses:
        print("  " + render_row(guess, feedback))
    remaining = max_attempts - len(guesses)
    for _ in range(remaining):
        print("  " + "  ".join([f"{DIM} _ {RESET}"] * word_length))
    print()


def display_keyboard(guesses: List[Tuple[str, List[str]]]) -> None:
    """Show a mini keyboard with letter statuses."""
    status: dict = {}
    priority = {"green": 3, "yellow": 2, "grey": 1}
    for guess, feedback in guesses:
        for ch, fb in zip(guess, feedback):
            if priority.get(fb, 0) > priority.get(status.get(ch), 0):
                status[ch] = fb
    rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    for row in rows:
        cells = []
        for ch in row:
            fb = status.get(ch)
            if fb:
                cells.append(f"{COLOR_MAP[fb]}{ch.upper()}{RESET}")
            else:
                cells.append(ch.upper())
        print("  " + " ".join(cells))
    print()


def display_welcome() -> None:
    """Show a beautiful ASCII art welcome banner."""
    banner = f"""
{BOLD}{CYAN}
    ╔═══════════════════════════════════════════════╗
    ║                                               ║
    ║   ██╗    ██╗ ██████╗ ██████╗ ██████╗ ██╗      ║
    ║   ██║    ██║██╔═══██╗██╔══██╗██╔══██╗██║      ║
    ║   ██║ █╗ ██║██║   ██║██████╔╝██║  ██║██║      ║
    ║   ██║███╗██║██║   ██║██╔══██╗██║  ██║██║      ║
    ║   ╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝███████╗ ║
    ║    ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝ ║
    ║                                               ║
    ╚═══════════════════════════════════════════════╝{RESET}

    {DIM}Guess the word. You have 6 tries.{RESET}
    {GREEN} A {RESET} = right spot   {YELLOW} A {RESET} = wrong spot   {GREY} A {RESET} = not in word
"""
    for line in banner.split("\n"):
        print(line)
        time.sleep(0.04)
    print()


def display_mode_menu() -> str:
    """Show the game mode selection menu and return the chosen mode key."""
    slow_print(f"\n  {BOLD}🎮  Choose your mode:{RESET}", 0.02)
    print()
    icons = {"Normal": "📖", "Fantasy": "🐉", "Tech": "💻", "Food": "🍕", "Sports": "⚽"}
    for key, (name, _) in GAME_MODES.items():
        icon = icons.get(name, "")
        slow_print(f"    {BOLD}{CYAN}[{key}]{RESET}  {icon}  {name}", 0.015)
    print()

    while True:
        choice = input(f"  Enter mode (1-5): ").strip()
        if choice in GAME_MODES:
            display_mode_intro(choice)
            return choice
        print(f"  {RED}Invalid choice. Please enter 1-5.{RESET}")


def display_mode_intro(mode_key: str) -> None:
    """Show a themed ASCII art intro for the selected mode."""
    name = GAME_MODES[mode_key][0]

    intros = {
        "1": f"""
{BOLD}{CYAN}
    ┌─────────────────────────────────────────┐
    │          📖  N O R M A L  📖            │
    │                                         │
    │    The classic Wordle experience.        │
    │    Pure vocabulary, pure skill.          │
    │    No theme — just you vs. the word.     │
    │                                         │
    └─────────────────────────────────────────┘{RESET}
""",
        "2": f"""
{BOLD}{MAGENTA}
    ┌─────────────────────────────────────────┐
    │         🐉  F A N T A S Y  🐉           │
    │                                         │
    │    Enter the realm of myth & legend.     │
    │    Dragons, spells, and ancient lore     │
    │    await the worthy adventurer...        │
    │                                         │
    │    ⚔️  May your quests be victorious.    │
    └─────────────────────────────────────────┘{RESET}
""",
        "3": f"""
{BOLD}\033[32m
    ┌─────────────────────────────────────────┐
    │           💻  T E C H  💻               │
    │                                         │
    │    > initializing wordle.exe ...         │
    │    > loading silicon vocabulary ...      │
    │    > compile your guesses wisely.        │
    │                                         │
    │    01001000 01001001               █▓░   │
    └─────────────────────────────────────────┘{RESET}
""",
        "4": f"""
{BOLD}\033[33m
    ┌─────────────────────────────────────────┐
    │           🍕  F O O D  🍕               │
    │                                         │
    │    Welcome to the kitchen!               │
    │    Spices, flavors, and ingredients      │
    │    are on the menu today.                │
    │                                         │
    │    🧑‍🍳 Bon appétit, word chef!           │
    └─────────────────────────────────────────┘{RESET}
""",
        "5": f"""
{BOLD}\033[34m
    ┌─────────────────────────────────────────┐
    │         ⚽  S P O R T S  ⚽              │
    │                                         │
    │    Step onto the field of words!         │
    │    Goals, matches, and champions         │
    │    — it's game time.                     │
    │                                         │
    │    🏆 Give it your best shot!            │
    └─────────────────────────────────────────┘{RESET}
""",
    }

    intro = intros.get(mode_key, "")
    for line in intro.split("\n"):
        print(line)
        time.sleep(0.04)
    print()


def display_difficulty_menu() -> str:
    """Show difficulty sub-menu for Normal mode. Returns 'easy', 'medium', or 'hard'."""
    slow_print(f"\n  {BOLD}🎯  Choose difficulty:{RESET}", 0.02)
    print()
    options = [
        ("1", "easy",   "🟢 Easy",   "3 hints — clue after attempts 1, 2, and 3 (final hint is a giveaway)."),
        ("2", "medium", "🟡 Medium", "2 hints — subtler clues after attempts 2 and 4."),
        ("3", "hard",   "🔴 Hard",   "1 hint — a single cryptic clue after attempt 4."),
    ]
    for key, _, label, desc in options:
        slow_print(f"    {BOLD}{CYAN}[{key}]{RESET}  {label}", 0.015)
        slow_print(f"         {DIM}{desc}{RESET}", 0.005)
    print()
    mapping = {k: v for k, v, _, _ in options}
    while True:
        choice = input(f"  Enter difficulty (1-3): ").strip()
        if choice in mapping:
            diff = mapping[choice]
            label = dict((v, l) for _, v, l, _ in options)[diff]
            slow_print(f"\n  {BOLD}Difficulty set:{RESET} {label}\n", 0.02)
            return diff
        print(f"  {RED}Invalid choice. Please enter 1-3.{RESET}")


# ─── Stats ─────────────────────────────────────────────────────────────────────

def load_stats() -> dict:
    if STATS_FILE.exists():
        return json.loads(STATS_FILE.read_text())
    return {"played": 0, "wins": 0, "streak": 0, "max_streak": 0, "distribution": {}}


def save_stats(stats: dict) -> None:
    STATS_FILE.write_text(json.dumps(stats, indent=2))


def update_stats(stats: dict, won: bool, attempts: int, max_attempts: int) -> dict:
    stats["played"] += 1
    if won:
        stats["wins"] += 1
        stats["streak"] += 1
        stats["max_streak"] = max(stats["max_streak"], stats["streak"])
        key = str(attempts)
        stats["distribution"][key] = stats["distribution"].get(key, 0) + 1
    else:
        stats["streak"] = 0
    return stats


def show_stats(stats: dict) -> None:
    print(f"\n{BOLD}📊  Statistics{RESET}")
    print(f"  Played: {stats['played']}   "
          f"Win%%: {stats['wins']*100//max(stats['played'],1)}%%   "
          f"Streak: {stats['streak']}   "
          f"Best: {stats['max_streak']}")
    if stats["distribution"]:
        print(f"  {DIM}Guess distribution:{RESET}")
        for k in sorted(stats["distribution"]):
            bar = "█" * stats["distribution"][k]
            print(f"    {k}: {bar} {stats['distribution'][k]}")
    print()

# ─── Main game loop ───────────────────────────────────────────────────────────

def generate_hints(secret: str) -> List[str]:
    """Three specific, word-related hints for each Normal-mode word.
    Hint 1: a vivid clue about what it is or where you find it.
    Hint 2: a defining feature, color, sound, or sensation.
    Hint 3: a famous association, story, or person tied to the word.
    """
    hints_map = {
        # ─── Original 50 (easier, clearer hints) ───
        "apple": ["A common fruit, often red or green.", "Keeps the doctor away, they say.", "Newton watched one fall from a tree."],
        "beach": ["A sandy place by the sea.", "You build castles here in summer.", "Waves, shells, and umbrellas everywhere."],
        "brain": ["The organ inside your skull.", "It controls your thoughts and body.", "Einstein had a famously studied one."],
        "bread": ["A baked food made from flour.", "Comes in loaves and slices.", "Goes well with butter or jam."],
        "chair": ["A piece of furniture for sitting.", "Has four legs and a back.", "Goldilocks tried three of them."],
        "cloud": ["A white shape floating in the sky.", "Made of tiny water droplets.", "Also where your files are stored online."],
        "clock": ["It tells you the time.", "Has hour and minute hands.", "Big Ben in London is a famous one."],
        "crown": ["Worn on a king or queen's head.", "Made of gold and jewels.", "Symbol of royalty and power."],
        "dance": ["A way of moving to music.", "Done at parties and weddings.", "Cinderella did this with her prince."],
        "earth": ["The planet we live on.", "Third from the sun.", "Mostly blue when seen from space."],
        "flame": ["The bright part of a fire.", "Hot, orange, and flickering.", "Lit at the start of the Olympics."],
        "ghost": ["A spirit said to haunt places.", "Often shown as a white floating figure.", "Scrooge was visited by three of them."],
        "glass": ["You drink water from one.", "Clear and breakable.", "Cinderella's slipper was made of it."],
        "grape": ["A small round fruit in bunches.", "Comes in green or purple.", "Wine is made from it."],
        "heart": ["The organ that pumps your blood.", "Symbol of love on Valentine's Day.", "Beats about 100,000 times a day."],
        "honey": ["A sweet golden food.", "Made by bees.", "Winnie the Pooh's favorite snack."],
        "horse": ["A large animal you can ride.", "Used to pull carriages.", "Measured in 'hands' for height."],
        "house": ["Where people live.", "Has rooms, doors, and windows.", "Three pigs each built one in a fairy tale."],
        "knife": ["A sharp tool for cutting.", "Used in the kitchen every day.", "Comes with a fork and spoon."],
        "lemon": ["A sour yellow fruit.", "Used to make lemonade.", "Slang for a bad car."],
        "light": ["The opposite of darkness.", "Comes from the sun or a bulb.", "Travels faster than anything else."],
        "lions": ["Big cats that live in prides.", "The males have a mane.", "Known as the king of the jungle."],
        "money": ["What you use to buy things.", "Comes as coins or paper notes.", "People work to earn it."],
        "mouse": ["A small furry rodent.", "Cats love to chase it.", "Also the device you click with."],
        "music": ["Sounds arranged to please the ear.", "You listen to it on the radio or phone.", "Mozart composed a lot of it."],
        "night": ["The dark part of the day.", "When the moon and stars come out.", "When most people sleep."],
        "ocean": ["A huge body of salt water.", "Whales and sharks live in it.", "Covers most of the Earth."],
        "paint": ["Liquid color you put on walls.", "Artists use it on canvas.", "Van Gogh used it in swirls."],
        "paper": ["Made from trees.", "What you write or print on.", "Can be folded into airplanes."],
        "phone": ["A device you call people on.", "Now fits in your pocket.", "Invented by Alexander Graham Bell."],
        "piano": ["A large instrument with black and white keys.", "Has 88 keys total.", "Beethoven kept playing it even when deaf."],
        "pizza": ["A round Italian food.", "Topped with cheese and tomato sauce.", "Delivered in a square box."],
        "plane": ["A flying machine with wings.", "Takes you across countries.", "The Wright Brothers built the first one."],
        "queen": ["The female ruler of a kingdom.", "The most powerful piece in chess.", "Elizabeth II ruled Britain for 70 years."],
        "river": ["Flowing fresh water on land.", "Runs from mountains to the sea.", "The Nile is a famous one."],
        "robot": ["A machine that can do tasks.", "Often pictured as metal humans.", "WALL-E is a famous lonely one."],
        "rocky": ["Full of stones, like a beach or hill.", "Also a famous boxing movie.", "Ran up museum stairs in Philadelphia."],
        "sheep": ["A fluffy farm animal.", "Their wool makes sweaters.", "People count them to fall asleep."],
        "sleep": ["What you do at night in bed.", "You dream during it.", "A princess fell into a long one in a fairy tale."],
        "smile": ["A happy expression on your face.", "Shows your teeth in a friendly way.", "The Mona Lisa has a famous mysterious one."],
        "snake": ["A long animal with no legs.", "It slithers and hisses.", "Tempted Eve in the Garden of Eden."],
        "snowy": ["Covered in white winter flakes.", "Describes a Christmas day in the north.", "Tintin's little white dog has this name."],
        "stone": ["A small piece of rock.", "Used to build castles and walls.", "David used one to defeat Goliath."],
        "sugar": ["Sweet white grains in your tea.", "Used in baking cakes and cookies.", "Comes from cane or beets."],
        "sword": ["A long sharp blade.", "Knights fought with them.", "King Arthur's was called Excalibur."],
        "table": ["Furniture you eat dinner on.", "Usually has four legs.", "King Arthur's famous one was round."],
        "tiger": ["A big orange cat with black stripes.", "Lives in the jungles of Asia.", "The largest of all wild cats."],
        "train": ["A long vehicle on rails.", "Pulled by an engine.", "Harry Potter took one from platform 9¾."],
        "water": ["A clear liquid you drink.", "Made of hydrogen and oxygen.", "Covers most of the planet."],
        "zebra": ["An African animal with stripes.", "Looks like a horse in pajamas.", "No two have the same pattern."],
        # ─── New 100 (easier, clearer hints) ───
        "angel": ["A heavenly being with wings.", "Often placed on top of a Christmas tree.", "In a famous movie, one earns its wings when a bell rings."],
        "arrow": ["Shot from a bow.", "Cupid uses one to make people fall in love.", "William Tell shot an apple with one."],
        "actor": ["A person who performs in films or plays.", "Wins Oscars at award shows.", "Walks the red carpet in Hollywood."],
        "album": ["A collection of songs by an artist.", "The Beatles made many famous ones.", "Comes on vinyl, CD, or streaming now."],
        "anvil": ["A heavy iron block a blacksmith uses.", "Cartoons love dropping them on characters.", "Hammer strikes hot metal on it."],
        "badge": ["A small pin showing rank or honor.", "Police officers wear one on their chest.", "Boy Scouts collect lots of them."],
        "bench": ["A long seat in a park.", "Where extra players wait in a game.", "Judges sit on one in court."],
        "blink": ["A quick close and open of your eyes.", "You do it without thinking.", "Happens in less than a second."],
        "bloom": ["When a flower opens up.", "Happens most in spring.", "Also means to be at your best."],
        "brick": ["A red rectangular building block.", "Houses and walls are made of them.", "The wolf couldn't blow this house down."],
        "broom": ["A tool for sweeping the floor.", "Witches fly on one.", "Harry Potter plays Quidditch on one."],
        "candy": ["A sweet treat for kids.", "Given out on Halloween.", "Hansel and Gretel found a house made of it."],
        "cabin": ["A small wooden house in the woods.", "Lincoln was born in one.", "Often near a lake for vacations."],
        "cliff": ["A tall steep rock face.", "You shouldn't stand too close to the edge.", "Wile E. Coyote always falls off them."],
        "coral": ["A colorful structure under the sea.", "Forms reefs where fish live.", "Also a pinkish-orange color."],
        "crane": ["A tall bird with long legs.", "Also a tall machine that lifts heavy things.", "Folded thousands of times in origami tradition."],
        "diary": ["A book where you write your daily thoughts.", "Anne Frank kept a famous one.", "Often has a small lock and key."],
        "diver": ["A person who jumps into water.", "Olympic ones do flips before splashing.", "Wears a mask to explore underwater."],
        "drone": ["A small flying robot with a camera.", "Buzzes overhead without a pilot.", "Also a male bee."],
        "eagle": ["A large bird of prey.", "America's national bird.", "Has very sharp eyesight."],
        "ember": ["A small glowing piece of a dying fire.", "Red and hot but not flaming.", "Pixar made a movie with this name."],
        "enemy": ["The opposite of a friend.", "Someone who fights against you.", "In wars, the side you battle."],
        "fable": ["A short story with a moral.", "Often has talking animals.", "Aesop wrote many famous ones."],
        "fence": ["A barrier around a yard.", "Keeps things in or out.", "Robert Frost said good ones make good neighbors."],
        "field": ["A wide open area of grass or crops.", "Where farmers grow corn or wheat.", "Also where soccer is played."],
        "flock": ["A group of birds or sheep.", "Moves together in the sky or field.", "A shepherd watches over one."],
        "frost": ["A thin layer of ice on grass or windows.", "Forms on cold mornings.", "Jack pinches your nose with it."],
        "globe": ["A round model of the Earth.", "Spins on a stand on a desk.", "Shakespeare's theatre had this name."],
        "grain": ["A tiny seed like rice or wheat.", "Bread and cereal are made from it.", "Stored in tall silos on farms."],
        "guard": ["A person who protects something.", "Stands in front of palaces.", "Buckingham Palace's wear tall furry hats."],
        "haven": ["A safe place to escape to.", "A harbor for ships in a storm.", "Also a Yale university city in Connecticut."],
        "honor": ["Doing the right thing with pride.", "Soldiers fight for it.", "There's a saying about this even among thieves."],
        "image": ["A picture or photo.", "What you see in a mirror.", "Worth a thousand words, they say."],
        "ivory": ["The hard white material from elephant tusks.", "Color of old piano keys.", "Sadly, the reason elephants are hunted."],
        "jelly": ["A wobbly sweet food on a plate.", "Spread on bread with peanut butter.", "Some sea creatures share the name."],
        "judge": ["The person in charge of a courtroom.", "Wears a black robe and bangs a gavel.", "Decides who wins on talent shows."],
        "karma": ["The idea that what you do comes back to you.", "A core belief in Hindu and Buddhist faiths.", "Reddit users earn 'points' with this name."],
        "kayak": ["A small narrow boat for one person.", "You paddle with both ends of the oar.", "Spelled the same forwards and backwards."],
        "knock": ["The sound made by tapping a door.", "Three of them start a 'who's there?' joke.", "Opportunity is said to do it once."],
        "lance": ["A long pointed weapon.", "Used by knights on horseback.", "Lance Armstrong was a famous cyclist."],
        "latch": ["A small fastener on a door or gate.", "Lifts up to open.", "Babies do this when feeding."],
        "lever": ["A bar you push or pull to lift things.", "One of the simple machines.", "Archimedes said with one he could move the Earth."],
        "magic": ["Tricks that look impossible.", "Pulled from a hat with a rabbit.", "Taught at Hogwarts in Harry Potter."],
        "mango": ["A sweet tropical fruit.", "Yellow inside, green or red outside.", "Called the 'king of fruits' in India."],
        "march": ["The third month of the year.", "Soldiers walk in step doing it.", "Named after the Roman god of war."],
        "medal": ["An award hung on a ribbon.", "Olympic winners get gold, silver, or bronze.", "Soldiers earn them for bravery."],
        "mirth": ["A fancy word for laughter and joy.", "Found at parties and feasts.", "Common in Dickens' Christmas stories."],
        "mocha": ["A coffee drink with chocolate.", "Named after a port in Yemen.", "Also a brown shade of color."],
        "novel": ["A long fictional book.", "Read for fun on weekends.", "Also means something brand new."],
        "north": ["The direction a compass points.", "Where the Arctic is.", "Polaris, the pole star, hangs above it."],
        "olive": ["A small green or black fruit.", "Grows on trees in the Mediterranean.", "A branch of it is a peace symbol."],
        "onion": ["A vegetable that makes you cry.", "Has many layers, like Shrek says ogres do.", "The base of many cooked meals."],
        "organ": ["A large keyboard instrument in a church.", "Also a body part like the heart or lungs.", "Bach composed great music for it."],
        "pearl": ["A small white gem from an oyster.", "Worn on necklaces.", "A famous harbor in Hawaii has this name."],
        "petal": ["One of the colored parts of a flower.", "Plucked in 'loves me, loves me not'.", "Falls off when the flower fades."],
        "pixel": ["The smallest dot on a digital screen.", "Cameras count them in megapixels.", "Looks like a tiny square when zoomed in."],
        "pluck": ["To pull something off quickly.", "What you do to guitar strings.", "Also means courage or bravery."],
        "porch": ["A covered area outside the front door.", "Where rocking chairs go.", "Common on old American houses."],
        "prism": ["A clear glass shape that splits light.", "Makes a rainbow from sunlight.", "Featured on a famous Pink Floyd album cover."],
        "quiet": ["The opposite of loud.", "Required in libraries.", "What teachers ask noisy classes to be."],
        "quill": ["A feather used as a pen long ago.", "Dipped in ink to write.", "Also the spike on a porcupine."],
        "raven": ["A large black bird, smarter than it looks.", "Edgar Allan Poe wrote a famous poem about one.", "Also an NFL team in Baltimore."],
        "razor": ["A sharp blade for shaving.", "Modern ones have multiple blades.", "Occam had a famous principle named after one."],
        "relic": ["A very old object from the past.", "Often kept in museums or churches.", "Indiana Jones searches for them."],
        "rifle": ["A long gun with a grooved barrel.", "Used by hunters and soldiers.", "Also means to search through quickly."],
        "robin": ["A small bird with a red chest.", "First sign of spring in many places.", "Also Batman's young sidekick."],
        "salsa": ["A spicy tomato dip for chips.", "Also a lively Latin dance.", "Comes mild, medium, or hot."],
        "scarf": ["A long piece of cloth for your neck.", "Keeps you warm in winter.", "Doctor Who wore a famously long one."],
        "scorn": ["Strong dislike or contempt.", "A 'woman scorned' is a famous warning.", "Shows on your face as a sneer."],
        "scout": ["A person sent ahead to look around.", "Boy and Girl ones earn merit badges.", "Also the narrator of To Kill a Mockingbird."],
        "shore": ["The land right next to the sea.", "Where waves wash up.", "A famous reality show is set on Jersey's."],
        "skull": ["The bones of your head.", "Hamlet held one and gave a speech.", "Pirate flags have one and crossbones."],
        "spice": ["Something added to food for flavor.", "Pepper, cinnamon, and cumin are types.", "A 90s girl group sang about wanting it."],
        "spine": ["The bones down the middle of your back.", "Also the side of a book where the title is.", "Means courage in expressions."],
        "stage": ["The platform where actors perform.", "Shakespeare said all the world is one.", "Where bands play at concerts."],
        "steam": ["The hot vapor from boiling water.", "Rises from kettles and tea cups.", "Powered the first locomotives."],
        "stork": ["A tall bird with long legs and beak.", "Folklore says it delivers babies.", "Wades in shallow ponds for fish."],
        "swarm": ["A huge group of bees or insects.", "One of locusts plagued ancient Egypt.", "Moves together as if one body."],
        "tango": ["A passionate dance for two.", "Born in Argentina.", "Often danced with a rose in the teeth."],
        "tarot": ["A deck of cards used to tell fortunes.", "Read by candlelight by mystics.", "Has cards like 'The Fool' and 'The Tower'."],
        "thorn": ["A sharp point on a plant stem.", "Roses are famous for them.", "Sleeping Beauty's castle was surrounded by them."],
        "tooth": ["A hard white thing in your mouth.", "Kids put them under their pillow for the fairy.", "Wisdom ones often need to be removed."],
        "torch": ["A burning stick for light.", "The Statue of Liberty holds one up.", "British word for a flashlight."],
        "tower": ["A very tall narrow building.", "Pisa has a famous leaning one.", "Rapunzel let her hair down from one."],
        "trace": ["A tiny bit of something left behind.", "Detectives look for it at crime scenes.", "Also means a small amount in chemistry."],
        "trout": ["A speckled fish from rivers and lakes.", "Popular with fly fishermen.", "Lives in cold clear water."],
        "vault": ["A heavy strong room in a bank.", "Where money and gold are locked away.", "Gymnasts also leap over an apparatus called this."],
        "vinyl": ["A round black music record.", "Spins on a turntable.", "Made a comeback after CDs."],
        "vivid": ["Very bright and clear.", "Describes a colorful dream.", "Like a memory you can see in detail."],
        "voter": ["A person casting a ballot.", "Lines up at polling stations on election day.", "Has an inked finger in some countries."],
        "waltz": ["A graceful ballroom dance in 3/4 time.", "Strauss wrote many famous ones.", "Cinderella danced one before midnight."],
        "wheat": ["A golden grain grown in fields.", "Used to make bread and pasta.", "Separated from chaff in old sayings."],
        "whirl": ["A quick spinning motion.", "Water does this going down a drain.", "Dervishes spin in this way as a dance."],
        "weave": ["To make cloth by crossing threads.", "Done on a loom.", "Spiders do this to make their webs."],
        "witch": ["A woman said to use magic.", "Famously feared in Salem in 1692.", "Hermione is one in Harry Potter."],
        "wreck": ["A badly damaged ship or car.", "The Titanic became a famous one.", "A nervous person might say they feel like one."],
        "yacht": ["A fancy private boat.", "Sailed by the wealthy.", "Spelled in a strange and tricky way."],
        "yield": ["To give in or give way.", "A triangular yellow road sign says this.", "Also means how much a crop produces."],
        "youth": ["The time of being young.", "Ponce de León searched for a fountain of it.", "Said to be 'wasted on the young'."],
        "zesty": ["Full of lively flavor.", "Lemon or lime peel adds this taste.", "Also describes a fun energetic personality."],
    }

    if secret in hints_map:
        # Reverse so trickier hints come first (HINT 1 & 2) and the
        # easiest, most giveaway hint is shown last as the FINAL HINT.
        return list(reversed(hints_map[secret]))

    # Fallback (shouldn't trigger — Normal list is fully covered).
    return [
        "Recall a famous story, person, or place tied to it.",
        "Think about its color, shape, or sound.",
        "Picture where you'd find this in everyday life.",
    ]


def play_round(
    valid_words: List[str],
    secret: str,
    max_attempts: int = 6,
    word_length: int = 5,
    mode_name: str = "Normal",
    difficulty: str = "easy",
) -> Tuple[bool, int]:
    """Play one round. Returns (won, attempts_used)."""
    guesses: List[Tuple[str, List[str]]] = []
    icons = {"Normal": "📖", "Fantasy": "🐉", "Tech": "💻", "Food": "🍕", "Sports": "⚽"}
    icon = icons.get(mode_name, "")

    # Hint system (Normal mode only). Schedule depends on difficulty.
    # generate_hints returns hints in order: [trickiest, medium, easiest/giveaway]
    raw_hints = generate_hints(secret) if mode_name == "Normal" else []
    if mode_name == "Normal" and raw_hints:
        if difficulty == "easy":
            # 3 hints after attempts 1, 2, 3 — keep original order (final hint = giveaway)
            hint_schedule = {1: ("HINT 1", raw_hints[0]),
                             2: ("HINT 2", raw_hints[1]),
                             3: ("FINAL HINT", raw_hints[2])}
        elif difficulty == "medium":
            # 2 subtler hints after attempts 2 and 4 (skip the giveaway)
            hint_schedule = {2: ("HINT 1", raw_hints[0]),
                             4: ("HINT 2", raw_hints[1])}
        else:  # hard
            # 1 cryptic hint after attempt 4
            hint_schedule = {4: ("ONLY HINT", raw_hints[0])}
    else:
        hint_schedule = {}

    slow_print(f"\n{BOLD}{'═' * 40}{RESET}", 0.01)
    slow_print(f"{BOLD}  {icon} WORDLE — {mode_name} Mode{RESET}", 0.02)
    slow_print(f"{BOLD}{'═' * 40}{RESET}", 0.01)
    slow_print(f"  You have {CYAN}{max_attempts}{RESET} attempts. Type '{DIM}quit{RESET}' to exit.\n", 0.02)

    for attempt in range(1, max_attempts + 1):
        while True:
            raw = input(f"  Attempt {attempt}/{max_attempts}: ").strip().lower()
            if raw == "quit":
                print(f"\n  The word was: {BOLD}{secret.upper()}{RESET}")
                return False, attempt
            if raw == "hint":
                slow_print(f"  {DIM}Hints are automatic — keep playing!{RESET}", 0.02)
                continue
            error = validate_guess(raw, word_length, valid_words)
            if error:
                print(f"  {RED}{error}{RESET}")
            else:
                break

        feedback = get_feedback(raw, secret)
        guesses.append((raw, feedback))
        display_board(guesses, max_attempts, word_length)
        display_keyboard(guesses)

        # Show hints based on difficulty schedule (Normal mode only)
        if hint_schedule and attempt in hint_schedule and raw != secret:
            label, hint_text = hint_schedule[attempt]
            slow_print(f"\n  💡 {BOLD}{CYAN}{label}:{RESET} {hint_text}", 0.02)
            print()

        if raw == secret:
            msgs = ["Genius!", "Magnificent!", "Impressive!", "Splendid!", "Great!", "Phew!"]
            typing_effect(f"  🎉 {msgs[attempt - 1]} You got it in {attempt} guess{'es' if attempt > 1 else ''}!")
            return True, attempt

    slow_print(f"\n  😔 Out of attempts! The word was: {BOLD}{secret.upper()}{RESET}", 0.03)
    return False, max_attempts


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Terminal Wordle Clone")
    parser.add_argument("--wordfile", default="words.txt", help="Path to word list file")
    parser.add_argument("--length", type=int, default=5, help="Word length (default 5)")
    args = parser.parse_args()

    word_length = args.length
    all_words = load_words(args.wordfile, word_length)
    stats = load_stats()

    os.system("clear" if os.name != "nt" else "cls")
    display_welcome()

    while True:
        # Mode selection
        mode_key = display_mode_menu()
        mode_name, themed_list = GAME_MODES[mode_key]

        difficulty = "easy"
        if mode_name == "Normal":
            # Use the curated NORMAL_WORDS list so hints are guaranteed to exist
            mode_words = [w for w in NORMAL_WORDS if len(w) == word_length] or get_easy_words(all_words)
            valid_words = list(set(all_words + mode_words))
            difficulty = display_difficulty_menu()
        elif themed_list:
            # Filter themed words to correct length & ensure they exist
            mode_words = [w for w in themed_list if len(w) == word_length]
            if not mode_words:
                print(f"  {RED}No {word_length}-letter words for this mode. Falling back to Normal.{RESET}")
                mode_words = get_easy_words(all_words)
                mode_name = "Normal"
            # For themed modes, accept any word from the full dictionary as a guess
            valid_words = list(set(all_words + mode_words))
        else:
            mode_words = get_easy_words(all_words)
            valid_words = all_words

        secret = choose_word(mode_words)
        won, attempts = play_round(valid_words, secret, max_attempts=6, word_length=word_length, mode_name=mode_name, difficulty=difficulty)
        stats = update_stats(stats, won, attempts, 6)
        save_stats(stats)
        show_stats(stats)

        again = input("  Play again? (y/n): ").strip().lower()
        if again != "y":
            typing_effect(f"\n  {BOLD}Thanks for playing! 👋{RESET}", 0.03)
            break


if __name__ == "__main__":
    main()
