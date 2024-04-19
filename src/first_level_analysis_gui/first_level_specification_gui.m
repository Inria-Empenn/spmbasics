%-----------------------------------------------------------------------
% Job saved on 17-Apr-2024 17:01:04 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7771)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
home = getenv('HOME');
root = fullfile(home, 'spmbasics', '/data/MoAEpilot'); % must be edited according to the name of the data folder
script_path = fullfile(home, 'spmbasics', '/src/first_level_analysis_gui');
sub = {'sub-01'}; 
disp(['Starting preprocessing for ', sub]);

anat_dir = fullfile(root, sub, 'anat'); % this combines the root with a specific subject directory to create the full path to the folder containing anatomical data

func_dir = fullfile(root, sub, 'func'); % this combines the root with a specific subject directory to create the full path to the folder containing functional data

 % find the structural file
anat = spm_select('FPList', anat_dir, '^sub-01_T1w.nii$'); % this will return the full path (FP) to the T1 file from the anat directory

    %find and select the functional data
func = spm_select('ExtFPList', func_dir, '^swarsub-01_task-auditory_bold.nii$', NaN);

matlabbatch{1}.spm.stats.fmri_spec.dir = cellstr(script_path);
matlabbatch{1}.spm.stats.fmri_spec.timing.units = 'scans';
matlabbatch{1}.spm.stats.fmri_spec.timing.RT = 7;
matlabbatch{1}.spm.stats.fmri_spec.timing.fmri_t = 16;
matlabbatch{1}.spm.stats.fmri_spec.timing.fmri_t0 = 8;
matlabbatch{1}.spm.stats.fmri_spec.sess.scans = cellstr(func);
matlabbatch{1}.spm.stats.fmri_spec.sess.cond.name = 'listening';
matlabbatch{1}.spm.stats.fmri_spec.sess.cond.onset = [6
                                                      18
                                                      30
                                                      42
                                                      54
                                                      66
                                                      78];
matlabbatch{1}.spm.stats.fmri_spec.sess.cond.duration = 6;
matlabbatch{1}.spm.stats.fmri_spec.sess.cond.tmod = 0;
matlabbatch{1}.spm.stats.fmri_spec.sess.cond.pmod = struct('name', {}, 'param', {}, 'poly', {});
matlabbatch{1}.spm.stats.fmri_spec.sess.cond.orth = 1;
matlabbatch{1}.spm.stats.fmri_spec.sess.multi = {''};
matlabbatch{1}.spm.stats.fmri_spec.sess.regress = struct('name', {}, 'val', {});
matlabbatch{1}.spm.stats.fmri_spec.sess.multi_reg = {''};
matlabbatch{1}.spm.stats.fmri_spec.sess.hpf = 128;
matlabbatch{1}.spm.stats.fmri_spec.fact = struct('name', {}, 'levels', {});
matlabbatch{1}.spm.stats.fmri_spec.bases.hrf.derivs = [0 0];
matlabbatch{1}.spm.stats.fmri_spec.volt = 1;
matlabbatch{1}.spm.stats.fmri_spec.global = 'None';
matlabbatch{1}.spm.stats.fmri_spec.mthresh = 0.8;
matlabbatch{1}.spm.stats.fmri_spec.mask = {''};
matlabbatch{1}.spm.stats.fmri_spec.cvi = 'AR(1)';

disp(['Completed preprocessing for ', sub]) % add a print statement telling you which subject has been processed

spm_jobman('run',matlabbatch) 
