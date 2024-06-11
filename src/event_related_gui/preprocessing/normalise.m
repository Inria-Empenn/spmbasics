%-----------------------------------------------------------------------
% Job saved on 18-Apr-2024 14:56:24 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7771)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
%
home = getenv('HOME');
root = fullfile(home, 'spmbasics', '/data/output/face_rep_gui');
func = spm_select('FPList', fullfile(root,'RawEPI'), '^sM.*\.img$');
anat = spm_select('FPList', fullfile(root,'Structural'), '^sM.*\.img$');

matlabbatch{1}.spm.spatial.normalise.write.subj.def = cellstr(spm_file(anat,'prefix','y_','ext','nii'));

matlabbatch{1}.spm.spatial.normalise.write.subj.resample = cellstr(spm_file(func,'prefix','ar'));
matlabbatch{1}.spm.spatial.normalise.write.woptions.bb = [-78 -112 -70
                                                          78 76 85];
matlabbatch{1}.spm.spatial.normalise.write.woptions.vox = [3 3 3];
matlabbatch{1}.spm.spatial.normalise.write.woptions.interp = 4;
matlabbatch{1}.spm.spatial.normalise.write.woptions.prefix = 'w';

save(fullfile(scriptdir,'normalise.mat'),'matlabbatch');
spm_jobman('run',matlabbatch);