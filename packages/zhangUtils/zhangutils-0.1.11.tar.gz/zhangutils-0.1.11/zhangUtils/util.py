__version__ = '0.1.6'

import torchvision
from torchvision import transforms
import torch
import numpy as np
from PIL import Image
from skimage import io
from skimage.metrics import structural_similarity
import torch.nn.functional as F
import os
import PIL.JpegImagePlugin

def show(img):

    if torch.is_tensor(img):
        img = transforms.ToPILImage()(img)
        img.show()
        return
    
    if type(img) == PIL.JpegImagePlugin.JpegImageFile:
        img.show()
        return
    
    if type(img) == Image.Image:
        img.show()
        return

    img = torch.from_numpy(img)
    img = transforms.ToPILImage()(img)
    img.show()

def shape(tensor):
    print(tensor.size())

def saveImage(img, img_name='test', img_path='./images'):
    #img 图片
    #img_name 仅需图片的名字，无需'.jpg'
    #img_path 图片存储路径
    if os.path.exists(img_path) == False:
        os.makedirs(img_path)

    if isinstance(img, np.ndarray):
        img = torch.from_numpy(img)
        img = transforms.ToPILImage()(img)
    
    if torch.is_tensor(img):
        torchvision.utils.save_image(img, os.path.join(img_path, img_name + '.jpg')) 
        return

    img.save(os.path.join(img_path, img_name + '.jpg'))

def readImage(imagePath, typeNumber=1):

    #typyNumber返回的照片参数
    #                       1:ndarry 2:tensor 3:PIL.Image
    img = io.imread(imagePath)

    if typeNumber == 1:
        return img

    if typeNumber == 2:
        return transforms.ToTensor()(img)
    
    # PIL Image
    if typeNumber == 3:
        return Image.open(imagePath).convert('RGB')
    

def ssim(cleanImagePath, dehazeImagePath):
    clean_image = transforms.ToTensor()(io.imread(cleanImagePath)) #转为tensor,并且将数据进行归一化
    dehaze_image = transforms.ToTensor()(io.imread(dehazeImagePath))
    ssim_val = structural_similarity(clean_image.permute(1, 2, 0).cpu().numpy(), dehaze_image.permute(1, 2, 0).numpy(), data_range=1, multichannel=True, channel_axis=-1)
    return ssim_val

def psnr(cleanImagePath, dehazeImagePath):
    clean_image = transforms.ToTensor()(io.imread(cleanImagePath))#转为tensor,并且将数据进行归一化
    dehaze_image = transforms.ToTensor()(io.imread(dehazeImagePath))
    psnr_val = 10 * torch.log10(1 / F.mse_loss(dehaze_image, clean_image))
    return psnr_val.item()

def evaluation(gtImagesPath, dehazeImagesPath):
    ssim_val = 0
    psnr_val = 0
    dehazeImagesName = os.listdir(dehazeImagesPath)
    for i in dehazeImagesName:
        gtImagePath = os.path.join(gtImagesPath, i)
        dehazeImagePath = os.path.join(dehazeImagesPath, i)
        ssim_val += ssim(gtImagePath, dehazeImagePath)
        psnr_val += psnr(gtImagePath, dehazeImagePath)

    ssim_val /= len(dehazeImagesName)
    psnr_val /= len(dehazeImagesName)

    return ssim_val, psnr_val
    



  