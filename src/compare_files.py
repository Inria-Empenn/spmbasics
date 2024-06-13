
import os
import hashlib
import numpy as np
import nibabel as nb


base_dir = os.path.join(os.environ['HOME'], 'spmbasics')
data_dir = os.path.join(base_dir, 'data')
output_dir = os.path.join(data_dir, 'output')
src_dir = os.path.join(base_dir, 'src')
blockdata_dir = os.path.join(data_dir, 'MoAEpilot')
guiblock_dir = os.path.join(output_dir, 'MoAEpilot_gui')
batchblock_dir = os.path.join(output_dir, 'MoAEpilot_batch')
scriptblock_dir = os.path.join(output_dir, 'MoAEpilot_script')
nipype_block_dir = os.path.join(output_dir, 'nipype/block_preprocesss/_subject_id_01_task_name_auditory')

eventdata_dir = os.path.join(data_dir, 'face_rep') 
eventgui_dir = os.path.join(output_dir, 'face_rep_gui')
eventbatch_dir = os.path.join(output_dir, 'face_rep_batch')
eventscript_dir = os.path.join(output_dir, 'face_rep_script')

nipype_event_dir = os.path.join(output_dir, 'nipype/event_preproc/_subject_id_M03953')
results_dir = os.path.join(base_dir, 'results')

file_extension = ['.nii', '.img']

def calculate_shasums(input_folder):
    '''
    This function calculates the SHA256sums of the files in the input directory and writes them to a text file.
    '''
    #init_output_filename = f"{os.path.splitext(input_folder)[0]}_init_shasums.txt" 
    # to get the initial values of the shasums
    output_filename = f"{os.path.splitext(input_folder)[0]}_shasums.txt"
    #init_output_file = open(init_output_filename, 'w')
    output_file = open(output_filename, 'w')
    shasums = [] # to store the shasums

    for root, dir, files in os.walk(input_folder):
        for file in files:
            if any(file.endswith(ext) for ext in file_extension):
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    sha_sum = hashlib.sha256(f.read()).hexdigest()
                    shasums.append(sha_sum)

     # Write the checksums to the file
    for sha_sum in shasums:
        #init_output_file.write(f"{sha_sum}\n")
        output_file.write(f"{sha_sum}\n")

    output_file.close()
    #init_output_file.close()
    # return init_output_filename
    return output_filename



#calculate_shasums(blockdata_dir)
#calculate_shasums(guiblock_dir)
#calculate_shasums(batchblock_dir)
#calculate_shasums(scriptblock_dir)
#calculate_shasums(eventdata_dir)
#calculate_shasums(eventgui_dir)
#calculate_shasums(eventbatch_dir)
#calculate_shasums(eventscript_dir)
#calculate_shasums(nipype_event_dir)

def comparetxtfiles(input_file1, input_file2):
    '''
    This function compares the SHA256sums of the files in the input directories and writes the results to a text file.
    '''
    if not os.path.isfile(input_file1):
        raise Exception(f"Input file {input_file1} does not exist")
    else :
        if not os.path.isfile(input_file2):
         raise Exception(f"Input file {input_file2} does not exist")
        
    _, output_tail = os.path.split(f"{os.path.splitext(input_file2)[0]}_comparisons.txt")    
    output_filepath = os.path.join(results_dir, output_tail)
    output_file = open(output_filepath, 'w')
    
    #with open(output_filepath, 'w') as f:
    shasums1 = []
    shasums2 = []
    shasums = []
    with open(input_file1, 'r') as f:
        for line in f:
            shasums1.append(line.strip())
    with open(input_file2, 'r') as f:
        for line in f:
            shasums2.append(line.strip())
    if shasums1 == shasums2:
        output_file.write(f"SHA256sums are identical for {input_file1} and {input_file2}\n")
        shasums.append(output_file)
    else:
        output_file.write(f"SHA256sums are not identical for {input_file1} and {input_file2}\n")
        shasums.append(output_file)
    return output_filepath

#comparetxtfiles(f"{blockdata_dir}_init_shasums.txt", f"{guiblock_dir}_init_shasums.txt")
#comparetxtfiles(f"{blockdata_dir}_init_shasums.txt", f"{batchblock_dir}_init_shasums.txt")
#comparetxtfiles(f"{blockdata_dir}_init_shasums.txt", f"{scriptblock_dir}_init_shasums.txt")

def calculate_compare(input_folder1, input_folder2):
    if not os.path.isdir(input_folder1):
        raise Exception(f"Input folder {input_folder1} does not exist")
    if not os.path.isdir(input_folder2):
        raise Exception(f"Input folder {input_folder2} does not exist")

    #results_dir = "results"  # Replace this with the actual results directory path
    os.makedirs(results_dir, exist_ok=True)
    _, output_tail = os.path.split(f"{os.path.splitext(input_folder2)[0]}_comparisons.txt")
    output_filepath = os.path.join(results_dir, output_tail)

    def get_nifti_files(folder):
        nifti_files = []
        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith('.nii'):
                    nifti_files.append(os.path.join(root, file))
        return nifti_files

    def calculate_sha256(filepath):
        with open(filepath, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    def load_nifti_data(filepath):
        return nb.load(filepath).get_fdata()

    nifti_files1 = get_nifti_files(input_folder1)
    nifti_files2 = get_nifti_files(input_folder2)

    if len(nifti_files1) != len(nifti_files2):
        raise Exception("Mismatched number of files between input directories")

    with open(output_filepath, 'w') as output_file:
        for file1, file2 in zip(nifti_files1, nifti_files2):
            data_array1 = load_nifti_data(file1)
            print(data_array1.shape)
            data_array2 = load_nifti_data(file2)
            print(data_array2.shape)
            #if data_array1.shape != data_array2.shape:
               # raise Exception("Input data must have the same shape")

            mse = np.mean((data_array1 - data_array2) ** 2)
            corr_coef = np.corrcoef(data_array1.flatten(), data_array2.flatten())[0, 1]
            sha1 = calculate_sha256(file1)
            sha2 = calculate_sha256(file2)

            output_file.write(f"File pair: {file1} and {file2}\n")
            output_file.write(f"Mean Square Error (MSE): {mse}\n")
            output_file.write(f"Correlation coefficient: {corr_coef}\n")
            output_file.write(f"SHA256 sum {'matches' if sha1 == sha2 else 'does not match'}\n\n")

    return output_filepath

#calculate_compare(blockdata_dir, guiblock_dir)
#calculate_compare(blockdata_dir, batchblock_dir)
#calculate_compare(blockdata_dir, scriptblock_dir)
#calculate_compare(eventdata_dir, eventgui_dir)
#calculate_compare(eventdata_dir, eventbatch_dir)
#calculate_compare(eventdata_dir, eventscript_dir)
