%-----------------------------------------------------------------------
% Job saved on 18-Apr-2024 14:57:27 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7771)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
%%

home = getenv('HOME');
root = fullfile(home, 'spmbasics', '/data/face_rep')
func = spm_select('FPList', fullfile(root,'RawEPI'), '^rsM.*\.img$');
scriptdir = fullfile(home, 'spmbasics', '/src/event_related_gui/preprocessing/matfiles');

disp('Starting preprocessing...'); 

matlabbatch{1}.spm.temporal.st.scans(1) = {cellstr(func)};
%%
matlabbatch{1}.spm.temporal.st.nslices = 24;
matlabbatch{1}.spm.temporal.st.tr = 2;
matlabbatch{1}.spm.temporal.st.ta = 1.92;
matlabbatch{1}.spm.temporal.st.so = [24 23 22 21 20 19 18 17 16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1];
matlabbatch{1}.spm.temporal.st.refslice = 12;
matlabbatch{1}.spm.temporal.st.prefix = 'a';

disp('Completed preprocessing...')

save(fullfile(scriptdir,'slice_timing.mat'),'matlabbatch');
spm_jobman('run',matlabbatch);
