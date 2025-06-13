# Keyboard Action Recorder & Playback Tool

A background Python utility that records and replays keyboard actions with customizable automation, encryption, and UI themes. Originally created to automate tedious typing tasks (like writing common code structures), this was my first Python project and continues to help streamline my coding workflow today.

---

## Features

### 🎬 Record & Playback
- **Ctrl+Shift+R**: Start or stop recording keyboard actions.
- After recording:
  - Choose how many times to replay the actions.
  - Option to **replay with no delay** between keypresses.
  - Save the recording with a custom name.

### ⚙️ Settings Menu (`Ctrl+Shift+S`)
Opens a multi-tab interface with the following:

---

### 🔁 Shortcuts / Automations
- Run previously saved shortcuts (with same playback options).
- Create automations: assign saved shortcuts to custom keybindings.
- Delete existing shortcuts or automations.

---

### 🎨 Miscellaneous Settings
- **Display Settings**:
  - Toggle between light or dark mode.
  - Choose a color theme (uses `customtkinter`).
- **File Settings**:
  - Choose to **compress and encrypt** saved shortcuts/automations.
  - **Encryption Notes**:
    - A compiled Python script is generated with a key stored inside.
    - The key **self-destructs** if the program’s file path is changed or the key is accessed directly.
    - **Warning**: If the key is destroyed, encrypted data is permanently lost.

---

### 📚 Information
- GitHub Releases – Link to release versions.
- YouTube Tutorial *(no longer available)*.
- Support via Venmo – Optional donation link.

---

## Usage Ideas

This tool is ideal for:
- Automating repetitive keyboard input.
- Creating code snippet macros (e.g., auto-writing a `for` loop or `if` block).
- Reducing fatigue from typing boilerplate code.

---

## 💻 How to Run

1. **Install Dependencies**  
   Make sure you have Python 3 installed. and run
   ```bash
   python src/main.py
    ```
2. This will automatically install the required libraries.
3. Program will continue to run in the background and the user can use the keybinding to record or open settings.
