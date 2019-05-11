# sprich

The easy to use plaintext dialog format.

Sprich (German: *speak*) is a tool for game developers to easily manage dialogs
for NPCs. It features a nice human readable format for creating the dialogs
and compiles them to JSON for you to embed in your game.

## Usage
Put all the `.sprich` files you want to compile in one directory and run:

    sprich input_directory

or

    sprich input_directory output_directory

Which will compile the files and place the resulting JSON - Files in the output
directory, or in the input directory, if no output directory was specified.

## Syntax
Each file consists of several states and other statements which are all on
their own line. In the following I will describe the intended behaviour for all
statements, in your game however you can exploit them as you wish.

Consult the folder `examples` for a few examples of the syntax in action.

Each state can have several actions followed by several options. If no options
are given or no action transitions into a new state the dialog is over.

### states
The default start state in sprich is considered to be named `[+]` and other
states can be named by a mix of letters, numbers and underscores.

### messages
The simplest action is a message your character should say:

    [+]
    "Hello!"

### options
Once all actions in a state have been processed you can show options to your user.
They define a text that should be selectable follow by an optional state and a
condition. The option should only be selectable/visible if the condition holds true.
If no state is given the option ends the dialog.

Conditions are always strings that your game needs to process.

    [+]
    "Hello! How are you?"
    > "Good" [good]
    > "Bad" [bad] "mood == 0"
    > "I don't want to talk"

### function calls
You can call any function with parameters seperated by spaces. A function call
is denoted by a `\`.

    [+]
    \think
    \feel "happy" 3
    "Nice to meet you!"

### instant transitions
Instants can be used for intermediate states. They start with a `->` followed by
a state and an optional condition. If no condition is given the instant will be
acted out immediately. This can be useful for checking conditions at the start
of a dialog.

    [+]
    -> [grumpy] "weather == bad"
    -> [happy]
