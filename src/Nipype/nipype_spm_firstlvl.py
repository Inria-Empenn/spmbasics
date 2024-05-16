#!/usr/bin/env python
# coding: utf-8

from nilearn import plotting

import os
import json
from nipype.interfaces.spm import Level1Design, EstimateModel, EstimateContrast
from nipype.algorithms.modelgen import SpecifySPMModel
from nipype.interfaces.utility import Function, IdentityInterface
from nipype.interfaces.io import SelectFiles, DataSink
from nipype import Workflow, Node
from nipype.interfaces import spm
from nipype.interfaces import fsl
from nipype.interfaces import matlab as mlab

# matlab may requre absolute paths to work properly

spm.SPMCommand.set_mlab_paths(paths=os.path.abspath('./Documents/MATLAB/spm12/'), matlab_cmd='/soft/matlab_hd/R2020b/bin/glnxa64/MATLAB -nodesktop -nosplash')


mlab.MatlabCommand.set_default_matlab_cmd("/soft/matlab_hd/R2020b/bin/glnxa64/MATLAB  -nodesktop -nosplash")
mlab.MatlabCommand.set_default_paths(os.path.abspath('./Documents/MATLAB/spm12/'))



spm.SPMCommand().version


fsl.FSLCommand.set_default_output_type('NIFTI')

base_dir = os.path.join(os.environ['HOME'], 'spmbasics/data/')

experiment_dir = os.path.join(base_dir, 'output')
output_dir = 'datasink'
working_dir = 'workingdir'

# list of subject identifiers
subject_list = ['01']
task_id = ['auditory']

# TR of functional images
with open(os.path.join(base_dir, 'MoAEpilot/task-auditory_bold.json'), 'rt') as fp:
    task_info = json.load(fp)
TR = task_info['RepetitionTime']

# Smoothing width used during preprocessing
fwhm = [6]

# SpecifyModel - Generates SPM-specific Model
modelspec = Node(SpecifySPMModel(concatenate_runs=False,
                                 input_units='scans',
                                 output_units='scans',
                                 time_repetition=TR,
                                 high_pass_filter_cutoff=128),
                 name="modelspec")

# Level1Design - Generates an SPM design matrix same as the first level tutorial
level1design = Node(Level1Design(bases={'hrf': {'derivs': [0, 0]}},
                                 timing_units='scans',
                                 interscan_interval=TR,
                                 volterra_expansion_order=1,
                                 flags={'mthresh': 0.8},
                                 global_intensity_normalization='none',
                                 microtime_onset=8,
                                 microtime_resolution=16,
                                 model_serial_correlations='AR(1)'),
                    name="level1design")

# EstimateModel - estimate the parameters of the model
level1estimate = Node(EstimateModel(estimation_method={'Classical': 1}),
                      write_residuals=False, 
                      name="level1estimate")

# EstimateContrast - estimates contrasts
level1conest = Node(EstimateContrast(), name="level1conest")


condition_names = ['listening']

cont01 = ['listening > rest','T', condition_names, [1, 0]]

contrast_list = [cont01]

def subjectinfo(subject_id):

    import pandas as pd
    import os
    from nipype.interfaces.base import Bunch
    base_dir = os.path.join(os.environ['HOME'], 'spmbasics/data/')
    trialinfo = pd.read_table(os.path.join(base_dir, 'MoAEpilot/sub-01/func/sub-01_task-auditory_events.tsv'))
    trialinfo.head()
    conditions = []
    onsets = []
    durations = []

    for group in trialinfo.groupby('trial_type'):
        conditions.append(group[0])
        onsets.append(list(group[1].onset - 10)) # subtracting 10s due to removing of 4 dummy scans
        durations.append(group[1].duration.tolist())

    subject_info = [Bunch(conditions=conditions,
                          onsets=onsets,
                          durations=durations,
                          #amplitudes=None,
                          tmod=None,
                          pmod=None,
                          #regressor_names=None,
                          #regressors=None
                         )]

    return subject_info  # this output will later be returned to infosource

# Get Subject Info - get subject specific condition information
getsubjectinfo = Node(Function(input_names=['subject_id'],
                               output_names=['subject_info'],
                               function=subjectinfo),
                      name='getsubjectinfo')




# Infosource - a function free node to iterate over the list of subject names
infosource = Node(IdentityInterface(fields=['subject_id',
                                            'contrasts'],
                                    contrasts=contrast_list),
                  name="infosource")
infosource.iterables = [('subject_id', subject_list)]

# SelectFiles - to grab the data (alternativ to DataGrabber)
templates = {'func': os.path.join(working_dir, 'block_preproc_art', '_subject_id_{subject_id}_task_name_{task_id}',
                         'sub-{subject_id}_task-{task_id}_bold.nii'),
             'rptxt': os.path.join(working_dir, 'block_preproc_art', '_subject_id_{subject_id}_task_name_{task_id}', 'realign/'
                             'rp_sub-{subject_id}_task-{task_id}_bold.txt'),
             'outliers': os.path.join(working_dir, 'block_preproc_art', '_subject_id_{subject_id}_task_name_{task_id}', 'art/',
                             'art.warsub-{subject_id}_task-{task_id}_bold_outliers.txt')}
selectfiles = Node(SelectFiles(templates,
                               base_directory=experiment_dir,
                               sort_filelist=True),
                   name="selectfiles")
selectfiles.inputs.task_id = 'auditory'

# Datasink - creates output folder for important outputs
datasink = Node(DataSink(base_directory=experiment_dir,
                         container=output_dir),
                name="datasink")




# Initiation of the 1st-level analysis workflow
l1analysis = Workflow(name='l1analysis_out')
l1analysis.base_dir = os.path.join(experiment_dir, working_dir)

# Connect up the 1st-level analysis components
l1analysis.connect([(infosource, selectfiles, [('subject_id', 'subject_id')]),
                    (infosource, getsubjectinfo, [('subject_id',
                                                   'subject_id')]),
                    (getsubjectinfo, modelspec, [('subject_info',
                                                  'subject_info')]),
                    (infosource, level1conest, [('contrasts', 'contrasts')]),
                    (selectfiles, modelspec, [('func', 'functional_runs')]),
                    (selectfiles, modelspec, [('rptxt', 'realignment_parameters'),
                                             ('outliers', 'outlier_files')]),
                    (modelspec, level1design, [('session_info',
                                                'session_info')]),
                    (level1design, level1estimate, [('spm_mat_file',
                                                     'spm_mat_file')]),
                    (level1estimate, level1conest, [('spm_mat_file',
                                                     'spm_mat_file'),
                                                    ('beta_images',
                                                     'beta_images'),
                                                    ('residual_image',
                                                  'residual_image')]),
                    (level1conest, datasink, [('spm_mat_file', '1stLevel.@spm_mat'),
                                              ('spmT_images', '1stLevel.@T'),
                                              ('con_images', '1stLevel.@con'),
                                              ('spmF_images', '1stLevel.@F'),
                                              ('ess_images', '1stLevel.@ess'),
                                              ]),
    
                    ])



# Create 1st-level analysis output graph
l1analysis.write_graph(graph2use='colored', format='png', dotfilename='colored_l1analysis.dot', simple_form=True)


l1analysis.run('MultiProc', plugin_args={'n_procs': 4})



