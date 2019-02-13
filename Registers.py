import sublime
import sublime_plugin

SELECTIONS = [('text', [])] * 10


class OutputRegisterCommand(sublime_plugin.TextCommand):
    def run(self, edit, num):
        selection = SELECTIONS[num][1]
        if SELECTIONS[num][0] == 'macro':
            for macro_cmd in selection:
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


class InputClipboardCommand(sublime_plugin.TextCommand):
    def run(self, edit, num):
        SELECTIONS[num] = ('text', [sublime.get_clipboard()])


class InputMacroCommand(sublime_plugin.TextCommand):
    def run(self, edit, num):
        SELECTIONS[num] = ('macro', sublime.get_macro())


class ClearRegistersCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global SELECTIONS
        SELECTIONS = [('text', [])] * 10
