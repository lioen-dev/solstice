import os
import sys
import tempfile
import subprocess

def parse():
    result = []
    current_block = []
    in_block = False
    brace_count = 0
    
    with open(sys.argv[1], 'r') as file:
        for line in file:
            line = line.strip()
            
            # Skip empty lines or comments
            if not line or line.startswith('~'):
                continue
            
            # Check for opening brace
            if '{' in line:
                in_block = True
                brace_count += line.count('{')
                current_block.append(line)
                continue
            
            # If we're in a block
            if in_block:
                brace_count += line.count('{')
                brace_count -= line.count('}')
                current_block.append(line)
                
                # If we've closed all braces
                if brace_count == 0:
                    in_block = False
                    # Merge the block into a single line
                    merged_line = ' '.join(current_block)
                    result.append(merged_line)
                    current_block = []
                continue
            
            # Normal line outside of block
            result.append(line)
    
    return result

def run_interpreter(parsed_lines):
    # Create a temporary file to store the parsed code
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
        for line in parsed_lines:
            temp_file.write(line + '\n')
        temp_file_path = temp_file.name

    try:
        # Run the interpreter with the temporary file
        interpreter_path = os.path.join(os.path.dirname(__file__), 'interpreter.py')
        subprocess.run([sys.executable, interpreter_path, temp_file_path])
    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)

def init():
    print("Parsing...")
    if len(sys.argv) > 1:
        try:
            parsed_lines = parse()
            run_interpreter(parsed_lines)
        except FileNotFoundError:
            print(f"File {sys.argv[1]} not found!")
        except Exception as e:
            print(f"Error reading file: {e}")
    else:
        interpreter_path = os.path.join(os.path.dirname(__file__), 'interpreter.py')
        subprocess.run([sys.executable, interpreter_path])

init()