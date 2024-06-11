%-----------------------------------------------------------------------
% Job saved on 16-Apr-2024 14:32:08 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7771)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
home = getenv('HOME');

% path of your data file
root = fullfile(home, 'spmbasics', '/data/output/MoAEpilot_gui'); % must be edited according to the name of the data folder
sub = {'sub-01'}; 

anat_dir = fullfile(root, sub, 'anat'); % this combines the root with a specific subject directory to create the full path to the folder containing anatomical data

func_dir = fullfile(root, sub, 'func'); % this combines the root with a specific subject directory to create the full path to the folder containing functional data

 % find the structural file
deformation = spm_select('FPList', anat_dir, '^y_sub-.*\.nii$'); % this will return the full path (FP) to the T1 file from the anat directory

    %find and select the functional data
st_realigned = spm_select('ExtFPList', func_dir, '^arsub-.*\.nii$', NaN); % this will give the full path to the task data, NaN will ensure you are loading all volumes present (i.e. consider the 4D file as a whole)

matlabbatch{1}.spm.spatial.normalise.write.subj.def(1) = cellstr(deformation);
matlabbatch{1}.spm.spatial.normalise.write.subj.resample(1) = cellstr(st_realigned);
matlabbatch{1}.spm.spatial.normalise.write.woptions.bb = [-78 -112 -70
                                                          78 76 85];
matlabbatch{1}.spm.spatial.normalise.write.woptions.vox = [3 3 3];
matlabbatch{1}.spm.spatial.normalise.write.woptions.interp = 4;
matlabbatch{1}.spm.spatial.normalise.write.woptions.prefix = 'w';

disp(['Completed preprocessing for ', sub]) % add a print statement telling you which subject has been processed
save preprocessing_normalisation matlabbatch % save the setup into a matfile called preprocessing_batch.mat
spm_jobman('run',matlabbatch) % execute the batch