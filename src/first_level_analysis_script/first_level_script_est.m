%-----------------------------------------------------------------------
% Job saved on 22-Apr-2024 10:58:57 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7771)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
home = getenv('HOME');

script_path = fullfile(home, 'spmbasics', '/data/output/first_level_analysis_script');
sub = {'sub-01'}; 
disp(['Starting first level estimation...', sub]);

matlabbatch{1}.spm.stats.fmri_est.spmmat = cellstr(fullfile(script_path,'SPM.mat'));
matlabbatch{1}.spm.stats.fmri_est.write_residuals = 0;
matlabbatch{1}.spm.stats.fmri_est.method.Classical = 1;

disp(['Completed first level estimation...', sub]) 

spm_jobman('run',matlabbatch) 