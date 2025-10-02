import ollama
from PySide6.QtCore import QObject, Signal

from config import MODEL_NAME, SYSTEM_PROMPT

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