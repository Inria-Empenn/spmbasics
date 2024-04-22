%-----------------------------------------------------------------------
% Job saved on 18-Apr-2024 14:58:54 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7771)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
home = getenv('HOME');

% path of your data file

script_path = fullfile(home, 'spmbasics', '/data/output/first_level_script');

disp(['Starting inference...']);
matlabbatch{1}.spm.stats.con.spmmat = cellstr(fullfile(script_path,'SPM.mat'));
matlabbatch{1}.spm.stats.con.consess{1}.tcon.name = 'Listening > Rest';
matlabbatch{1}.spm.stats.con.consess{1}.tcon.weights = [1 0];
% matlabbatch{1}.spm.stats.con.consess{2}.tcon.name = 'Rest > Listening';
% matlabbatch{1}.spm.stats.con.consess{2}.tcon.weights = [-1 0];

% Inference Results
%--------------------------------------------------------------------------
matlabbatch{2}.spm.stats.results.spmmat = cellstr(fullfile(script_path,'SPM.mat'));
matlabbatch{2}.spm.stats.results.conspec.contrasts = 1;
matlabbatch{2}.spm.stats.results.conspec.threshdesc = 'FWE';
matlabbatch{2}.spm.stats.results.conspec.thresh = 0.05;
matlabbatch{2}.spm.stats.results.conspec.extent = 0;
matlabbatch{2}.spm.stats.results.print = true;
% Inference should be edited accordingly with the GUI, including overlays
% Rendering
%--------------------------------------------------------------------------
matlabbatch{3}.spm.util.render.display.rendfile = {fullfile(spm('Dir'),'canonical','cortex_20484.surf.gii')};
matlabbatch{3}.spm.util.render.display.conspec.spmmat = cellstr(fullfile(script_path,'SPM.mat'));
% matlabbatch{3}.spm.util.render.display.conspec.contrasts = 1;
$ matlabbatch{3}.spm.util.render.display.conspec.threshdesc = 'FWE';
% matlabbatch{3}.spm.util.render.display.conspec.thresh = 0.05;
% matlabbatch{3}.spm.util.render.display.conspec.extent = 0;

disp(['Completed inference']);

spm_jobman('run',matlabbatch)