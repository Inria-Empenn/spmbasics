%-----------------------------------------------------------------------
% Job saved on 18-Apr-2024 14:52:51 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7771)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
home = getenv('HOME');
scriptdir = fullfile(home, 'spmbasics', '/data/output/event_related_gui/categorical');
matfile = fullfile(scriptdir, 'SPM.mat');
disp('Starting categorical modelling estimation');

matlabbatch{1}.spm.stats.fmri_est.spmmat = cellstr(matfile);
matlabbatch{1}.spm.stats.fmri_est.write_residuals = 0;
matlabbatch{1}.spm.stats.fmri_est.method.Classical = 1;

disp('Finished categorical modelling estimation');

% save(fullfile(scriptdir,'categorical_est.mat'),'matlabbatch');
spm_jobman('run',matlabbatch);