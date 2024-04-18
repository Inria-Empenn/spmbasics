home = getenv('HOME');
script_path = fullfile(home, 'spmbasics', '/src/first_level_analysis_script');
disp(['Starting preprocessing']);
matlabbatch{1}.spm.stats.fmri_est.spmmat = cellstr(fullfile(script_path,'SPM.mat'));
matlabbatch{1}.spm.stats.fmri_est.write_residuals = 0;
matlabbatch{1}.spm.stats.fmri_est.method.Classical = 1;
disp(['Completed preprocessing']) 
spm_jobman('run',matlabbatch) 