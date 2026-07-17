import os

def dump_codebase(output_filename="ai_context.md"):
    # The file extensions you want to capture
    allowed_extensions = {".py", ".md", ".json"}
    
    # Get the absolute path of the directory where this script is located
    root_dir = os.path.dirname(os.path.abspath(__file__)) or "."
    
    with open(output_filename, "w", encoding="utf-8") as out_file:
        out_file.write("# Project Codebase\n\n")
        
        # os.walk automatically goes through all subfolders
        for dirpath, _, filenames in os.walk(root_dir):
            for filename in filenames:
                _, ext = os.path.splitext(filename)
                
                # Check if the file matches our desired extensions
                if ext.lower() in allowed_extensions:
                    
                    # Prevent the script from reading its own output file or itself
                    if filename == output_filename or filename == os.path.basename(__file__):
                        continue
                        
                    # Build the full file path and a clean relative path
                    file_path = os.path.join(dirpath, filename)
                    relative_path = os.path.relpath(file_path, root_dir)
                    
                    try:
                        with open(file_path, "r", encoding="utf-8") as in_file:
                            content = in_file.read()
                            
                        # Format the output specifically for AI readability
                        out_file.write(f"### File: `/{relative_path}`\n")
                        
                        # Map extensions to markdown language tags
                        lang = ext.replace(".", "")
                        if lang == "py": 
                            lang = "python"
                        
                        out_file.write(f"```{lang}\n")
                        out_file.write(content)
                        # Ensure the code block closes cleanly on a new line
                        if not content.endswith('\n'):
                            out_file.write("\n")
                        out_file.write("```\n\n")
                        
                    except Exception as e:
                        out_file.write(f"### File: `/{relative_path}`\n")
                        out_file.write(f"> Error reading file: {str(e)}\n\n")

    print(f"Codebase successfully aggregated into '{output_filename}'")

if __name__ == "__main__":
    dump_codebase()