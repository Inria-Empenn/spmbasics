#!/usr/bin/env python
# coding: utf-8

# ## Categorical Modelling



import os

from nipype.interfaces import fsl 
from nipype.interfaces import spm
from nipype.interfaces.spm import Level1Design, EstimateModel, EstimateContrast
from nipype.algorithms.modelgen import SpecifySPMModel
from nipype.interfaces import matlab as mlab
from nipype.interfaces.io import SelectFiles, DataSink


from nipype.interfaces.utility import Function, IdentityInterface

from nipype.interfaces.base import Bunch
from nipype import DataGrabber, Workflow, Node
from scipy.io.matlab import loadmat



spm.SPMCommand.set_mlab_paths(paths=os.path.abspath(os.path.join(os.environ['HOME'], 'Documents/MATLAB/spm12/')), matlab_cmd='/soft/matlab_hd/R2020b/bin/glnxa64/MATLAB -nodesktop -nosplash')



mlab.MatlabCommand.set_default_matlab_cmd("/soft/matlab_hd/R2020b/bin/glnxa64/MATLAB  -nodesktop -nosplash")
mlab.MatlabCommand.set_default_paths(os.path.abspath(os.path.join(os.environ['HOME'], 'Documents/MATLAB/spm12/')))



fsl.FSLCommand.set_default_output_type('NIFTI')



base_dir = os.path.join(os.environ['HOME'], 'spmbasics/data/')




experiment_dir = os.path.join(base_dir, 'output')
data_dir = os.path.abspath(os.path.join(base_dir, 'face_rep'))
output_dir = 'nipype'
working_dir = 'workingdir'

# list of subject identifiers
subject_list = ['M03953']

# TR of functional images
TR = 2.


# Smoothing width used during preprocessing
fwhm = [8]


#mat =  loadmat(os.path.join(data_dir, "sots.mat"), mat_dtype=True, matlab_compatible=True, struct_as_record=True)


mat = loadmat(os.path.join(data_dir, "sots.mat"), mat_dtype=True, matlab_compatible=True, struct_as_record=True, simplify_cells=True)
#sot = mat['sot'][1]

#itemlag = mat['itemlag'][0]
#onsets=[sot[0], sot[1], sot[2], sot[3]],

#mat = loadmat(os.path.join(data_dir, "sots.mat"), struct_as_record=False)
#sot = mat['sot'][0]
#itemlag = mat['itemlag'][0]

#subjectinfo = [
#    Bunch(
#        conditions=['N1', 'N2', 'F1', 'F2'],
#        onsets=[sot[0], sot[1], sot[2], sot[3]],
#        durations=[[0], [0], [0], [0]],
#        amplitudes=None,
#        tmod=None,
#        pmod=None,
#        regressor_names=None,
#        regressors=None)
#]


subjectinfo = [
    Bunch(
        conditions=['N1', 'N2', 'F1', 'F2'],
        onsets=[ mat['sot'][0], mat['sot'][1],  mat['sot'][2],  mat['sot'][3]],
        durations=[[0], [0], [0], [0]],
        amplitudes=None,
        tmod=None,
        pmod=None,
        regressor_names=None,
        regressors=None)
]

# design matrix setting




cond1 = ('positive effect of condition', 'T',
         ['N1', 'N2', 'F1', 'F2'], [1, 1, 1, 1])
cond2 = ('positive effect of condition_dtemo', 'T',
          ['N1', 'N2', 'F1', 'F2'], [1, 1, 1, 1])
cond3 = ('positive effect of condition_ddisp', 'T',
          ['N1', 'N2', 'F1', 'F2'], [1, 1, 1, 1])
# non-famous > famous
fam1 = ('positive effect of Fame', 'T',
        ['N1', 'N2', 'F1', 'F2'], [1, 1, -1, -1])
fam2 = ('positive effect of Fame_dtemp', 'T',
        ['N1', 'N2', 'F1', 'F2'], [1, 1, -1, -1])
fam3 = ('positive effect of Fame_ddisp', 'T',
        ['N1', 'N2', 'F1', 'F2'], [1, 1, -1, -1])
# rep1 > rep2
rep1 = ('positive effect of Rep', 'T',
        ['N1', 'N2', 'F1', 'F2'], [1, -1, 1, -1])
rep2 = ('positive effect of Rep_dtemp', 'T',
        ['N1', 'N2', 'F1', 'F2'], [1, -1, 1, -1])
rep3 = ('positive effect of Rep_ddisp', 'T',
        ['N1', 'N2', 'F1', 'F2'], [1, -1, 1, -1])
int1 = ('positive interaction of Fame x Rep', 'T',
        ['N1', 'N2', 'F1', 'F2'], [-1, -1, -1, 1])
int2 = ('positive interaction of Fame x Rep_dtemp', 'T',
        ['N1', 'N2', 'F1', 'F2'], [1, -1, -1, 1])
int3 = ('positive interaction of Fame x Rep_ddisp', 'T',
        ['N1', 'N2', 'F1', 'F2'], [1, -1, -1, 1])

contf1 = ['average effect condition', 'F', [cond1, cond2, cond3]]
contf2 = ['main effect Fam', 'F', [fam1, fam2, fam3]]
contf3 = ['main effect Rep', 'F', [rep1, rep2, rep3]]
contf4 = ['interaction: Fam x Rep', 'F', [int1, int2, int3]]
contrast_list = [
    cond1, cond2, cond3, fam1, fam2, fam3, rep1, rep2, rep3, int1, int2, int3,
    contf1, contf2, contf3, contf4
]




# SpecifyModel - Generates SPM-specific Model
specifymodel = Node(SpecifySPMModel(concatenate_runs=False,
                                 input_units='scans',
                                 output_units='scans',
                                 time_repetition=TR,
                                 high_pass_filter_cutoff=128,
                                 subject_info = subjectinfo),
                 name="specifymodel")

# Level1Design - Generates an SPM design matrix same as the first level tutorial
eventcategorical = Node(Level1Design(bases={'hrf': {'derivs': [0, 0]}},
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
                    name="eventcategorical")

# EstimateModel - estimate the parameters of the model
categoricalestimate = Node(EstimateModel(estimation_method={'Classical': 1}),
                      write_residuals=False, 
                      name="categoricalestimate")

# EstimateContrast - estimates contrasts
categoricalconest = Node(EstimateContrast(contrasts = contrast_list),
                    use_derivs=True, 
                    name="categoricalconest")



# Infosource - a function free node to iterate over the list of subject names
infosource = Node(IdentityInterface(fields=['subject_id',
                                            'contrasts'],
                                    contrasts=contrast_list),
                  name="infosource")
infosource.iterables = [('subject_id', subject_list)]


templates = {'func': os.path.join(output_dir, 'preproc', '_subject_id_{subject_id}',
                         's{subject_id}_0005_0006_merged.nii'),
             'mc_param': os.path.join(output_dir, 'preproc', '_subject_id_{subject_id}',
                         'rp_s{subject_id}_0005_0006_merged.txt'),
             'outliers': os.path.join(output_dir, 'preproc', '_subject_id_{subject_id}', 
                             'art.wars{subject_id}_0005_0006_merged_outliers.txt')}
selectfiles = Node(SelectFiles(templates,
                               base_directory=experiment_dir,
                               sort_filelist=True),
                   name="selectfiles")

# Datasink - creates output folder for important outputs
datasink = Node(DataSink(base_directory=experiment_dir,
                         container=output_dir),
                name="datasink")




# Initiation of the 1st-level analysis workflow
event_cat = Workflow(name='event_cat')
event_cat.base_dir = os.path.join(experiment_dir, working_dir)

# Connect up the 1st-level analysis components
event_cat.connect([(infosource, selectfiles, [('subject_id', 'subject_id')]),
                    (infosource, categoricalconest, [('contrasts', 'contrasts')]),
                    (selectfiles, specifymodel, [('func', 'functional_runs')]),
                    (selectfiles, specifymodel, [('mc_param', 'realignment_parameters'),
                                                ('outliers', 'outlier_files')]),
                    (specifymodel, eventcategorical, [('session_info','session_info')]),
                    (eventcategorical, categoricalestimate, [('spm_mat_file','spm_mat_file')]),                    
                    (categoricalestimate, categoricalconest, [('spm_mat_file','spm_mat_file'),
                                                    ('beta_images','beta_images'),
                                                   ('residual_image', 'residual_image')]),
                    (categoricalconest, datasink, [('spm_mat_file', 'event_cat.@spm_mat'),
                                              ('spmT_images', 'event_cat.@T'),
                                              ('con_images', 'event_cat.@con'),
                                              ('spmF_images', 'event_cat.@F'),
                                              ('ess_images', 'event_cat.@ess')]),
                    ])




event_cat.write_graph(graph2use='colored', format='png', dotfilename='colored_graph.dot', simple_form=True)



event_cat.write_graph(graph2use='flat', format='png', dotfilename='flat_graph.dot', simple_form=True)




event_cat.run('MultiProc', plugin_args={'n_procs': 4})
