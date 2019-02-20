# Registers

## Description
A Sublime Text plugin that adds the option to save text and macros to registers for quick use.
There are 10 possiblle registers, defined by a number from 0 to 9.
The input text can be some selected text or the text current in the clipboard.
Additonally, it's also possible to record the current native sublime macro in use into one of the resgisters, regardless of the content.

## Keyboard shortcuts

`ctrl+alt+[0-9]`: Output the chosen register save the current selected text into the current cursor position.  
E.g. `ctrl+alt+1` outputs register 1.

`ctrl+shift+r`, `[0-9]`: Inputs the current selected text into the chosen register.

`ctrl+shift+e`, `[0-9]`: Inputs the text current in the clipboard into the chosen register.

`ctrl+shift+q`, `[0-9]`: Inputs the current recorded macro into the chosen register.

`ctrl+alt+c`: Clear the content of all registers.
