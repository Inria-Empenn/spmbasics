#!/usr/bin/env python

# coding: utf-8
from nilearn import plotting
# get_ipython().run_line_magic('matplotlib', 'inline')
import os
import json
from nipype.interfaces import fsl 
from nipype.interfaces import spm
from nipype.interfaces.spm import (Realign, SliceTiming, Coregister,  NewSegment,  Normalize12, Smooth)
from nipype.interfaces import matlab as mlab
from nipype.interfaces.io import SelectFiles, DataSink
import nipype.interfaces.utility as util 
import nipype.pipeline.engine as pe
import nipype.interfaces.io as nio
from nipype import DataGrabber, Workflow, Node



spm.SPMCommand.set_mlab_paths(paths=os.path.abspath('./Documents/MATLAB/spm12/'), matlab_cmd='/soft/matlab_hd/R2020b/bin//glnxa64/MATLAB -nodesktop -nosplash')
# alternative to the above line just as a reminder

# mlab.MatlabCommand.set_default_paths(os.path.abspath('./Documents/MATLAB/spm12/')
# mlab.MatlabCommand.set_default_matlab_cmd("/soft/matlab_hd/R2020b/bin/glnxa64/MATLAB  -nodesktop -nosplash") # set default matlab location to be used by spm
# spm.SPMCommand().version  # checking spm version to be sure it is imported.
fsl.FSLCommand.set_default_output_type('NIFTI') # to make sure output type is NIFTI

# defining workflow name and base direction

preproc = Workflow(name='block_preproc', base_dir=os.path.abspath('./spmbasics/data/output'))

base_dir = os.path.join(os.environ['HOME'], 'spmbasics/data/')

# grabbing data

grabber =  Node(DataGrabber(infields=['subject_id'],
                      outfields=['anat', 'func']),
          name='datagrabber')

grabber.inputs.base_directory = os.path.join(base_dir, 'MoAEpilot_raw/')

grabber.inputs.template = '*'
grabber.inputs.sort_filelist = True

# specify the template
grabber.inputs.template_args = {'anat': [['subject_id']],
                           'func': [['subject_id', 'task_name']]}
grabber.inputs.field_template = {'anat': 'sub-%02d/anat/*_T1w.nii',
                            'func': 'sub-%02d/func/*_task-%s_bold.nii'}

grabber.inputs.subject_id = 1
grabber.inputs.task_name = "auditory"

# realigning the functional images

realigner = Node(interface=Realign(), name='realign')
# realigner.inputs.in_files = func_file # this can change
realigner.inputs.register_to_mean = True
realigner.inputs.fwhm = 5
realigner.inputs.interp = 2
realigner.inputs.quality = 0.9
realigner.inputs.separation = 4
realigner.inputs.wrap = [0, 0, 0]
realigner.inputs.write_which = [2, 1]
realigner.inputs.write_interp = 4 
realigner.inputs.write_wrap = [0, 0, 0]
realigner.inputs.jobtype = 'estwrite'
realigner.inputs.out_prefix = 'r'

# slice timing settings

slicetiming = Node(interface=SliceTiming(), name = 'slicetiming')
# st.inputs.in_files = anat_file
slicetiming.inputs.num_slices = 64
slicetiming.inputs.time_repetition = 7.
slicetiming.inputs.time_acquisition = 6.8906
slicetiming.inputs.slice_order = list(range(64,0,-1))
slicetiming.inputs.ref_slice = 32
slicetiming.inputs.out_prefix = 'a'


# coregistration settings

coregister = Node(Coregister(), name="coregister")
coregister.inputs.jobtype = 'estimate'
coregister.inputs.cost_function = 'nmi'# normalized mutual information
coregister.inputs.fwhm = [7.0, 7.0]
coregister.inputs.separation = [4.0, 2.0]
coregister.inputs.tolerance = [0.02, 0.02, 0.02, 0.001, 0.001, 0.001, 0.01, 0.01, 0.01, 0.001, 0.001, 0.001]

# segmentation settings

tpm_path = os.path.abspath(os.path.join(os.environ['HOME'], 'Documents/MATLAB/spm12/tpm/', 'TPM.nii'))


segment =  Node(spm.NewSegment(), name="newsegment")
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


# normalization settings

normalize = Node(Normalize12(), name="normalize")
normalize.inputs.jobtype = 'write'
normalize.inputs.write_bounding_box =  [[-78, -112, -70], [78, 76, 85]]
normalize.inputs.write_voxel_sizes = [3, 3, 3]
normalize.inputs.write_interp = 4
normalize.inputs.out_prefix = 'w'

# smoothing settings

smooth = Node(Smooth(), name="smooth")
smooth.inputs.fwhm = [6, 6, 6]
smooth.inputs.data_type = 0
smooth.inputs.implicit_masking = False
smooth.inputs.out_prefix = 's'

# connecting the nodes and the data

sink = Node(interface=DataSink(),
                   name='sink')
sink.inputs.base_directory = os.path.join(base_dir, 'output')



preproc.connect([(grabber, realigner, [('func', 'in_files')]),
                 (realigner, slicetiming, [('realigned_files', 'in_files')]),
                 (realigner, coregister, [('mean_image', 'target')]),
                 (grabber, coregister, [('anat', 'source')]), 
                (coregister, segment, [('coregistered_source', 'channel_files')]),
                (segment, normalize, [('forward_deformation_field', 'deformation_file')]),
                (slicetiming, normalize, [('timecorrected_files', 'apply_to_files')]),
                 (normalize, smooth, [('normalized_files', 'in_files')]),
])

# writing the workflow graph

preproc.write_graph(graph2use='colored', format='png', simple_form=True)


# running the workflow


preproc.run()