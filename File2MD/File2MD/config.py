# ==============================================================================
# 1. APPLICATION CONFIGURATION
# ==============================================================================

MODEL_NAME = "granite4:tiny-h"

# Enhanced system prompt with clearer instructions
SYSTEM_PROMPT = """YOUR SOLE FUNCTION is to convert the user's raw text input into well-structured markdown. You are a formatting tool, NOT a creative assistant, editor, or conversational AI.

CRITICAL DIRECTIVES:
1.  OUTPUT MARKDOWN ONLY. Your entire response must be valid markdown text and nothing else. NO exceptions.
2.  ABSOLUTELY NO CONVERSATIONAL TEXT. Do not include headers like "Here is the markdown:" or any explanations, apologies, or comments.
3.  DO NOT ALTER THE CONTENT. You are forbidden from rephrasing, summarizing, correcting, adding to, or interpreting the user's original text. Your task is to structure the existing content, not change it.
4.  PRESERVE 100% OF THE ORIGINAL TEXT. Every word from the input must be present in the output. No words may be added or removed.
5.  ENCLOSE IN TAGS. Your entire output MUST be wrapped in a single `<markdown>`...`</markdown>` block. Start your response with `<markdown>` and end it with `</markdown>`.

Your output must be a pure, 1:1 markdown representation of the input text, enclosed in the specified tags. Failure to adhere to these rules makes your output useless."""

# ==============================================================================
# 2. PROFESSIONAL WINDOWS-STYLE THEME
# ==============================================================================

# --- SVG Icons for Splitter Handle ---
# A subtle 'grabber' icon for the default state
SVG_HANDLE_NORMAL = """
<svg width="10" height="30" xmlns="http://www.w3.org/2000/svg">
  <circle cx="5" cy="11" r="1.5" fill="#6E6E6E"/>
  <circle cx="5" cy="15" r="1.5" fill="#6E6E6E"/>
  <circle cx="5" cy="19" r="1.5" fill="#6E6E6E"/>
</svg>
""".replace("\n", "").strip()

# Directional arrows for the hover state
SVG_HANDLE_HOVER = """
<svg width="10" height="40" xmlns="http://www.w3.org/2000/svg">
  <path d="M 2 16 L 5 13 L 8 16" stroke="#FFFFFF" fill="none" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 2 24 L 5 27 L 8 24" stroke="#FFFFFF" fill="none" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
""".replace("\n", "").strip()


STYLESHEET_MONO = f"""
/* General */
QWidget {{
    background-color: #1e1e1e;
    color: #d4d4d4;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 9pt;
}}

QMainWindow {{
    border: 1px solid #333333;
}}

/* Custom Title Bar */
#TitleBar {{
    background-color: #2d2d2d;
    border-bottom: 1px solid #333333;
    height: 32px;
}}
#TitleBar #TitleLabel {{
    color: #cccccc;
    font-weight: 600;
    font-size: 10pt;
    padding-left: 8px;
}}
#TitleBar QPushButton {{
    background: transparent;
    border: none;
    width: 45px;
    height: 32px;
    font-family: "Webdings";
    color: #cccccc;
    font-size: 10pt;
}}
#TitleBar QPushButton:hover {{
    background-color: #3e3e3e;
    color: #ffffff;
}}
#TitleBar QPushButton#CloseButton:hover {{
    background-color: #c42b1c;
    color: #ffffff;
}}

/* Text Editors */
QPlainTextEdit, QTextEdit {{
    background-color: #252526;
    border: 1px solid #333333;
    border-radius: 4px;
    padding: 8px;
    selection-background-color: #264f78;
    selection-color: #ffffff;
    font-size: 10pt;
}}
QPlainTextEdit:focus, QTextEdit:focus {{
    border: 1px solid #007fd4;
}}

/* Container for Web View to match Text Edit style */
#WebViewContainer {{
    background-color: #252526;
    border: 1px solid #333333;
    border-radius: 4px;
}}

/* Main Action Button */
QPushButton#ConvertButton {{
    background-color: #007fd4;
    color: #ffffff;
    border: 1px solid #007fd4;
    padding: 6px 12px;
    border-radius: 4px;
    font-weight: 600;
    height: 28px;
}}
QPushButton#ConvertButton:hover {{
    background-color: #108fe4;
    border-color: #108fe4;
}}
QPushButton#ConvertButton:pressed {{
    background-color: #006dba;
    border-color: #006dba;
}}
QPushButton#ConvertButton:disabled {{
    background-color: #3a3d41;
    color: #888888;
    border-color: #3a3d41;
}}

/* Secondary Buttons */
QPushButton[class="SecondaryButton"] {{
    background-color: #3a3d41;
    color: #d4d4d4;
    border: 1px solid #3a3d41;
    padding: 6px 12px;
    border-radius: 4px;
    font-weight: 400;
    height: 28px;
}}
QPushButton[class="SecondaryButton"]:hover {{
    background-color: #4a4d51;
    border-color: #4a4d51;
}}
QPushButton[class="SecondaryButton"]:pressed {{
    background-color: #2a2d31;
}}
QPushButton[class="SecondaryButton"]:disabled {{
    background-color: #2d2d2d;
    color: #666666;
    border-color: #2d2d2d;
}}

/* Status Bar */
QStatusBar {{
    background-color: #2d2d2d;
    color: #aaaaaa;
    border-top: 1px solid #333333;
    height: 22px;
}}

/* Make all widgets inside the status bar transparent */
QStatusBar > * {{
    background-color: transparent;
}}

/* Progress Bar */
QProgressBar {{
    border: 1px solid #333333;
    border-radius: 3px;
    text-align: center;
    background-color: #252526;
    color: #d4d4d4;
    height: 6px;
    font-size: 8pt;
}}
QProgressBar::chunk {{
    background-color: #007fd4;
    border-radius: 2px;
}}

/* Splitter */
QSplitter::handle:horizontal {{
    background-color: transparent;
    width: 10px;
    image: url('data:image/svg+xml,{SVG_HANDLE_NORMAL}');
    background-repeat: no-repeat;
    background-position: center center;
}}
QSplitter::handle:horizontal:hover {{
    background-color: #007fd4;
    image: url('data:image/svg+xml,{SVG_HANDLE_HOVER}');
}}

/* Scrollbars */
QScrollBar:vertical {{
    border: none;
    background-color: #1e1e1e;
    width: 12px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background-color: #4d4d4d;
    border-radius: 6px;
    min-height: 25px;
}}
QScrollBar::handle:vertical:hover {{
    background-color: #5d5d5d;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
QScrollBar:horizontal {{
    border: none;
    background-color: #1e1e1e;
    height: 12px;
    margin: 0;
}}
QScrollBar::handle:horizontal {{
    background-color: #4d4d4d;
    border-radius: 6px;
    min-width: 25px;
}}
QScrollBar::handle:horizontal:hover {{
    background-color: #5d5d5d;
}}

/* Section Header Labels */
QLabel[class="SectionHeader"] {{
    color: #999999;
    font-size: 8pt;
    font-weight: 600;
    padding-bottom: 4px;
    text-transform: uppercase;
}}
"""

# Markdown CSS for rendered output, matches the application theme
MARKDOWN_CSS = """
<style>
/* Base Body Style */
body {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    line-height: 1.7;
    color: #d4d4d4;
    padding: 4px 0; /* Vertical padding only, horizontal is handled by container */
    background-color: #252526;
}

/* Custom Scrollbar for WebKit browsers (QWebEngineView) */
::-webkit-scrollbar {
    width: 12px;
    height: 12px;
}
::-webkit-scrollbar-track {
    background: #252526; /* Match the body background */
}
::-webkit-scrollbar-thumb {
    background-color: #4d4d4d;
    border-radius: 6px;
    border: 2px solid #252526; /* Creates a padding effect */
}
::-webkit-scrollbar-thumb:hover {
    background-color: #5d5d5d;
}

/* Markdown Content Styles */
h1, h2, h3, h4, h5, h6 {
    font-weight: 600;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    color: #ffffff;
}
h1 { font-size: 2em; border-bottom: 2px solid #3e3e3e; padding-bottom: 0.3em; }
h2 { font-size: 1.6em; border-bottom: 1px solid #333333; padding-bottom: 0.3em; }
h3 { font-size: 1.3em; }
h4 { font-size: 1.1em; }
p { margin: 0.8em 0; }
code {
    background-color: #1e1e1e;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 0.9em;
    color: #ce9178;
    border: 1px solid #333333;
}
pre {
    background-color: #1e1e1e;
    padding: 12px;
    border-radius: 4px;
    overflow-x: auto;
    border: 1px solid #333333;
}
pre code {
    background: none;
    padding: 0;
    border: none;
    color: #d4d4d4;
}
blockquote {
    border-left: 4px solid #4a4a4a;
    padding-left: 16px;
    margin-left: 0;
    color: #a0a0a0;
    font-style: italic;
}
ul, ol {
    margin: 0.8em 0;
    padding-left: 2em;
}
li {
    margin: 0.4em 0;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}
th, td {
    border: 1px solid #333333;
    padding: 8px 12px;
    text-align: left;
}
th {
    background-color: #2d2d2d;
    font-weight: 600;
}
tr:nth-child(even) {
    background-color: #2a2d31;
}
hr {
    border: none;
    border-top: 1px solid #333333;
    margin: 2em 0;
}
a {
    color: #3794ff;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
strong {
    font-weight: 700;
    color: #569cd6;
}
em {
    font-style: italic;
    color: #d4d4d4;
}
</style>
"""