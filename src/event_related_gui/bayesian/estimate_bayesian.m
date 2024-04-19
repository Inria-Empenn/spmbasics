%-----------------------------------------------------------------------
% Job saved on 18-Apr-2024 14:50:36 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7771)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
home = getenv('HOME');
scriptdir = fullfile(home, 'spmbasics', '/src/event_related_gui/bayesian')
matfile = fullfile(scriptdir, 'SPM.mat');

matlabbatch{1}.spm.stats.fmri_est.spmmat = cellstr(matfile);
matlabbatch{1}.spm.stats.fmri_est.write_residuals = 0;
matlabbatch{1}.spm.stats.fmri_est.method.Bayesian.space.volume.block_type = 'Slices';
matlabbatch{1}.spm.stats.fmri_est.method.Bayesian.signal = 'UGL';
matlabbatch{1}.spm.stats.fmri_est.method.Bayesian.ARP = 3;
matlabbatch{1}.spm.stats.fmri_est.method.Bayesian.noise.UGL = 1;
matlabbatch{1}.spm.stats.fmri_est.method.Bayesian.LogEv = 'No';
matlabbatch{1}.spm.stats.fmri_est.method.Bayesian.anova.first = 'No';
matlabbatch{1}.spm.stats.fmri_est.method.Bayesian.anova.second = 'Yes';
matlabbatch{1}.spm.stats.fmri_est.method.Bayesian.gcon = struct('name', {}, 'convec', {});

save(fullfile(scriptdir,'parametric_est.mat'),'matlabbatch');
spm_jobman('run',matlabbatch);
