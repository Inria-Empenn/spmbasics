#!/usr/bin/env python
# coding: utf-8


import os
from nipype.interfaces import spm
from nipype.interfaces.base import traits
from nipype.interfaces.base import TraitedSpec
from nipype.interfaces.matlab import MatlabCommand, MatlabInputSpec

import nipype.interfaces.matlab as mlab

# matlab_cmd = '/soft/matlab_hd/R2020b/bin//glnxa64/MATLAB'
# spm.SPMCommand.set_mlab_paths(matlab_cmd=matlab_cmd)


spm.SPMCommand.set_mlab_paths(paths=os.path.abspath('./Documents/MATLAB/spm12/'), matlab_cmd='/soft/matlab_hd/R2020b/bin//glnxa64/MATLAB -nodesktop -nosplash')



spm.SPMCommand().version




mlab.MatlabCommand.set_default_matlab_cmd("/soft/matlab_hd/R2020b/bin/glnxa64/MATLAB -nodesktop -nosplash")




res = mlab.MatlabCommand(script="").run()
print(res.runtime.stdout)



# MatlabCommand(matlab_cmd='/soft/matlab_hd/R2020b/bin//glnxa64/MATLAB -nodesktop -nosplash')



class HelloWorldInputSpec(MatlabInputSpec):
    name = traits.Str(mandatory=True, desc='Name of person to say hello to')


class HelloWorldOutputSpec(TraitedSpec):
    matlab_output = traits.Str()


class HelloWorld(MatlabCommand):
    """Basic Hello World that displays Hello <name> in MATLAB

    Returns
    -------

    matlab_output : capture of matlab output which may be
                    parsed by user to get computation results

    Examples
    --------

    >>> hello = HelloWorld()
    >>> hello.inputs.name = 'hello_world'
    >>> out = hello.run()
    >>> print out.outputs.matlab_output
    """

    MatlabCommand.set_default_paths('/soft/matlab_hd/R2020b/bin//glnxa64/MATLAB')
    
    input_spec = HelloWorldInputSpec
    output_spec = HelloWorldOutputSpec

    def _my_script(self):
        """This is where you implement your script"""
        script = """
        disp('Hello %s Python')
        two = 1 + 1
        """ % (
            self.inputs.name
        )
        return script

    def run(self, **inputs):
        # Inject your script
        self.inputs.script = self._my_script()
        results = super(MatlabCommand, self).run(**inputs)
        stdout = results.runtime.stdout
        # Attach stdout to outputs to access matlab results
        results.outputs.matlab_output = stdout
        return results

    def _list_outputs(self):
        outputs = self._outputs().get()
        return outputs


# Printing hello world python using matlab


hello = HelloWorld()
hello.inputs.name = 'hello_world'
out = hello.run()
print(out.outputs.matlab_output)