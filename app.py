import os
import joblib
import pefile
import pandas as pd
from flask import Flask
from flask_cors import CORS
import hashlib
import csv

app = Flask(__name__)
CORS(app)
app.static_folder = 'static'

# Load your ML model
model_path = r"RF_model.joblib"
scaler = r'scalar.joblib'

model = joblib.load(model_path)
scalar = joblib.load(scaler)



def extract_features(file_obj):
    try:
        pe = pefile.PE(data=file_obj.read())
    except pefile.PEFormatError as e:
        return jsonify({'error': 'Unable to read the PE file. Please upload a valid PE file.'}), 400

    # Calculate resource sizes
    resource_sizes = []
    if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE'):
        for resource_type in pe.DIRECTORY_ENTRY_RESOURCE.entries:
            if hasattr(resource_type, 'directory'):
                for resource_id in resource_type.directory.entries:
                    if hasattr(resource_id, 'directory'):
                        for resource_lang in resource_id.directory.entries:
                            data_rva = resource_lang.data.struct.OffsetToData
                            size = resource_lang.data.struct.Size
                            resource_sizes.append(size)
    
    mean_resource_size = sum(resource_sizes) / len(resource_sizes) if resource_sizes else 0
    min_resource_size = min(resource_sizes) if resource_sizes else 0
    max_resource_size = max(resource_sizes) if resource_sizes else 0

    
    features = {
        'Machine': pe.FILE_HEADER.Machine,
        'SizeOfOptionalHeader': pe.FILE_HEADER.SizeOfOptionalHeader,
        'Characteristics': pe.FILE_HEADER.Characteristics,
        'MajorLinkerVersion': pe.OPTIONAL_HEADER.MajorLinkerVersion,
        'MinorLinkerVersion': pe.OPTIONAL_HEADER.MinorLinkerVersion,
        'SizeOfCode': pe.OPTIONAL_HEADER.SizeOfCode,
        'SizeOfInitializedData': pe.OPTIONAL_HEADER.SizeOfInitializedData,
        'SizeOfUninitializedData': pe.OPTIONAL_HEADER.SizeOfUninitializedData,
        'AddressOfEntryPoint': pe.OPTIONAL_HEADER.AddressOfEntryPoint,
        'BaseOfCode': pe.OPTIONAL_HEADER.BaseOfCode,
        'BaseOfData': pe.OPTIONAL_HEADER.BaseOfData if pe.FILE_HEADER.Machine == pefile.MACHINE_TYPE['IMAGE_FILE_MACHINE_I386'] else 0,
        'ImageBase': pe.OPTIONAL_HEADER.ImageBase,
        'SectionAlignment': pe.OPTIONAL_HEADER.SectionAlignment,
        'FileAlignment': pe.OPTIONAL_HEADER.FileAlignment,
        'MajorOperatingSystemVersion': pe.OPTIONAL_HEADER.MajorOperatingSystemVersion,
        'MinorOperatingSystemVersion': pe.OPTIONAL_HEADER.MinorOperatingSystemVersion,
        'MajorImageVersion': pe.OPTIONAL_HEADER.MajorImageVersion,
        'MinorImageVersion': pe.OPTIONAL_HEADER.MinorImageVersion,
        'MajorSubsystemVersion': pe.OPTIONAL_HEADER.MajorSubsystemVersion,
        'MinorSubsystemVersion': pe.OPTIONAL_HEADER.MinorSubsystemVersion,
        'SizeOfImage': pe.OPTIONAL_HEADER.SizeOfImage,
        'SizeOfHeaders': pe.OPTIONAL_HEADER.SizeOfHeaders,
        'CheckSum': pe.OPTIONAL_HEADER.CheckSum,
        'Subsystem': pe.OPTIONAL_HEADER.Subsystem,
        'DllCharacteristics': pe.OPTIONAL_HEADER.DllCharacteristics,
        'SizeOfStackReserve': pe.OPTIONAL_HEADER.SizeOfStackReserve,
        'SizeOfStackCommit': pe.OPTIONAL_HEADER.SizeOfStackCommit,
        'SizeOfHeapReserve': pe.OPTIONAL_HEADER.SizeOfHeapReserve,
        'SizeOfHeapCommit': pe.OPTIONAL_HEADER.SizeOfHeapCommit,
        'LoaderFlags': pe.OPTIONAL_HEADER.LoaderFlags,
        'NumberOfRvaAndSizes': pe.OPTIONAL_HEADER.NumberOfRvaAndSizes,
        'SectionsNb': len(pe.sections),
        'SectionsMeanEntropy': sum(section.get_entropy() for section in pe.sections) / len(pe.sections),
        'SectionsMinEntropy': min(section.get_entropy() for section in pe.sections),
        'SectionsMaxEntropy': max(section.get_entropy() for section in pe.sections),
        'SectionsMeanRawsize': sum(section.SizeOfRawData for section in pe.sections) / len(pe.sections),
        'SectionsMinRawsize': min(section.SizeOfRawData for section in pe.sections),
        'SectionMaxRawsize': max(section.SizeOfRawData for section in pe.sections),
        'SectionsMeanVirtualsize': sum(section.Misc_VirtualSize for section in pe.sections) / len(pe.sections),
        'SectionsMinVirtualsize': min(section.Misc_VirtualSize for section in pe.sections),
        'SectionMaxVirtualsize': max(section.Misc_VirtualSize for section in pe.sections),
        'ImportsNbDLL': len(pe.DIRECTORY_ENTRY_IMPORT),
        'ImportsNb': sum(len(entry.imports) for entry in pe.DIRECTORY_ENTRY_IMPORT),
        'ImportsNbOrdinal': sum(len(entry.imports) for entry in pe.DIRECTORY_ENTRY_IMPORT if entry.imports[0].name is None),
        'ExportNb': len(pe.DIRECTORY_ENTRY_EXPORT.symbols) if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT') else 0,
        'ResourcesNb': len(pe.DIRECTORY_ENTRY_RESOURCE.entries) if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE') else 0,

        'ResourcesMeanEntropy': sum(getattr(entry, 'get_entropy', lambda: 0)() for entry in pe.DIRECTORY_ENTRY_RESOURCE.entries) \
            / len(pe.DIRECTORY_ENTRY_RESOURCE.entries) if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE') else 0,
        
        'ResourcesMinEntropy': min(getattr(entry, 'get_entropy', lambda: 0)() \
                                   for entry in pe.DIRECTORY_ENTRY_RESOURCE.entries) if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE') else 0,

        'ResourcesMaxEntropy': max(getattr(entry, 'get_entropy', lambda: 0)() \
                                   for entry in pe.DIRECTORY_ENTRY_RESOURCE.entries) if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE') else 0,
        
        'ResourcesMeanSize': mean_resource_size,
            
        'ResourcesMinSize': min_resource_size,
        'ResourcesMaxSize': max_resource_size,
        'LoadConfigurationSize': pe.DIRECTORY_ENTRY_LOAD_CONFIG.struct.Size if hasattr(pe, 'DIRECTORY_ENTRY_LOAD_CONFIG') else 0,
        'VersionInformationSize': len(pe.VS_FIXEDFILEINFO) if hasattr(pe, 'VS_FIXEDFILEINFO') else 0,
    }

    return pd.DataFrame([features])



def calculate_file_hash(file_obj, algorithm='sha256'): 
    """Calculate the hash of a file.""" 
    hash_func = getattr(hashlib, algorithm)() 
    file_obj.seek(0)  # Ensure the file cursor is at the beginning 
    for chunk in iter(lambda: file_obj.read(4096), b''): 
        hash_func.update(chunk) 
 
    return hash_func.hexdigest() 
 
def check_malware(file, malware_hashes):
    """Check if the file matches any known malware hashes."""
    file_hash = calculate_file_hash(file)

    with open(malware_hashes, 'r') as f:
        reader = csv.reader(f)
        is_malware:bool = False
        for row in reader:
            if file_hash in row[0]:
                print('Record found! \n', row)
                is_malware = True
    return is_malware, file_hash

    

if __name__ == '__main__':
    from routes import *  
    app.run(debug=True, port=5000)
