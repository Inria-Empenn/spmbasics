%-----------------------------------------------------------------------
% Job saved on 16-Apr-2024 14:32:34 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7771)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
spmDir = fullfile(userpath, 'spm12');
spmwhere = fullfile(spmDir); 
home = getenv('HOME');
user = getenv('USER');

root = fullfile(home, 'spmbasics', '/data/MoAEpilot'); % must be edited according to the name of the data folder
sub = {'sub-01'}; 

disp(['Starting preprocessing for ', sub]); % add a print statement to tell you which subject is being processed

anat_dir = fullfile(root, sub, 'anat'); % this combines the root with a specific subject directory to create the full path to the folder containing anatomical data

 % find the structural file
anat = spm_select('FPList', anat_dir, '^sub-01_T1w.nii$'); % this will return the full path (FP) to the T1 file from the anat directory

tpm_dir = fullfile(spmDir, 'tpm'); 
% {[tpm_dir filesep 'TPM.nii,' num2str(1)]}
%p = {[ tpm_dir '/TPM.nii,1']};
matlabbatch{1}.spm.spatial.preproc.channel.vols(1) = cellstr(anat);
matlabbatch{1}.spm.spatial.preproc.channel.biasreg = 0.001;
matlabbatch{1}.spm.spatial.preproc.channel.biasfwhm = 60;
matlabbatch{1}.spm.spatial.preproc.channel.write = [0 1];
matlabbatch{1}.spm.spatial.preproc.tissue(1).tpm = {[ tpm_dir '/TPM.nii,1']} ; %nthis needs to work and needs to be tested
matlabbatch{1}.spm.spatial.preproc.tissue(1).ngaus = 1;
matlabbatch{1}.spm.spatial.preproc.tissue(1).native = [1 0];
matlabbatch{1}.spm.spatial.preproc.tissue(1).warped = [0 0];
matlabbatch{1}.spm.spatial.preproc.tissue(2).tpm = {[ tpm_dir '/TPM.nii,2']};
matlabbatch{1}.spm.spatial.preproc.tissue(2).ngaus = 1;
matlabbatch{1}.spm.spatial.preproc.tissue(2).native = [1 0];
matlabbatch{1}.spm.spatial.preproc.tissue(2).warped = [0 0];
matlabbatch{1}.spm.spatial.preproc.tissue(3).tpm = {[ tpm_dir '/TPM.nii,3']};
matlabbatch{1}.spm.spatial.preproc.tissue(3).ngaus = 2;
matlabbatch{1}.spm.spatial.preproc.tissue(3).native = [1 0];
matlabbatch{1}.spm.spatial.preproc.tissue(3).warped = [0 0];
matlabbatch{1}.spm.spatial.preproc.tissue(4).tpm ={[ tpm_dir '/TPM.nii,4']};
matlabbatch{1}.spm.spatial.preproc.tissue(4).ngaus = 3;
matlabbatch{1}.spm.spatial.preproc.tissue(4).native = [1 0];
matlabbatch{1}.spm.spatial.preproc.tissue(4).warped = [0 0];
matlabbatch{1}.spm.spatial.preproc.tissue(5).tpm = {[ tpm_dir '/TPM.nii,5']};
matlabbatch{1}.spm.spatial.preproc.tissue(5).ngaus = 4;
matlabbatch{1}.spm.spatial.preproc.tissue(5).native = [1 0];
matlabbatch{1}.spm.spatial.preproc.tissue(5).warped = [0 0];
matlabbatch{1}.spm.spatial.preproc.tissue(6).tpm = {[ tpm_dir '/TPM.nii,6']};
matlabbatch{1}.spm.spatial.preproc.tissue(6).ngaus = 2;
matlabbatch{1}.spm.spatial.preproc.tissue(6).native = [0 0];
matlabbatch{1}.spm.spatial.preproc.tissue(6).warped = [0 0];
matlabbatch{1}.spm.spatial.preproc.warp.mrf = 1;
matlabbatch{1}.spm.spatial.preproc.warp.cleanup = 1;
matlabbatch{1}.spm.spatial.preproc.warp.reg = [0 0.001 0.5 0.05 0.2];
matlabbatch{1}.spm.spatial.preproc.warp.affreg = 'mni';
matlabbatch{1}.spm.spatial.preproc.warp.fwhm = 0;
matlabbatch{1}.spm.spatial.preproc.warp.samp = 3;
matlabbatch{1}.spm.spatial.preproc.warp.write = [0 1];
matlabbatch{1}.spm.spatial.preproc.warp.vox = NaN;
matlabbatch{1}.spm.spatial.preproc.warp.bb = [NaN NaN NaN
                                              NaN NaN NaN];
                                          
disp(['Completed preprocessing for ', sub]) % add a print statement telling you which subject has been processed
save preprocessing_segmentation matlabbatch % save the setup into a matfile called preprocessing_batch.mat
spm_jobman('run',matlabbatch) % execute the batch

