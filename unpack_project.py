import os
import re

def unpack_markdown_to_project(md_filepath, output_dir="."):
    """
    Parses a combined project markdown file and unpacks it back 
    into individual files and directories.
    """
    if not os.path.exists(md_filepath):
        print(f"Error: Source markdown file '{md_filepath}' not found.")
        return

    print(f"Starting unpack sequence from: {md_filepath}")
    
    with open(md_filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex breakdown:
    # ### File: `(.*?)` matches the file path header block
    # \n```[a-zA-Z]*\n(.*?)``` matches the code block and captures the inside content
    pattern = re.compile(r"### File:\s*`([\s\S]*?)`\s*\n```[a-zA-Z]*\n([\s\S]*?)```", re.MULTILINE)
    matches = pattern.findall(content)

    if not matches:
        print("No files found to unpack. Check if the heading format matches '### File: `path`'.")
        return

    for filepath, file_content in matches:
        # Clean leading slashes or whitespaces to prevent path logic breaks
        filepath = filepath.strip().lstrip("/")
        
        # Combine target directory with the intended file path
        target_path = os.path.join(output_dir, filepath)
        
        # Extract the directory portion of the path
        parent_dir = os.path.dirname(target_path)
        
        # Automatically create directories if they don't exist yet
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
            print(f"Created directory: {parent_dir}")

        # Write the captured content back into the fresh file
        with open(target_path, 'w', encoding='utf-8') as target_file:
            target_file.write(file_content)
            
        print(f"Successfully unpacked: {target_path}")

    print("\nUnpacking sequence complete!")

if __name__ == "__main__":
    # Change 'project_backup.md' to whatever your source file is named
    unpack_markdown_to_project("ai_context.md", output_dir="recreated_project")