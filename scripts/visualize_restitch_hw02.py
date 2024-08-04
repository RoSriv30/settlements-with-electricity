import pyprojroot
import sys
root = pyprojroot.here()
sys.path.append(str(root))
from src.preprocessing.subtile_esd_hw02 import restitch
from pathlib import Path
import numpy as np


def main():
    import pyprojroot
    root = pyprojroot.here()
    import matplotlib.pyplot as plt
    sys.path.append(root)
    print(f'Added {root} to path.')
    
    # run this code only after you have already created the subtiles in the directory "data/processed/Train/subtiles"
    stitched_sentinel2 = restitch(Path(root/"data/processed/Train1x1/subtiles"), "sentinel2", "Tile1", (0,4), (0,4))
    print(len(stitched_sentinel2[0]))
    plt.imshow(np.dstack([stitched_sentinel2[0][0,3,:,:], stitched_sentinel2[0][0,2,:,:], stitched_sentinel2[0][0,1,:,:]]))
    plt.show()

if __name__ == "__main__":
    main()