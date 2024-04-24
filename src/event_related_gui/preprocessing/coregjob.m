%-----------------------------------------------------------------------
% Job saved on 22-Apr-2024 17:26:56 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7771)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------

home = getenv('HOME');
root = fullfile(home, 'spmbasics', '/data/face_rep');
func = spm_select('ExtFPList', fullfile(root,'RawEPI'), '^sM.*\.img$');
mean = spm_select('FPList', fullfile(root,'RawEPI'), '^meansM.*\.img$');

anat = spm_select('FPList', fullfile(root,'Structural'), '^sM.*\.img$'); % y_sM03953_0007.nii

scriptdir = fullfile(home, 'spmbasics', '/src/event_related_gui/preprocessing/matfiles');
disp('Starting preprocessing...'); 

matlabbatch{1}.spm.spatial.coreg.estimate.ref(1) = cellstr(mean);
matlabbatch{1}.spm.spatial.coreg.estimate.source(1) = cellstr(anat);
matlabbatch{1}.spm.spatial.coreg.estimate.other = {''};
matlabbatch{1}.spm.spatial.coreg.estimate.eoptions.cost_fun = 'nmi';
matlabbatch{1}.spm.spatial.coreg.estimate.eoptions.sep = [4 2];
matlabbatch{1}.spm.spatial.coreg.estimate.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
matlabbatch{1}.spm.spatial.coreg.estimate.eoptions.fwhm = [7 7];

disp('Completed preprocessing...')
save(fullfile(scriptdir,'coreg.job.mat'),'matlabbatch');
spm_jobman('run',matlabbatch);