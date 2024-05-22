import hashlib

import os

base_dir = os.path.join(os.environ['HOME'], 'spmbasics')
data_dir = os.path.join(base_dir, 'data')
output_dir = os.path.join(base_dir, 'output')
src_dir = os.path.join(base_dir, 'src')
referencedata_dir = os.path.join(base_dir, 'facerep') #MoAEpilot
nipype_dir = os.path.join(src_dir, 'nipype')
results_dir = os.path.join(base_dir, 'results')

file_extension = '.nii'

def calculate_shasums(input_folder, file_extension):
    output_file = f"{os.path.splitext(input_folder)[0]}_shasums.txt"

    shasums = []

    for root, files in os.walk(input_folder):
        for file in files:
            if file.endswith(file_extension):
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    sha_sum = hashlib.sha256(f.read()).hexdigest()
                    shasums.append(sha_sum)

    with open(output_file, 'w') as f:
        f.write('\n'.join(shasums)) # check if it knows output folder
    return output_file

calculate_shasums(data_dir)




def compare_shasums(reference, file1):
    output_file = os.path.join(results_dir, 'all_results.txt')
    outputs = []
    with open(reference, 'r') as ref_file, open(file1, 'r') as file1:
        ref_content = ref_file.read()
        file1_content = file1.read()
        if ref_content == file1_content:
            with open(output_file, 'a') as output:
                output.write(f"SHA256sums are identical for {reference} and {file1}\n")
                outputs.append(output)
        else:
            with open(output_file, 'a') as output:
                output.write(f"SHA256sums are not identical for {reference} and {file1}\n")
                outputs.append(output)
    with open(output_file, 'w') as f:
        f.write('\n'.join(outputs))
    return output_file

compare_shasums('data_shasums.txt', 'reference_shasums.txt')       

