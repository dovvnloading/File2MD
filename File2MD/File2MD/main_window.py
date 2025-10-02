import os
import markdown

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QPlainTextEdit, QTextEdit, QFileDialog, QSplitter,
    QStatusBar, QLabel, QProgressBar, QStackedLayout
)
from PySide6.QtCore import Qt, QThread, QTimer, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView

from ui_components import CustomTitleBar
from worker import ConversionWorker
from config import MARKDOWN_CSS

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

        self.toggle_view_button = QPushButton("View: Raw")
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
        self.toggle_view_button.setText("View: Raw" if self.render_mode else "View: Rendered")
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
            # If we're in render mode and an error occurs, the error message
            # likely contains newlines that won't show. Switch to raw view
            # to ensure the message is readable.
            self.toggle_view_mode() 
        else:
            # If we're already in raw view, just update the text.
            self._update_output_display()
            
        self.status_label.setText("Conversion failed.")
        self.reset_convert_button()

    def reset_convert_button(self):
        self.convert_button.setEnabled(True)
        self.convert_button.setText("Convert to Markdown")
        if self.progress_bar.parent():
            self.statusBar().removeWidget(self.progress_bar)