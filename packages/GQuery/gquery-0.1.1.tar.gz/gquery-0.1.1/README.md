# Software for One-fit-all Transformer for Multimodal Geophysical Inversion: Method and Application
## Jiang Yiran<sup>1</sup>, Ma Jianwei<sup>2</sup>, Ning Jieyuan<sup>2</sup>, Li Jiaqi<sup>2</sup>, Wu Han<sup>3</sup>, Bao Tiezhao<sup>2</sup>
1 Harbin Institute of Technology, Harbin, China;

2 School of Earth and Space Sciences, Peking University, Beijing, China;

3 Institute of Geophysics, China Earthquake Administration, Beijing, China;

## Install
For linux
```bash
conda create -n G-Query python pytorch torchvision torchaudio pytorch-cuda keras==3.2.1 numpy scipy netCDF4 matplotlib -c pytorch -c nvidia
conda activate G-Query
pip install cython dispCal
pip install dist/gquery-0.1.0.tar.gz
```
for mac
```bash
conda create -n G-Query    numpy scipy netCDF4 matplotlib 
conda activate G-Query
pip install torch torchvision torchaudio keras==3.2.1 cython dispCal
pip install dist/gquery-0.1.0.tar.gz
```


## train and run
In the test directory
```bash
python train.py --job train --mN 10
```
use the run.ipynb to see the simple example of prediction

## test dataset
The test dataset is in test/tmp.mat

## inversion result
The inversion result is in test/USA.mat and test/huang.mat