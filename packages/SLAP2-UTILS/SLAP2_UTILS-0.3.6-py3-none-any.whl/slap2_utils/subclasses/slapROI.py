class slapROI(): 

    """
        A class used to store information related to region of interests.
    
        Attributes
        ----------
        constructor : str
            The constructor of the ROI.
        roiType : str
            The type of ROI in question (rectangle vs arbitary ROI).
        imageMode : str
            A string that represent how the ROI is imaged (raster vs integrated).
        targetRate : int
            The target sample rate that the user inputted (default is 2 kHz).
        shapeData : list
            A list that represent the shape of the ROI.
        z : int
            An integer that represent the z layer of the ROI in question.
        
    
        Descriptions for methods:
        --------------------------
               
                
        Methods
        ---------
        __init__() :
            Initialize all of the fields with values, which takes an input of h5file (a file that is created after recording) and a reference to the ROI in question.
    
        Return
        -------
            Self with populated fields.
    
        """
    
    def __init__(self, h5file, roiRef):
        
        self.constructor = None
        self.roiType = None
        self.imageMode = None
        self.targetRate = None
        self.shapeData = None
        self.z = None
        
        self.constructor = ''.join([chr(_char[0]) for _char in h5file[roiRef]['constructor']])
        if 'Rectangle' in self.constructor:
            self.roiType = 'RectangleRoi'
        else:
            self.roiType = 'ArbitraryRoi'
        
        self.shapeData = h5file[roiRef]['shapeData'][:].copy()
        if h5file[roiRef]['imagingMode']['ClassName'][0][0] == 1:
            self.imageMode = "Raster"
        else:
            self.imageMode = 'Integrate'
        self.targetRate = h5file[roiRef]['targetRate'][0][0]
        self.z = h5file[roiRef]['z'][0][0]
