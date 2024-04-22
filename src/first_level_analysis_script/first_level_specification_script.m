home = getenv('HOME');
root = fullfile(home, 'spmbasics', '/data/output/MoAEpilot_batch/'); % must be edited according to the name of the data folder
sub = {'sub-01'}; 
disp(['Starting specifications of first level analysis for ', sub]);

anat_dir = fullfile(root, sub, 'anat'); % this combines the root with a specific subject directory to create the full path to the folder containing anatomical data

func_dir = fullfile(root, sub, 'func');
%anat = spm_select('FPList', anat_dir, '^sub-01_T1w.nii$'); % this will return the full path (FP) to the T1 file from the anat directory
pwd
    %find and select the functional data
func = spm_select('ExtFPList', func_dir, '^swarsub-.*\.nii$', NaN);
script_path = fullfile(home, 'spmbasics', '/data/output/first_level_script');

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

disp(['Completed making SPM mat for ', sub]) 

spm_jobman('run',matlabbatch) 
