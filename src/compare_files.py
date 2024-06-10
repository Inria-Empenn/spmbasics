
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
batchblock_dir = os.path.join(output_dir, 'MoAEpilot_batch')
scriptblock_dir = os.path.join(output_dir, 'MoAEpilot_script')
nipype_block_dir = os.path.join(output_dir, 'nipype/block_preprocess/_subject_id_01_task_name_auditory')

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



def calculate_compare_old(input_folder1, input_folder2):
    '''
    This function calculates and compares the files if only one sub directory is present.
    '''
    if not os.path.isdir(input_folder1):
        raise Exception(f"Input folder {input_folder1} does not exist")
    else :
        if not os.path.isdir(input_folder2):
         raise Exception(f"Input folder {input_folder2} does not exist")
        
    _, output_tail = os.path.split(f"{os.path.splitext(input_folder1)[0]}_comparisons.txt")    
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
    return  output_filepath

#calculate_compare(blockdata_dir, guiblockref_dir)
#calculate_compare(blockdata_dir, batchblock_dir)
#

def calculate_compare_twolvl(input_folder1, input_folder2):
    '''
    This function checks the 2 level deeper sub directories, of the input directories for example:
    maindir->
        subdir->
              subdir->
                   file(s)
    searches for nifti files and loads them into memory. It calculates the Mean Square Error (MSE), correlation coefficients and  SHA256sums.
    After calculating all these, compares them and writes the results to a text file.

    Parameters:
    input_folder1 (str): The first input directory
    input_folder2 (str): The second input directory

    '''
    if not os.path.isdir(input_folder1):
        raise Exception(f"Input folder {input_folder1} does not exist")
    else :
        if not os.path.isdir(input_folder2):
         raise Exception(f"Input folder {input_folder2} does not exist")
        
    _, output_tail = os.path.split(f"{os.path.splitext(input_folder2)[0]}_comparisons.txt")    
    output_filepath = os.path.join(results_dir, output_tail)
    output_file = open(output_filepath, 'w')
    
    #with open(output_filepath, 'w') as f:
        
    mse = [] # to store mse
    corr= []
    mse2 = []
    corr2 = []
    shasums = []
    shasums1 = []
    shasums2 = []
    shasums3 = []
    shasums4 = []
    # data_files ={}
    file_extension = ['.nii', '.img']
    subfolders1 = [os.path.join(input_folder1, d) for d in sorted(os.listdir(input_folder1)) if os.path.isdir(os.path.join(input_folder1, d))]
    for subfolder1 in subfolders1:
        subsubfolders1 = [os.path.join(subfolder1, d) for d in sorted(os.listdir(subfolder1)) if os.path.isdir(os.path.join(subfolder1, d))]
        for root1, _, files1 in os.walk(subsubfolders1[0]):
            for file1 in files1:
                if any(file1.endswith(ext) for ext in file_extension):
                    file1_path = os.path.join(root1, file1)
                    with open (file1_path, 'rb') as f:
                        sha1_sum = hashlib.sha256(f.read()).hexdigest()
                        shasums1.append(sha1_sum)
                    data_file1 = nb.load(file1_path)
                    data_array1 = data_file1.get_fdata()
        for root2, _, files2 in os.walk(subsubfolders1[1]):
            for file2 in files2:
                if any(file2.endswith(ext) for ext in file_extension):
                    file2_path = os.path.join(root2, file2)
                    with open (file2_path, 'rb') as f:
                        sha2_sum = hashlib.sha256(f.read()).hexdigest()
                        shasums2.append(sha2_sum)
                    data_file2 = nb.load(file2_path)
                    data_array2 = data_file2.get_fdata()
    subfolders2 = [os.path.join(input_folder2, d) for d in sorted(os.listdir(input_folder2)) if os.path.isdir(os.path.join(input_folder2, d))]
    for subfolder2 in subfolders2:
        subsubfolders2 = [os.path.join(subfolder2, d) for d in sorted(os.listdir(subfolder2)) if os.path.isdir(os.path.join(subfolder2, d))]
        for root3, _, files3 in os.walk(subsubfolders2[0]):
            for file3 in files3:
                if any(file3.endswith(ext) for ext in file_extension):
                    file3_path = os.path.join(root3, file3)
                    with open (file3_path, 'rb') as f:
                        sha3_sum = hashlib.sha256(f.read()).hexdigest()
                        shasums3.append(sha3_sum)
                    data_file3 = nb.load(file3_path)
                    data_array3 = data_file3.get_fdata()
        for root4, _, files4 in os.walk(subsubfolders2[1]):
            for file4 in files4:
                if any(file4.endswith(ext) for ext in file_extension):
                    file4_path = os.path.join(root4, file4)
                    with open (file4_path, 'rb') as f:
                        sha4_sum = hashlib.sha256(f.read()).hexdigest()
                        shasums4.append(sha4_sum)
                    data_file4 = nb.load(file4_path)
                    data_array4 = data_file4.get_fdata()
    if data_array1.size != data_array3.size:
        raise Exception("input data must have the same size")
    error =np.sum((data_array1.astype("float") - data_array3.astype("float")) ** 2)
    error /= float(data_array1.shape[0] * data_array3.shape[1])
    mse.append(error)
    for error in mse:
        output_file.write(f"The Mean Square Error (MSE) calculation of the {file1_path} and {file3_path}, is = {error}\n")
    corr_coef = np.corrcoef(data_array1.flatten(), data_array3.flatten())[0, 1]
    corr.append(corr_coef)
    for corr_coef in corr:
        output_file.write(f"The correlation coefficient of the {file1_path} and {file3_path}, is ={corr_coef}\n")
    if shasums1 == shasums3: 
        output_file.write(f"SHA256sums are identical for {file1_path} and {file3_path}\n")
        shasums.append(output_file)
    else:
        output_file.write(f"SHA256sums are not identical for {file1_path} and {file3_path}\n")
        shasums.append(output_file)
    if data_array2.size != data_array4.size:
        raise Exception("input data must have the same size")
    error2 =np.sum((data_array2.astype("float") - data_array4.astype("float")) ** 2)
    error2 /= float(data_array2.shape[0] * data_array4.shape[1])    
    mse2.append(error2)
    for error2 in mse2:
        output_file.write(f"The Mean Square Error (MSE) calculation of the {file2_path} and {file4_path}, is = {error2}\n")
    corr_coef2 = np.corrcoef(data_array2.flatten(), data_array4.flatten())[0, 1]
    corr2.append(corr_coef2)
    for corr_coef2 in corr:
        output_file.write(f"The correlation coefficient of the {file2_path} and {file4_path}, is ={corr_coef2}\n")
    if shasums2 == shasums4:        
        output_file.write(f"SHA256sums are identical for {file2_path} and {file4_path}\n")
        shasums.append(output_file)
    else:
        output_file.write(f"SHA256sums are not identical for {file2_path} and {file4_path}\n")
        shasums.append(output_file)    
    return  output_filepath  
#calculate_compare_twolvl(blockdata_dir, guiblockref_dir)
#calculate_compare_twolvl(blockdata_dir, batchblock_dir)
#calculate_compare_twolvl(blockdata_dir, scriptblock_dir)
#calculate_compare_twolvl(blockdata_dir, nipype_block_dir)

def calculate_compare(input_folder1, input_folder2):
    '''
    This function checks the 1 level deeper sub directories, of the input directories for example:
    maindir->
        subdir->
                file(s)
    searches for nifti files and loads them into memory. It calculates the Mean Square Error (MSE), correlation coefficients and  SHA256sums.
    After calculating all these, compares them and writes the results to a text file.

    Parameters:
    input_folder1 (str): The first input directory
    input_folder2 (str): The second input directory

    '''
    if not os.path.isdir(input_folder1):
        raise Exception(f"Input folder {input_folder1} does not exist")
    else :
        if not os.path.isdir(input_folder2):
         raise Exception(f"Input folder {input_folder2} does not exist")
        
    _, output_tail = os.path.split(f"{os.path.splitext(input_folder2)[0]}_comparisons.txt")    
    output_filepath = os.path.join(results_dir, output_tail)
    output_file = open(output_filepath, 'w')
    
    #with open(output_filepath, 'w') as f:
        
    mse = [] # to store mse
    corr= []
    mse2 = []
    corr2 = []
    shasums = []
    shasums1 = []
    shasums2 = []
    shasums3 = []
    shasums4 = []
    # data_files ={}
    file_extension = ['.nii', '.img']
    subfolders1 = [os.path.join(input_folder1, d) for d in sorted(os.listdir(input_folder1)) if os.path.isdir(os.path.join(input_folder1, d))]
    for root1, _, files1 in os.walk(subfolders1[0]):
        for file1 in files1:
            if any(file1.endswith(ext) for ext in file_extension):
                file1_path = os.path.join(root1, file1)
                with open (file1_path, 'rb') as f:
                    sha1_sum = hashlib.sha256(f.read()).hexdigest()
                    shasums1.append(sha1_sum)
                data_file1 = nb.load(file1_path)
                data_array1 = data_file1.get_fdata()
    for root2, _, files2 in os.walk(subfolders1[1]):
        for file2 in files2:
            if any(file2.endswith(ext) for ext in file_extension):
                file2_path = os.path.join(root2, file2)
                with open (file2_path, 'rb') as f:
                    sha2_sum = hashlib.sha256(f.read()).hexdigest()
                    shasums2.append(sha2_sum)
                data_file2 = nb.load(file2_path)
                data_array2 = data_file2.get_fdata()
    subfolders2 = [os.path.join(input_folder2, d) for d in sorted(os.listdir(input_folder2)) if os.path.isdir(os.path.join(input_folder2, d))]
    for root3, _, files3 in os.walk(subfolders2[0]):
        for file3 in files3:
            if any(file3.endswith(ext) for ext in file_extension):
                file3_path = os.path.join(root3, file3)
                with open (file3_path, 'rb') as f:
                    sha3_sum = hashlib.sha256(f.read()).hexdigest()
                    shasums3.append(sha3_sum)
                data_file3 = nb.load(file3_path)
                data_array3 = data_file3.get_fdata()
    for root4, _, files4 in os.walk(subfolders2[1]):
        for file4 in files4:
            if any(file4.endswith(ext) for ext in file_extension):
                file4_path = os.path.join(root4, file4)
                with open (file4_path, 'rb') as f:
                    sha4_sum = hashlib.sha256(f.read()).hexdigest()
                    shasums4.append(sha4_sum)
                data_file4 = nb.load(file4_path)
                data_array4 = data_file4.get_fdata()
    if data_array1.size != data_array3.size:
        raise Exception("input data must have the same size")
    error =np.sum((data_array1.astype("float") - data_array3.astype("float")) ** 2)
    error /= float(data_array1.shape[0] * data_array3.shape[1])
    mse.append(error)
    for error in mse:
        output_file.write(f"The Mean Square Error (MSE) calculation of the {file1_path} and {file3_path}, is = {error}\n")
    corr_coef = np.corrcoef(data_array1.flatten(), data_array3.flatten())[0, 1]
    corr.append(corr_coef)
    for corr_coef in corr:
        output_file.write(f"The correlation coefficient of the {file1_path} and {file3_path}, is ={corr_coef}\n")
    if shasums1 == shasums3: 
        output_file.write(f"SHA256sums are identical for {file1_path} and {file3_path}\n")
        shasums.append(output_file)
    else:
        output_file.write(f"SHA256sums are not identical for {file1_path} and {file3_path}\n")
        shasums.append(output_file)
    if data_array2.size != data_array4.size:
        raise Exception("input data must have the same size")
    error2 =np.sum((data_array2.astype("float") - data_array4.astype("float")) ** 2)
    error2 /= float(data_array2.shape[0] * data_array4.shape[1])    
    mse2.append(error2)
    for error2 in mse2:
        output_file.write(f"The Mean Square Error (MSE) calculation of the {file2_path} and {file4_path}, is = {error2}\n")
    corr_coef2 = np.corrcoef(data_array2.flatten(), data_array4.flatten())[0, 1]
    corr2.append(corr_coef2)
    for corr_coef2 in corr:
        output_file.write(f"The correlation coefficient of the {file2_path} and {file4_path}, is ={corr_coef2}\n")
    if shasums2 == shasums4:        
        output_file.write(f"SHA256sums are identical for {file2_path} and {file4_path}\n")
        shasums.append(output_file)
    else:
        output_file.write(f"SHA256sums are not identical for {file2_path} and {file4_path}\n")
        shasums.append(output_file)    
    return  output_filepath 

#calculate_compare(eventdata_dir, eventgui_dir)
#calculate_compare(eventdata_dir, eventbatch_dir)
#calculate_compare(eventdata_dir, eventscript_dir)
#calculate_compare(eventdata_dir, nipype_event_dir)    