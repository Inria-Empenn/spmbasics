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
      1. Load [realignment_batch.m](src/batch_step/realignment_batch.m) first. Select your data from the menu by specifiying  ```Data> Session```
      2. Then load [slice timing_batch.m](src/batch_step/slice_timing_batch.m)
      3. Follow by [coregistration_batch.m](src/batch_step/coregistration_batch.m)
      4. Continue by loading [segmentation_batch.m](src/batch_step/segmentation_batch.m)
      5. Load [normalization_batch.m](src/batch_step/normalisation_batch.m)
      6. Lastly [smoothing_batch.m](src/batch_step/smoothing_batch.m)
 *   For Batch interface
     * Load [batch interface GUI](src/batch/preprocessing_batch.m) at the first step of the Batch interface ```Realign: Estimate &Reslice ``` select your data by specifiying  ```Data> Session```
 *   For Scripting 
 [preprocessing_script.m ](src/preprocessing_dep.m) controls the job of [preprocessing_script_job.m](src/preprocessing_dep_job.m) it is also possible to run the ```_job.m``` file separately. Inthis example I edited and used ```preprocessing_script_job.m```
 Make sure to indicate correct file paths for these files.

## Further on reproducibility

SPM has a display and check reg features to visually inspect the outputs.
Visual inspection does not guarantee that all the results are the same.
To ensure about all of the steps producing same results after the same preprocessing steps, you can use this tiny (just *122* lines) bash script.
This script basically lists and compares the ```sha25sum``` values of the designated folders containing nifti files.  

Instructions to check hash values using the provided bash script:

* The script is in ```/src``` folder, named as ```shasum_checker.sh``` 

* Important note regarding to the base folder: Base folder should contain the results from the [batch_step](https://www.fil.ion.ucl.ac.uk/spm/docs/tutorials/fmri/block/preprocessing/introduction/) interface. It is recommended to run the ```shasum_checker.sh``` on it once it is finished and then lock the writing access using ``` chmod a=rx -R filename ``` for linux. 


* Make sure to save your results of preprocessing into different folders and direct their paths accordingly.

* For example, for results which obtained from  interface create a ```BATCH``` folder with the input data and make SPM run from there so it will create results of the  batch interface.

Lastly keep in mind that every  instruction in this repo can change and serves the purpose of  my learning and testing. 

If you notice anything needs to be edited or fixed, feel free to open an issue. 
Thanks for your time and attention. :smile: 
