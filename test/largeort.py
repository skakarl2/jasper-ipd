import heapq
import os

def sort_large_file(input_path, output_path, chunk_size=1000000):
    temp_files = []

    # Step 1: Read and sort chunks
    with open(input_path, 'r') as f:
        chunk = []
        for line in f:
            chunk.append(line)
            if len(chunk) >= chunk_size:
                chunk.sort()
                temp_path = f'{input_path}_chunk_{len(temp_files)}.tmp'
                with open(temp_path, 'w') as tmpf:
                    tmpf.writelines(chunk)
                temp_files.append(temp_path)
                chunk = []
        if chunk:
            chunk.sort()
            temp_path = f'{input_path}_chunk_{len(temp_files)}.tmp'
            with open(temp_path, 'w') as tmpf:
                tmpf.writelines(chunk)
            temp_files.append(temp_path)

    # Step 2: Merge chunks
    files = [open(p, 'r') for p in temp_files]
    with open(output_path, 'w') as out:
        for line in heapq.merge(*files):
            out.write(line)

    for f in files:
        f.close()
    for p in temp_files:
        os.remove(p)

# Usage example:
# sort_large_file('huge_input.txt', 'sorted_output.txt')