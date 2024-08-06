import h5py
import numpy as np

#From https://stackoverflow.com/a/34401029/22888642
# Generator for datasets only 
def _dataset_iterator(g, prefix=''):
   for key, item in g.items():
        path = '{}/{}'.format(prefix, key)
        if isinstance(item, h5py.Dataset): # test for dataset
            yield path
        elif isinstance(item, h5py.Group): # test for group (go down)
            yield from _dataset_iterator(item, path)

class VFS:
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.file = None
        if (file_path is not None):
            self.open(file_path)

    def __del__(self):
        if self.file is not None:
            self.file.close()

    def __getitem__(self, dataset_path):
        print(f"Getting {dataset_path}") 
        if self.file is None:
            raise ValueError("HDF5 file is not open")

        dataset = self.file[dataset_path]
        byte_array = dataset[()].tobytes()
        return byte_array
    
    def _parse_path(self, path):
        if self.file is None:
            raise ValueError("HDF5 file is not open")
        #Split the path into parts
        if (path[0] == '/'):
            basepath = '/'
            path = path[1:]
        else:
            basepath = self.current_dir
        parts = path.split('/') 
        #Iterate over the parts
        for part in parts:
            #If the part is empty, continue
            if part == '':
                continue
            #If the part is '..', move up one directory
            if part == '..':
                basepath = '/'.join(basepath.split('/')[:-1])
            if part == '.':
                continue
            #Otherwise, move to the specified directory
            else:
                #If the right hand character is a '/', remove it
                if basepath[-1] == '/':
                    basepath = basepath[:-1]
                basepath = basepath + '/' + part
        return basepath
    
    def cd(self, path):
        if self.file is None:
            raise ValueError("HDF5 file is not open")
        #Parse the path
        new_dir = self._parse_path(path)
        #Check if the directory exists
        if new_dir not in self.file:
            raise ValueError(f"Directory {new_dir} does not exist")
        self.current_dir = new_dir
        
    def ls(self, path=None):
        if self.file is None:
            raise ValueError("HDF5 file is not open")
        if path is None:
            path = self.current_dir
        #Parse the path
        new_dir = self._parse_path(path)
        #Check if the directory exists
        if new_dir not in self.file:
            raise ValueError(f"Directory {new_dir} does not exist")
        #List the groups in the directory
        #List only the datasets in the directory
        for name in self.file[new_dir]:
            #If the object is a dataset, print it simply
            if isinstance(self.file[new_dir][name], h5py.Dataset):
                print(name)
            #If the object is a group, print it with a '/'
            if isinstance(self.file[new_dir][name], h5py.Group):
                print(name + '/')

    def get(self, path):
        if self.file is None:
            raise ValueError("HDF5 file is not open")
        path = self._parse_path(path)
        #Parse the path
        return self[path]
    
    def put(self, path, data):
        if self.file is None:
            raise ValueError("HDF5 file is not open")
        #If data is not a byte array, convert it
        if not isinstance(data, bytes):
            #If data is a string, convert it to bytes
            if isinstance(data, str):
                data = data.encode('utf-8')
            #If data is a list, convert it to bytes
            if isinstance(data, list):
                data = bytes(data)
            if isinstance(data, np.ndarray):
                data = data.tobytes()
        path = self._parse_path(path)
        #If the path already exists, delete it
        if path in self.file:
            del self.file[path]
        #Create the dataset and set the size to the size of the data
        #At this point data should be a byte array
        #Convert it to a 1D numpy array of uint8
        data = np.frombuffer(data, dtype=np.uint8)
        dataset = self.file.create_dataset(path, data=data)
        
    def rm(self, path, confirm=False):
        if self.file is None:
            raise ValueError("HDF5 file is not open")
        path = self._parse_path(path)
        #If the path does not exist, raise an error
        if path not in self.file:
            raise ValueError(f"Path {path} does not exist")
        #If running interactively, ask for confirmation
        if not confirm:
            confirm = input(f"Delete {path}? (y/n): ") == 'y'
        if confirm:
            del self.file[path]
        else:
            print(f"Path {path} not deleted")

    def mkdir(self, path):
        if self.file is None:
            raise ValueError("HDF5 file is not open")
        path = self._parse_path(path)
        #If the path already exists, raise an error
        if path in self.file:
            raise ValueError(f"Path {path} already exists")
        #This should work like mkdir -p
        #Split the path into parts
        parts = path.split('/')
        #Iterate over the parts
        #Because of _parse_path, this will always be an absolute path
        #Start at the root
        current = self.file['/']
        for part in parts:
            if (part == ''):
                continue
            print (part)
            if part in current:
                current = current[part]
            else:
                current = current.create_group(part)

    def open(self, filename):
        if self.file is not None:
            raise ValueError("HDF5 file is already open")
        self.file = h5py.File(filename, 'a')
        self.file_path = filename
        self.current_dir = '/'

    def close(self):
        if self.file is None:
            raise ValueError("HDF5 file is not open")
        self.file.close()
        self.file = None

    #A method to list the datasets in the file
    def list_datasets(self):
        if self.file is None:
            raise ValueError("HDF5 file is not open")
        self.file.visititems(lambda name, obj: print(name))

    def get_data_names(self):
        return _dataset_iterator(self.file)
    def get_toplevel_groups(self):
        grps = []
        for key,item in self.file.items():
            if isinstance(item, h5py.Group):
                grps.append(key)
        return grps
