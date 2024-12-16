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
import torch.nn.functional as F
from PIL import Image
import numpy as np

def process_chunk(model, chunk, device):
    with torch.no_grad():
        chunk = chunk.to(device)
        return model(chunk)

def split_image(img_tensor, window_size=512, overlap=64):
    """Split image into overlapping chunks."""
    _, _, h, w = img_tensor.shape
    chunks = []
    positions = []
    
    for y in range(0, h, window_size - overlap):
        for x in range(0, w, window_size - overlap):
            # Calculate chunk boundaries
            y1 = y
            x1 = x
            y2 = min(y + window_size, h)
            x2 = min(x + window_size, w)
            
            # Extract chunk
            chunk = img_tensor[:, :, y1:y2, x1:x2]
            
            # Pad if necessary to maintain consistent size
            if chunk.shape[2] < window_size or chunk.shape[3] < window_size:
                ph = window_size - chunk.shape[2]
                pw = window_size - chunk.shape[3]
                chunk = F.pad(chunk, (0, pw, 0, ph))
            
            chunks.append(chunk)
            positions.append((y1, y2, x1, x2))
    
    return chunks, positions

def merge_chunks(chunks, positions, original_size, window_size=512, overlap=64):
    """Merge overlapping chunks with linear blending."""
    h, w = original_size
    result = torch.zeros((1, 3, h, w), device=chunks[0].device)
    weights = torch.zeros((1, 3, h, w), device=chunks[0].device)
    
    for chunk, (y1, y2, x1, x2) in zip(chunks, positions):
        # Calculate actual chunk size (might be smaller at edges)
        chunk_h = y2 - y1
        chunk_w = x2 - x1
        
        # Extract the valid portion of the chunk (without padding)
        valid_chunk = chunk[:, :, :chunk_h, :chunk_w]
        
        # Create weight mask
        weight = torch.ones_like(valid_chunk)
        
        # Apply linear blending in overlap regions
        if overlap > 0:
            for i in range(overlap):
                weight_value = i / overlap
                # Blend left edge if not at image boundary
                if x1 > 0 and i < chunk_w:
                    weight[:, :, :, i] *= weight_value
                # Blend right edge if not at image boundary
                if x2 < w and chunk_w - i - 1 >= 0:
                    weight[:, :, :, -(i + 1)] *= weight_value
                # Blend top edge if not at image boundary
                if y1 > 0 and i < chunk_h:
                    weight[:, :, i, :] *= weight_value
                # Blend bottom edge if not at image boundary
                if y2 < h and chunk_h - i - 1 >= 0:
                    weight[:, :, -(i + 1), :] *= weight_value
        
        result[:, :, y1:y2, x1:x2] += valid_chunk * weight
        weights[:, :, y1:y2, x1:x2] += weight
    
    # Normalize by weights to complete blending
    valid_mask = weights > 0
    result[valid_mask] = result[valid_mask] / weights[valid_mask]
    
    return result



def main():
    parser = argparse.ArgumentParser(description='Shadow')
    parser.add_argument('--input_dir', type=str, default='/ShadowDataset/test/')
    parser.add_argument('--output_dir', type=str, default='output/')
    parser.add_argument('--chunk_size', type=int, default=512, help='Size of sliding window')
    parser.add_argument('--overlap', type=int, default=64, help='Overlap between windows')
    args = parser.parse_args()

     # Ensure paths end with slash
    args.input_dir = os.path.join(args.input_dir, '')
    args.output_dir = os.path.join(args.output_dir, '')
    print('')
    print(f'input_dir: {args.input_dir}')
    print(f'output_dir: {args.output_dir}')
    print(f'chunk size: {args.chunk_size}. If algorithm is stuck, reduce chunk size to fit inside VRAM.')
    print('')
    
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir, exist_ok=True)
    
    test_dataset = dehaze_test_dataset(args.input_dir)
    test_loader = DataLoader(dataset=test_dataset, batch_size=1, shuffle=False, num_workers=0)
    
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    
    model = final_net()
    
    try:
        model.remove_model.load_state_dict(torch.load(os.path.join('weights', 'shadowremoval.pkl'), map_location='cpu'), strict=True)
        print('Loading removal_model success')
    except:
        print('Loading removal_model error')
        return

    try:
        model.enhancement_model.load_state_dict(torch.load(os.path.join('weights', 'refinement.pkl'), map_location='cpu'), strict=True)
        print('Loading enhancement model success')
    except:
        print('Loading enhancement model error')
        return

    model = model.to(device)
    model.eval()
    
    total_time = 0
    with torch.no_grad():
        for batch_idx, (input_img, name) in enumerate(test_loader):
            print(f"Processing {name[0]}")
            
            # Get image dimensions
            _, _, h, w = input_img.shape
            print(f"Image size: {w}x{h}")
            
            # Split image into chunks
            chunks, positions = split_image(input_img, args.chunk_size, args.overlap)
            print(f"Split into {len(chunks)} chunks")
            
            # Process each chunk
            processed_chunks = []
            for i, chunk in enumerate(chunks):
                print(f"Processing chunk {i+1}/{len(chunks)}")
                processed_chunk = process_chunk(model, chunk, device)
                processed_chunks.append(processed_chunk)
                torch.cuda.empty_cache()  # Clear GPU memory after each chunk
            
            # Merge chunks
            result = merge_chunks(processed_chunks, positions, (h, w), args.chunk_size, args.overlap)
            
            # Save result
            name = re.findall(r"\d+", str(name))
            save_path = os.path.join(args.output_dir, f"{name[0]}.png")
            print(f"Saving result to {save_path}")
            imwrite(result, save_path, range=(0, 1))
            
            torch.cuda.empty_cache()

if __name__ == '__main__':
    main()
