from __future__ import print_function
from builtins import str
from builtins import range
import os 
from nipype.interfaces import io as nio  # Data i/o #
from nipype.interfaces import matlab as mlab    # import matlab
from nipype.interfaces import fsl as fsl  # fsl
from nipype.interfaces import utility as niu  # utility
from nipype.pipeline import engine as pe  # pypeline engine
from nipype import Workflow, Node # pypline engine is enough, importing these for convenience.
# from nipype.algorithms import rapidart as ra  # artifact detection

# SPM specific interfaces
from nipype.interfaces import spm as spm 
import nipype.interfaces.spm.utils as spmu

from nipype.interfaces.spm import Realign
from nipype.interfaces.spm import SliceTiming
from nipype.interfaces.spm import Coregister
from nipype.interfaces.spm import NewSegment #SPM12 Segmentation
from nipype.interfaces.spm import Normalize12 # SPM12 normalize
from nipype.interfaces.spm import Smooth



from nipype.interfaces.matlab import MatlabCommand

spm.SPMCommand.set_mlab_paths(paths=os.path.abspath('./Documents/MATLAB/spm12/'), matlab_cmd='/soft/matlab_hd/R2020b/bin//glnxa64/MATLAB -nodesktop -nosplash')
# alternative to the above line just as a reminder

# mlab.MatlabCommand.set_default_paths(os.path.abspath('./Documents/MATLAB/spm12/')
# mlab.MatlabCommand.set_default_matlab_cmd("/soft/matlab_hd/R2020b/bin/glnxa64/MATLAB  -nodesktop -nosplash") # set default matlab location to be used by spm
# spm.SPMCommand().version  # checking spm version to be sure it is imported.
fsl.FSLCommand.set_default_output_type('NIFTI') # to make sure output type is NIFTI

# defining workflow name and base direction

preproc = Workflow(name='block_preproc', base_dir=os.path.abspath('./spmbasics/data/output'))

# realigning the functional images

realigner = Node(interface=spm.Realign(), name='realign')
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

slicetimed = Node(interface=spm.SliceTiming(), name = 'slicetiming')
slicetimed.inputs.num_slices = 64
slicetimed.inputs.time_repetition = 7.
slicetimed.inputs.time_acquisition = 6.8906
slicetimed.inputs.slice_order = list(range(64,0,-1))
slicetimed.inputs.ref_slice = 32
slicetimed.inputs.out_prefix = 'a'

# coregistration settings

coregister = Node(spm.Coregister(), name="coregister")
coregister.inputs.jobtype = 'estimate'
coregister.inputs.cost_function = 'nmi'
coregister.inputs.fwhm = [7.0, 7.0]
coregister.inputs.separation = [4.0, 2.0]
coregister.inputs.tolerance = [0.02, 0.02, 0.02, 0.001, 0.001, 0.001, 0.01, 0.01, 0.01, 0.001, 0.001, 0.001]

# segmentation settings

seg =  Node(spm.NewSegment(), name="newsegment")
seg.inputs.affine_regularization = 'mni'
seg.inputs.channel_info = (0.001, 60, (False, True)) #save bias corrected map
tissue1 = ((os.path.abspath('./Documents/MATLAB/spm12/tpm/TPM.nii'), 1), 1, (True, False), (False, False))
tissue2 = ((os.path.abspath('./Documents/MATLAB/spm12/tpm/TPM.nii'), 2), 1, (True, False), (False, False))
tissue3 = ((os.path.abspath('./Documents/MATLAB/spm12/tpm/TPM.nii'), 3), 2, (True, False), (False, False))
tissue4 = ((os.path.abspath('./Documents/MATLAB/spm12/tpm/TPM.nii'), 4), 3, (True, False), (False, False))
tissue5 = ((os.path.abspath('./Documents/MATLAB/spm12/tpm/TPM.nii'), 5), 4, (True, False), (False, False))
tissue6 = ((os.path.abspath('./Documents/MATLAB/spm12/tpm/TPM.nii'), 6), 2, (False, False), (False, False))
seg.inputs.tissues = [tissue1, tissue2, tissue3, tissue4, tissue5, tissue6]
seg.inputs.warping_regularization = [0, 0.001, 0.5, 0.05, 0.2]
seg.inputs.sampling_distance = 3
seg.inputs.write_deformation_fields = [False, True] 

# normalization settings

normalize = Node(spm.Normalize12(), name="normalize")
normalize.inputs.jobtype = 'write'
normalize.inputs.write_bounding_box =  [[-78, -112, -70], [78, 76, 85]]
normalize.inputs.write_voxel_sizes = [3, 3, 3]
normalize.inputs.write_interp = 4
normalize.inputs.out_prefix = 'w'

# smoothing settings

smooth = Node(spm.Smooth(), name="smooth")
smooth.inputs.fwhm = [6, 6, 6]
smooth.inputs.data_type = 0
smooth.inputs.implicit_masking = False
smooth.inputs.out_prefix = 's'

# connecting the nodes

preproc.connect([(realigner, slicetimed, [('realigned_files', 'in_files')]),
                    (slicetimed, coregister, [('timecorrected_files', 'source')]),
                    (realigner, coregister, [('mean_image', 'target')]),
                    (coregister, seg, [('coregistered_files', 'channel_files')]),
                    (coregister, normalize, [('coregistered_files', 'apply_to_files')]),
                    (seg, normalize, [('transformation_mat', 'parameter_file')]), # check this
                    (normalize, smooth, [('normalized_files', 'in_files')])])

# selecting and assigning input data
# this part is not final yet, it needs careful thinking and tests 

datasink = Node(nio.DataSink(), name='sinker')
datasink.inputs.base_directory = os.path.abspath('./spmbasics/data/output')
preproc.connect([(realigner, datasink, [('in_files', 'realign.@in_files')]),]) # check this


# writing the workflow graph

preproc.write_graph(graph2use='colored', format='png', simple_form=True)

# running the workflow

preproc.run()