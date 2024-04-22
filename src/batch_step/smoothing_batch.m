%-----------------------------------------------------------------------
% Job saved on 16-Apr-2024 14:32:55 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7771)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
home = getenv('HOME');
user = getenv('USER');
% path of your data file
root = fullfile(home, 'spmbasics', '/data/MoAEpilot'); % must be edited according to the name of the data folder
sub = {'sub-01'}; 


func_dir = fullfile(root, sub, 'func'); % this combines the root with a specific subject directory to create the full path to the folder containing functional data

    %find and select the functional data
normalized = spm_select('ExtFPList', func_dir, '^warsub-.*\.nii$', NaN); % this will give the full path to the task data, NaN will ensure you are loading all volumes present (i.e. consider the 4D file as a whole)

matlabbatch{1}.spm.spatial.smooth.data = cellstr(normalized);
matlabbatch{1}.spm.spatial.smooth.fwhm = [6 6 6];
matlabbatch{1}.spm.spatial.smooth.dtype = 0;
matlabbatch{1}.spm.spatial.smooth.im = 0;
matlabbatch{1}.spm.spatial.smooth.prefix = 's';

disp(['Completed preprocessing for ', sub]) % add a print statement telling you which subject has been processed
save preprocessing_smoothing matlabbatch % save the setup into a matfile called preprocessing_batch.mat
spm_jobman('run',matlabbatch) % execute the batch