# This is calculation of shifts from 2 volumetric traces that are already recorded

import skimage as ski
import sys

# xyzshift is calculated based on phase_cross_correlation method in skimage
def xyzshift(path1,path2):

    # Read both image
    imstack1 = ski.io.imread(path1,plugin="tifffile")

    imstack2 = ski.io.imread(path2,plugin="tifffile")

    # Calculation of shifts are here
    x = ski.registration.phase_cross_correlation(imstack1[0], imstack2[0], upsample_factor=100, space='real', disambiguate=False,
                                            reference_mask=None, moving_mask=None,
                                            normalization=None)

    # The outputs are actually returned as print value in MATLAB
    print(x[0][0], x[0][1], x[0][2])
    return x[0]

def main():

    # Sanity check: whether enough arguments are prvided
    if len(sys.argv)<2:
        print('No path to tif file given')
        sys.exit(1)

    # Get path name from each input value
    Path1 = sys.argv[1]

    Path2 = sys.argv[2]

    # Calls xyzshift method
    xyzshift(Path1,Path2)

if __name__ == "__main__":
    main()
