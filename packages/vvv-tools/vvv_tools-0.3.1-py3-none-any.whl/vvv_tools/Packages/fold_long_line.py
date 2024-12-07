import sublime
import sublime_plugin

class FoldExcessLengthOnLoad(sublime_plugin.EventListener):
    def __init__(self):
        self.max_line_length = 500  # 定义最大行长度

    def on_load(self, view):
        self.fold_excess_length(view)

    def fold_excess_length(self, view):
        settings = sublime.load_settings('Preferences.sublime-settings')
        max_line_length = settings.get('max_line_length', self.max_line_length)
        
        for region in view.lines(sublime.Region(0, view.size())):
            line_text = view.substr(region)
            if len(line_text) > max_line_length:
                excess_region = sublime.Region(region.begin() + max_line_length, region.end())
                view.fold(excess_region)

    def on_activated(self, view):
        self.fold_excess_length(view)