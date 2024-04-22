home = getenv('HOME');
script_path = fullfile(home, 'spmbasics', '/data/output/first_level_script');
disp(['Starting estimation...']);
matlabbatch{1}.spm.stats.fmri_est.spmmat = cellstr(fullfile(script_path,'SPM.mat'));
matlabbatch{1}.spm.stats.fmri_est.write_residuals = 0;
matlabbatch{1}.spm.stats.fmri_est.method.Classical = 1;
disp(['Completed estimation.']) 
spm_jobman('run',matlabbatch) 