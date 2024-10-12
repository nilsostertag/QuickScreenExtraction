import subprocess
import os
import tempfile

def open_in_notepad(text):
    # Erstelle eine temporäre Datei im Textmodus
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w', encoding='utf-8') as temp_file:
        # Schreibe den Text in die temporäre Datei
        temp_file.write(text)
        # Speichere den Pfad der Datei
        temp_file_path = temp_file.name

    # Öffne die temporäre Datei mit dem Standard-Editor (Notepad in diesem Fall)
    subprocess.Popen(['notepad.exe', temp_file_path])

    # Hinweis: Da die Datei mit `delete=False` geöffnet wurde, wird sie nicht automatisch gelöscht.
    # Die Datei kann manuell gelöscht werden, sobald Notepad geschlossen wurde.
    return temp_file_path  # Den Pfad zurückgeben, falls man ihn später verwenden möchte