""" Augmentations Implemented as Callable Classes."""
import cv2
import numpy as np
import torch
import random
from typing import Dict

def apply_per_band(img, transform):
    """
    Helpful function to allow you to more easily implement
    transformations that are applied to each band separately.
    Not necessary to use, but can be helpful.
    """
    result = np.zeros_like(img)
    for band in range(img.shape[0]):
        transformed_band = transform(img[band].copy())
        result[band] = transformed_band

    return result

class Blur(object):
    """
        Blurs each band separately using cv2.blur

        Parameters:
            kernel: Size of the blurring kernel
            in both x and y dimensions, used
            as the input of cv.blur

        This operation is only done to the X input array.
    """
    def __init__(self, kernel=3):
        self.kernel = kernel

    def __call__(self, sample: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """
            Performs the blur transformation.

            Input:
                sample: Dict[str, np.ndarray]
                    Has two keys, 'X' and 'y'.
                    Each of them has shape (bands, width, height)

            Output:
                transformed: Dict[str, np.ndarray]
                    Has two keys, 'X' and 'y'.
                    Each of them has shape (bands, width, height)
        """
        
        # sample must have X and y in a dictionary format

        #  dimensions of img: (t, bands, tile_height, tile_width)
        transformed_X = apply_per_band(sample['X'], lambda x: cv2.blur(x, (self.kernel, self.kernel)))
        return {'X': transformed_X, 'y': sample['y']}

class AddNoise(object):
    """
        Adds random gaussian noise using np.random.normal.

        Parameters:
            mean: float
                Mean of the gaussian noise
            std_lim: float
                Maximum value of the standard deviation
    """
    def __init__(self, mean=0, std_lim=0.):
        self.mean = mean
        self.std_lim = std_lim

    def __call__(self, sample):
        """
            Performs the add noise transformation.
            A random standard deviation is first calculated using
            random.uniform to be between 0 and self.std_lim

            Random noise is then added to each pixel with
            mean self.mean and the standard deviation
            that was just calculated

            The resulting value is then clipped using
            numpy's clip function to be values between
            0 and 1.

            This operation is only done to the X array.

            Input:
                sample: Dict[str, np.ndarray]
                    Has two keys, 'X' and 'y'.
                    Each of them has shape (bands, width, height)

            Output:
                transformed: Dict[str, np.ndarray]
                    Has two keys, 'X' and 'y'.
                    Each of them has shape (bands, width, height)
        """
        
        std_dev = random.uniform(0, self.std_lim)
        noise = np.random.normal(self.mean, std_dev, size=sample['X'].shape)
        noisy_X = np.clip(sample['X'] + noise, 0, 1)
        return {'X': noisy_X, 'y': sample['y']}

class RandomVFlip(object):
    """
        Randomly flips all bands vertically in an image with probability p.

        Parameters:
            p: probability of flipping image.
    """
    def __init__(self, p=0.5):
        self.p = p

    def __call__(self, sample):
        """
            Performs the random flip transformation using cv.flip.

            Input:
                sample: Dict[str, np.ndarray]
                    Has two keys, 'X' and 'y'.
                    Each of them has shape (bands, width, height)

            Output:
                transformed: Dict[str, np.ndarray]
                    Has two keys, 'X' and 'y'.
                    Each of them has shape (bands, width, height)
        """

        X = sample['X']
        y = sample['y']

        if np.random.rand() < self.p:
            X = apply_per_band(X, lambda x: cv2.flip(x, 0))
            y = apply_per_band(y, lambda x: cv2.flip(x, 0))

        return {'X': X, 'y': y}
            
        

class RandomHFlip(object):
    """
        Randomly flips all bands horizontally in an image with probability p.

        Parameters:
            p: probability of flipping image.
    """
    def __init__(self, p=0.5):
        self.p = p

    def __call__(self, sample):
        """
            Performs the random flip transformation using cv.flip.

            Input:
                sample: Dict[str, np.ndarray]
                    Has two keys, 'X' and 'y'.
                    Each of them has shape (bands, width, height)

            Output:
                transformed: Dict[str, np.ndarray]
                    Has two keys, 'X' and 'y'.
                    Each of them has shape (bands, width, height)
        """
        X = sample['X']
        y = sample['y']

        if np.random.rand() < self.p:
            X = apply_per_band(X, lambda x: cv2.flip(x, 1))
            y = apply_per_band(y, lambda x: cv2.flip(x, 1))

        return {'X': X, 'y': y}
        

class ToTensor(object):
    """
        Converts numpy.array to torch.tensor
    """
    def __call__(self, sample):
        """
            Transforms all numpy arrays to tensors

            Input:
                sample: Dict[str, np.ndarray]
                    Has two keys, 'X' and 'y'.
                    Each of them has shape (bands, width, height)

            Output:
                transformed: Dict[str, torch.Tensor]
                    Has two keys, 'X' and 'y'.
                    Each of them has shape (bands, width, height)
        """
        return {'X': torch.tensor(sample['X']), 'y': torch.tensor(sample['y'])}
