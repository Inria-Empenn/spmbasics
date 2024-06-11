%-----------------------------------------------------------------------
% Job saved on 16-Apr-2024 14:20:28 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7771)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
home = getenv('HOME');
user = getenv('USER');
% path of your data file
root = fullfile(home, 'spmbasics', '/data/output/MoAEpilot_gui'); % must be edited according to the name of the data folder
sub = {'sub-01'}; 
disp(['Starting preprocessing for ', sub]); % add a print statement to tell you which subject is being processed

realigned_dir = fullfile(root, sub, 'func'); % this combines the root with a specific subject directory to create the full path to the folder containing functional data

 % find the structural file
    %find and select the functional data
realigned = spm_select('ExtFPList', realigned_dir, '^rsub-.*\.nii$', NaN); % this will give the full path to the task data, NaN will ensure you are loading all volumes present (i.e. consider the 4D file as a whole)

%cd(func_dir) % move into the subject specific folder containing the functional data

matlabbatch{1}.spm.temporal.st.scans{1}(1) = cellstr(realigned);
matlabbatch{1}.spm.temporal.st.nslices = 64;
matlabbatch{1}.spm.temporal.st.tr = 7;
matlabbatch{1}.spm.temporal.st.ta = 6.8906;
matlabbatch{1}.spm.temporal.st.so = [64 63 62 61 60 59 58 57 56 55 54 53 52 51 50 49 48 47 46 45 44 43 42 41 40 39 38 37 36 35 34 33 32 31 30 29 28 27 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1];
matlabbatch{1}.spm.temporal.st.refslice = 32;
matlabbatch{1}.spm.temporal.st.prefix = 'a';

disp(['Completed preprocessing for ', sub]) % add a print statement telling you which subject has been processed
save preprocessing_slice_timing matlabbatch % save the setup into a matfile called preprocessing_batch.mat
spm_jobman('run',matlabbatch) % execute the batch

