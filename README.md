# Shadow_R

# Dehazing_R

This is the official PyTorch implementation of our dehazing method for NTIRE 2024 Image Shadow Removal Challenge --- Fidelity Track & Perceptual Track

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
Download [our saved model for NTIRE 2024 Image Shadow Removal Challenge --- Fidelity Track & Perceptual Track]([https://drive.google.com/file/d/17cV2VeKXp2dFfMaTwdWTdfKqWQUs7g8f/view?usp=drive_link](https://drive.google.com/file/d/1ntXl9vGVOFGel1-Pu1vbbWidOU3QH-IM/view?usp=sharing)) and unzip it into the folder ./weights to reproduce our test result.

# How to reproduce our test result
Download above saved models

Run test.py and find results in the folder ./results. 

Please note new generated results may have subtle varations with [our submitted test results](https://drive.google.com/file/d/1kuHr5r29cZufNQcFfNza1qbINRnnMBQM/view?usp=sharing) due to the device difference, please feel free to choose our submitted results or your generated images for user study.






