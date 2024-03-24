import torch
import argparse
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision.utils import save_image as imwrite
import os
import time
import re
from torchvision import transforms
from test_dataset import dehaze_test_dataset
from model import final_net


parser = argparse.ArgumentParser(description='Shadow')
parser.add_argument('--test_dir', type=str, default='./ShadowDataset/test/')
parser.add_argument('--output_dir', type=str, default='results/')
parser.add_argument('-test_batch_size', help='Set the testing batch size', default=1, type=int)
args = parser.parse_args()
output_dir =args.output_dir
if not os.path.exists(output_dir + '/'):
    os.makedirs(output_dir + '/', exist_ok=True)
test_dir = args.test_dir
test_batch_size = args.test_batch_size

test_dataset = dehaze_test_dataset(test_dir)
test_loader = DataLoader(dataset=test_dataset, batch_size=test_batch_size, shuffle=False, num_workers=0)

device = 'cuda:0'
print(device)

model = final_net()

try:
    model.remove_model.load_state_dict(torch.load(os.path.join('weights', 'shadowremoval.pkl'), map_location='cpu'), strict=True)
    print('loading removal_model success')
except:
    print('loading removal_model error')


try:
    model.enhancement_model.load_state_dict(torch.load(os.path.join('weights', 'refinement.pkl'), map_location='cpu'), strict=True)
    print('loading enhancement model success')
except:
    print('loading enhancement model error')

model = model.to(device)

total_time = 0
with torch.no_grad():
    model.eval()

    start = time.time()
    for batch_idx, (input, name) in enumerate(test_loader):
        print(name[0])
        input = input.to(device)
        frame_out = model(input)
        frame_out = frame_out.to(device)
    
        name = re.findall("\d+",str(name))
        imwrite(frame_out, os.path.join(output_dir, str(name[0])+'.png'), range=(0, 1))













