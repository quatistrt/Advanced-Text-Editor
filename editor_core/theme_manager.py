class ThemeManager:
    THEMES = {
        "Dracula": {
            "bg": "#282a36", "fg": "#f8f8f2", "select": "#44475a",
            "keyword": "#ff79c6", "func": "#50fa7b", "string": "#f1fa8c", "comment": "#6272a4"
        },
        "Monokai": {
            "bg": "#272822", "fg": "#f8f8f2", "select": "#49483e",
            "keyword": "#f92672", "func": "#a6e22e", "string": "#e6db74", "comment": "#75715e"
        },
        "Nord": {
            "bg": "#2e3440", "fg": "#d8dee9", "select": "#434c5e",
            "keyword": "#81a1c1", "func": "#88c0d0", "string": "#a3be8c", "comment": "#4c566a"
        },
        "Solarized Dark": {
            "bg": "#002b36", "fg": "#839496", "select": "#073642",
            "keyword": "#859900", "func": "#268bd2", "string": "#2aa198", "comment": "#586e75"
        },
        "One Dark Pro": {
            "bg": "#282c34", "fg": "#abb2bf", "select": "#3e4451",
            "keyword": "#c678dd", "func": "#61afef", "string": "#98c379", "comment": "#5c6370"
        },
    }

    @staticmethod
    def get_theme(name):
        return ThemeManager.THEMES.get(name, ThemeManager.THEMES["Dracula"])

    @staticmethod
    def list_themes():
        return list(ThemeManager.THEMES.keys())
