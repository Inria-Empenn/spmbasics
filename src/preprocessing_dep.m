% List of open inputs
% Processing a single-subject fMRI dataset, auditory task.
%  Edited on 10-Apr-2024 03:30:37 by mel 
% Prerequisites:
% - Matlab R2020b (on Fedora 39 readily compiled)
% - SPM12 neuroimage processing toolbox: https://www.fil.ion.ucl.ac.uk/spm/software/spm12/
% - Single subject fMRI data: https://www.fil.ion.ucl.ac.uk/spm/data/auditory/

nrun = 1; % enter the number of runs here
jobfile = {'/home/matay/spm_batches/preprocessing_dep_job.m'};
jobs = repmat(jobfile, 1, nrun);
inputs = cell(0, nrun);
for crun = 1:nrun
end
spm('defaults', 'FMRI');
spm_jobman('run', jobs, inputs{:});
