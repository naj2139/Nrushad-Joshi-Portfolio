# Trie-Based Contacts Lookup

A C++ solution to the HackerRank Data Structures problem "Contacts," which asks: given a stream of `add`/`find` operations on a set of contact names, efficiently report how many stored contacts share a given prefix — extended here with a third `search` operation that checks for an exact, complete contact.

## Overview

Contacts are stored in a **trie (prefix tree)**, where each node represents one letter along some inserted name. The program supports three operations, read from the command line as `<command> <value>` pairs:

| Operation | Input | Behavior |
|---|---|---|
| `add <name>` | a contact name | Inserts the name into the trie |
| `find <partial>` | a prefix | Returns how many stored contacts start with that prefix |
| `search <word>` | a full word | Returns `Yes` if `word` was inserted as a complete contact, `No` if it only exists as a prefix of a longer contact |

## Example

**Input:**
```
add superhero search superhero search super find sup
```

**Output:**
```
[1, No]
```

Here, `search superhero` would return `Yes` on its own (an exact match exists), but since `search super` runs afterward — and `"super"` was never added as its own contact, only as a prefix of `"superhero"` — the final printed result is `No`. `find sup` counts 1 contact ("superhero") starting with that prefix.

## Key Implementation Details

- **Prefix counting at insertion time** — each trie node tracks `prefix_count`, incremented for every contact that passes through it during `add`. This lets `find` answer "how many contacts share this prefix?" in O(prefix length) time, without rescanning all stored contacts.
- **End-of-word marker via a shared sentinel node** — `children[ALPHABET_LENGTH]` (index 26) is used purely as a null/non-null flag marking "a contact ends here." Since its contents are never read, every completed word points at one shared `endMarker` node allocated once in `main`, rather than a fresh heap allocation per word.
- **Whole-word vs. prefix distinction** — `search` walks the same letter path as `find`, but only returns `Yes` if the end-of-word marker is set at the final node, correctly distinguishing a real contact (`"superhero"`) from a string that merely happens to be a prefix of one (`"super"`).
- **General input handling** — commands and values are lowercased in place before processing, so mixed-case input on the command line is handled consistently.

## Usage

Build everything with the included `Makefile`:
```bash
make all
```

Or build just this project:
```bash
make contacts
```

Run against a sequence of operations:
```bash
./Contacts/contacts add superhero search superhero search super find sup
```