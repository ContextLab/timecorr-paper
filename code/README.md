This folder contains notebooks to replicate analyses and figures:

To replicate the figures for the analysis, download the content of the data folder provided [here](https://drive.google.com/file/d/1CZYe8eyAkZFuLqfwwlKoeijgkjdW6vFs/view?usp=sharing), put the zip file in `timecorr_paper` folder and extract it.

Figure 2. Run `notebooks/synthetic_data.ipynb`

Figure 3. Run `notebooks/timecorr_higher_order_search.ipynb`

Figure 4 - 5. Run `notebooks/decode_levels.ipynb`

Figure 6. 
 1. Run `notebooks/neurosynth_analysis.ipynb` to generate the neurosynth decoding terms. 
 The notebook provides code to run to test the analysis with a subset of features, but to run the full analysis (commented out code),
 you'll want to scale up to a cluster.
 2. Run `notebooks/bos_for_plots.ipynb` to generate brain objects.
 3. Run `scripts/plot_largest_abs.py` to generate visbrain plots. 
 
Figure 9. Run `notebooks/kernels.ipynb`

Supp. Figure 1 - 4. Run `notebooks/decode_levels_kernels.ipynb`

Supp. Figure 5 - 8. 
 1. Run `notebooks/neurosynth_analysis.ipynb` to generate the neurosynth decoding terms. 
 The notebook provides code to run to test the analysis with a subset of features, but to run the full analysis (commented out code),
 you'll want to scale up to a cluster.
 2. Run `notebooks/bos_for_plots.ipynb` to generate brain objects.
 3. Run `scripts/plot_15.py` to generate visbrain plots. 

Supp. Figure 9. Run `notebooks/pca_features.ipynb`

To replicate the content of the data folder, run the following cluster scripts:

1. `pieman_cluster_param_search.py` - replicates the results in the folder `data/results/level_analysis_optimized_param_search`
2. `pieman_cluster_submit_order_up.py` - replicates the results in the folder `data/results/mean_corrs`
3. `higher_order_sims.py` - replicates the results in the folder `data/results/higher_order_sims_search`
