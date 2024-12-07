import h5py
import numpy as np
from scipy import signal


def returnStimTime(stimFile, distance=250, hz=5000):
    """Return start and stop times of visual stimuli from a TTL trace.

    This function reads a TTL trace from an HDF5 file and identifies the start and stop times of visual stimuli 
    based on peaks in the trace.

    Parameters
    ----------
    stimFile : str
        Path to the HDF5 file containing the TTL trace.
    distance : int, optional
        Minimum number of samples between consecutive peaks. Default is 250.
    hz : int, optional
        Sampling rate of the TTL trace in Hertz. Default is 5000 Hz.

    Returns
    -------
    start : list of float
        List of start times of the visual stimuli in seconds.
    stop : list of float
        List of stop times of the visual stimuli in seconds.
    """
    stimLog = h5py.File(stimFile, 'r')
    TTL_Trace = stimLog['TTL'][:]
    peaks, _ = signal.find_peaks(np.diff(TTL_Trace), height=2.5, distance=distance)
    start = [peaks[i]*(1/hz) for i in range(0, len(peaks), 2)]
    stop = [peaks[i]*(1/hz) for i in range(1, len(peaks), 2)]
    return start, stop
