import h5py
from .slapROI import slapROI

class AcquisitionContainer():
    """
        A class used to load a SLAP2 binary metadatafile for data processing. This is also an attribute for the datafile object

        Attributes
        ----------
        AcquisitionPlan : dict
            A dictionary that contains 3 subinstances of ['AcquisitionContainer'], ['ParsePlan'], and ['acqParsePlan'].
        DmdPatternSequence : list
            A list containing information related to the patterning of the sequences.
        ParsePlan : dict
            A dictionary that contains various instances related to how region of interest is parsed through.
        ROIs : list
            A list that contains information related to the region of interests.
        ScannerParameters : dict
            A dictionary that stores information related to the scanned parameter (not implemented yet, consider removing).
        constructor : str
            A string that describes how the plan is constructed.
            
            
        Descriptions for methods:
        --------------------------

        Methods
        ----------
        __init__() :
            Fill the fields mentioned above.

        Return
        -------
            Self with populated fields. 
                
    """
    
    def __init__(self, metadatafile):
        self.AcquisitionPlan = None
        self.DmdPatternSequence = None
        self.ParsePlan = {}
        self.ROIs = []
        self.ScannerParameters = ''
        self.constructor = ''


        acqParsePlan = {}
        with h5py.File(metadatafile, 'r') as hdf_file:
            # Read the contents of the HDF5 file into the metaData dictionary

            self.AcquisitionPlan = hdf_file['AcquisitionContainer']['AcquisitionPlan'][:]
            self.DmdPatternSequence = hdf_file['AcquisitionContainer']['DmdPatternSequence'][:]

            for i in range(hdf_file['AcquisitionContainer']['ROIs']['rois'][:].shape[0]):
                roi_ref = hdf_file['AcquisitionContainer']['ROIs']['rois'][i][0]
                self.ROIs.append(slapROI(hdf_file, roi_ref))
                
                
            for _key in hdf_file['AcquisitionContainer']['ParsePlan'].keys():
                try:
                    self.ParsePlan[_key] = hdf_file['AcquisitionContainer']['ParsePlan'][_key][:]
                except:
                    if _key == 'acqParsePlan':
                        _data = {}
                        for _subkey in hdf_file['AcquisitionContainer']['ParsePlan']['acqParsePlan'].keys():
                            _data[_subkey] = []
                            for _ref in (list(hdf_file['AcquisitionContainer']['ParsePlan']['acqParsePlan'][_subkey][:])):
                                _data[_subkey].append(hdf_file[_ref[0]][:])
                            acqParsePlan[_key] = _data

            
            _refs = []
            for index in range(len(hdf_file['AcquisitionContainer']['ParsePlan']['pixelReplacementMaps'][:])):
                _refs.append(hdf_file['AcquisitionContainer']['ParsePlan']['pixelReplacementMaps'][:][index][0])
            self.ParsePlan['pixelReplacementMaps'] = [hdf_file[_ref][:] for _ref in _refs]
            self.ParsePlan['acqParsePlan'] = acqParsePlan['acqParsePlan']
