#!/usr/bin/env python
# coding: utf-8

# ## Preprocessing

# In[1]:


from nilearn import plotting
import os
import json
from nipype.interfaces import fsl 
from nipype.interfaces import spm
from nipype.interfaces.spm import (Realign, SliceTiming, Coregister,  NewSegment,  Normalize12, Smooth)
from nipype.interfaces import matlab as mlab
from nipype.interfaces.io import SelectFiles, DataSink
from nipype.algorithms import rapidart as ra
from nipype.interfaces.utility import IdentityInterface
from nipype import Workflow, Node

# necessary to let nipype know about matlab path



spm.SPMCommand.set_mlab_paths(paths=os.path.abspath(os.path.join(os.environ['HOME'], 'Documents/MATLAB/spm12/')), matlab_cmd='/soft/matlab_hd/R2020b/bin/glnxa64/MATLAB -nodesktop -nosplash')



mlab.MatlabCommand.set_default_matlab_cmd("/soft/matlab_hd/R2020b/bin/glnxa64/MATLAB  -nodesktop -nosplash")
mlab.MatlabCommand.set_default_paths(os.path.abspath(os.path.join(os.environ['HOME'], 'Documents/MATLAB/spm12/')))




# spm.SPMCommand().version




fsl.FSLCommand.set_default_output_type('NIFTI')





base_dir = os.path.join(os.environ['HOME'], 'spmbasics/data/')





experiment_dir = os.path.join(base_dir, 'output')
output_dir = 'nipype'
working_dir = 'workingdir'

# list of subject identifiers
subject_id = ['01']

task_id = ['auditory']


# TR of functional images
with open(os.path.join(base_dir, 'MoAEpilot/task-auditory_bold.json'), 'rt') as fp:
    task_info = json.load(fp)
TR = task_info['RepetitionTime']

# Smoothing width used during preprocessing
fwhm = [6]



# Infosource - a function free node to iterate over the list of subject names
infosource = Node(IdentityInterface(fields=['subject_id', 'task_name']),
                  name="infosource")
infosource.iterables = [('subject_id', subject_id),
                        ('task_name', task_id)]
# SelectFiles - to grab the data (alternativ to DataGrabber)
anat_file = os.path.join( base_dir, 'MoAEpilot/', 'sub-{subject_id}', 'anat',  'sub-{subject_id}_T1w.nii' )
func_file = os.path.join( base_dir, 'MoAEpilot/', 'sub-{subject_id}', 'func',
                'sub-{subject_id}_task-{task_name}_bold.nii')

templates = {'anat': anat_file,
             'func': func_file}
selectfiles = Node(SelectFiles(templates,
                               base_directory=base_dir),
                   name="selectfiles")

# Datasink - creates output folder for the needed outputs
datasink = Node(DataSink(base_directory=experiment_dir,
                         container=output_dir),
                name="datasink")



realigner = Node(interface=Realign(), name='realign')
realigner.inputs.register_to_mean = True
realigner.inputs.fwhm = 5
realigner.inputs.interp = 2
realigner.inputs.quality = 0.9
realigner.inputs.separation = 4
realigner.inputs.wrap = [0, 0, 0]
realigner.inputs.write_which = [2, 1]
realigner.inputs.write_interp = 4 
realigner.inputs.write_wrap = [0, 0, 0]
realigner.inputs.write_mask = True
realigner.inputs.jobtype = 'estwrite'
realigner.inputs.out_prefix = 'r'



slicetiming = Node(interface=SliceTiming(), name = 'slicetiming')
slicetiming.inputs.num_slices = 64
slicetiming.inputs.time_repetition = 7.
slicetiming.inputs.time_acquisition = 6.8906
slicetiming.inputs.slice_order = list(range(64,0,-1))
slicetiming.inputs.ref_slice = 32
slicetiming.inputs.out_prefix = 'a'


coregister = Node(Coregister(), name="coregister")
coregister.inputs.jobtype = 'estimate'
coregister.inputs.cost_function = 'nmi'
coregister.inputs.fwhm = [7.0, 7.0]
coregister.inputs.separation = [4.0, 2.0]
coregister.inputs.tolerance = [0.02, 0.02, 0.02, 0.001, 0.001, 0.001, 0.01, 0.01, 0.01, 0.001, 0.001, 0.001]
coregister.inputs.out_prefix = 'c'



tpm_path = os.path.abspath(os.path.join(os.environ['HOME'], 'Documents/MATLAB/spm12/tpm/', 'TPM.nii'))



segment =  Node(NewSegment(), name="newsegment")
segment.inputs.affine_regularization = 'mni'
segment.inputs.channel_info = (0.001, 60, (False, True)) #save bias corrected map
tissue1 = ((tpm_path, 1), 1, (True, False), (False, False))
tissue2 = ((tpm_path, 2), 1, (True, False), (False, False))
tissue3 = ((tpm_path, 3), 2, (True, False), (False, False))
tissue4 = ((tpm_path, 4), 3, (True, False), (False, False))
tissue5 = ((tpm_path, 5), 4, (True, False), (False, False))
tissue6 = ((tpm_path, 6), 2, (False, False), (False, False))
segment.inputs.tissues = [tissue1, tissue2, tissue3, tissue4, tissue5, tissue6]
segment.inputs.warping_regularization = [0, 0.001, 0.5, 0.05, 0.2]
segment.inputs.sampling_distance = 3
segment.inputs.write_deformation_fields = [False, True] 



normalize = Node(Normalize12(), name="normalize") #old normalize now
normalize.inputs.jobtype = 'write'
normalize.inputs.write_bounding_box =  [[-78, -112, -70], [78, 76, 85]]
normalize.inputs.write_voxel_sizes = [3, 3, 3]
normalize.inputs.write_interp = 4
normalize.inputs.out_prefix = 'w'



smooth = Node(Smooth(), name="smooth")
smooth.inputs.fwhm = [6, 6, 6]
smooth.inputs.data_type = 0
smooth.inputs.implicit_masking = False
smooth.inputs.out_prefix = 's'



art = Node(ra.ArtifactDetect(), name="art")
art.inputs.use_differences = [True, False] # successive motion, # intensity parameter
art.inputs.use_norm = True
art.inputs.norm_threshold = 1
art.inputs.zintensity_threshold = 3
art.inputs.mask_type = 'spm_global'
art.inputs.intersect_mask = True
art.inputs.bound_by_brainmask = True
art.inputs.parameter_source = 'SPM'
art.inputs.plot_type='png'


def get_vox_dims(volume):
    import nibabel as nb
    if isinstance(volume, list):
        volume = volume[0]
    nii = nb.load(volume)
    hdr = nii.header
    voxdims = hdr.get_zooms()
    return [float(voxdims[0]), float(voxdims[1]), float(voxdims[2])]


block_preprocess = Workflow(name='nipype_block_preprocess')
block_preprocess.base_dir = os.path.join(experiment_dir, working_dir)



block_preprocess.connect([(infosource, selectfiles, [('subject_id', 'subject_id'),
                                              ('task_name', 'task_name')]),
                 (selectfiles, realigner, [('func', 'in_files')]),
                 (selectfiles, datasink, [('func', 'block_preprocess.@func'),
                                          ('anat', 'block_preprocess.@anat')]),  
                 (realigner, datasink, [('realignment_parameters', 'block_preprocess.@realignement_parameters'),
                                        ('realigned_files', 'block_preprocess.@realigned_files'),
                                        ('mean_image', 'block_preprocess.@mean_image')]),
                 (realigner, slicetiming, [('realigned_files', 'in_files')]),  
                 (slicetiming, datasink, [('timecorrected_files', 'block_preprocess.@timecorrected_files')]),
                 (realigner, coregister, [('mean_image', 'target')]),
                 (selectfiles, coregister, [('anat', 'source')]), 
                 (coregister, datasink, [('coregistered_source', 'block_preprocess.@coregisered_source')]),
                 (coregister, segment, [('coregistered_source', 'channel_files')]),
                 (segment, datasink, [('bias_corrected_images', 'block_preprocess.@bias_corrected_images'),
                                      ('transformation_mat', 'block_preprocess.@transformation_mat'),
                                      ('native_class_images', 'block_preprocess.@native_class_images'),
                                      ('forward_deformation_field', 'block_preprocess.@forward_deformation_field')]),
                 (segment, normalize, [('forward_deformation_field', 'deformation_file')]),
                 (slicetiming, normalize, [('timecorrected_files', 'apply_to_files')]), 
                 (normalize, datasink, [('normalized_files', 'block_preprocess.@normalized_files')]),
                 (normalize, smooth, [('normalized_files', 'in_files')]),
                 (smooth, datasink, [('smoothed_files', 'block_preprocess.@smoothed_files')]),
                 (realigner, art, [('realignment_parameters', 'realignment_parameters')]),
                 (normalize, art, [('normalized_files', 'realigned_files')]),
                 (art, datasink, [('outlier_files', 'block_preprocess.@outlier_files'),
                                  ('plot_files', 'block_preprocess.@plot_files')])
])



# Create 1st-level analysis output graph
block_preprocess.write_graph(graph2use='colored', format='png', dotfilename='colored_block.dot', simple_form=True)



# Create 1st-level analysis output graph
block_preprocess.write_graph(graph2use='flat', format='png', dotfilename='flat_block.dot', simple_form=True)





block_preprocess.run('MultiProc', plugin_args={'n_procs': 4})

