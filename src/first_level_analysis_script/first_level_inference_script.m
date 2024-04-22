%-----------------------------------------------------------------------
% Job saved on 18-Apr-2024 14:58:54 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7771)
% cfg_basicio BasicIO - Unknown
%----------------------------------------------------------------------

spmDir = fullfile(userpath, 'spm12');

spm('Defaults','fMRI');

%spm_jobman('initcfg');

home = getenv('HOME');

sub = {'sub-01'};
script_path = fullfile(home, 'spmbasics', '/data/output/first_level_analysis_script');

disp(['Starting first level inference...', sub]);


matlabbatch{1}.spm.stats.con.spmmat = cellstr(fullfile(script_path,'SPM.mat'));
matlabbatch{1}.spm.stats.con.consess{1}.tcon.name = 'listening > rest';
matlabbatch{1}.spm.stats.con.consess{1}.tcon.weights = [1 0];


% Inference Results
%--------------------------------------------------------------------------
matlabbatch{2}.spm.stats.results.spmmat = cellstr(fullfile(script_path,'SPM.mat'));
matlabbatch{2}.spm.stats.results.conspec.contrasts = 1; % this is to load the contrast 
% in gui we define contrast and select it it automatically starts by asking
% mask
matlabbatch{2}.spm.stats.results.conspec.mask.none = 1;
matlabbatch{2}.spm.stats.results.conspec.threshdesc = 'FWE';
matlabbatch{2}.spm.stats.results.conspec.thresh = 0.05;
matlabbatch{2}.spm.stats.results.conspec.extent = 0;
matlabbatch{2}.spm.stats.results.print = false;


% Rendering
%--------------------------------------------------------------------------
% To plot the rendered brain figure

matlabbatch{3}.spm.util.render.display.rendfile = {fullfile(spmDir,'canonical','cortex_20484.surf.gii')};
matlabbatch{3}.spm.util.render.display.conspec.spmmat = cellstr(fullfile(script_path,'SPM.mat'));
matlabbatch{3}.spm.util.render.display.conspec.contrasts = 1;
matlabbatch{3}.spm.util.render.display.conspec.threshdesc = 'FWE';
matlabbatch{3}.spm.util.render.display.conspec.thresh = 0.05;
matlabbatch{3}.spm.util.render.display.conspec.extent = 0;


disp(['Completed first level inference...', sub]) 

spm_jobman('run',matlabbatch)