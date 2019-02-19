import sublime
import sublime_plugin
import json
import os

OUTFILE = 'Persistent/saved_registers.json'


def check_selections():
    if len(SELECTIONS) != 10:
        return False
    try:
        for t, content in SELECTIONS:
            if t not in ('text', 'macro') or not isinstance(content, list):
                return False
    except Exception:
        return False

    return True


DIR_PATH = os.path.dirname(os.path.realpath(__file__))

with open(DIR_PATH + '/' + OUTFILE, 'r') as f:
    SELECTIONS = json.load(f)

if not check_selections():
    SELECTIONS = [('text', [])] * 10


def _save_as_json():
    with open(DIR_PATH + '/' + OUTFILE, 'w') as f:
        json.dump(SELECTIONS, f)


class OutputRegisterCommand(sublime_plugin.TextCommand):
    def run(self, edit, num):
        selection = SELECTIONS[num][1]
        if SELECTIONS[num][0] == 'macro':
            for macro_cmd in selection:
                if macro_cmd['args'] is None:
                    self.view.run_command(macro_cmd['command'])
                else:
                    self.view.run_command(macro_cmd['command'],
                                          args=macro_cmd['args'])
        else:
            sel = self.view.sel()
            if len(selection) > 1:
                for out, cur_pos in zip(selection, sel):
                    self.view.insert(edit, cur_pos.begin(), out)
            elif len(selection) > 0:
                out = selection[0]
                for cur_pos in sel:
                    self.view.insert(edit, cur_pos.begin(), out)


class InputSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit, num):
        SELECTIONS[num] = ('text', [self.view.substr(region)
                                    for region in self.view.sel()])
        _save_as_json()


class InputClipboardCommand(sublime_plugin.TextCommand):
    def run(self, edit, num):
        SELECTIONS[num] = ('text', [sublime.get_clipboard()])
        _save_as_json()


class InputMacroCommand(sublime_plugin.TextCommand):
    def run(self, edit, num):
        SELECTIONS[num] = ('macro', sublime.get_macro())
        _save_as_json()


class ClearRegistersCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global SELECTIONS
        SELECTIONS = [('text', [])] * 10
        _save_as_json()
