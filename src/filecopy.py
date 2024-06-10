import os
import shutil

base_dir = os.path.join(os.environ['HOME'], 'spmbasics')
data_dir = os.path.join(base_dir, 'data')
output_dir = os.path.join(data_dir, 'output')
src_dir = os.path.join(base_dir, 'src')
blockdatanat_dir = os.path.join(data_dir, 'MoAEpilot/sub-01/anat')
nipype_block_dir = os.path.join(output_dir, 'nipype/block_preprocesss/_subject_id_01_task_name_auditory')
#nipype_block_main = os.path.join(output_dir, 'nipype/block_preprocesss')

def find_and_copy(target_dir, search_names, destination_dir):
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            for name in search_names:
                if name in file:
                    source_path = os.path.join(root, file)
                    destination_path = os.path.join(destination_dir, file)
                    shutil.copy2(source_path, destination_path)
                    print(f"File '{file}' copied to '{destination_dir}'")

# Example usage

#search_names = ["y_sub-01_T1w.nii", "msub-01_T1w.nii"]

search_names = ["sub-01_task-auditory_bold.nii"]
target_dir = nipype_block_dir
#target_dir = nipype_block_main
destination_dir = blockdatanat_dir
#destination_dir = nipype_block_dir

find_and_copy(target_dir, search_names, destination_dir)
#find_and_copy(target_dir, search_names, destination_dir)