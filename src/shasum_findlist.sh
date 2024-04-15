#!/bin/bash
# finds the nifti file according to extension sorts alphabetically and prints shasums

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
DATADIR="$BASEDIR/data/MoAEpilot_bids_batch_step/sub-01" #where data is stored
FUNCDIR="$DATADIR/func" #functional subfolder
ANATDIR="$DATADIR/anat" #anatomical subfolder

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

# Iterate over functional fmris'
for func_subfolder in "$FUNCDIR"; do
    calculate_shasums "$func_subfolder"
done

# Iterate over anatomical data
for anat_subfolder in "$ANATDIR"; do
    calculate_shasums "$anat_subfolder"
done