#%%
"""
Reference:
[1] Synthcity: facilitating innovative use cases of synthetic data in different data modalities
- https://github.com/vanderschaarlab/synthcity/blob/main/src/synthcity/metrics/eval_statistical.py
"""
#%%
import numpy as np
from tqdm import tqdm
import torch

from scipy.stats import entropy, ks_2samp
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.neighbors import NearestNeighbors

from . import utility
#%%
def KLDivergence(train, syndata, continuous_features):
    """
    Marginal statistical fidelity: KL-Divergence
    : lower is better
    """
    
    ### square-root choice
    n = len(train)
    num_bins = int(np.ceil(np.sqrt(n)))
    
    # get distribution of continuous variables
    cont_freqs = utility.get_frequency(
        train[continuous_features], 
        syndata[continuous_features], 
        n_histogram_bins=num_bins
    )
    
    result = [] 
    for col in train.columns:
        if col in continuous_features:
            gt, syn = cont_freqs[col]
            kl_div = entropy(syn, gt)
        else:
            pmf_p = train[col].value_counts(normalize=True)
            pmf_q = syndata[col].value_counts(normalize=True)
            
            # Ensure that both PMFs cover the same set of categories
            all_categories = pmf_p.index.union(pmf_q.index)
            pmf_p = pmf_p.reindex(all_categories, fill_value=0)
            pmf_q = pmf_q.reindex(all_categories, fill_value=0)
            
            # Avoid division by zero and log(0) by filtering out zero probabilities
            non_zero_mask = (pmf_p > 0) & (pmf_q > 0)
            
            kl_div = np.sum(pmf_q[non_zero_mask] * np.log(pmf_q[non_zero_mask] / pmf_p[non_zero_mask]))
        result.append(kl_div)
    return np.mean(result)
#%%
def GoodnessOfFit(train, syndata, continuous_features):
    """
    Marginal statistical fidelity: Kolmogorov-Smirnov test & Chi-Squared test
    : lower is better
    """
    
    result = [] 
    for col in train.columns:
        if col in continuous_features:
            # Compute the Kolmogorov-Smirnov test for goodness of fit.
            statistic, _ = ks_2samp(train[col], syndata[col])
        else:
            pmf_p = train[col].value_counts(normalize=True) # expected
            pmf_q = syndata[col].value_counts(normalize=True) # observed
            
            # Ensure that both PMFs cover the same set of categories
            all_categories = pmf_p.index.union(pmf_q.index)
            pmf_p = pmf_p.reindex(all_categories, fill_value=0)
            pmf_q = pmf_q.reindex(all_categories, fill_value=0)
            
            # Avoid division by zero and log(0) by filtering out zero probabilities
            non_zero_mask = pmf_p > 0
            
            # Compute the Chi-Squared test for goodness of fit.
            statistic = ((pmf_q[non_zero_mask] - pmf_p[non_zero_mask]) ** 2 / pmf_p[non_zero_mask]).sum()
        result.append(statistic)
    return np.mean(result)
#%%
def MaximumMeanDiscrepancy(train, syndata, continuous_features, categorical_features):
    """
    Joint statistical fidelity: Maximum Mean Discrepancy (MMD)
    : lower is better
    
    - MMD using RBF (gaussian) kernel (i.e., k(x,y) = exp(-gamma * ||x-y||^2 / 2))
    """
    
    ### pre-processing
    train_ = train.copy()
    syndata_ = syndata.copy()
    # continuous: min-max scaling
    scaler = MinMaxScaler().fit(train_[continuous_features])
    train_[continuous_features] = scaler.transform(train_[continuous_features])
    syndata_[continuous_features] = scaler.transform(syndata_[continuous_features])
    # categorical: one-hot encoding
    scaler = OneHotEncoder(handle_unknown='ignore').fit(train_[categorical_features])
    train_ = np.concatenate([
        train_[continuous_features].values,
        scaler.transform(train_[categorical_features]).toarray()
    ], axis=1)
    syndata_ = np.concatenate([
        syndata_[continuous_features].values,
        scaler.transform(syndata_[categorical_features]).toarray()
    ], axis=1)
    
    XX = metrics.pairwise.rbf_kernel(
        train_.reshape(len(train_), -1),
        train_.reshape(len(train_), -1),
    )
    YY = metrics.pairwise.rbf_kernel(
        syndata_.reshape(len(syndata_), -1),
        syndata_.reshape(len(syndata_), -1),
    )
    XY = metrics.pairwise.rbf_kernel(
        train_.reshape(len(train_), -1),
        syndata_.reshape(len(syndata_), -1),
    )
    MMD = XX.mean() + YY.mean() - 2 * XY.mean() # squared MMD
    return np.sqrt(MMD)
#%%
def phi(s, D):
    return (1 + (4 * s) / (2 * D - 3)) ** (-1 / 2)

def cramer_wold_distance_function(x_batch, x_gen):
    gamma_ = (4 / (3 * x_batch.size(0))) ** (2 / 5)
    
    cw1 = torch.cdist(x_batch, x_batch) ** 2 
    cw2 = torch.cdist(x_gen, x_gen) ** 2 
    cw3 = torch.cdist(x_batch, x_gen) ** 2 
    cw_x = phi(cw1 / (4 * gamma_), D=x_batch.size(1)).sum()
    cw_x += phi(cw2 / (4 * gamma_), D=x_batch.size(1)).sum()
    cw_x += -2 * phi(cw3 / (4 * gamma_), D=x_batch.size(1)).sum()
    cw_x /= (2 * x_batch.size(0) ** 2 * torch.tensor(torch.pi * gamma_).sqrt())
    return cw_x

def CramerWoldDistance(train, syndata, continuous_features, categorical_features, device):
    """
    Joint statistical fidelity: Cramer-Wold Distance
    : lower is better
    """
    
    ### pre-processing
    train_ = train.copy()
    syndata_ = syndata.copy()
    # continuous: min-max scaling
    scaler = MinMaxScaler().fit(train_[continuous_features])
    train_[continuous_features] = scaler.transform(train_[continuous_features])
    syndata_[continuous_features] = scaler.transform(syndata_[continuous_features])
    # categorical: one-hot encoding
    scaler = OneHotEncoder(handle_unknown='ignore').fit(train_[categorical_features])
    train_ = np.concatenate([
        train_[continuous_features].values,
        scaler.transform(train_[categorical_features]).toarray()
    ], axis=1)
    syndata_ = np.concatenate([
        syndata_[continuous_features].values,
        scaler.transform(syndata_[categorical_features]).toarray()
    ], axis=1)
    train_ = torch.tensor(train_).to(device)
    syndata_ = torch.tensor(syndata_).to(device)
    
    if len(train_) > 10000: # large dataset case
        CWs = []
        for _ in tqdm(range(10), desc="Batch Cramer-Wold Distance..."):
            idx = np.random.choice(range(len(train_)), 2000, replace=False)
            train_small = train_[idx, :]
            syndata_small = syndata_[idx, :]
            cw = cramer_wold_distance_function(train_small, syndata_small)
            CWs.append(cw.cpu().numpy().item())
        cw = np.mean(CWs)
    else:
        cw = cramer_wold_distance_function(train_, syndata_)
        cw = cw.cpu().numpy().item()
    return np.sqrt(cw) # square-root distance
#%%
def naive_alpha_precision_beta_recall(train, syndata, continuous_features, categorical_features):
    """
    Reference:
    - https://github.com/vanderschaarlab/synthcity/blob/main/src/synthcity/metrics/eval_statistical.py
    """
    ### pre-processing
    train_ = train.copy()
    syndata_ = syndata.copy()
    # continuous: min-max scaling
    scaler = MinMaxScaler().fit(train_[continuous_features])
    train_[continuous_features] = scaler.transform(train_[continuous_features])
    syndata_[continuous_features] = scaler.transform(syndata_[continuous_features])
    # categorical: one-hot encoding
    scaler = OneHotEncoder(handle_unknown='ignore').fit(train_[categorical_features])
    train_ = np.concatenate([
        train_[continuous_features].values,
        scaler.transform(train_[categorical_features]).toarray()
    ], axis=1)
    syndata_ = np.concatenate([
        syndata_[continuous_features].values,
        scaler.transform(syndata_[categorical_features]).toarray()
    ], axis=1)
    
    n_steps = 30
    alphas = np.linspace(0, 1, n_steps) 
    
    emb_center = np.mean(train_, axis=0) # true embedding center
    synth_center = np.mean(syndata_, axis=0) # synthetic embedding center
    
    # L2 distance from true to embedding center
    dist = np.sqrt(((train_ - emb_center) ** 2).sum(axis=1)) 
    # Ball with quantiles of radii 
    # = approximation of the subset that supports a probability mass of alpha
    Radii = np.quantile(dist, alphas) 
    
    # L2 distance from synthetic to embedding center
    synth_to_center = np.sqrt(((syndata_ - emb_center) ** 2).sum(axis=1))
    
    nbrs_real = NearestNeighbors(n_neighbors=2, n_jobs=-1, p=2).fit(train_)
    real_to_real, _ = nbrs_real.kneighbors(train_) # distance to neighbors

    nbrs_synth = NearestNeighbors(n_neighbors=1, n_jobs=-1, p=2).fit(syndata_)
    # (distance to neighbors, indices of closest synthetic data point to real data)
    real_to_synth, real_to_synth_args = nbrs_synth.kneighbors(train_) 
    
    # Let us find closest real point to any real point, excluding itself (therefore, 1 instead of 0)
    real_to_real = real_to_real[:, 1].squeeze()
    real_to_synth = real_to_synth.squeeze()
    real_to_synth_args = real_to_synth_args.squeeze()
    
    # closest synthetic data points
    # = approximation of true data points using synthetic data points
    real_synth_closest = syndata_[real_to_synth_args] 
    real_synth_closest_d = np.sqrt(((real_synth_closest - synth_center) ** 2).sum(axis=1)) 
    # Ball with quantiles of Radii
    # = approximation of the subset that supports a probability mass of beta
    closest_synth_Radii = np.quantile(real_synth_closest_d, alphas)
    
    alpha_precision_curve = []
    beta_recall_curve = []
    for k in range(len(Radii)):
        alpha_precision = np.mean(
            synth_to_center <= Radii[k]
        )
        beta_recall = np.mean(
            (real_synth_closest_d <= closest_synth_Radii[k]) * (real_to_synth <= real_to_real)
        )
        alpha_precision_curve.append(alpha_precision)
        beta_recall_curve.append(beta_recall)
    
    # Riemann integral
    delta_precision_alpha = 1 - 2 * np.abs(alphas - np.array(alpha_precision_curve)).sum() * (alphas[1] - alphas[0])
    delta_beta_recall = 1 - 2 * np.abs(alphas - np.array(beta_recall_curve)).sum() * (alphas[1] - alphas[0])
    return delta_precision_alpha, delta_beta_recall
#%%