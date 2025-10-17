<div align="center">

<img width="753" height="450" alt="File2MD_Banner_001" src="https://github.com/user-attachments/assets/f6a909e8-68ff-4a57-a9a4-8047e98e8f32" />


# File2MD

### A Modern Desktop App for AI-Powered Text-to-Markdown Conversion

<p>
    <a href="https://github.com/dovvnloading/File2MD/blob/main/LICENSE">
        <img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License: Apache 2.0">
    </a>
    <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python Version">
    <img src="https://img.shields.io/badge/Framework-PySide6-2796EC.svg" alt="Framework: PySide6">
    <img src="https://img.shields.io/badge/AI-Ollama-000000.svg" alt="AI Backend: Ollama">
    <a href="https://github.com/dovvnloading/File2MD">
        <img src="https://img.shields.io/github/last-commit/dovvnloading/File2MD" alt="Last Commit">
    </a>
</p>

</div>

---

**File2MD** is a sleek, efficient desktop application that leverages the power of local large language models via [Ollama](https://ollama.com/) to instantly convert raw text into beautifully structured Markdown. It's designed for developers, writers, and anyone who needs to quickly format notes, documentation, or content without relying on cloud-based services.

<br>



<img width="1371" height="867" alt="Screenshot 2025-10-02 145623" src="https://github.com/user-attachments/assets/a25bdc9b-9376-4fd3-a968-75421b6dcf1d" />


## Key Features

-   **🔒 Private, Local-First AI**: All text processing happens on your machine. Your data never leaves your computer, ensuring complete privacy and offline functionality.
-   **⚡ Real-Time Streaming Output**: Watch the formatted Markdown appear token-by-token, providing an interactive and responsive experience.
-   **↔️ Dual-View Interface**: A side-by-side view allows you to see your raw text and the formatted output simultaneously.
-   **🎨 Rendered & Raw Preview**: Toggle between a live, beautifully styled HTML preview and the raw Markdown source with a single click.
-   **✨ Modern & Themed UI**: Built with PySide6, the application features a professional, dark-themed UI that is both aesthetic and functional.
-   **📂 File Operations**: Easily load text from `.txt` or `.md` files and save your final Markdown output.

## Technology Stack

-   **Backend**: Python 3
-   **GUI Framework**: PySide6
-   **AI Engine**: Ollama
-   **Markdown Parsing**: Python-Markdown library

## Getting Started

Follow these instructions to get File2MD up and running on your local machine.

### Prerequisites

1.  **Python**: Ensure you have Python 3.9 or newer installed.
2.  **Ollama**: You must have the [Ollama](https://ollama.com/) application installed and running on your system.
3.  **Ollama Model**: Pull the required model by running the following command in your terminal:
    ```sh
    ollama pull granite4:tiny-h
    ```
    > **Note:** You can configure a different model by changing the `MODEL_NAME` variable in `config.py`.

### Installation & Launch

1.  **Clone the Repository**
    ```sh
    git clone https://github.com/dovvnloading/File2MD.git
    cd File2MD
    ```

2.  **Create and Activate a Virtual Environment** (Recommended)
    ```sh
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    A `requirements.txt` is needed to install the necessary packages. Create the file with the content below, or find it in the repository.

    **`requirements.txt`:**
    ```
    PySide6
    ollama
    Markdown
    PySide6-WebEngine
    ```

    Install the packages using pip:
    ```sh
    pip install -r requirements.txt
    ```

4.  **Run the Application**
    With Ollama running in the background and your virtual environment active, launch the app:
    ```sh
    python File2MD.py
    ```

## Usage

1.  **Load Content**: Click `Load File` to open a text or markdown file, or simply paste your text into the "Input" pane on the left.
2.  **Convert**: Click the `Convert to Markdown` button.
3.  **View Output**: The AI-formatted Markdown will stream into the "Markdown Output" pane on the right.
4.  **Toggle View**: Use the `View: Raw` / `View: Rendered` button to switch between the raw Markdown source and a styled HTML preview.
5.  **Save or Copy**: Once the conversion is complete, use the `Save` or `Copy` buttons to export your result.

## Project Structure

The project is organized into several modules to maintain clean architecture and separation of concerns.

-   `File2MD.py`: The main entry point of the application. It initializes the Qt Application and the main window.
-   `main_window.py`: Contains the `MainWindow` class, which defines the UI layout, connects signals/slots, and manages the application's state.
-   `config.py`: A centralized module for all static configuration, including the AI model name, system prompt, and UI stylesheets.
-   `worker.py`: Defines the `ConversionWorker` class, which runs the Ollama AI conversion in a separate thread to keep the UI responsive.
-   `ui_components.py`: Houses custom UI widgets, such as the `CustomTitleBar`, to keep the main window code clean.

## License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](https://github.com/dovvnloading/File2MD/blob/main/LICENSE) file for more details.

---

<div align="center">
Made with ❤️ by dovvnloading
</div>
