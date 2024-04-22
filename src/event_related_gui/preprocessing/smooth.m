%-----------------------------------------------------------------------
% Job saved on 18-Apr-2024 16:01:57 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7771)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
%%
home = getenv('HOME');
root = fullfile(home, 'spmbasics', '/data/face_rep_gui')
func = spm_select('FPList', fullfile(root,'RawEPI'), '^warsM.*\.img$');


scriptdir = fullfile(home, 'spmbasics', '/src/event_related_gui/preprocessing/matfiles');

disp('Starting preprocessing...'); 

matlabbatch{1}.spm.spatial.smooth.data(1) = {cellstr(func)};
%%
matlabbatch{1}.spm.spatial.smooth.fwhm = [8 8 8];
matlabbatch{1}.spm.spatial.smooth.dtype = 0;
matlabbatch{1}.spm.spatial.smooth.im = 0;
matlabbatch{1}.spm.spatial.smooth.prefix = 's';

disp('Completed preprocessing...')
save(fullfile(scriptdir,'smooth.mat'),'matlabbatch');

spm_jobman('run',matlabbatch);