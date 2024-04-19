%-----------------------------------------------------------------------
% Job saved on 17-Apr-2024 17:00:41 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7771)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
home = getenv('HOME');
script_path = fullfile(home, 'spmbasics', '/src/first_level_analysis_gui');
disp(['Starting preprocessing']);
matlabbatch{1}.spm.stats.fmri_est.spmmat = cellstr(fullfile(script_path,'SPM.mat'));
matlabbatch{1}.spm.stats.fmri_est.write_residuals = 0;
matlabbatch{1}.spm.stats.fmri_est.method.Classical = 1;
disp(['Completed preprocessing']) 
spm_jobman('run',matlabbatch) 