# spmbasics, a reproduction attempt


[![DOI](https://zenodo.org/badge/784344321.svg)](https://zenodo.org/doi/10.5281/zenodo.10953222)
### Understanding  and reproducing SPM Tutorials.

<Project description>
  
## Table of contents

   * [Overview](#Overview)

   * [data](https://github.com/mselimata/spmbasics/tree/main/data#readme)
   * [figures](https://github.com/mselimata/spmbasics/blob/main/figures/README.md)

   *  [code](https://github.com/mselimata/spmbasics/tree/main/src)

   * [results](https://github.com/mselimata/spmbasics/blob/main/results/README.md)

   * [How to reproduce each step](#How-to-reproduce-each-step)

   * [Further on reproducibility](#Further-on-reproducibility)

## Overview

This repo contains my reproduction of the SPM12 tutorials with MATLAB. 
You can find the code in [src](https://github.com/mselimata/spmbasics/tree/main/src) folder.


Version of the software used:```MATLAB R2020b``` & ```SPM12```.


 
 ## How to Reproduce Each Step

 *   For GUI interface, .mat files in the ```src/spm_mat``` must be loaded subsequently 
      1. Load [realignment](src/spm_mat/realignment_batch.mat) first. Select your data from the menu by specifiying  ```Data> Session```
      2. Then load [slice timing](src/spm_mat/slice_timing_batch.mat)
      3. Follow by [coregistration](src/spm_mat/coregistration_batch.mat)
      4. Continue by loading [segmentation](src/spm_mat/segmentation_batch.mat)
      5. Load [normalization](src/spm_mat/normalisation_batch.mat)
      6. Lastly [smoothing](src/spm_mat/smoothing_batch.mat)
 *   For Batch interface
     * Load [batch interface GUI mat](src/spm_mat/batch_preprocessing_batch.mat) at the first step of the Batch interface ```Realign: Estimate &Reslice ``` select your data by specifiying  ```Data> Session```
 *   For Scripting 
 [preprocessing_dep.m ](src/preprocessing_dep.m) controls the job of [preprocessing_dep_job.m](src/preprocessing_dep_job.m) it is also possible to run the ```_job.m``` file separately.
 Make sure to indicate correct file paths for these files.

## Further on reproducibility

SPM has a display and check reg features to visually inspect the outputs.
Visual inspection does not guarantee that all the results are the same.
To ensure about all of the steps producing same results after the same preprocessing steps, you can use this tiny bash script TODO add file and link on your results folders to compare if they are identical or not based on their unique hash values. 

Instructions in checking hash values using bash script or one liner

1. In order to compare functional files for example, place ```checksummer.sh``` in  ```GUI/sub-01/func/``` folder. 
It will create an output and you can change output name accordingly.
Repeat this process for the copies of your SCRIPT and BATCH folders.

2. In order to copy only the hash values ```cut -c-64 file.sha256 > copyfile.sha256``` 
This way it only contains the hash values.

3. ```diff3 hasfile1 hashfile2 hashfile3``` 
should not be producing output.
That means all your nifti files are same.



If you notice anything needs to be edited or fixed, feel free to open an issue. 
Thanks for your time and attention. :smile: 
