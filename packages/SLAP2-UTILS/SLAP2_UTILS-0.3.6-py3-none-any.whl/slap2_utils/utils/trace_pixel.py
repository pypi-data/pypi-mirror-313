import numpy as np
import re
import trace

class TracePixel:
    """
    A class used to represent and manipulate a single trace pixel from a SLAP2 data file.

    Attributes
    ----------
    fileName : str
        The name of the file to be loaded.
    superPixelId : int
        The identifier for the superpixel.
    superPixelNumPixels : int
        The number of pixels in the superpixel.
    superPixelNumPixelsSelected : int
        The number of selected pixels in the superpixel.
    byteOffsets : list
        A list of byte offsets for data extraction.
    lineIdxs : list
        A list of line indices for data extraction.
    data : list
        The loaded data for the trace pixel.
    isLoaded : bool
        A flag indicating whether the data is loaded.
    firstCycleOffsetBytes : int
        The offset for the first cycle in bytes.
    numCycles : int
        The number of cycles.
    bytesPerCycle : int
        The number of bytes per cycle.
    linesPerCycle : int
        The number of lines per cycle.
    y : int
        An unspecified variable, initialized to -1.
    

    Descriptions for methods:
    ----------
           
            
    Methods
    ---------
    __init__() :
        Initialize the fields with values.

    Return
    -------
        Self with populated fields.

    Methods
    ---------
    load(hMemmap=None) :
        Loads the data for the trace pixel from the specified memory-mapped file, which is given as an input (hMemmap).

    Return
    -------
        Self with edited data field and isLoaded changed to true.
    
    """


    def __init__(self):
        self.fileName = ""  # Name of the file to be loaded
        self.superPixelId = 0  # Identifier for the superpixel
        self.superPixelNumPixels = 0  # Number of pixels in the superpixel
        self.superPixelNumPixelsSelected = 0  # Number of selected pixels in the superpixel
        self.byteOffsets = []  # List of byte offsets for data extraction
        self.lineIdxs = []  # List of line indices for data extraction
        self.data = None  # Loaded data
        self.isLoaded = False  # Flag indicating whether data is loaded
        self.firstCycleOffsetBytes = 0  # Offset for the first cycle in bytes
        self.numCycles = 0  # Number of cycles
        self.bytesPerCycle = 0  # Number of bytes per cycle
        self.linesPerCycle = 0  # Number of lines per cycle
        self.y = -1  # Unspecified variable, initialized to -1

    def load(self, hMemmap=None):
        """
        Loads the data for the trace pixel from the specified memory-mapped file.

        Parameters
        ----------
        hMemmap : np.memmap, optional
            An optional memory-mapped file object. If provided, this object will be used to load the data.
            If not provided, a new memory-mapped file object will be created based on the fileName attribute.

        Returns
        -------
        None
        """
        # Check if data is already loaded
        allLoaded = self.isLoaded
        if allLoaded:
            return

        loadedFilename = ""  # Initialize loaded filename

        if hMemmap is not None:
            # If a memory map object is provided, get its filename and set the format
            loadedFilename = hMemmap.Filename
            hMemmap.Format = 'int16'

        # Update filename to change the extension from .meta to .dat
        fileName_ = self.fileName
        fileName_ = re.sub(r'\.meta$', '.dat', fileName_, flags=re.IGNORECASE)

        if loadedFilename != fileName_:
            # Create a new memory map if the filename does not match
            hMemmap = np.memmap(fileName_, dtype='int16', mode='r')
            loadedFilename = fileName_

        # Calculate byte offsets for each cycle
        cycleIdxs = np.arange(0, self.numCycles, dtype=np.uint64)
        cycleByteOffsets = self.firstCycleOffsetBytes + cycleIdxs * self.bytesPerCycle

        # Convert byte offsets to sample offsets (assuming 2 bytes per sample)
        cycleSampleOffsets = [int(x // 2) for x in cycleByteOffsets]
        sampleOffsets = [int(x // 2) for x in self.byteOffsets]

        # Create a 2D array of sample offsets
        _sampleOffsets = np.zeros((len(self.byteOffsets), len(cycleSampleOffsets)), dtype='uint64')
        for i in range(len(self.byteOffsets)):
            _sampleOffsets[i, :] = sampleOffsets[i] + np.array(cycleSampleOffsets)
        
        sampleOffsets = _sampleOffsets
        sampleOffsets = sampleOffsets.astype('int64')  # Ensure offsets are in int64 format

        # Ensure the offsets do not exceed the length of the memory-mapped file
        if (sampleOffsets[0, :][len(sampleOffsets[0, :]) - 1]) > len(hMemmap):
            sampleOffsets[0, :][len(sampleOffsets[0, :]) - 1] = len(hMemmap)

        data_ = []  # List to store the loaded data
        # Extract data from the memory-mapped file using the calculated offsets
        for i in range(sampleOffsets.shape[0]):
            data_.append(np.take(hMemmap, (sampleOffsets[i, :] - 1), 0))
        
        self.data = data_  # Assign the loaded data to the class attribute
        self.isLoaded = True  # Mark data as loaded



