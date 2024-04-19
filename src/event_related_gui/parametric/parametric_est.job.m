%-----------------------------------------------------------------------
% Job saved on 18-Apr-2024 14:55:21 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7771)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
home = getenv('HOME');
scriptdir = fullfile(home, 'spmbasics', '/src/event_related_gui/parametric')
matfile = fullfile(scriptdir, 'SPM.mat');

matlabbatch{1}.spm.stats.fmri_est.spmmat = cellstr(matfile);
matlabbatch{1}.spm.stats.fmri_est.write_residuals = 0;
matlabbatch{1}.spm.stats.fmri_est.method.Classical = 1;
save(fullfile(scriptdir,'parametric_est.mat'),'matlabbatch');
spm_jobman('run',matlabbatch);
