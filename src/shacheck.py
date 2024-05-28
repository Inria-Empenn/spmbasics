
import os
import hashlib
import numpy as np
import nibabel as nb

base_dir = os.path.join(os.environ['HOME'], 'spmbasics')
data_dir = os.path.join(base_dir, 'data')
output_dir = os.path.join(data_dir, 'output')
src_dir = os.path.join(base_dir, 'src')
blockdata_dir = os.path.join(data_dir, 'MoAEpilot')
guiblockref_dir = os.path.join(output_dir, 'MoAEpilot_gui')
batchblock_dir = os.path.join(output_dir, 'MoAEpilot_batch')
scriptblock_dir = os.path.join(output_dir, 'MoAEpilot_script')

eventdata_dir = os.path.join(data_dir, 'face_rep') 
eventgui_dir = os.path.join(output_dir, 'face_rep_gui')
eventbatch_dir = os.path.join(output_dir, 'face_rep_batch')
eventscript_dir = os.path.join(output_dir, 'face_rep_script')

nipype_event_dir = os.path.join(output_dir, 'nipype/event_preproc/_subject_id_M03953')
results_dir = os.path.join(base_dir, 'results')

file_extension = ['.nii', '.img']

def calculate_shasums(input_folder):
    #init_output_filename = f"{os.path.splitext(input_folder)[0]}_init_shasums.txt" 
    # to get the initial values of the shasums
    output_filename = f"{os.path.splitext(input_folder)[0]}_shasums.txt"
    #init_output_file = open(init_output_filename, 'w')
    output_file = open(output_filename, 'w')
    shasums = [] # to store the shasums
    with open(input_folder, 'rb') as f:
                    sha_sum = hashlib.sha256(f.read()).hexdigest()
                    shasums.append(sha_sum)

     # Write the checksums to the file
    for sha_sum in shasums:
        #init_output_file.write(f"{sha_sum}\n")
        output_file.write(f"{sha_sum}\n")

    output_file.close()
    #init_output_file.close()
    return output_filename

def mse(dataA, dataB):
    if dataA.size != dataB.size:
        raise Exception("input data must have the same size")
    arrayA = np.array(dataA)
    arrayB = np.array(dataB)
    error =np.sum((arrayA.astype("float") - arrayB.astype("float")) ** 2)
    error /= float(arrayA.shape[0] * arrayA.shape[1])
    return error

def correlation(dataA, dataB):
    if dataA.size != dataB.size:
        raise Exception("input data must have the same size")
    arrayA = np.array(dataA)
    arrayB = np.array(dataB)
    corr_coef = np.corrcoef(arrayA.flatten(), arrayB.flatten())[0, 1]
    return corr_coef

def mse_corr_output(dataA, dataB):
    output_filename = f"{os.path.splitext(dataA)[0]}_comparison.txt"
    with open(output_filename, 'w') as f:
        mse_value = mse(dataA, dataB)
        corr_value = correlation(dataA, dataB)
        f.write(f"Mean Squared Error is {mse_value}\n")
        f.write(f"Correlation Coefficient is {corr_value}\n")

def load_data(input_folder):
    if not os.path.isdir(input_folder):
        raise Exception(f"Input folder {input_folder} does not exist")

    data_files ={}
    file_extension = ['.nii', '.img']
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if any(file.endswith(ext) for ext in file_extension):
                file_path = os.path.join(root, file)
                data_file = nb.load(file_path)
                data_array = data_file.get_fdata() # making an array of image
                data_files[file_path] = { "data_array": data_array}
                return data_files

# calculate_shasums(blockdata_dir)
# calculate_shasums(guiblockref_dir)
# calculate_shasums(batchblock_dir)
# calculate_shasums(scriptblock_dir)
calculate_shasums(eventdata_dir)
calculate_shasums(eventgui_dir)
calculate_shasums(eventbatch_dir)
calculate_shasums(eventscript_dir)
calculate_shasums(nipype_event_dir)


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

#reference_file= os.path.join(output_dir, "MoAEpilot_shasums.txt")
#nipype_file = os.path.join(output_dir, "nipype_shasums.txt")
#compare_shasums(nipype_file, reference_file) 

# compare shasums and all measures.



