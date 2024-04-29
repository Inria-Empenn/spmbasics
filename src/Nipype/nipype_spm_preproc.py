from __future__ import print_function
from builtins import str
from builtins import range
import os.path as op  # system function
from nipype.interfaces import io as nio  # Data i/o #
from nipype.interfaces import matlab as mlab    # how to run matlab
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
from nipype.interfaces.spm import Segment
from nipype.interfaces.spm import Normalize12 # SPM12 normalize
from nipype.interfaces.spm import Smooth



from nipype.interfaces.matlab import MatlabCommand
MatlabCommand.set_default_paths('/home/matay/Documents/MATLAB/spm12')
spm.SPMCommand.set_mlab_paths(paths='/home/matay/Documents/MATLAB/spm12/', matlab_cmd='/soft/matlab_hd/R2020b/bin//glnxa64/MATLAB -nodesktop -nosplash')
# spm.SPMCommand().version  # checking spm version to be sure it is imported.
fsl.FSLCommand.set_default_output_type('NIFTI')

