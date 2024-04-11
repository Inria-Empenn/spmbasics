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

## Overview

This repo contains my reproduction of the SPM12 tutorials with MATLAB. 
You can find the code in [src](https://github.com/mselimata/spmbasics/tree/main/src) folder.


Version of the software used:```MATLAB R2020b``` & ```SPM12```.


 
 ## How to Reproduce Each Step
 TODO - add details and links
Follow the guideline below for each process:
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
 [preprocessing m ](src/preprocessing_dep.m)

If you notice anything needs to be edited or fixed, feel free to open an issue. 
Thanks for your time and attention. :smile: 
