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
