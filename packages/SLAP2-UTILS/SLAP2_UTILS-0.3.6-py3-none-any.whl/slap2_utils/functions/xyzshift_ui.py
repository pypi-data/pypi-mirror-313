import skimage as ski
import sys
import tifffile
import json
from ._phase_cross_correlation import phase_cross_correlation
def xyzshift_UI(path1,slice,image):
    
    slice = float(slice)
    imstack1 = tifffile.imread(path1)
    _data = tifffile.tiffcomment(path1)
    _stackInfo = json.loads(_data)
    store = tifffile.imread(path1, aszarr=True)

    zindexlist = _stackInfo['zsAbsolute']

    # See which one has the least error and shift from there
    besterror = 1000000000000000000000000000000
    bestindex = -100

    shift = []

    for i in range(len(imstack1[0])):
        #result = ski.registration.phase_cross_correlation(imstack1[0][i], image, upsample_factor=100, space='real', disambiguate=False,
             #                                        reference_mask=None, moving_mask=None,
              #                                       normalization=None)
        
        result = phase_cross_correlation(imstack1[0][i], image, upsample_factor=100, space='real', disambiguate=False,
                                                     reference_mask=None, moving_mask=None,
                                                     normalization=None)

        if result[1] < besterror:
            besterror = result[1]
            bestindex = i
            shift = result[0]
    z_change = zindexlist[bestindex] - slice
    print(z_change, shift[0], shift[1])

def main():
    # Loading bunch of stuff

    if len(sys.argv)<2:
        print('No path to tif file given')
        sys.exit(1)

    Path1 = sys.argv[1]

    Slice = sys.argv[2]

    I = sys.argv[3]

    image = tifffile.imread(I)



    xyzshift_UI(Path1,Slice,image)

if __name__ == "__main__":
    main()