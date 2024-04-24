%-----------------------------------------------------------------------
% Job saved on 18-Apr-2024 14:53:45 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7771)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
home = getenv('HOME');
root = fullfile(home, 'spmbasics', '/data/face_rep');
func = spm_select('FPList', fullfile(root,'RawEPI'), '^swarsM.*\.img$');
txt = spm_select('FPList', fullfile(root,'RawEPI'), '^rp_sM.*\.txt$'); % rp_sM03953_0005_0006.txt
scriptdir = fullfile(home, 'spmbasics', '/data/output/event_related_gui/categorical');
% onsets    = load(fullfile(root,'sots.mat'));
% condnames = {'N1' 'N2' 'F1' 'F2'};

disp('Starting categorical modelling specifications');

matlabbatch{1}.spm.stats.fmri_spec.dir = cellstr(scriptdir);
matlabbatch{1}.spm.stats.fmri_spec.timing.units = 'scans';
matlabbatch{1}.spm.stats.fmri_spec.timing.RT = 2;
matlabbatch{1}.spm.stats.fmri_spec.timing.fmri_t = 24;
matlabbatch{1}.spm.stats.fmri_spec.timing.fmri_t0 = 12;
%

matlabbatch{1}.spm.stats.fmri_spec.sess.scans = cellstr(func);
                                                 
%
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(1).name = 'N1';
%
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(1).onset = [6.74996666666667
                                                         15.7499666666667
                                                         17.9999666666667
                                                         26.9999666666667
                                                         29.2499666666667
                                                         31.4999666666667
                                                         35.9999666666667
                                                         42.7499666666667
                                                         65.2499666666667
                                                         67.4999666666667
                                                         74.2499666666667
                                                         92.2499666666667
                                                         112.499966666667
                                                         119.249966666667
                                                         123.749966666667
                                                         125.999966666667
                                                         137.249966666667
                                                         141.749966666667
                                                         143.999966666667
                                                         146.249966666667
                                                         155.249966666667
                                                         159.749966666667
                                                         161.999966666667
                                                         164.249966666667
                                                         204.749966666667
                                                         238.499966666667];
%
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(1).duration = 0;
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(1).tmod = 0;
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(1).pmod = struct('name', {}, 'param', {}, 'poly', {});
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(1).orth = 1;
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(2).name = 'N2';
%%
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(2).onset = [13.4999666666667
                                                         40.4999666666667
                                                         47.2499666666667
                                                         56.2499666666667
                                                         89.9999666666667
                                                         94.4999666666667
                                                         96.7499666666667
                                                         134.999966666667
                                                         148.499966666667
                                                         184.499966666667
                                                         191.249966666667
                                                         202.499966666667
                                                         215.999966666667
                                                         233.999966666667
                                                         236.249966666667
                                                         242.999966666667
                                                         245.249966666667
                                                         256.499966666667
                                                         260.999966666667
                                                         281.249966666667
                                                         290.249966666667
                                                         303.749966666667
                                                         310.499966666667
                                                         319.499966666667
                                                         339.749966666667
                                                         341.999966666667];
%%
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(2).duration = 0;
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(2).tmod = 0;
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(2).pmod = struct('name', {}, 'param', {}, 'poly', {});
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(2).orth = 1;
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(3).name = 'F1';
%%
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(3).onset = [-3.33333333333366e-05
                                                         2.24996666666667
                                                         8.99996666666667
                                                         11.2499666666667
                                                         22.4999666666667
                                                         44.9999666666667
                                                         51.7499666666667
                                                         60.7499666666667
                                                         62.9999666666667
                                                         76.4999666666667
                                                         78.7499666666667
                                                         85.4999666666667
                                                         98.9999666666667
                                                         101.249966666667
                                                         103.499966666667
                                                         116.999966666667
                                                         130.499966666667
                                                         150.749966666667
                                                         170.999966666667
                                                         188.999966666667
                                                         227.249966666667
                                                         265.499966666667
                                                         283.499966666667
                                                         285.749966666667
                                                         287.999966666667
                                                         344.249966666667];
%%
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(3).duration = 0;
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(3).tmod = 0;
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(3).pmod = struct('name', {}, 'param', {}, 'poly', {});
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(3).orth = 1;
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(4).name = 'F2';
%%
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(4).onset = [33.7499666666667
                                                         49.4999666666667
                                                         105.749966666667
                                                         152.999966666667
                                                         157.499966666667
                                                         168.749966666667
                                                         177.749966666667
                                                         179.999966666667
                                                         182.249966666667
                                                         197.999966666667
                                                         222.749966666667
                                                         240.749966666667
                                                         254.249966666667
                                                         267.749966666667
                                                         269.999966666667
                                                         274.499966666667
                                                         294.749966666667
                                                         299.249966666667
                                                         301.499966666667
                                                         314.999966666667
                                                         317.249966666667
                                                         326.249966666667
                                                         332.999966666667
                                                         335.249966666667
                                                         337.499966666667
                                                         346.499966666667];
%
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(4).duration = 0;
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(4).tmod = 0;
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(4).pmod = struct('name', {}, 'param', {}, 'poly', {});
matlabbatch{1}.spm.stats.fmri_spec.sess.cond(4).orth = 1;
matlabbatch{1}.spm.stats.fmri_spec.sess.multi = {''};
matlabbatch{1}.spm.stats.fmri_spec.sess.regress = struct('name', {}, 'val', {});
matlabbatch{1}.spm.stats.fmri_spec.sess.multi_reg = cellstr(txt);
matlabbatch{1}.spm.stats.fmri_spec.sess.hpf = 128;
matlabbatch{1}.spm.stats.fmri_spec.fact(1).name = 'Fam';
matlabbatch{1}.spm.stats.fmri_spec.fact(1).levels = 2;
matlabbatch{1}.spm.stats.fmri_spec.fact(2).name = 'Rep';
matlabbatch{1}.spm.stats.fmri_spec.fact(2).levels = 2;
matlabbatch{1}.spm.stats.fmri_spec.bases.hrf.derivs = [1 1];
matlabbatch{1}.spm.stats.fmri_spec.volt = 1;
matlabbatch{1}.spm.stats.fmri_spec.global = 'None';
matlabbatch{1}.spm.stats.fmri_spec.mthresh = 0.8;
matlabbatch{1}.spm.stats.fmri_spec.mask = {''};
matlabbatch{1}.spm.stats.fmri_spec.cvi = 'AR(1)';

disp('Starting categorical modelling specifications');
save(fullfile(scriptdir,'categorical_spec.mat'),'matlabbatch');

spm_jobman('run',matlabbatch);