#!/usr/bin/env python
# coding: utf-8

# ## Parametric Modelling


from nilearn import plotting
import os
import json
from nipype.interfaces import fsl 
from nipype.interfaces import spm
from nipype.interfaces.spm import (Realign, SliceTiming, Coregister,  NewSegment,  Normalize12, Smooth)
from nipype.interfaces.spm import Level1Design, EstimateModel, EstimateContrast
from nipype.algorithms.modelgen import SpecifySPMModel
from nipype.interfaces import matlab as mlab
from nipype.interfaces.io import SelectFiles, DataSink
import nipype.interfaces.utility as util 
from nipype.algorithms import rapidart as ra
from nipype.interfaces.utility import Function, IdentityInterface
import nipype.pipeline.engine as pe
import nipype.interfaces.io as nio
from nipype.interfaces.base import Bunch
from nipype import DataGrabber, Workflow, Node
from scipy.io.matlab import loadmat



# necessary to let nipype know about matlab path



spm.SPMCommand.set_mlab_paths(paths=os.path.abspath(os.path.join(os.environ['HOME'], 'Documents/MATLAB/spm12/')), matlab_cmd='/soft/matlab_hd/R2020b/bin/glnxa64/MATLAB -nodesktop -nosplash')



mlab.MatlabCommand.set_default_matlab_cmd("/soft/matlab_hd/R2020b/bin/glnxa64/MATLAB  -nodesktop -nosplash")
mlab.MatlabCommand.set_default_paths(os.path.abspath(os.path.join(os.environ['HOME'], 'Documents/MATLAB/spm12/')))



# spm.SPMCommand().version



fsl.FSLCommand.set_default_output_type('NIFTI')



base_dir = os.path.join(os.environ['HOME'], 'spmbasics/data/')



experiment_dir = os.path.join(base_dir, 'output')
data_dir = os.path.abspath(os.path.join(base_dir, 'face_rep'))
output_dir = 'datasink'
working_dir = 'workingdir'

# list of subject identifiers
subject_list = ['M03953']

# TR of functional images
TR = 2.


# Smoothing width used during preprocessing
fwhm = [8]


# add how to refer sots




#mat0 = mat = loadmat(os.path.join(data_dir, "sots.mat"), mat_dtype=True, matlab_compatible=True, struct_as_record=True)


# In[11]:


#mat = loadmat(os.path.join(data_dir, "sots.mat"), mat_dtype=True, matlab_compatible=True, struct_as_record=True, simplify_cells=True)
#sot = mat['sot'][1]

#itemlag = mat['itemlag'][0]
#onsets=[sot[0], sot[1], sot[2], sot[3]],
# itemlag = mat['itemlag']




mat = loadmat(os.path.join(data_dir, "sots.mat"), struct_as_record=False, simplify_cells=True)
sot = mat['sot']
itemlag = mat['itemlag']



subjectinfo_param = [
    Bunch(
        conditions=['N1', 'N2', 'F1', 'F2'],
        onsets=[sot[0], sot[1], sot[2], sot[3]],
        durations=[[0], [0], [0], [0]],
        amplitudes=None,
        tmod=None,
        pmod=[
            None,
            Bunch(name=['Lag'], param=itemlag[1].astype(dtype='float64').tolist(), poly=[2]),
            None,
            Bunch(name=['Lag'], param=itemlag[3].astype(dtype='float64').tolist(), poly=[2])
        ],
        regressor_names=None,
        regressors=None)
]



cont1 = ('Famous_lag1', 'T', ['F2xLag^1'], [1])
cont2 = ('Famous_lag2', 'T', ['F2xLag^2'], [1])
fcont1 = ('Famous Lag', 'F', [cont1, cont2])
paramcontrasts = [cont1, cont2, fcont1]




# SpecifyModel - Generates SPM-specific Model
specmodel = Node(SpecifySPMModel(concatenate_runs=False,
                                 input_units='scans',
                                 output_units='scans',
                                 time_repetition=TR,
                                 high_pass_filter_cutoff=128,
                                 subject_info = subjectinfo_param),
                 name="specmodel")

# Level1Design - Generates an SPM design matrix same as the first level tutorial
eventparam = Node(Level1Design(bases={'hrf': {'derivs': [0, 0]}},
                                 timing_units='scans',
                                 interscan_interval=TR,
                                 volterra_expansion_order=1, # no model interction
                                 flags={'mthresh': 0.8},
                                 global_intensity_normalization='none',
                                 microtime_onset=12,
                                 microtime_resolution=24,
                                 #factor_info = [dict(name = 'Fame', levels = 2), # figure out factorized output names
                                 #               dict(name = 'Rep', levels = 2)],
                                 model_serial_correlations='AR(1)'), #matlabbatch{1}.spm.stats.fmri_spec.cvi = 'AR(1)';
                    name="eventparam")

# EstimateModel - estimate the parameters of the model
paramestimate = Node(EstimateModel(estimation_method={'Classical': 1}),
                      write_residuals=False, 
                      name="paramestimate")

# EstimateContrast - estimates contrasts
paramconest = Node(EstimateContrast(contrasts = paramcontrasts),
                    use_derivs=False, 
                    name="paramconest")



# Infosource - a function free node to iterate over the list of subject names
infosource = Node(IdentityInterface(fields=['subject_id',
                                            'contrasts'],
                                    contrasts=paramcontrasts),
                  name="infosource")
infosource.iterables = [('subject_id', subject_list)]


templates = {'func': os.path.join(output_dir, 'preproc', '_subject_id_{subject_id}',
                         's{subject_id}_0005_0006_merged.nii'),
             'mc_param': os.path.join(output_dir, 'preproc', '_subject_id_{subject_id}',
                         'rp_s{subject_id}_0005_0006_merged.txt'),
             'outliers': os.path.join(output_dir, 'preproc', '_subject_id_{subject_id}', 
                             'art.wars{subject_id}_0005_0006_merged_outliers.txt'),
             'smooths': os.path.join(output_dir, 'preproc', '_subject_id_{subject_id}',
                         'swars{subject_id}_0005_0006_merged.nii')}
selectfiles = Node(SelectFiles(templates,
                               base_directory=experiment_dir,
                               sort_filelist=True),
                   name="selectfiles")

# Datasink - creates output folder for important outputs
datasink = Node(DataSink(base_directory=experiment_dir,
                         container=output_dir),
                name="datasink")







def makelist(item):
    return [item]




# Initiation of the 1st-level analysis workflow
event_param = Workflow(name='event_param')
event_param.base_dir = os.path.join(experiment_dir, working_dir)

# Connect up the 1st-level analysis components
event_param.connect([(infosource, selectfiles, [('subject_id', 'subject_id')]),
                    (infosource, paramconest, [('contrasts', 'contrasts')]),
                    (selectfiles, specmodel, [(('func', makelist),  'functional_runs')]), 
                    (selectfiles, specmodel, [('mc_param', 'realignment_parameters'),
                                                ('outliers', 'outlier_files')]),
                    (specmodel, eventparam, [('session_info','session_info')]),
                    (eventparam, paramestimate, [('spm_mat_file','spm_mat_file')]),                    
                    (paramestimate, paramconest, [('spm_mat_file','spm_mat_file'),
                                                  ('beta_images','beta_images'),
                                                  ('residual_image', 'residual_image')]),
                    (paramconest, datasink, [('spm_mat_file', 'event_param.@spm_mat'),
                                              ('spmT_images', 'event_param.@T'),
                                              ('con_images', 'event_param.@con'),
                                              ('spmF_images', 'event_param.@F'),
                                              ('ess_images', 'event_param.@ess')]),
                    ])



event_param.write_graph(graph2use='colored', format='png', dotfilename='colored_graph.dot', simple_form=True)



event_param.write_graph(graph2use='flat', format='png', dotfilename='flat_graph.dot', simple_form=True)








event_param.run('MultiProc', plugin_args={'n_procs': 4})



