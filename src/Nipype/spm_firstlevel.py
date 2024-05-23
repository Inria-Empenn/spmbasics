#!/usr/bin/env python
# coding: utf-8

# ## First Level Analysis



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


spm.SPMCommand.set_mlab_paths(paths=os.path.abspath(os.path.join(os.environ['HOME'], 'Documents/MATLAB/spm12/')), matlab_cmd='/soft/matlab_hd/R2020b/bin/glnxa64/MATLAB -nodesktop -nosplash')


# In[3]:


mlab.MatlabCommand.set_default_matlab_cmd("/soft/matlab_hd/R2020b/bin/glnxa64/MATLAB  -nodesktop -nosplash")
mlab.MatlabCommand.set_default_paths(os.path.abspath(os.path.join(os.environ['HOME'], 'Documents/MATLAB/spm12/')))



fsl.FSLCommand.set_default_output_type('NIFTI')




base_dir = os.path.join(os.environ['HOME'], 'spmbasics/data/')


data_dir = os.path.join(base_dir, 'MoAEpilot/task-auditory_bold.json')


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
FirstLeveldesign = Node(Level1Design(bases={'hrf': {'derivs': [0, 0]}},
                                 timing_units='scans',
                                 interscan_interval=TR,
                                 volterra_expansion_order=1,
                                 flags={'mthresh': 0.8},
                                 global_intensity_normalization='none',
                                 microtime_onset=8,
                                 microtime_resolution=16,
                                 model_serial_correlations='AR(1)'),
                    name="FirstLeveldesign")

# EstimateModel - estimate the parameters of the model
FirstLevelestimate = Node(EstimateModel(estimation_method={'Classical': 1}),
                      write_residuals=True, 
                      name="FirstLevelestimate")

# EstimateContrast - estimates contrasts
FirstLevelconest = Node(EstimateContrast(), name="FirstLevelconest")



# Condition names
condition_names = ['listening']
#onsets = [6,18, 30, 42, 54, 66, 78]
# Contrasts
#onsets = ['listening',      'T', condition_names, [6, 18, 30, 42, 54, 66, 78]
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
templates = {'func': os.path.join(output_dir, 'preproc', '_subject_id_{subject_id}_task_name_{task_id}',
                         'swarsub-{subject_id}_task-{task_id}_bold.nii'),
             'rptxt': os.path.join(output_dir, 'preproc', '_subject_id_{subject_id}_task_name_{task_id}', 
                             'rp_sub-{subject_id}_task-{task_id}_bold.txt'),
             'outliers': os.path.join(output_dir, 'preproc', '_subject_id_{subject_id}_task_name_{task_id}', 
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
FirstLevel = Workflow(name='FirstLevel')
FirstLevel.base_dir = os.path.join(experiment_dir, working_dir)

# Connect up the 1st-level analysis components
FirstLevel.connect([(infosource, selectfiles, [('subject_id', 'subject_id')]),
                    (infosource, getsubjectinfo, [('subject_id','subject_id')]),
                    (getsubjectinfo, modelspec, [('subject_info','subject_info')]),
                    (infosource, FirstLevelconest, [('contrasts', 'contrasts')]),
                    (selectfiles, modelspec, [('func', 'functional_runs')]),
                    (selectfiles, modelspec, [('rptxt', 'realignment_parameters'),
                                             ('outliers', 'outlier_files')]),
                    (modelspec, FirstLeveldesign, [('session_info','session_info')]),
                    (FirstLeveldesign, FirstLevelestimate, [('spm_mat_file','spm_mat_file')]),
                    (FirstLevelestimate, FirstLevelconest, [('spm_mat_file','spm_mat_file'),
                                                            ('beta_images','beta_images'),
                                                            ('residual_image','residual_image')]),
                    (FirstLevelestimate, datasink, [('mask_image','FirstLevel.@mask_image'),
                                                    ('beta_images','FirstLevel.@beta_images'),
                                                    ('residual_images','FirstLevel.@residual_images'),
                                                    ('residual_image','FirstLevel.@residual_image'),
                                                    ('RPVimage', 'FirstLevel.@RPVimage')
                                               ]),
                    (FirstLevelconest, datasink, [('spm_mat_file', 'FirstLevel.@spm_mat'),
                                                  ('spmT_images', 'FirstLevel.@T'),
                                                  ('con_images', 'FirstLevel.@con'),
                                                  ('ess_images', 'FirstLevel.@ess'),
                                              ]),
    
                    ])


# Create 1st-level analysis output graph
FirstLevel.write_graph(graph2use='colored', format='png', dotfilename='colored_l1analysis.dot', simple_form=True)

# Visualize the graph
from IPython.display import Image
Image(filename=os.path.join(FirstLevel.base_dir, 'FirstLevel', 'colored_l1analysis.png'))



FirstLevel.write_graph(graph2use='flat', format='png', dotfilename='flat_l1analysis.dot', simple_form=True)


FirstLevel.run('MultiProc', plugin_args={'n_procs': 4})



from nilearn.plotting import plot_stat_map
anatimg = './spmbasics/data/MoAEpilot/sub-01/anat/sub-01_T1w.nii'


plot_stat_map(
    './spmbasics/data/output/datasink/1stLevel/_subject_id_01/spmT_0001.nii', title='tstat',
    bg_img=anatimg, threshold=3, display_mode='z', cut_coords=(-5, 0, 16, 20, 25), dim=-1);

