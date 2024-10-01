import os
import re

def find_php_files(directory):
    php_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.php'):
                php_files.append(os.path.join(root, file))
    return php_files

def extract_functions_from_php(file_path):
    functions = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        # Fallback für nicht-UTF-8 Dateien
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                content = file.read()
        except Exception as e:
            print(f"Fehler beim Lesen der Datei {file_path}: {e}")
            return functions  # Rückkehr mit leerer Liste, falls Dekodierung fehlschlägt

    # Finde die Funktionsblöcke (einschließlich der Funktionstexte)
    function_matches = re.findall(r'(function\s+[^\s\(]+\s*\([^\)]*\)\s*\{[^}]*\})', content, re.DOTALL)
    return function_matches

def sanitize_filename(func_name):
    # Entfernt ungültige Zeichen für Dateinamen
    return re.sub(r'[^\w\-_\.]', '_', func_name)

def write_function_to_file(function_text, func_name, output_dir):
    # Bereinigen des Funktionsnamens für den Dateinamen
    sanitized_name = sanitize_filename(func_name)
    # Erstelle das Ausgabe-Verzeichnis, falls es noch nicht existiert
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Erstelle eine Datei mit dem bereinigten Funktionsnamen im PhpFunctions-Verzeichnis
    output_file = os.path.join(output_dir, f"{sanitized_name}.php.func")
    with open(output_file, 'w', encoding='utf-8') as file:
        # Kopfzeile schreiben
        file.write("<?php\n")
        file.write("/*\n * PHP Funktionsextraktor\n */\n\n")
        # Funktionstext schreiben
        file.write(function_text)
        # Fußzeile schreiben
        file.write("\n?>")

def main(directory, output_dir):
    php_files = find_php_files(directory)
    for php_file in php_files:
        functions = extract_functions_from_php(php_file)
        for function_text in functions:
            # Finde den Funktionsnamen, um die Datei korrekt zu benennen
            func_name_match = re.search(r'function\s+([^\s\(]+)', function_text)
            if func_name_match:
                func_name = func_name_match.group(1)
                # Schreibe die Funktion in eine eigene Datei im PhpFunctions-Verzeichnis
                write_function_to_file(function_text, func_name, output_dir)
    
    print(f"Extracted functions from {len(php_files)} PHP files and saved them to the '{output_dir}' directory.")

if __name__ == "__main__":
    directory = "."  # Hauptverzeichnis (aktuelles Verzeichnis)
    output_dir = "PhpFunctions"  # Verzeichnis für die Ausgabedateien

    main(directory, output_dir)
