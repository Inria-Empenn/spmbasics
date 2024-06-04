
import os
import hashlib
import numpy as np
import nibabel as nb


base_dir = os.path.join(os.environ['HOME'], 'spmbasics')
data_dir = os.path.join(base_dir, 'data')
output_dir = os.path.join(data_dir, 'output')
src_dir = os.path.join(base_dir, 'src')
blockdata_dir = os.path.join(data_dir, 'MoAEpilot')
blockanat_dir = os.path.join(data_dir, 'MoAEpilot/sub-01/anat')
blockfunc_dir = os.path.join(data_dir, 'MoAEpilot/sub-01/func')
guiblockref_dir = os.path.join(output_dir, 'MoAEpilot_gui')
guiblockrefa_dir = os.path.join(output_dir, 'MoAEpilot_gui/sub-01/anat')
guiblockreff_dir = os.path.join(output_dir, 'MoAEpilot_gui/sub-01/func')
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



# calculate_shasums(blockdata_dir)
# calculate_shasums(guiblockref_dir)
# calculate_shasums(batchblock_dir)
# calculate_shasums(scriptblock_dir)
#calculate_shasums(eventdata_dir)
#calculate_shasums(eventgui_dir)
#calculate_shasums(eventbatch_dir)
#calculate_shasums(eventscript_dir)
#calculate_shasums(nipype_event_dir)



def calculate_compare(input_folder1, input_folder2):
    if not os.path.isdir(input_folder1):
        raise Exception(f"Input folder {input_folder1} does not exist")
    else :
        if not os.path.isdir(input_folder2):
         raise Exception(f"Input folder {input_folder2} does not exist")
        
    head, output_tail = os.path.split(f"{os.path.splitext(input_folder1)[0]}_comparisons.txt")    
    output_filepath = os.path.join(results_dir, output_tail)
    output_file = open(output_filepath, 'w')
    
    #with open(output_filepath, 'w') as f:
        
    mse = [] # to store mse
    corr = []
    shasums1 = []
    shasums2 = []
    shasums = []
    # data_files ={}
    file_extension = ['.nii', '.img']
    for root1, dirs, files1 in os.walk(input_folder1):
        for file1 in files1:
            if any(file1.endswith(ext) for ext in file_extension):
                file1_path = os.path.join(root1, file1)
                with open (file1_path, 'rb') as f:
                    sha1_sum = hashlib.sha256(f.read()).hexdigest()
                    shasums1.append(sha1_sum)
                data_file1 = nb.load(file1_path)
                data_array1 = data_file1.get_fdata() # making an array of image
    for root2, dirs2, files2 in os.walk(input_folder2):
        for file2 in files2:
            if any(file2.endswith(ext) for ext in file_extension):
                file2_path = os.path.join(root2, file2)
                with open (file2_path, 'rb') as f:
                    sha2_sum = hashlib.sha256(f.read()).hexdigest()
                    shasums2.append(sha2_sum)
                data_file2 = nb.load(file2_path)
                data_array2 = data_file2.get_fdata() # making an array of image            
    if data_array1.size != data_array2.size:
        raise Exception("input data must have the same size")
    error =np.sum((data_array1.astype("float") - data_array2.astype("float")) ** 2)
    error /= float(data_array1.shape[0] * data_array2.shape[1])
    mse.append(error)
    for error in mse:
        output_file.write(f"The Mean Square Error (MSE) calculation of the {file1_path} and {file2_path}, is = {error}\n")
    corr_coef = np.corrcoef(data_array1.flatten(), data_array2.flatten())[0, 1]
    corr.append(corr_coef)
    for corr_coef in corr:
        output_file.write(f"The correlation coefficient of the {file1_path} and {file2_path}, is ={corr_coef}\n")
                # data_files[file_path] = { "data_array": data_array}
    if shasums1 == shasums2:
        output_file.write(f"SHA256sums are identical for {file1_path} and {file2_path}\n")
        shasums.append(output_file)
    else:
            output_file.write(f"SHA256sums are not identical for {file1_path} and {file2_path}\n")
            shasums.append(output_file)
    # f.write('\n'.join(shasums))    
    return  output_filepath

#calculate_compare(blockdata_dir, guiblockref_dir)
#calculate_compare(blockdata_dir, batchblock_dir)
# above code works on given directory but not in subdirectories, currently subdirectories needs to be addressed explicitly which is not neat, I know...