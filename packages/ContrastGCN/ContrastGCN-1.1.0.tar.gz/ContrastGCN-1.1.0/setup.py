from setuptools import find_packages, setup

setup(
    name='ContrastGCN',
    version='1.1.0',
    description='ContrastGCN: An interpretable ensemble framework for automatic cell type annotation in single-cell chromatin accessibility data',
    long_description='ContrastGCN is an interpretable ensemble framework that integrates contrastive learning and Graph Convolutional Networks (GCN) to efficiently and automatically annotate cell types in scCAS data. Through extensive experiments across diverse datasets, ContrastGCN has demonstrated superior performance not only in accurately annotating known cell types but also in effectively identifying novel cell types absent in the training set. ContrastGCN also shows robustness across scCAS datasets with varying levels of imbalance and cell counts. Notably, ContrastGCN excels in cross-batch and cross-tissue annotations, indicating its broad applicability in scCAS data analysis. Moreover, comprehensive downstream analyses further reveal that ContrastGCN can deliver valuable cell-type-specific biological insights, thereby greatly enhancing our understanding of intricate biological mechanisms.',
    long_description_content_type='text/markdown',
    author='Yifan Huang',
    python_requires=">=3.10.10",
    packages=find_packages(),
    install_requires=[
        'scanpy>=1.9.1',
        'torch>=2.0.1',
        'torch_geometric>=2.5.2',
        'scikit-learn>=1.3.2',
        'scipy>=1.11.4',
    ],
)
