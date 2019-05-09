# vocativ

The easy to use plaintext dialog format.

---

Compiles to JSON and is work in progress.

Notes:
* The start state is called `[+]`
* If there are multiple states with the same name, one is chosen at random. (Including `[+]`)
* Each `.vocativ` file is a single dialog from a character.
* Empty lines are ignored.
* The rest of a line after a `#` is ignored.

## TODO
* Intermediate states that do nothing but have a few actions and then
    immediately switch into the next state.
* Use lark-parser for easier grammar definition
