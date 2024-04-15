#!/bin/bash
# finds the nifti files in the subject sub folders
# gets sha26sum values and sorts according to the file names
# prints only the sha256sum values to the output file.


# Function to find the base directory containing both src and data
find_basedir() {
    # to store the dir variable
    local dir="$1" 
    #to create a search loop for base directiory
    while [[ "$dir" != "/" ]]; do  
        # if there is src and data set this as the base directory
        if [[ -d "$dir/src" && -d "$dir/data" ]]; then 
            # to print the base directory
            echo "$dir"
            return
        fi
        # to set the directory to the parent directory
        dir=$(dirname "$dir")
    done
    echo "Base directory not found"
}

# Determining the base directory using the 'find_basedir' function

BASEDIR=$(find_basedir "$(pwd)")
# without this part script does not stop because it needs to exit, exit 1 does that.
if [[ "$BASEDIR" == "Base directory not found" ]]; then
    echo "Error: Base directory not found."
    exit 1
fi

# Define paths relative to the base directory
SRCDIR="$BASEDIR/src"
DATADIR="$BASEDIR/data" #where all data is stored
# Reference folder is the folder which contains all results from batch interface step by step
# All other folders will be compared with this.
REFERENCEDIR="$DATADIR/MoAEpilot" 
# Output folder of the batch interface
BATCHDIR="$DATADIR/output/MoAEpilot_bids_batch" 
# Output folder of the script interface
SCRIPTDIR="$DATADIR/output/MoAEpilot_bids_script"  

RESULTSDIR="$BASEDIR/results"

# defining file extension to search for the defined file extension 
file_extension=".nii"

#Now we are looking for the nifti files in the functional and anatomical subfolders
# calculating their shasums 
# and storing them in a file with the same name as the subfolder.

calculate_shasums() {
    local input_folder="$1"
    local output_file="${input_folder%.*}_shasums.txt" #to create the output file accordingly

    # Initialize an array to store all SHA256 sums
    shasums=()

    # Find files with the specified extension in the input folder and its subfolders
    # IFS is to set filed separator actually not used here just keeping it to have it for the future
    while IFS= read -r -d '' file; do
        # Calculate sha256sum, print only the first column and sort the output 
        sha_sum=$(sha256sum "$file" | awk '{print $1}' | sort)
        
        # This is to append the sha256 sum to the array
        shasums+=("$sha_sum")
# this one liner looks for the files containing the 'file_extension' in the folder and prints.
    done < <(find "$input_folder" -type f -name "*$file_extension" -print0)

    # Print all SHA256 sums to the output file
    printf "%s\n" "${shasums[@]}" > "$output_file"
}

compare_shasums() {
    # first director to compare
    local dir1="$1"
    # second directory to compare
    local dir2="$2"
    # output folder to store the comparison result
    local output_file="$RESULTSDIR/comparison_results.txt"

    # Get the SHA256 sums of files in the first directory
    shasums_dir1=($(find "$dir1" -type f -name "*$file_extension" -exec sha256sum {} + | awk '{print $1}' | sort))

    # Get the SHA256 sums of files in the second directory
    shasums_dir2=($(find "$dir2" -type f -name "*$file_extension" -exec sha256sum {} + | awk '{print $1}' | sort))

    # Compare the arrays of SHA256 sums if they are identical or not 
    if [ "${shasums_dir1[*]}" == "${shasums_dir2[*]}" ]; then
        echo "SHA256 sums are identical for $dir1 and $dir2" >> "$output_file"
    else
        echo "SHA256 sums are different for $dir1 and $dir2" >> "$output_file"
    fi
}
##############################################################
# Iterate over the REFERENCE folder to calculate shasums for all the nifti files'
# THIS NEEDS TO BE DONE ONCE FOR THE REFERENCE FOLDER 
# It is recommended to run it once then comment it out
# lock your reference folder and reference txt to avooid overwriting
#for ref_subfolder in "$REFERENCEDIR"; do
#    calculate_shasums "$ref_subfolder"
#done
##############################################################


# TO COMPARE THEM WITH THE REFERENCEDIR
# Iterate over BATCH folder to calculate shasums for all nifti files'
for batch_subfolder in "$BATCHDIR"; do
    calculate_shasums "$batch_subfolder"
    compare_shasums "$batch_subfolder" "$REFERENCEDIR/MoAEpilot_shasums.txt"
done

# Iterate over SCRIPT folder to calculate shasums for all nifti files'
for script_subfolder in "$SCRIPTDIR"; do
    calculate_shasums "$script_subfolder"
    compare_shasums "$script_subfolder" "$REFERENCEDIR/MoAEpilot_shasums.txt"
done

# TO COMPARE THEM WITH EACH OTHER
compare_shasums "$BATCHDIR" "$SCRIPTDIR"