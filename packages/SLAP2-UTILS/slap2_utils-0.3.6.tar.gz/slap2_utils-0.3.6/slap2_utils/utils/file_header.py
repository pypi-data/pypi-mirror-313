# Utility functions for the Slap2DataFile
def load_file_header_v2(obj, rawUint32):
    """
        A function that does several sanity checks to the integrity and validity of the file. It also translates the raw data that are inputted as raw uint32 array.

        Return
        -------
            Translated header and number of cycles (num_cycles)    

    """
    # Data format:
    # uint32_t magic_start          = MAGIC_NUMBER;
    # uint32_t file_version         = 1;
    # uint32_t fileHeaderSize_Bytes = XXXX;
    #
    # uint32_t fieldId  = XXXX;
    # uint32_t fieldVal = XXXX;
    # uint32_t fieldId  = XXXX;
    # uint32_t fieldVal = XXXX;
    #
    # ...
    #
    # uint32_t magic_end           = MAGIC_NUMBER;

    
    file_magic_number = rawUint32[0]
    assert file_magic_number == obj.MAGIC_NUMBER, 'Data format error.'

    file_format_version = rawUint32[1]
    assert file_format_version == 2, 'Unknown format version'

    file_header_size_bytes = rawUint32[2]
    file_header_entries = file_header_size_bytes // 4

    
    header_end_magic_number = rawUint32[int(file_header_entries)-1]
    assert header_end_magic_number == obj.MAGIC_NUMBER, 'Data corruption in file header.'

    field_value_pairs = rawUint32[3:file_header_entries - 1]
    field_value_pairs = field_value_pairs.reshape(-1, 2)

    header_ = translate_field_value_pairs(field_value_pairs)
    header_ = translate_channel_mask(header_)
    header_ = translate_reference_timestamp(header_)
    header_['file_version'] = file_format_version
    header_['magic_start'] = file_magic_number
    header_['magic_end'] = header_end_magic_number
    header = header_

    file_size_bytes = len(rawUint32) * 4
    num_cycles = int((file_size_bytes - header_['firstCycleOffsetBytes']) / header_['bytesPerCycle'])
    
    total_num_lines = num_cycles * header['linesPerCycle']
    num_channels = float(header['numChannels'])
    return header, num_cycles

def translate_field_value_pairs(field_value_pairs):
    """
        A function that maps field IDs to names. The input is field value pairs, which are to be translated into a dictionary format.
        Parameters
        ----------
        field_value_pairs : numpy array 
        pairs of field names and values from the file header
        
        Return
        -------
            Dictionary that contains the field value pairs

    """
    file_header_fields = [
        "firstCycleOffsetBytes",
        "lineHeaderSizeBytes",
        "laserPathIdx",
        "bytesPerCycle",
        "linesPerCycle",
        "superPixelsPerCycle",
        "dmdPixelsPerRow",
        "dmdPixelsPerColumn",
        "numChannels",
        "channelMask",
        "numSlices",
        "channelsInterleave",
        "fpgaSystemClock_Hz",
        "referenceTimestamp_lower",
        "referenceTimestamp_upper"
    ]

    map = {i: field for i, field in enumerate(file_header_fields)}

    struct_out = {}
    for idx in range(field_value_pairs.shape[0]):
        field = field_value_pairs[idx, 0]
        value = field_value_pairs[idx, 1]

        if field in map:
            field = map[field]
            struct_out[field] = float(value)
        else:
            print(f'Warning: Unknown field/value pair in header: fieldID={field} value={value}')

    return struct_out

def translate_channel_mask(header):
    """
        A function that translates the channel mask from the header as the input. It then has various checks that validate the number of channels specified.
        Parameters
        ----------
        header : memap 
        Header of SLAP2 binary file read as Uint32
        
        Return
        -------
            It returns the header itself if it indeed passed all checks.

    """
    assert 'channelMask' in header
    channels = [bit for bit in range(32) if (int(header['channelMask']) & (1 << bit)) != 0]
    header['channels'] = channels
    assert 'numChannels' in header
    assert len(channels) == header['numChannels'], 'Data integrity error: header field ''numChannels'' does not agree with header field ''channelMask'''
    return header

def translate_reference_timestamp(header):
    """
        A function that function combines the lower and upper parts of the reference timestamp if it does exist. 
        Parameters
        ----------
        header : memap 
        Header of SLAP2 binary file read as Uint32
        
    
        Return
        -------
            It returns the header that has the combined reference timestamp in it.

    """
    if 'referenceTimestamp_lower' in header and 'referenceTimestamp_upper' in header:
        reference_timestamp_lower = header['referenceTimestamp_lower']
        reference_timestamp_upper = int(header['referenceTimestamp_upper']) << 32
        header['referenceTimestamp'] = int(reference_timestamp_lower) | reference_timestamp_upper
    return header
