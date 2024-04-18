%-----------------------------------------------------------------------
% Job saved on 16-Apr-2024 14:20:46 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7771)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
home = getenv('HOME');
user = getenv('USER');
% path of your data file
root = fullfile(home, 'spmbasics', '/data/MoAEpilot'); % must be edited according to the name of the data folder
sub = {'sub-01'}; 
disp(['Starting preprocessing for ', sub]); % add a print statement to tell you which subject is being processed

func_dir = fullfile(root, sub, 'func'); % this combines the root with a specific subject directory to create the full path to the folder containing functional data

 % find the structural file
    %find and select the functional data
func = spm_select('ExtFPList', func_dir, '^sub-01_task-auditory_bold.nii$', NaN); % this will give the full path to the task data, NaN will ensure you are loading all volumes present (i.e. consider the 4D file as a whole)

%cd(func_dir) % move into the subject specific folder containing the functional data

matlabbatch{1}.spm.spatial.realign.estwrite.data{1} = cellstr(func);
matlabbatch{1}.spm.spatial.realign.estwrite.eoptions.quality = 0.9;
matlabbatch{1}.spm.spatial.realign.estwrite.eoptions.sep = 4;
matlabbatch{1}.spm.spatial.realign.estwrite.eoptions.fwhm = 5;
matlabbatch{1}.spm.spatial.realign.estwrite.eoptions.rtm = 1;
matlabbatch{1}.spm.spatial.realign.estwrite.eoptions.interp = 2;
matlabbatch{1}.spm.spatial.realign.estwrite.eoptions.wrap = [0 0 0];
matlabbatch{1}.spm.spatial.realign.estwrite.eoptions.weight = '';
matlabbatch{1}.spm.spatial.realign.estwrite.roptions.which = [2 1];
matlabbatch{1}.spm.spatial.realign.estwrite.roptions.interp = 4;
matlabbatch{1}.spm.spatial.realign.estwrite.roptions.wrap = [0 0 0];
matlabbatch{1}.spm.spatial.realign.estwrite.roptions.mask = 1;
matlabbatch{1}.spm.spatial.realign.estwrite.roptions.prefix = 'r';
disp(['Completed preprocessing for ', sub]) % add a print statement telling you which subject has been processed
save preprocessing_realignment matlabbatch % save the setup into a matfile called preprocessing_batch.mat
spm_jobman('run',matlabbatch) % execute the batch
