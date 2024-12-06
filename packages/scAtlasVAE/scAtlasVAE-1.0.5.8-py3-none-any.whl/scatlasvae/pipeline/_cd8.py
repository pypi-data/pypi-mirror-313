import scanpy as sc
import pandas as pd
import numpy as np
import torch
from ..model import scAtlasVAE
from ..tools import umap_alignment

def run_transfer_cd8(
    adata_reference: sc.AnnData,
    adata_query: sc.AnnData,
    state_dict_path: str,
    label_key: str = 'cell_type',
    device = 'cpu'
):
    state_dict = torch.load(state_dict_path, map_location=device)
    # compatible with scatlasvae version 0.0.1
    if 'new_adata_key' in state_dict['model_config']:
        state_dict['model_config']['unlabel_key'] = state_dict['model_config'].pop('new_adata_key')

    adata_query.obs[label_key] = 'undefined'

    adata_query.obs[label_key] = pd.Categorical(
        list(adata_query.obs[label_key]),
        categories=pd.Categorical(adata_reference.obs[label_key]).categories
    )

    vae_model_transfer = scAtlasVAE(
      adata=adata_query,
       pretrained_state_dict=state_dict['model_state_dict'],
       device=device,
       **state_dict['model_config']
    )
    adata_query.obsm['X_gex'] = vae_model_transfer.get_latent_embedding()
    adata_query.obsm['X_umap'] = umap_alignment(
        adata_reference.obsm['X_gex'],
        adata_reference.obsm['X_umap'],
        adata_query.obsm['X_gex'],
        method='knn',
        n_neighbors=3
    )['embedding']
    df = vae_model_transfer.predict_labels(return_pandas=True)
    adata_query.obs[label_key] = list(df[label_key])

    return adata_query  