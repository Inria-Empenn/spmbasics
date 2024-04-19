%-----------------------------------------------------------------------
% Job saved on 16-Apr-2024 14:31:55 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7771)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
home = getenv('HOME');
user = getenv('USER');
% path of your data file
root = fullfile(home, 'spmbasics', '/data/MoAEpilot'); % must be edited according to the name of the data folder
sub = {'sub-01'}; 

disp(['Starting preprocessing for ', sub]); % add a print statement to tell you which subject is being processed

anat_dir = fullfile(root, sub, 'anat'); % this combines the root with a specific subject directory to create the full path to the folder containing anatomical data

func_dir = fullfile(root, sub, 'func'); % this combines the root with a specific subject directory to create the full path to the folder containing functional data

 % find the structural file
anat = spm_select('FPList', anat_dir, '^sub-01_T1w.nii$'); % this will return the full path (FP) to the T1 file from the anat directory

    %find and select the functional data
mean = spm_select('ExtFPList', func_dir, '^meansub-.*\.nii$', NaN); % this will give the full path to the task data, NaN will ensure you are loading all volumes present (i.e. consider the 4D file as a whole)


matlabbatch{1}.spm.spatial.coreg.estimate.ref(1) = cellstr(mean);
matlabbatch{1}.spm.spatial.coreg.estimate.source = cellstr(anat);
matlabbatch{1}.spm.spatial.coreg.estimate.other = {''};
matlabbatch{1}.spm.spatial.coreg.estimate.eoptions.cost_fun = 'nmi';
matlabbatch{1}.spm.spatial.coreg.estimate.eoptions.sep = [4 2];
matlabbatch{1}.spm.spatial.coreg.estimate.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
matlabbatch{1}.spm.spatial.coreg.estimate.eoptions.fwhm = [7 7];

disp(['Completed preprocessing for ', sub]) % add a print statement telling you which subject has been processed
save preprocessing_coregistration matlabbatch % save the setup into a matfile called preprocessing_batch.mat
spm_jobman('run',matlabbatch) % execute the batch