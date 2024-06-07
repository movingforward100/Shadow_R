&nbsp;

<div align="center">
<p align="center"> <img src="figure/logo.png" width="200px"> </p>


[![arXiv](https://img.shields.io/badge/arxiv-paper-179bd3)](https://arxiv.org/abs/2303.06705)
[![NTIRE](https://img.shields.io/badge/NTIRE_Perceptual_2024-leaderboard-179bd3)](https://codalab.lisn.upsaclay.fr/competitions/17546#results)
[![NTIRE](https://img.shields.io/badge/NTIRE_Fidelity_2024-leaderboard-179bd3)](https://codalab.lisn.upsaclay.fr/competitions/17640#results)





# ShadowR-R

This is the official PyTorch implementation of our solution for NTIRE 2024 Image Shadow Removal Challenge --- Fidelity Track & Perceptual Track

# Environment:

CUDA Version: 11.0

Python 3.8

# Dependencies:

torch==1.10.0

torchvision==0.9.0

pytorch_lightning=2.0.0

timm=0.6.12

opencv-python 

kornia

einops



# Our saved Model
Download [our saved model for NTIRE 2024 Image Shadow Removal Challenge --- Fidelity Track & Perceptual Track](https://drive.google.com/file/d/1ntXl9vGVOFGel1-Pu1vbbWidOU3QH-IM/view?usp=sharing) and unzip it into the folder ./weights to reproduce our test result.

# How to reproduce our test result
Download above saved models

Run test.py and find results in the folder ./results. Please note the weight path in Line 34 and Line 41 of test.py.

If you have any problems in reproducing our result, please contact wdong1745376@gmail.com as soon as possible.






