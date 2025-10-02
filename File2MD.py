import sys
import os
import ollama
import markdown

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QPlainTextEdit, QTextEdit, QFileDialog, QSplitter,
    QStatusBar, QLabel, QSizeGrip, QProgressBar, QStackedLayout
)
from PySide6.QtCore import (
    Qt, QPoint, QThread, Signal, QObject, QTimer, QUrl
)
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings

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

# ==============================================================================
# 3. WORKER THREAD FOR LLM COMMUNICATION
# ==============================================================================

class ConversionWorker(QObject):
    new_token = Signal(str)
    finished = Signal()
    error = Signal(str)
    progress = Signal(int)

    def __init__(self, text_to_convert):
        super().__init__()
        self.text_to_convert = text_to_convert

    def run(self):
        try:
            stream = ollama.generate(
                model=MODEL_NAME,
                prompt=self.text_to_convert,
                system=SYSTEM_PROMPT,
                stream=True
            )

            token_count = 0
            for chunk in stream:
                token = chunk.get('response', '')
                self.new_token.emit(token)
                token_count += 1
                if token_count % 10 == 0:
                    self.progress.emit(min(90, token_count // 10))

        except Exception as e:
            error_message = f"{type(e).__name__}: {e}"
            if "connection refused" in str(e).lower():
                error_message += "\n\nCannot connect to Ollama.\nPlease ensure the Ollama application is running."
            elif "model" in str(e).lower() and "not found" in str(e).lower():
                error_message += f"\n\nModel '{MODEL_NAME}' not found.\nRun: ollama pull {MODEL_NAME}"
            self.error.emit(error_message)
        finally:
            self.progress.emit(100)
            self.finished.emit()

# ==============================================================================
# 4. UI IMPLEMENTATION
# ==============================================================================

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_window = parent
        self.setObjectName("TitleBar")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.title_label = QLabel("File2MD")
        self.title_label.setObjectName("TitleLabel")
        layout.addWidget(self.title_label)

        layout.addStretch()

        self.minimize_button = QPushButton("0")
        self.minimize_button.clicked.connect(self.parent_window.showMinimized)
        self.maximize_button = QPushButton("1")
        self.maximize_button.clicked.connect(self.toggle_maximize_restore)
        self.close_button = QPushButton("r")
        self.close_button.setObjectName("CloseButton")
        self.close_button.clicked.connect(self.parent_window.close)

        layout.addWidget(self.minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(self.close_button)

    def toggle_maximize_restore(self):
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
            self.maximize_button.setText("1")
        else:
            self.parent_window.showMaximized()
            self.maximize_button.setText("2")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.parent_window.start_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.parent_window.start_pos is not None:
            if not self.parent_window.isMaximized():
                delta = event.globalPosition().toPoint() - self.parent_window.start_pos
                self.parent_window.move(self.parent_window.x() + delta.x(), self.parent_window.y() + delta.y())
                self.parent_window.start_pos = event.globalPosition().toPoint()
    
    def mouseReleaseEvent(self, event):
        self.parent_window.start_pos = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File2MD")
        self.setMinimumSize(900, 700)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.markdown_buffer = ""
        self.render_mode = True

        # Emulation state
        self.final_content = ""
        self.display_buffer = ""
        self.emulation_index = 0
        self.emulation_timer = QTimer(self)
        self.emulation_timer.timeout.connect(self._emulate_stream_tick)

        main_widget = QWidget()
        self.main_layout = QVBoxLayout(main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.title_bar = CustomTitleBar(self)
        self.main_layout.addWidget(self.title_bar)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(12, 12, 12, 12)
        content_layout.setSpacing(8)

        self.setup_ui(content_layout)
        self.main_layout.addWidget(content_widget)

        status_bar = QStatusBar()
        status_bar.setSizeGripEnabled(True)
        self.setStatusBar(status_bar)

        self.status_label = QLabel("Ready")
        self.statusBar().addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(150)
        
        self.setCentralWidget(main_widget)
        self.start_pos = None

    def setup_ui(self, layout):
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(6)

        self.load_button = QPushButton("Load File")
        self.load_button.clicked.connect(self.load_file)
        self.load_button.setProperty("class", "SecondaryButton")
        controls_layout.addWidget(self.load_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_all)
        self.clear_button.setProperty("class", "SecondaryButton")
        controls_layout.addWidget(self.clear_button)

        self.convert_button = QPushButton("Convert to Markdown")
        self.convert_button.setObjectName("ConvertButton")
        self.convert_button.clicked.connect(self.start_conversion_process)
        controls_layout.addWidget(self.convert_button)

        controls_layout.addStretch()

        self.toggle_view_button = QPushButton("View: Rendered")
        self.toggle_view_button.clicked.connect(self.toggle_view_mode)
        self.toggle_view_button.setProperty("class", "SecondaryButton")
        controls_layout.addWidget(self.toggle_view_button)

        self.copy_button = QPushButton("Copy")
        self.copy_button.clicked.connect(self.copy_output)
        self.copy_button.setProperty("class", "SecondaryButton")
        self.copy_button.setEnabled(False)
        controls_layout.addWidget(self.copy_button)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_output)
        self.save_button.setProperty("class", "SecondaryButton")
        self.save_button.setEnabled(False)
        controls_layout.addWidget(self.save_button)

        layout.addLayout(controls_layout)

        splitter = QSplitter(Qt.Horizontal)

        input_container = QWidget()
        input_layout = QVBoxLayout(input_container)
        input_layout.setContentsMargins(0, 6, 0, 0)
        input_layout.setSpacing(0)
        input_label = QLabel("Input")
        input_label.setProperty("class", "SectionHeader")
        input_layout.addWidget(input_label)
        self.input_text = QPlainTextEdit()
        self.input_text.setPlaceholderText("Paste your text here or load a file...")
        input_layout.addWidget(self.input_text)
        splitter.addWidget(input_container)

        output_panel_container = QWidget()
        output_panel_layout = QVBoxLayout(output_panel_container)
        output_panel_layout.setContentsMargins(0, 6, 0, 0)
        output_panel_layout.setSpacing(0)
        output_label = QLabel("Markdown Output")
        output_label.setProperty("class", "SectionHeader")
        output_panel_layout.addWidget(output_label)

        self.output_container = QWidget()
        self.output_layout = QStackedLayout(self.output_container)
        self.output_layout.setContentsMargins(0,0,0,0)

        self.output_raw_text = QTextEdit()
        self.output_raw_text.setReadOnly(True)
        self.output_raw_text.setPlaceholderText("Formatted markdown will appear here...")
        self.output_layout.addWidget(self.output_raw_text)

        self.web_view_container = QWidget()
        self.web_view_container.setObjectName("WebViewContainer")
        web_view_layout = QVBoxLayout(self.web_view_container)
        web_view_layout.setContentsMargins(8, 8, 8, 8)

        self.output_web_view = QWebEngineView()
        self.output_web_view.page().setBackgroundColor(Qt.GlobalColor.transparent)
        web_view_layout.addWidget(self.output_web_view)

        self.output_layout.addWidget(self.web_view_container)

        output_panel_layout.addWidget(self.output_container)
        splitter.addWidget(output_panel_container)
        
        splitter.setSizes([300, 600])
        layout.addWidget(splitter, 1)

        self._update_output_display()

    def _parse_markdown_from_buffer(self, buffer_text):
        start_tag = "<markdown>"
        end_tag = "</markdown>"

        start_index = buffer_text.find(start_tag)
        if start_index == -1:
            return ""

        content_start_index = start_index + len(start_tag)
        end_index = buffer_text.rfind(end_tag)

        if end_index == -1 or end_index < content_start_index:
            return ""
        else:
            return buffer_text[content_start_index:end_index].strip()

    def _update_output_display(self):
        if self.render_mode:
            self.output_layout.setCurrentWidget(self.web_view_container)
            html_content = markdown.markdown(self.display_buffer, extensions=['fenced_code', 'tables', 'nl2br'])
            full_html = f'<!DOCTYPE html><html><head><meta charset="utf-8">{MARKDOWN_CSS}</head><body>{html_content}</body></html>'
            self.output_web_view.setHtml(full_html, QUrl("about:blank"))
        else:
            self.output_layout.setCurrentWidget(self.output_raw_text)
            self.output_raw_text.setPlainText(self.display_buffer)

    def clear_all(self):
        self.input_text.clear()
        self.markdown_buffer = ""
        self.display_buffer = ""
        self.final_content = ""
        self.copy_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.status_label.setText("Ready")
        self._update_output_display()
        
    def toggle_view_mode(self):
        self.render_mode = not self.render_mode
        self.toggle_view_button.setText("View: Rendered" if self.render_mode else "View: Raw")
        self._update_output_display()

    def copy_output(self):
        QApplication.clipboard().setText(self.markdown_buffer)
        self.status_label.setText("Copied to clipboard")
        QTimer.singleShot(3000, lambda: self.status_label.setText("Ready"))

    def save_output(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Markdown", "", "Markdown Files (*.md);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.markdown_buffer)
                self.status_label.setText(f"Saved: {os.path.basename(file_path)}")
                QTimer.singleShot(5000, lambda: self.status_label.setText("Ready"))
            except Exception as e:
                self.status_label.setText(f"Error saving file: {e}")

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Text File", "", "Text Files (*.txt);;Markdown Files (*.md);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.input_text.setPlainText(f.read())
                self.status_label.setText(f"Loaded: {os.path.basename(file_path)}")
                QTimer.singleShot(3000, lambda: self.status_label.setText("Ready"))
            except Exception as e:
                self.status_label.setText(f"Error loading file: {e}")

    def start_conversion_process(self):
        input_content = self.input_text.toPlainText()
        if not input_content.strip():
            self.status_label.setText("Input is empty.")
            QTimer.singleShot(3000, lambda: self.status_label.setText("Ready"))
            return

        self.convert_button.setEnabled(False)
        self.convert_button.setText("Converting...")
        self.copy_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.status_label.setText("Processing with AI...")
        
        self.statusBar().addPermanentWidget(self.progress_bar)
        self.progress_bar.show()
        self.progress_bar.setValue(0)

        # Reset buffers for new conversion
        self.markdown_buffer = ""
        self.display_buffer = ""
        self.final_content = ""
        self.emulation_index = 0
        self._update_output_display()

        self.thread = QThread()
        self.worker = ConversionWorker(input_content)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.new_token.connect(self.append_token)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_conversion_finished)
        self.worker.error.connect(self.on_conversion_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def append_token(self, token):
        self.markdown_buffer += token

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def on_conversion_finished(self):
        raw_output = self.markdown_buffer
        self.final_content = self._parse_markdown_from_buffer(raw_output)
        
        parsed_successfully = bool(self.final_content)

        if not parsed_successfully:
            # Fallback: use the raw output if parsing fails
            self.final_content = raw_output.strip()
            self.status_label.setText("Parsing failed, showing raw output.")
        else:
            self.status_label.setText("Conversion complete. Rendering...")

        # The final, clean content is now also stored in markdown_buffer for copy/save
        self.markdown_buffer = self.final_content

        if self.final_content:
            self.emulation_timer.start(5)  # Start emulated streaming
        else: # Handle case where there is no output at all
            self.on_emulation_finished(parsed_successfully)


    def _emulate_stream_tick(self):
        if self.emulation_index < len(self.final_content):
            # Add a small chunk of characters to make streaming feel smooth
            chunk_size = max(1, len(self.final_content) // 200) # Adjust chunk size based on content length
            chunk = self.final_content[self.emulation_index : self.emulation_index + chunk_size]
            self.display_buffer += chunk
            self.emulation_index += chunk_size
            self._update_output_display()
        else:
            self.emulation_timer.stop()
            self.on_emulation_finished(True)
    
    def on_emulation_finished(self, parsed_successfully):
        # Final update to ensure the last chunk is rendered
        self.display_buffer = self.final_content
        self._update_output_display()
        
        if parsed_successfully:
            self.status_label.setText("Conversion complete.")
        else:
            self.status_label.setText("Conversion complete (parsing tags failed).")

        self.copy_button.setEnabled(True)
        self.save_button.setEnabled(True)
        self.reset_convert_button()
        QTimer.singleShot(5000, lambda: self.status_label.setText("Ready"))

    def on_conversion_error(self, error_message):
        self.display_buffer = f"An error occurred:\n\n{error_message}"
        if self.render_mode:
            self.toggle_view_mode()
        else:
            self._update_output_display()
            
        self.status_label.setText("Conversion failed.")
        self.reset_convert_button()

    def reset_convert_button(self):
        self.convert_button.setEnabled(True)
        self.convert_button.setText("Convert to Markdown")
        if self.progress_bar.parent():
            self.statusBar().removeWidget(self.progress_bar)

# ==============================================================================
# 5. APPLICATION ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET_MONO)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
