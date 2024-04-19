%-----------------------------------------------------------------------
% Job saved on 18-Apr-2024 14:55:57 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7771)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
home = getenv('HOME');
root = fullfile(home, 'spmbasics', '/data/face_rep_gui')

mean= spm_select('FPList', fullfile(root,'Structural'), '^meansM.*\.img$'); % y_sM03953_0007.nii
anat = spm_select('FPList', fullfile(root,'Structural'), '^sM.*\.img$'); %sM03953_0007.img

matlabbatch{1}.spm.spatial.coreg.estimate.ref(1) = {cellstr(mean)};
matlabbatch{1}.spm.spatial.coreg.estimate.source(1) = {cellstr(anat)};
matlabbatch{1}.spm.spatial.coreg.estimate.other = {''};
matlabbatch{1}.spm.spatial.coreg.estimate.eoptions.cost_fun = 'nmi';
matlabbatch{1}.spm.spatial.coreg.estimate.eoptions.sep = [4 2];
matlabbatch{1}.spm.spatial.coreg.estimate.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
matlabbatch{1}.spm.spatial.coreg.estimate.eoptions.fwhm = [7 7];
save(fullfile(scriptdir,'coreg.job.mat'),'matlabbatch');
spm_jobman('run',matlabbatch);