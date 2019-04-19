import sublime
import sublime_plugin


settings_filename = 'Registers.sublime-settings'

REG_SET = sublime.load_settings(settings_filename)


class OutputRegisterCommand(sublime_plugin.TextCommand):
    def run(self, edit, num):
        if REG_SET.has('register_' + str(num)):
            mode, selection = REG_SET.get('register_' + str(num))
            if mode == 'macro':
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
        else:
            REG_SET.set('register_' + str(num), ['text', []])


class _InputCommand(sublime_plugin.TextCommand):
    def run(self, edit, num):
        data = self.get_data()
        REG_SET.set('register_' + str(num), data)
        sublime.save_settings(settings_filename)


class InputSelectionCommand(_InputCommand):
    def get_data(self):
        return ['text', [self.view.substr(region)
                         for region in self.view.sel()]]


class InputClipboardCommand(_InputCommand):
    def get_data(self):
        return ['text', [sublime.get_clipboard()]]


class InputMacroCommand(_InputCommand):
    def get_data(self):
        return ['macro', sublime.get_macro()]


class ClearRegistersCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for num in range(10):
            REG_SET.set('register_' + str(num), ['text', []])
            sublime.save_settings(settings_filename)
