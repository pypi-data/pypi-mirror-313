# coding: utf-8
# Author: Gauthier Patin
# Licence: GNU GPL v3.0

import os
import pandas as pd
import numpy as np
import colour
from typing import Optional, Union, List, Tuple
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter
from scipy.interpolate import interp1d
import seaborn as sns
import matplotlib.pyplot as plt
from uncertainties import ufloat, ufloat_fromstr, unumpy
from pathlib import Path
import importlib.resources as pkg_resources
import xarray as xr
from scipy.interpolate import RegularGridInterpolator
from ipywidgets import *

# underlying modules of the  microfading package
from . import plotting
from . import databases
from . import process_rawfiles




def get_datasets(rawfiles:Optional[bool] = False, BWS:Optional[bool] = True, stdev:Optional[bool] = False):
    """Retrieve exemples of dataset files. These files are meant to give the users the possibility to test the MFT class and its functions.  

    Parameters
    ----------
    rawfiles : Optional[bool], optional
        Whether to get rawdata files, by default False
        The raw files were obtained from microfading analyses performed with the Fotonowy device and consist of four files per analysis.

    BWS : Optional[bool], optional
        Whether to include the microfading measurements on blue wool standards (BWS), by default True

    stdev : Optional[bool], optional
        Whether to have microfading measurements wiht standard deviation values, by default False

    Returns
    -------
    list
        It returns a list of strings, where each string corresponds the absolute path of a microfading measurement excel file. Subsequently, one can use the list as input for the MFT class. 
    """

    if stdev:
        data_files = [
            '2024-144_MF.BWS0024.G01_avg_BW1_model_2024-07-30_MFT2.xlsx',
            '2024-144_MF.BWS0025.G01_avg_BW2_model_2024-08-02_MFT2.xlsx',
            '2024-144_MF.BWS0026.G01_avg_BW3_model_2024-08-07_MFT2.xlsx',
            '2024-144_MF.dayflower4.G01_avg_0h_model_2024-07-30_MFT2.xlsx',
            '2024-144_MF.indigo3.G01_avg_0h_model_2024-08-02_MFT2.xlsx',
        ]
        
    else:
        data_files = [
            '2024-144_MF.BWS0026.04_G02_BW3_model_2024-08-02_MFT1.xlsx',
            '2024-144_MF.BWS0025.04_G02_BW2_model_2024-08-02_MFT1.xlsx',
            '2024-144_MF.BWS0024.04_G02_BW1_model_2024-08-02_MFT1.xlsx',
            '2024-144_MF.yellowwood.01_G01_yellow_model_2024-08-01_MFT1.xlsx',
            '2024-144_MF.vermillon.01_G01_red_model_2024-07-31_MFT1.xlsx',
        ]

    if rawfiles:
        data_files = [
            '2024-8200 P-001 G01 uncleaned_01-spect_convert.txt',
            '2024-8200 P-001 G01 uncleaned_01-spect.txt',
            '2024-8200 P-001 G01 uncleaned_01.txt',
            '2024-8200 P-001 G01 uncleaned_01.rfc',
            '2024-144 BWS0024 G01 BW1_01-spect_convert.txt',
            '2024-144 BWS0024 G01 BW1_01-spect.txt',
            '2024-144 BWS0024 G01 BW1_01.txt',
            '2024-144 BWS0024 G01 BW1_01.rfc',
        ]

    if BWS == False:
        data_files = [x for x in data_files if 'BWS' not in x]

    

    # Get the paths to the data files within the package
    file_paths = []
    for file_name in data_files:
        
        with pkg_resources.path('microfading.datasets', file_name) as data_file:
             file_paths.append(data_file)

    return file_paths


def create_DB(folder:str):
    """Initiate the creation of databases.

    Parameters
    ----------
    folder : str
        Absolute path of the folder where the databases will be stored.

    Returns
    -------
        It creates the two empty databases as csv file (DB_projects.csv and DB_objects.csv), as well as six .txt files in the folder given as input.
    """

    DB = databases.DB()
    DB.create_db(folder_path=folder)


def folder_DB():
    """Retrieve the absolute path of the folder where the databases are located.

    Returns
    -------
    string or None        
    """
    
    DB = databases.DB()   

    
    if DB.folder_db.stem == "folder_path":
        print('Databases have not been created or have been deleted. Please, create databases by running the function "create_DB" from the microfading package.')
        return None
    
    else:    
        if 'DB_projects.csv' in os.listdir(DB.folder_db) and 'DB_objects.csv' in os.listdir(DB.folder_db):

            print(f'DB_projects.csv and DB_objects.csv files can be found in the following folder: {DB.folder_db}')    
            return DB.folder_db       

        else:
            print('Databases have not been created or have been deleted. Please, create databases by running the function "create_DB" from the microfading package.')
            return None


def get_DB(db:Optional[str] = 'all'):
    """Retrieve the databases

    Parameters
    ----------
    db : Optional[str], optional
        Choose which databases to retrieve, by default 'all'
        When 'projects', it returns the DB_projects.csv file
        When 'objects', it returns the DB_objects.csv file
        When 'all', it returns both file as a tuple

    Returns
    -------
    pandas dataframe or tuple
        It returns the databases as a pandas dataframe or a tuple if both dataframes are being asked.
    """

    DB = databases.DB()
    return DB.get_db(db=db)


def add_new_project():
    """Record the information about a new project inside the DB_projects.csv file.
    """

    DB = databases.DB()    
    return DB.add_new_project()


def add_new_object():
    """Record the information about a new object inside the DB_objects.csv file.
    """

    DB = databases.DB()    
    return DB.add_new_object()


def add_new_person():
    """Record the information of a new person inside the pesons.txt file.
    """

    DB = databases.DB()    
    return DB.add_new_person()


def update_DB_objects(new: str, old:Optional[str] = None):
    """Add a new column or modify an existing one in the DB_objects.csv file.

    Parameters
    ----------
    new : str
        value of the new column

    old : Optional[str], optional
        value of the old column to be replaced, by default None        
    """
    

    DB = databases.DB()
    DB.update_db_objects(new=new, old=old) 


def update_DB_projects(new: str, old:Optional[str] = None):
    """Add a new column or modify an existing one in the DB_projects.csv file.

    Parameters
    ----------
    new : str
        value of the new column
        
    old : Optional[str], optional
        value of the old column to be replaced, by default None        
    """

    DB = databases.DB()
    DB.update_db_projects(new=new, old=old) 


def process_rawdata(files: list, device: str, filenaming:Optional[str] = 'none', db:Optional[bool] = False, comment:Optional[str] = '', authors:Optional[str] = 'XX', interpolation:Optional[str] = 'He', step:Optional[float | int] = 0.1):
    """Process the microfading raw files created by the software that performed the microfading analysis. 

    Parameters
    ----------
    files : list
        A list of string that corresponds to the absolute path of the raw files.
    
    device : str
        Define the  microfading that has been used to generate the raw files ('fotonowy', 'sMFT').
    
    filenaming : Optional[str | list], optional
        Define the filename of the output excel file, by default 'none' 
        When 'none', it uses the filename of the raw files
        When 'auto', it creates a filename based on the info provided by the databases
        A list of parameters provided in the info sheet of the excel output can be used to create a filename   
    
    db : Optional[bool], optional
        Whether to make use of the databases, by default False
        When True, it will populate the info sheet in the interim file (the output excel file) with the data found in the databases.
        Make sure that the databases were created and that the information about about the project and the objects were recorded.
    
    comment : Optional[str], optional
        Whether to include a comment in the final excel file, by default ''
    
    authors : Optional[str], optional
        Initials of the persons that performed and processed the microfading measurements, by default 'XX' (unknown).
        Make sure that you registered the persons in the persons.txt file (see function 'add_new_person').
        If there are several persons, use a dash to connect the initials (e.g: 'JD-MG-OL').
    
    interpolation : Optional[str], optional
        Whether to perform the interpolation ('He', 'Hv', 't') or not ('none'), by default 'He'
        'He' performs interpolation based on the radiant exposure (MJ/m2)
        'Hv' performs interpolation based on the exposure dose (Mlxh)
        't' performs interpolation based on the exposure duration (sec)
    
    step : Optional[float  |  int], optional
        Interpolation step related to the scale previously mentioned ('He', 'Hv', 'time'), by default 0.1

    Returns
    -------
    Excel file
        It returns an excel file composed of three tabs (info, CIELAB, spectra).
    """

    if device.lower() == 'fotonowy':
        return process_rawfiles.MFT_fotonowy(files=files, filenaming=filenaming, db=db, comment=comment, authors=authors, interpolation=interpolation, step=step)
    
    elif device == 'sMFT':
        print('hello')
        return
    
         

class MFT(object):

    def __init__(self, files:list, BWS:Optional[bool] = True, stdev:Optional[bool] = False) -> None:
        """Instantiate a Microfading (MFT) class object in order to manipulate and visualize microfading analysis data.

        Parameters
        ----------
        files : list
            A list of string, where each string corresponds to the absolute path of text or csv file that contains the data and metadata of a single microfading measurement. The content of the file requires a specific structure, for which an example can be found in "datasets" folder of the microfading package folder (Use the get_datasets function to retrieve the precise location of such example files). If the file structure is not respected, the script will not be able to properly read the file and access its content.

        BWS : bool, optional
            When False, it ignores the measurements performed on BWS samples if included. 

        stdev: bool, optional
            Indicate whether the input files contains standard deviation values, by default False
        """
        self.files = files
        self.BWS = BWS
        self.stdev = stdev

        if self.BWS == False:
            self.files = [x for x in self.files if 'BW' not in x.name]


       
    def __repr__(self) -> str:
        return f'Microfading data class - Number of files = {len(self.files)}'
        

    
    def data_sp(self, wl_range:Union[int, float, list, tuple] = 'all', dose_unit:Optional[str] = 'He', dose_values:Union[int, float, list, tuple] = 'all', spectral_mode:Optional[str] = 'rfl'):
        """Retrieve the reflectance spectra related to the input files.

        Parameters
        ----------
        wl_range : Union[int, float, list, tuple], optional
            Select the wavelengths for which the spectral values should be given with a two-values tuple corresponding to the lowest and highest wavelength values, by default 'all'
            When 'all', it will returned all the available wavelengths contained in the datasets.
            A single wavelength value (an integer or a float number) can be entered.
            A list of specific wavelength values as integer or float can also be entered.
            A tuple of two or three values (min, max, step) will take the range values between these two first values. By default the step is equal to 1.

        dose_unit : string, optional
            Unit of the light energy dose, by default 'He'
            Any of the following units can be used: 'He', 'Hv', 't'. Where 'He' corresponds to radiant energy (MJ/m2), 'Hv' to exposure dose (Mlxh), and 't' to times (sec).

        dose_values : Union[int, float, list, tuple], optional
            Dose values for which the reflectance values will be returned, by default 'all'
            When 'all', it returns the reflectance values for all the dose values available in the given input data files.
            A single dose value (an integer or a float number) can be entered.
            A list of dose values, as integer or float, can also be entered.
            A tuple of three values (min, max, step) will be used in a numpy.arange() function to return an array of dose values. 

        spectral_mode : string, optional
            When 'rfl', it returns the reflectance spectra
            When 'abs', it returns the absorption spectra using the following equation: A = -log(R)

            
        Returns
        -------
        A list of pandas dataframes
            It returns a list of pandas dataframes where the columns correspond to the dose values and the rows correspond to the wavelengths.
        """

        data_sp = []
        files = self.read_files(sheets=['spectra', 'CIELAB'])        

        for file in files:
            df_sp = file[0]
            df_sp = df_sp.set_index(df_sp.columns[0])

            # whether to compute the absorption spectra
            if spectral_mode == 'abs':
                df_sp = np.log(df_sp) * (-1)
                

            # Set the dose unit
            if dose_unit == 'Hv':
                Hv = file[1]['Hv_Mlxh'].values
                df_sp.columns = Hv
                df_sp.index.name = 'wl-nm_Hv-Mlxh'
            
            elif dose_unit =='t':
                t = file[1]['t_sec'].values
                df_sp.columns = t
                df_sp.index.name = 'wl-nm_t-sec'
                

            # Set the wavelengths
            if isinstance(wl_range, tuple):
                if len(wl_range) == 2:
                    wl_range = (wl_range[0],wl_range[1],1)
                
                wavelengths = np.arange(wl_range[0], wl_range[1], wl_range[2])
                df_sp = df_sp.loc[wavelengths]

            elif isinstance(wl_range, int) or isinstance(wl_range, list):
                df_sp = df_sp.loc[wl_range]

            
            # Set the dose values 
            if isinstance(dose_values, tuple):
                if len(dose_values) == 2:
                    dose_values = (dose_values[0],dose_values[1],1)
                
                doses = np.arange(dose_values[0], dose_values[1], dose_values[2])
                
            elif isinstance(dose_values, int) or isinstance(dose_values, float):            
                doses = [dose_values]

            elif isinstance(dose_values, list):
                doses = dose_values

            else:
                doses = df_sp.columns


            # interpolate the reflectance values according to the wanted dose values
            interp = RegularGridInterpolator((df_sp.index,df_sp.columns), df_sp.values)

            pw, px = np.meshgrid(df_sp.index, doses, indexing='ij')     
            interp_data = interp((pw, px))    
            df_sp_interp = pd.DataFrame(interp_data, index=df_sp.index, columns=doses)  

            # append the spectral data
            data_sp.append(df_sp_interp)

        return data_sp
    
    
    def data_cielab(self, coordinates:Optional[list] = ['dE00'], dose_unit:Optional[str] = 'He', dose_values:Union[int, float, list, tuple] = 'all', index:Optional[bool] = True):
        """Retrieve the colourimetric values for one or multiple light dose values.

        Parameters
        ----------
        coordinates : Optional[list], optional
            Select the desired colourimetric coordinates from the following list: ['L*', 'a*','b*', 'C*', 'h', 'dL*', 'da*','db*', 'dC*', 'dh', 'dE76', 'dE00', 'dR_vis'], by default ['dE00']

        dose_unit : Optional[str], optional
            Unit of the light dose energy, by default ['He']
            Any of the following units can be added to the list: 'He', 'Hv', 't'. Where 'He' corresponds to radiant energy (MJ/m2), 'Hv' to exposure dose (Mlxh), and 't' to times (sec)

        dose_values : Union[int, float, list, tuple], optional
            Dose values for which the colourimetric values will be returned, by default 'all'
            When 'all', it returns the colourimetric values for all the dose values available in the given input data files.
            A single dose value (an integer or a float number) can be entered.
            A list of dose values, as integer or float, can also be entered.
            A tuple of three values (min, max, step) will be used in a numpy.arange() function to return an array of dose values. 

        index : Optional[bool], optional
            Whether to set the index of the returned dataframes, by default False

        Returns
        -------
        A list of pandas dataframes
            It returns the values of the wanted colour coordinates inside dataframes where each coordinate corresponds to a column.
        """
        
        # create a dictionary to store the light dose units
        dose_units = {'He':'He_MJ/m2', 'Hv':'Hv_Mlxh', 't': 't_sec'}


        # Retrieve the range light dose values
        if isinstance(dose_values, (float, int)):
            dose_values = [dose_values]

        elif isinstance(dose_values, tuple):
            dose_values = np.arange(dose_values[0], dose_values[1], dose_values[2])

        elif isinstance(dose_values, list):
            dose_values = dose_values        
        
        
        # Retrieve the data        
        original_data = self.read_files(sheets=['CIELAB'])
        original_data = [x[0] for x in original_data]

        
        # Add the delta LabCh values to the data dataframes   
        if original_data[0].columns.nlevels > 1:  # if there is more than one header level, than the data contains mean and std values
            
            delta_coord = [unumpy.uarray(d[coord, 'mean'], d[coord, 'std']) - unumpy.uarray(d[coord, 'mean'], d[coord, 'std'])[0] for coord in ['L*', 'a*', 'b*', 'C*', 'h'] for d in original_data]
            
            delta_means = [unumpy.nominal_values(x) for x in delta_coord]
            delta_stds = [unumpy.std_devs(x) for x in delta_coord]

            delta_coord_mean = [(f'd{coord}', 'mean') for coord in ['L*', 'a*', 'b*', 'C*', 'h']]
            delta_coord_std = [(f'd{coord}', 'std') for coord in ['L*', 'a*', 'b*', 'C*', 'h']]

            # Add the new columns to the dictionary
            data = []
            
            for d in original_data:
                #print(d)
                for coord_mean,delta_mean,coord_std,delta_std in zip(delta_coord_mean,delta_means, delta_coord_std,delta_stds):
                    #print(coord_mean)
                    #print(len(delta_mean))
                    d[coord_mean] = delta_mean
                    d[coord_std] = delta_std

                data.append(d)

            
            # Select the wanted dose_unit and coordinate        
            wanted_data = [x[[dose_units[dose_unit]] + coordinates] for x in data]        
            wanted_data = [x.set_index(x.columns[0]) for x in wanted_data]
            
        else:
            
            data = [d.assign(**{f'd{coord}': d[coord] - d[coord].values[0] for coord in ['L*', 'a*', 'b*', 'C*', 'h']}) for d in original_data]
                
            # Select the wanted dose_unit and coordinate        
            wanted_data = [x[[dose_units[dose_unit]] + coordinates] for x in data]        
            wanted_data = [x.set_index(x.columns[0]) for x in wanted_data]

        
        if isinstance(dose_values, str):
            if dose_values == 'all':
                interpolated_data = [x.reset_index() for x in wanted_data]
                   
        else:

            # Interpolation function, assuming linear interpolation
            interp_functions = lambda x, y: interp1d(x, y, kind='linear', bounds_error=False)

            
            # Double comprehension list to interpolate each dataframe in wanted_data
            interpolated_data = [
                pd.DataFrame({
                    col: interp_functions(df.index, df[col])(dose_values)
                    for col in df.columns
                }, index=dose_values)
                .rename_axis(dose_units[dose_unit])
                .reset_index()
                for df in wanted_data
            ]
            

        # Whether to set the index
        if index:
            interpolated_data = [x.set_index(x.columns[0]) for x in interpolated_data]
        
        return interpolated_data       
    

    def delta(self, coordinates:Optional[list] = ['dE00'], dose_unit:Optional[list] = ['He'], rate:Optional[bool] = False):
        """Retrieve the CIE delta values for a given set of colorimetric coordinates corresponding to the given microfading analyses.

        Parameters
        ----------
        coordinates : list, optional
            List of colorimetric coordinates, by default ['dE00']
            Any of the following coordinates can be added to the list: 'dE76', 'dE00', 'dR_vis' , 'L*', 'a*', 'b*', 'C*', 'h'.

        dose_unit : list, optional
            List of light energy doses, by default ['He']
            Any of the following units can be added to the list: 'He', 'Hv', 't'. Where 'He' corresponds to radiant energy (MJ/m2), 'Hv' to exposure dose (Mlxh), and 't' to times (sec)

        rate : bool, optional
            Whether to return the first derivative values of the desired coordinates, by default False

        Returns
        -------
        A list of pandas dataframes
            It returns a a list of pandas dataframes where each column corresponds to a light energy dose or a desired coordinate.
        """

        doses_dic = {'He': 'He_MJ/m2', 'Hv': 'Hv_Mlxh', 't': 't_sec'} 
        doses_labels = [doses_dic[x] for x in dose_unit]

        wanted_data = []
        

        if self.stdev == False: 
            
            doses = self.get_data(data=doses_labels) 
            data = self.get_data(data=coordinates)        
                        
            
            for el_data,el_dose in zip(data,doses):
                for col in el_data.columns:
                    if col in ['L*','a*','b*','C*','h']:
                        values = el_data[col]
                        values_delta = values - values[0]   

                        el_data[col] = values_delta
                        el_data.rename(columns={col:f'd{col}'}, inplace=True)
                
                if rate:   
                    
                    step_dose = el_dose.iloc[:,0].values[2]-el_dose.iloc[:,0].values[1]

                    el_data = pd.DataFrame(np.gradient(el_data.T.values, step_dose, axis=1).T, columns=el_data.columns)

                wanted_data.append(pd.concat([el_dose, el_data], axis=1))


        else:

            data = self.get_data(data=coordinates)[0] - self.get_data(data=coordinates)[0].iloc[0,:]
            doses = self.get_data(data=doses_labels)
            wanted_data = [pd.concat([doses[0],data], axis=1)]
            
            new_columns = []
            for i in wanted_data:
                for col in i.columns:
                    if col[1] in ['L*','a*','b*','C*','h']:
                        new_columns.append((col[0], f'd{col[1]}'))
                    else:
                        new_columns.append(col)

                i.columns = pd.MultiIndex.from_tuples(new_columns, names=i.columns.names)          
        
        
        return wanted_data


    def fit_data(self, plot:Optional[bool] = False, return_data:Optional[bool] = False, dose_unit:Optional[str] = 'He', coordinate:Optional[str] = 'dE00', equation:Optional[str] = 'c0*(x**c1)', initial_params:Optional[List[float]] = [0.1, 0.0], x_range:Optional[Tuple[int]] = (0, 1001, 1), save: Optional[bool] = False, path_fig: Optional[str] = 'default') -> Union[None, Tuple[np.ndarray, np.ndarray]]:
        """Fit the values of a given colourimetric coordinates. 

        Parameters
        ----------
        plot : bool, optional
            Whether to show the fitted data, by default False

        return_data : bool, optional
            Whether to return the fitted data, by default False

        dose_unit : string, optional
            Unit of the light energy dose, by default 'He'
            Any of the following units can be used: 'He', 'Hv', 't'. Where 'He' corresponds to radiant energy (MJ/m2), 'Hv' to exposure dose (Mlxh), and 't' to times (sec)

        coordinates : string, optional
            Select the desired colourimetric coordinates from the following list: ['L*', 'a*','b*', 'C*', 'h', 'dL*', 'da*','db*', 'dC*', 'dh', 'dE76', 'dE00', 'dR_vis'], by default 'dE00'

        equation : str, optional
            Mathematical equation used to fit the coordinate values, by default 'c0*(x**c1)'

        initial_params : Optional[List[float]], optional
            Initial guesses of the 'c' parameters given in the equation (c0, c1, c2, etc.), by default [0.1, 0.0]

        x_range : Optional[Tuple[int]], optional
            Values along which the fitted values should be computed (start, end, step), by default (0, 1001, 1)

        save : Optional[bool], optional
            Whether to save the plot, by default False

        path_fig : Optional[str], optional
            Absolute path of the figure to be saved, by default 'default'

        Returns
        -------
        Union[None, Tuple[np.ndarray, np.ndarray]]
            _description_
        """

        # Retrieve the range light dose values
        doses = {'He':'He_MJ/m2', 'Hv':'Hv_Mlxh', 't': 't_sec'}  
        x_values = np.arange(*x_range)
           
        # Retrieve the data
        original_data = self.get_data(data='cl')

        #original_data = self.get_data(data='dE') if self.data_category == 'interim' else self.get_data(data='dE')[0].astype(float)

        # Added the delta LabCh values to the data dataframes
        coordinates = ['L*', 'a*', 'b*', 'C*', 'h']
        data = [d.assign(**{f'd{coord}': d[coord] - d[coord].values[0] for coord in coordinates}) for d in original_data]
                
        # Select the wanted dose_unit and coordinate
        wanted_data = [x[[doses[dose_unit], coordinate]] for x in data]
        wanted_data = [x.set_index(x.columns[0]) for x in wanted_data]
        
        # Define the function to fit
        def fit_function(x, *params):
            param_dict = {f'c{i}': param for i, param in enumerate(params)}
            param_dict['x'] = x
            return eval(equation, globals(), param_dict)
    
        # Define boundaries for the parameters
        #bounds = ([-np.inf] * len(initial_params), [np.inf, 1]) if len(initial_params) == 2 else ([-np.inf] * len(initial_params), [np.inf, 1, np.inf])

        # Create an empty dataframe for the fitted data
        fitted_data = pd.DataFrame(index=pd.Series(x_values))

        # Empty list to store the labels
        fitted_labels = []

        # Emtpy list to store the optimized parameters
        fitted_parameters = []

        for d in wanted_data:
            # retrieve the x(light dose) and y(coordinate) values
            x, y = d.index, d.iloc[:,0]
                  
            # perform the curve fitting
            optimized_params, _ = curve_fit(fit_function, x, y, p0=initial_params, ) # bounds=bounds
            
            # generate fitted y data
            fitted_y = fit_function(x_values, *optimized_params)
            
            # append it to the fitted_data dataframe
            fitted_data = pd.concat([fitted_data, pd.DataFrame(fitted_y, index=pd.Series(x_values))], axis=1)
            
            # Calculate R-squared value
            residuals = y - fit_function(x, *optimized_params)
            ss_res, ss_tot = np.sum(residuals**2), np.sum((y - np.mean(y))**2)        
            r_squared = np.round(1 - (ss_res / ss_tot), 3)

            # Create a string representation of the equation with optimized parameters
            optimized_equation = equation
            for i, param in enumerate(optimized_params):
                optimized_equation = optimized_equation.replace(f'c{i}', str(np.round(param,2)))

            fitted_labels.append(f'{optimized_equation}, $R^2$ = {r_squared}')
            fitted_parameters.append(optimized_params)

        fitted_data.columns = [f'{x.split(".")[-1]}, $y$ = {y}' for x,y in zip(self.meas_ids, fitted_labels)]         
        
        if plot:
            labels_eq = {
                'L*': r'CIE $L^*$',
                'a*': r'CIE $a^*$',
                'b*': r'CIE $b^*$',
                'C*': r'CIE $C^*$',
                'h': r'CIE $h$',
                'dE76': r'$\Delta E^*_{ab}$',
                'dE00': r'$\Delta E^*_{00}$',
                'dR_VIS': r'$\Delta R_{\rm vis}$',
                'dL*': r'CIE $\Delta L^*$',
                'da*': r'CIE $\Delta a^*$',
                'db*': r'CIE $\Delta b^*$',
                'dC*': r'CIE $\Delta C^*$',
                'dh': r'CIE $\Delta h$',
            }

            labels_H = {
                'Hv': 'Exposure dose $H_v$ (Mlxh)',
                'He': 'Radiant Exposure $H_e$ (MJ/m²)',
                't' : 'Exposure duration (seconds)'
            }

            sns.set_theme(context='paper', font='serif', palette='colorblind')
            fig, ax = plt.subplots(1,1, figsize=(10,6))
            fs = 24

            
            pd.concat(wanted_data, axis=1).plot(ax=ax, color='0.7', ls='-', lw=5, legend=False)
            fitted_data.plot(ax=ax, lw=2, ls='--')

            #meas_line, = ax.plot(x,y, ls='-', lw=3)            
            #fitted_line, = ax.plot(x_values,fitted_y, ls='--', lw=2)

            ax.set_xlabel(labels_H[dose_unit], fontsize=fs)
            ax.set_ylabel(labels_eq[coordinate],fontsize=fs)
            
            #title = f'Microfading, {self.Id}, data fitting'
            #ax.set_title(title, fontsize = fs-4)   
            
            '''
            if coordinate.startswith('d'):                
                ax.set_ylim(0) 
            '''

            ax.set_xlim(0)    

            ax.xaxis.set_tick_params(labelsize=fs)
            ax.yaxis.set_tick_params(labelsize=fs)
        
            #plt.legend([meas_line,fitted_line], ["original data",f"$f(x) = {optimized_equation}$\n$R^2 = {r_squared:.3f}$"],fontsize=fs-6)
            #plt.tight_layout()
            

            if save:

                filename = self.make_filename('dEfit')

                if save:            
                    if path_fig == 'default':
                        path_fig = self.get_folder_figures() / filename

                    if path_fig == 'cwd':
                        path_fig = f'{os.getcwd()}/{filename}' 

                    plt.savefig(path_fig, dpi=300, facecolor='white')

            plt.show()
        
        if return_data:
            return fitted_parameters, fitted_data


    def read_files(self, sheets:Optional[list] = ['info', 'CIELAB', 'spectra']):
        """Read the data files given as argument when defining the instance of the MFT class.

        Parameters
        ----------
        sheets : Optional[list], optional
            Name of the excel sheets to be selected, by default ['info', 'CIELAB', 'spectra']

        Returns
        -------
        A list of list of pandas dataframes
            The content of each input data file is returned as a list pandas dataframes (3 dataframes maximum, one dataframe per sheet). Ultimately, the function returns a list of list, so that when there are several input data files, each list - related a single file - corresponds to a single element of a list.            
        """
        
        files = []        
                
        for file in self.files:

            df_info = pd.read_excel(file, sheet_name='info')
            df_sp = pd.read_excel(file, sheet_name='spectra')
            df_cl = pd.read_excel(file, sheet_name='CIELAB')
            
            if 'std' in list(df_sp.iloc[0,:].values):
                df_sp = pd.read_excel(file, sheet_name='spectra', header=[0,1], index_col=0)
                df_cl = pd.read_excel(file, sheet_name='CIELAB', header=[0,1])


            if sheets == ['info', 'CIELAB', 'spectra']:
                files.append([df_info, df_cl, df_sp])

            elif sheets == ['info']:
                files.append([df_info])

            elif sheets == ['CIELAB']:
                files.append([df_cl])

            elif sheets == ['spectra']:
                files.append([df_sp])

            elif sheets == ['spectra', 'CIELAB']:
                files.append([df_sp, df_cl])

            elif sheets == ['CIELAB','spectra']:
                files.append([df_cl, df_sp])

            elif sheets == ['info','CIELAB']:
                files.append([df_info, df_cl])

            elif sheets == ['info','spectra']:
                files.append([df_info, df_sp])

        return files
     

    def get_data(self, data:Union[str, list] = 'all', xarray:Optional[bool] = False):
        """Retrieve the microfading data.

        Parameters
        ----------
        data : str|list, optional
            Possibility to select the type of data, by default 'all'.
            When 'all', it returns all the data (spectral and colorimetric).
            When 'sp', it only returns the spectral data.
            When 'cl', it only returns the colorimetric data.  
            When 'Lab', it returns the CIE L*a*b* values.
            A list of strings can be entered to select specific colourimetric data among the following: ['dE76,'dE00','dR_vis', 'L*', 'a*', 'b*', 'C*', 'h'].

        xarray : bool, optional
            When True, the data are returned as an xarray.Dataset object, else as pandas dataframe object, by default False.

        Returns
        -------
        It returns a list of pandas dataframes or xarray.Dataset objects
        """

        all_files = self.read_files(sheets=['spectra','CIELAB'])
        all_data = []
        data_sp = [] 
        data_cl = [] 

        for data_file in all_files:

            sp = data_file[0].iloc[:,1:].values            
            wl = data_file[0].iloc[:,0].values
            He = data_file[1]['He_MJ/m2'].values
            Hv = data_file[1]['Hv_Mlxh'].values
            t = data_file[1]['t_sec'].values
            L = data_file[1]["L*"].values
            a = data_file[1]["a*"].values
            b = data_file[1]["b*"].values
            C = data_file[1]["C*"].values
            h = data_file[1]["h"].values
            dE76 = data_file[1]["dE76"].values
            dE00 = data_file[1]["dE00"].values
            dR_vis = data_file[1]["dR_vis"].values

            spectral_data = xr.Dataset(
                {
                    'sp': (['wavelength','dose'], sp)                
                },
                coords={
                    'wavelength': wl,   
                    'dose': He,
                    'He': ('dose', He),
                    'Hv': ('dose', Hv),  # Match radiant energy
                    't': ('dose', t)  # Match radiant energy
                }
            )

            color_data = xr.Dataset(
                {
                    'L*': (['dose'], L),
                    'a*': (['dose'], a),
                    'b*': (['dose'], b),
                    'C*': (['dose'], C),
                    'h': (['dose'], h),
                    'dE76': (['dose'], dE76),
                    'dE00': (['dose'], dE00),
                    'dR_vis': (['dose'], dR_vis),
                },
                coords={                    
                    'He': ('dose',He),
                    'Hv': ('dose',Hv),
                    't': ('dose',t),
                }
            )                
                    
            sp = spectral_data.set_xindex(["He","Hv","t"])
            cl = color_data.set_xindex(["He","Hv","t"])
            combined_data = xr.merge([sp, cl])

        all_data.append(combined_data)            
        
        
        if data == 'all':
            if xarray == False:                
                [data_sp.append(x[0]) for x in all_files]
                [data_cl.append(x[1]) for x in all_files]
                return data_sp, data_cl
            
            else:
                return all_data

        elif data == 'sp':
            if xarray == False:                
                [data_sp.append(x[0]) for x in all_files]   
                data_sp = [x.set_index(x.columns[0]) for x in data_sp]                         
            else:                
                data_sp = [x.sp for x in all_data]
                

            return data_sp
        
        elif data == 'cl':
            if xarray == False:
                [data_cl.append(x[1]) for x in all_files]
            else:
                data_cl = [x[['L*','a*','b*','C*','h','dE76','dE00','dR_vis']] for x in all_data]
            
            return data_cl
        
        elif data == 'Lab':
            if xarray == False:
                [data_cl.append(x[1][['L*','a*','b*']]) for x in all_files]
            else:
                data_cl = [x[['L*','a*','b*']] for x in all_data]

            return data_cl
        
        elif isinstance(data,list):
            if xarray == False:
                dic_doses = {'He': 'He_MJ/m2', 'Hv':'Hv_Mlxh', 't':'t_sec'}
                data = [dic_doses[x] if x in dic_doses.keys() else x for x in data]
                [data_cl.append(x[1][data]) for x in all_files]

            else:
                data = [elem for elem in data if elem not in ['Hv','He','t']]
                data_cl = [x[data] for x in all_data]
            
            return data_cl
        
        else:
            print("Enter a valid data parameter. It can either be a string ('sp', 'cl', 'Lab', 'all') or a list of strings ['dE00','dE76', 'L*', 'a*', 'b*', 'C*', 'h']")
            return None

    
    def get_metadata(self, labels:Optional[list] = 'all'):
        """Retrieve the metadata.

        Parameters
        ----------
        labels : Optional[list], optional
            A list of strings corresponding to the wanted metadata labels, by default 'all'
            The metadata labels can be found in the 'info' sheet of microfading excel files.
            When 'all', it returns all the metadata

        Returns
        -------
        pandas dataframe
            It returns the metadata inside a pandas dataframe where each column corresponds to a single file.
        """
        
        df = self.read_files()
        metadata = [x[0] for x in df]

        df_metadata = pd.DataFrame(index = metadata[0].set_index('parameter').index)

        for m in metadata:
            m = m.set_index('parameter')
            Id = m.loc['meas_id']['value']
            
            df_metadata[Id] = m['value']

        if labels == 'all':
            return df_metadata
        
        else:            
            return df_metadata.loc[labels]
       

    def JND(self, dose_unit:Optional[str] = 'Hv', JND_dE = 1.5, light_intensity=50, daily_exposure:Optional[int] = 10, yearly_exposure:Optional[int] = 365, fitting = True):
        """Compute the just noticeable difference (JND) corresponding to each input data file.

        Parameters
        ----------
        dose_unit : Optional[str], optional
            Unit of the light dose energy, by default ['He']
            Any of the following units can be added to the list: 'He', 'Hv', 't'. Where 'He' corresponds to radiant energy (MJ/m2), 'Hv' to exposure dose (Mlxh), and 't' to times (sec)

        JND_dE : float, optional
            The dE00 value corresponding to one JND, by default 1.5

        light_intensity : int, optional
            The illuminance or the irradiance value of the intended light source, by default 50

        daily_exposure : Optional[int], optional
            Amount of exposure hours per day, by default 10

        yearly_exposure : Optional[int], optional
            Amount of exposure days per year, by default 365

        fitting : bool, optional
            Whether to fit the microfading data necessary to compute the JND value, by default True

        Returns
        -------
        A list of numerical values as string (uncertainty string with a nominal and standard deviation value)
            It returns a list of numerical values corresponding to the amount of years necessary to reach one JND. 
        """

        H_step = 0.01
        dE_fitted = self.fit_data(dose_unit='Hv', x_range=(0,5.1,H_step), return_data=True)[1]
        dE_rate = np.gradient(dE_fitted.T.values, H_step, axis=1)
        dE_rate_mean = [np.mean(x[-20:]) for x in dE_rate]
        dE_rate_std = [np.std(x[-20:]) for x in dE_rate]

        rates = [ufloat(x, y) for x,y in zip(dE_rate_mean, dE_rate_std)]

        times_years = []

        for rate in rates:

            if dose_unit == 'Hv':
                
                JND_dose = (JND_dE / rate) * 1e6                     # in lxh
                time_hours = JND_dose / light_intensity
                time_years = time_hours / (daily_exposure * yearly_exposure)            

            if dose_unit == 'He':
                JND_dose = (JND_dE / rate) * 1e6                     # in J/m²
                time_sec = JND_dose / light_intensity
                time_hours = time_sec / 3600
                time_years = time_hours / (daily_exposure * yearly_exposure)

            times_years.append(time_years)

        return times_years


    def Lab(self, illuminant:Optional[str] = 'D65', observer:Optional[str] = '10'):
        """
        Retrieve the CIE L*a*b* values.

        Parameters
        ----------
        illuminant : (str, optional)  
            Reference *illuminant* ('D65', or 'D50'). by default 'D65'.
 
        observer : (str|int, optional)
            Reference *observer* in degree ('10' or '2'). by default '10'.

            
        Returns
        -------
        pandas dataframe
            It returns the L*a*b* values inside a dataframe where each column corresponds to a single file.
        """        
        observer = str(observer)

        illuminants = {'D65':colour.SDS_ILLUMINANTS['D65'], 'D50':colour.SDS_ILLUMINANTS['D50']}
        observers = {
            '10': 'cie_10_1964',
            '2' : 'cie_2_1931',
        }
        cmfs_observers = {
            '10': colour.colorimetry.MSDS_CMFS_STANDARD_OBSERVER["CIE 1964 10 Degree Standard Observer"],
            '2': colour.colorimetry.MSDS_CMFS_STANDARD_OBSERVER["CIE 1931 2 Degree Standard Observer"] 
            }
        
        ccs_ill = colour.CCS_ILLUMINANTS[observers[observer]][illuminant]

        meas_ids = self.meas_ids
        
        if self.stdev:
            df_sp = [x['mean'] for x in self.get_data(data='sp')]
        else:
            df_sp = self.get_data(data='sp')

        df_Lab = []
        

        for df, meas_id in zip(df_sp, meas_ids):            
            Lab_values = pd.DataFrame(index=['L*','a*','b*']).T           
            
            for col in df.columns:
                
                sp = df[col]
                wl = df.index
                sd = colour.SpectralDistribution(sp,wl)                

                XYZ = colour.sd_to_XYZ(sd,cmfs_observers[observer], illuminant=illuminants[illuminant])        
                Lab = np.round(colour.XYZ_to_Lab(XYZ/100,ccs_ill),3)               
                Lab_values = pd.concat([Lab_values, pd.DataFrame(Lab, index=['L*','a*','b*']).T], axis=0)
                Lab_values.index = np.arange(0,Lab_values.shape[0])

            Lab_values.columns = pd.MultiIndex.from_product([[meas_id], Lab_values.columns])
            df_Lab.append(Lab_values)

        return pd.concat(df_Lab, axis=1)
    

    def light_doses(self, dose_unit:Union[str,list] = 'all', max_doses:Optional[bool] = False):
        """Retrieve the light energy doses related to each microfading measurement.

        Parameters
        ----------
        dose_unit : Union[str,list], optional
            Unit of the light dose energy, by default 'all'
            Any of the following units can be added to the list: 'He', 'Hv', 't'. Where 'He' corresponds to radiant energy (MJ/m2), 'Hv' to exposure dose (Mlxh), and 't' to times (sec). When a single unit is requested, it can be given as a string value ('He', 'Hv', or 't').

        max_doses : bool, optional
            Whether to return the maximum light dose values, by default False.

        Returns
        -------
        list of pandas dataframes
            _description_
        """
        
        data = self.get_data(data='cl')

        if dose_unit == 'all':
            doses = [x[['He_MJ/m2', 'Hv_Mlxh', 't_sec']] for x in data]
        
        else:
            doses_dic = {'He':'He_MJ/m2', 'Hv':'Hv_Mlxh', 't':'t_sec'}
            
            if isinstance(dose_unit, list):
                dose_unit = [doses_dic[x] for x in dose_unit] 
                doses = [x[dose_unit] for x in data]

            else:
                doses = [x[doses_dic[dose_unit]] for x in data]

        if max_doses:
            doses = [x.iloc[-1,:] for x in doses]


        return doses
    
     
    @property
    def meas_ids(self):
        """Return the measurement id numbers corresponding to the input files.
        """
        info = self.get_metadata()        
        return info.loc['meas_id'].values


    def mean(self, return_data:Optional[bool] = True, criterion:Optional[str] = 'group', save:Optional[bool] = False, folder:Optional[str] = 'default', filename:Optional[str] = 'default'):
        """Compute mean and standard deviation values of several microfading measurements.

        Parameters
        ----------
        return_data : Optional[bool], optional
            Whether to return the data, by default True        

        criterion : Optional[str], optional
            _description_, by default 'group'            

        save : Optional[bool], optional
            Whether to save the average data as an excel file, by default False

        folder : Optional[str], optional
            Folder where the excel file will be saved, by default 'default'
            When 'default', the file will be saved in the same folder as the input files
            When '.', the file will be saved in the current working directory
            One can also enter a valid path as a string.

        filename : Optional[str], optional
            Filename of the excel file containing the average values, by default 'default'
            When 'default', it will use the filename of the first input file
            One can also enter a filename, but without a filename extension.

        Returns
        -------
        tuple, excel file
            It returns a tuple composed of three elements (info, CIELAB data, spectral data). When 'save' is set to True, an excel is created to stored the tuple inside three distinct excel sheet (info, CIELAB, spectra).

        Raises
        ------
        RuntimeError
            _description_
        """

        if len(self.files) < 2:        
            raise RuntimeError('Not enough files. At least two measurement files are required to compute the average values.')
        

        def mean_std_with_nan(arrays):
            '''Compute the mean of several numpy arrays of different shapes.'''
            
            # Find the maximum shape
            max_shape = np.max([arr.shape for arr in arrays], axis=0)
                    
            # Create arrays with NaN values
            nan_arrays = [np.full(max_shape, np.nan) for _ in range(len(arrays))]
                    
            # Fill NaN arrays with actual values
            for i, arr in enumerate(arrays):
                nan_arrays[i][:arr.shape[0], :arr.shape[1]] = arr
                    
            # Calculate mean
            mean_array = np.nanmean(np.stack(nan_arrays), axis=0)

            # Calculate std
            std_array = np.nanstd(np.stack(nan_arrays), axis=0)
                    
            return mean_array, std_array
        
        
        def to_float(x):
            try:
                return float(x)
            except ValueError:
                return x


        ###### SPECTRAL DATA #######

        data_sp = self.get_data(data='sp')

        # Get the energy dose step
        H_values = [x.columns.astype(float) for x in data_sp]       
        step_H = sorted(set([x[2] - x[1] for x in H_values]))[0]
        highest_He = np.max([x[-1] for x in H_values])

        # Average the spectral data
        sp = mean_std_with_nan(data_sp)
        sp_mean = sp[0]
        sp_std = sp[1] 
       

        # Wanted energy dose values          
        wanted_H = np.round(np.arange(0,highest_He+step_H,step_H),1)  

        if len(wanted_H) != sp_mean.shape[1]:            
            wanted_H = np.linspace(0,highest_He,sp_mean.shape[1])

        # Retrieve the wavelength range
        wl = self.wavelength.iloc[:,0]
        

        # Create a multi-index pandas DataFrame
        H_tuples = [(dose, measurement) for dose in wanted_H for measurement in ['mean', 'std']]
        multiindex_cols = pd.MultiIndex.from_tuples(H_tuples, names=['He_MJ/m2', 'Measurement'])
        
        data_df_sp = np.empty((len(wl), len(wanted_H) * 2))       
        data_df_sp[:, 0::2] = sp_mean
        data_df_sp[:, 1::2] = sp_std
        df_sp_final = pd.DataFrame(data_df_sp,columns=multiindex_cols, index=wl)
        df_sp_final.index.name = 'wavelength_nm'
                  
           

        ###### COLORIMETRIC DATA #######

        data_cl = self.get_data(data='dE')
        columns_cl = data_cl[0].columns

        # Average the colorimetric data    
        cl = mean_std_with_nan(data_cl)
        cl_mean = cl[0]
        cl_std = cl[1]

        # Create a multi-index pandas DataFrame
        cl_tuples = [(x, measurement) for x in data_cl[0].columns for measurement in ['mean', 'std']]
        multiindex_cols = pd.MultiIndex.from_tuples(cl_tuples, names=['coordinates', 'Measurement'])
        
        data_df_cl = np.empty((cl_mean.shape[0], cl_mean.shape[1] * 2))       
        data_df_cl[:, 0::2] = cl_mean
        data_df_cl[:, 1::2] = cl_std
        df_cl_final = pd.DataFrame(data_df_cl,columns=multiindex_cols, )
        df_cl_final.drop([('He_MJ/m2','std'), ('Hv_Mlxh','std'), ('t_sec','std')], axis=1, inplace=True)
        
        mapper = {('He_MJ/m2', 'mean'): ('He_MJ/m2', 'value'), ('Hv_Mlxh', 'mean'): ('Hv_Mlxh', 'value'), ('t_sec', 'mean'): ('t_sec', 'value')}
        df_cl_final.columns = pd.MultiIndex.from_tuples([mapper.get(x, x) for x in df_cl_final.columns])
        
    
        cl_cols = df_cl_final.columns
        cl_cols_level1 = [x[0] for x in cl_cols]
        cl_cols_level2 = [x[1] for x in cl_cols]
        df_cl_final.columns = np.arange(0,df_cl_final.shape[1])

        df_cl_final = pd.concat([pd.DataFrame(data=np.array([cl_cols_level2])), df_cl_final])
        df_cl_final.columns = cl_cols_level1
        df_cl_final = df_cl_final.set_index(df_cl_final.columns[0])
        

        ###### INFO #######

        data_info = self.get_metadata().fillna(' ')

        # Select the first column as a template
        df_info = data_info.iloc[:,0]
        

        # Rename title file
        df_info.rename({'[SINGLE MICRO-FADING ANALYSIS]': '[MEAN MICRO-FADING ANALYSES]'}, inplace=True)

        # Date time
        most_recent_dt = max(data_info.loc['date_time'])
        df_info.loc['date_time'] = most_recent_dt

        # Project data info
        df_info.loc['project_id'] = '_'.join(sorted(set(data_info.loc['project_id'].values)))
        df_info.loc['projectleider'] = '_'.join(sorted(set(data_info.loc['projectleider'].values)))
        df_info.loc['meelezer'] = '_'.join(sorted(set(data_info.loc['meelezer'].values)))
        df_info.loc['aanvraagdatum'] = '_'.join(sorted(set(data_info.loc['aanvraagdatum'].values)))
        df_info.loc['uiterste_datum'] = '_'.join(sorted(set(data_info.loc['uiterste_datum'].values)))

        # Object data info
        if len(set([x.split('_')[0] for x in data_info.loc['institution'].values])) > 1:
            df_info.loc['institution'] = '_'.join(sorted(set([x.split('_')[0] for x in data_info.loc['institution'].values])))
        
        df_info.loc['object_id'] = '_'.join(sorted(set(data_info.loc['object_id'].values)))
        df_info.loc['object_category'] = '_'.join(sorted(set(data_info.loc['object_category'].values)))
        df_info.loc['object_type'] = '_'.join(sorted(set(data_info.loc['object_type'].values)))
        df_info.loc['object_technique'] = '_'.join(sorted(set(data_info.loc['object_technique'].values)))
        df_info.loc['object_title'] = '_'.join(sorted(set(data_info.loc['object_title'].values)))
        df_info.loc['object_name'] = '_'.join(sorted(set(data_info.loc['object_name'].values)))
        df_info.loc['object_creator'] = '_'.join(sorted(set(data_info.loc['object_creator'].values)))
        df_info.loc['object_date'] = '_'.join(sorted(set(data_info.loc['object_date'].values)))
        df_info.loc['object_support'] = '_'.join(sorted(set(data_info.loc['object_support'].values)))
        df_info.loc['color'] = '_'.join(sorted(set(data_info.loc['color'].values)))
        df_info.loc['colorants'] = '_'.join(sorted(set(data_info.loc['colorants'].values)))
        df_info.loc['colorants_name'] = '_'.join(sorted(set(data_info.loc['colorants_name'].values)))
        df_info.loc['binding'] = '_'.join(sorted(set(data_info.loc['binding'].values)))
        df_info.loc['ratio'] = '_'.join(sorted(set(data_info.loc['ratio'].values)))
        df_info.loc['thickness_microns'] = '_'.join(sorted(set(data_info.loc['thickness_microns'].values)))
        df_info.loc['status'] = '_'.join(sorted(set(data_info.loc['status'].values)))

        # Device data info
        if len(set(data_info.loc['device'].values)) > 1:
            df_info.loc['device'] = '_'.join(sorted(set([x.split('_')[0] for x in data_info.loc['device'].values])))
        
        df_info.loc['measurement_mode'] = '_'.join(sorted(set(data_info.loc['measurement_mode'].values)))
        df_info.loc['zoom'] = '_'.join(sorted(set(data_info.loc['zoom'].values)))
        df_info.loc['iris'] = '_'.join(sorted(set(str(data_info.loc['iris'].values))))
        df_info.loc['geometry'] = '_'.join(sorted(set(data_info.loc['geometry'].values)))
        df_info.loc['distance_ill_mm'] = '_'.join(sorted(set(str(data_info.loc['distance_ill_mm'].values))))
        df_info.loc['distance_coll_mm'] = '_'.join(sorted(set(str(data_info.loc['distance_coll_mm'].values))))       

        if len(set(data_info.loc['fiber_fading'].values)) > 1:
            df_info.loc['fiber_fading'] = '_'.join(sorted(set([x.split('_')[0] for x in data_info.loc['fiber_fading'].values])))

        if len(set(data_info.loc['fiber_ill'].values)) > 1:
            df_info.loc['fiber_ill'] = '_'.join(sorted(set([x.split('_')[0] for x in data_info.loc['fiber_ill'].values])))

        if len(set(data_info.loc['fiber_coll'].values)) > 1:
            df_info.loc['fiber_coll'] = '_'.join(sorted(set([x.split('_')[0] for x in data_info.loc['fiber_coll'].values])))

        if len(set(data_info.loc['lamp_fading'].values)) > 1:
            df_info.loc['lamp_fading'] = '_'.join(sorted(set([x.split('_')[0] for x in data_info.loc['lamp_fading'].values])))

        if len(set(data_info.loc['lamp_ill'].values)) > 1:
            df_info.loc['lamp_ill'] = '_'.join(sorted(set([x.split('_')[0] for x in data_info.loc['lamp_ill'].values])))

        if len(set(data_info.loc['filter_fading'].values)) > 1:
            df_info.loc['filter_fading'] = '_'.join(sorted(set([x.split('_')[0] for x in data_info.loc['filter_fading'].values])))

        if len(set(data_info.loc['filter_ill'].values)) > 1:
            df_info.loc['filter_ill'] = '_'.join(sorted(set([x.split('_')[0] for x in data_info.loc['filter_ill'].values])))

        if len(set(data_info.loc['white_ref'].values)) > 1:
            df_info.loc['white_ref'] = '_'.join(sorted(set([x.split('_')[0] for x in data_info.loc['white_ref'].values])))
        

        # Analysis data info
        
        criterion_value = df_info.loc[criterion]
        object_id = df_info.loc['object_id']
        if criterion == 'group':            
            df_info.loc['meas_id'] = f'MF.{object_id}.{criterion_value}'
        elif criterion == 'object' or criterion == 'project':
             df_info.loc['meas_id'] = f'MF.{criterion_value}'
        else:
            print('Choose one of the following options for the criterion parameter: ["group", "object", "project"]')

        meas_nbs = '-'.join([x.split('.')[-1] for x in self.meas_ids])
        df_info.loc['group'] = f'{"-".join(sorted(set(data_info.loc["group"].values)))}_{meas_nbs}'    
        df_info.loc['group_description'] = '_'.join(sorted(set(data_info.loc['group_description'].values)))
        df_info.loc['background'] = '_'.join(sorted(set(data_info.loc['background'].values)))  

        if len(set(data_info.loc['specular_component'].values)) > 1:
            df_info.loc['specular_component'] = '_'.join(sorted(set([x.split('_')[0] for x in data_info.loc['specular_component'].values]))) 

        
        df_info.loc['integration_time_ms'] = np.round(np.mean(data_info.loc['integration_time_ms'].astype(float).values),1)
        df_info.loc['average'] = '_'.join([str(x) for x in sorted(set(data_info.loc['average'].astype(str).values))]) 
        df_info.loc['duration_min'] = np.round(np.mean(data_info.loc['duration_min'].values),1)
        df_info.loc['interval_sec'] = '_'.join([str(x) for x in sorted(set(data_info.loc['interval_sec'].values))])
        df_info.loc['measurements_N'] = '_'.join([str(x) for x in sorted(set(data_info.loc['measurements_N'].astype(str).values))])
        df_info.loc['illuminant'] = '_'.join(sorted(set(data_info.loc['illuminant'].values)))
        df_info.loc['observer'] = '_'.join(sorted(set(data_info.loc['observer'].values)))


        # Beam data info

        df_info.loc['beam_photo'] = '_'.join(sorted(set(data_info.loc['beam_photo'].values)))
        df_info.loc['resolution_micron/pixel'] = '_'.join(sorted(set(str(data_info.loc['resolution_micron/pixel'].values))))

        fwhm = data_info.loc['FWHM_micron']
        fwhm_avg = np.mean([i for i in [to_float(x) for x in fwhm] if isinstance(i, (int, float))])
        df_info.loc['FWHM_micron'] = fwhm_avg

        power_info = data_info.loc['power_mW']
        power_avg = np.mean([ufloat_fromstr(x.split('_')[1]) for x in power_info])
        power_ids = '-'.join(sorted(set([x.split('_')[0] for x in power_info])))
        df_info.loc['power_mW'] = f'{power_ids}_{power_avg}' 

        irr_values = [str(ufloat(x,0)) if isinstance(x, int) else x for x in data_info.loc['irradiance_W/m**2'] ] 
        irr_mean = np.int32(np.mean([unumpy.nominal_values(ufloat_fromstr(x)) for x in irr_values]))
        irr_std = np.int32(np.std([unumpy.nominal_values(ufloat_fromstr(x)) for x in irr_values]))
        irr_avg = ufloat(irr_mean, irr_std)    
        df_info.loc['irradiance_W/m**2'] = irr_avg
       
        lm = [x for x in data_info.loc['luminuous_flux_lm'].values]
        lm_avg = np.round(np.mean(lm),3)
        df_info.loc['luminuous_flux_lm'] = lm_avg

        ill = [x for x in data_info.loc['illuminance_Mlx']]
        ill_avg = np.round(np.mean(ill),3)
        df_info.loc['illuminance_Mlx'] = ill_avg

        
        # Results data info
        df_info.loc['totalDose_He_MJ/m**2'] = df_cl_final.index.values[-1]
        df_info.loc['totalDose_Hv_Mlxh'] = df_cl_final['Hv_Mlxh'].values[-1]
        df_info.loc['fittedEqHe_dE00'] = ''
        df_info.loc['fittedEqHv_dE00'] = ''
        df_info.loc['fittedRate_dE00_at_2Mlxh'] = ''
        df_info.loc['fittedRate_dE00_at_20MJ/m**2'] = ''
        df_info.loc['dE00_at_300klxh'] = ''
        df_info.loc['dE00_at_3MJ/m**2'] = ''
        df_info.loc['dEab_final'] = ufloat(df_cl_final['dE76'].values[-1][0], df_cl_final['dE76'].values[-1][1])
        df_info.loc['dE00_final'] = ufloat(df_cl_final['dE00'].values[-1][0], df_cl_final['dE00'].values[-1][1])
        df_info.loc['dR_VIS_final'] = ufloat(df_cl_final['dR_vis'].values[-1][0], df_cl_final['dR_vis'].values[-1][1])
        df_info.loc['Hv_at_1dE00'] = ''
        df_info.loc['BWSE'] = ''

        # Rename the column
        df_info.name = 'value'
                
        
        ###### SAVE THE MEAN DATAFRAMES #######
        
        if save:  

            # set the folder
            if folder == ".":
                folder = Path('.')  

            elif folder == 'default':
                folder = Path(self.files[0]).parent

            else:
                if Path(folder).exists():
                    folder = Path(folder)         

            # set the filename
            if filename == 'default':
                filename = f'{Path(self.files[0]).stem}_MEAN{Path(self.files[0]).suffix}'

            else:
                filename = f'{filename}.xlsx'

            
            # create a excel writer object
            with pd.ExcelWriter(folder / filename) as writer:

                df_info.to_excel(writer, sheet_name='info', index=True)
                df_cl_final.to_excel(writer, sheet_name="CIELAB", index=True)
                df_sp_final.to_excel(writer, sheet_name='spectra', index=True)
        

        ###### RETURN THE MEAN DATAFRAMES #######
            
        if return_data:
            return df_info, df_cl_final, df_sp_final
  

    def plot_CIELAB(self, stds=[], dose_unit:Optional[str] = 'He', dose_values:Union[int, float, list, tuple] = 'all', labels:Union[str,list] = 'default', title:Optional[str] = None, fontsize:Optional[int] = 24, legend_position:Optional[str] = 'in', legend_fontsize:Optional[int] = 24, legend_title:Optional[str] = None, save:Optional[bool] = False, path_fig:Optional[str] = 'cwd'):
        """Plot the Lab values related to the microfading analyses.

        Parameters
        ----------
        stds : list, optional
            A list of standard variation values respective to each element given in the data parameter, by default []

        dose_unit : str, optional
            Unit of the light energy dose, by default 'He'
            Any of the following units can be used: 'He', 'Hv', 't'. Where 'He' corresponds to radiant energy (MJ/m2), 'Hv' to exposure dose (Mlxh), and 't' to times (sec)

        dose_values : Union[int, float, list, tuple], optional        
            Values of the light dose energy, by default 'all'
            A single value (integer or float number), a list of multiple numerical values, or range values with a tuple (start, end, step) can be entered.
            When 'all', it takes the values found in the data. 

        labels : Union[str, list], optional
            A list of labels respective to each element given in the data parameter that will be shown in the legend. When the list is empty there is no legend displayed, by default 'default'
            When 'default', each label will composed of the Id number of the number followed by a short description

        title : Optional[str], optional
            Whether to add a title to the plot, by default None

        fontsize : Optional[int], optional
            Fontsize of the plot (title, ticks, and labels), by default 24

        legend_position : Optional[str], optional
            Position of the legend, by default 'in'
            The legend can either be inside the figure ('in') or outside ('out')

        legend_fontsize : Optional[int], optional
            Fontsize of the legend, by default 24

        legend_title : Optional[str], optional
            Add a title above the legend, by default ''

        save : bool, optional
            Whether to save the figure, by default False

        path_fig : str, optional
            Absolute path required to save the figure, by default 'cwd'
            When 'cwd', it will save the figure in the current working directory.

        Returns
        -------
        _type_
            It returns a figure with 4 subplots that can be saved as a png file.
        """

        data_Lab = self.data_cielab(coordinates=['L*', 'a*', 'b*'], dose_unit=dose_unit, dose_values=dose_values)
        data_Lab = [x.T.values for x in data_Lab]

        print(data_Lab)

        # Retrieve the metadata
        info = self.get_metadata()
        object_info = info.loc['object_type'].values[0]
        object_technique = info.loc['object_technique'][0]
        group_nb = info.loc['group'].values[0]
        group_descriptions = info.loc['group_description'].values
        group_description = group_descriptions[0]

        ids = [x for x in self.meas_ids if 'BW' not in x]
        meas_nbs = [x.split('.')[-1] for x in ids]

        # Define the labels
        if labels == 'default':
            labels = [f'{x}-{y}' for x,y in zip(self.meas_ids,group_descriptions)]
            legend_title = 'Measurement $n^o$'

        return plotting.CIELAB(data=data_Lab, labels=labels, title=title, fontsize=fontsize, legend_fontsize=legend_fontsize, legend_position=legend_position, legend_title=legend_title, save=save, path_fig=path_fig)


    def plot_delta(self, coordinates:Optional[list] = ['dE00'], dose_unit:Optional[str] = ['He'], labels = 'default', initial_values:Optional[bool] = False, colors:Union[str,list] = None, lw:Union[int,list] = 'default', title:Optional[str] = None, fontsize:Optional[int] = 24, legend_fontsize:Optional[int] = 24, legend_title:Optional[str] = None, save:Optional[bool] = False, path_fig:Optional[str] = 'cwd'):
        """Plot the delta values of choosen colorimetric coordinates related to the microfading analyses.

        Parameters
        ----------
        coordinates : list, optional
            List of colorimetric coordinates, by default ['dE00']
            Any of the following coordinates can be added to the list: 'dE76', 'dE00', 'dR_vis' , 'L*', 'a*', 'b*', 'C*', 'h'.

        dose_unit : a list of str, optional
            Unit of the light energy dose, by default ['He']
            Any of the following units can be used: 'He', 'Hv', 't'. Where 'He' corresponds to radiant energy (MJ/m2), 'Hv' to exposure dose (Mlxh), and 't' to times (sec)

        labels : Union[str, list], optional
            A list of labels respective to each element given in the data parameter that will be shown in the legend. When the list is empty there is no legend displayed, by default 'default'
            When 'default', each label will composed of the Id number of the number followed by a short description

        colors : Union[str, list], optional
            Define the colors of the curves, by default None
            When 'sample', the color of each line will be based on srgb values computed from the reflectance values. Alternatively, a single string value can be used to define the color (see matplotlib colour values) and will be applied to all the lines. Or a list of matplotlib colour values can be used. With a single coordinate, the list should have the same length as measurement files. With multiple coordinates, the list should have the same length as coordinates.

        lw : Union[int,list], optional
            Width of the lines, by default 'default'
            When 'default', it attributes a given a width according to each coordinates, otherwise it gives a value of 2.
            A single value (an integer) can be entered and applied to all the lines.
            A list of integers can also be entered. With a single coordinate, the list should have the same length as measurement files. With multiple coordinates, the list should have the same length as coordinates.

        title : Optional[str], optional
            Whether to add a title to the plot, by default None

        fontsize : Optional[int], optional
            Fontsize of the plot (title, ticks, and labels), by default 24

        legend_fontsize : Optional[int], optional
            Fontsize of the legend, by default 24

        legend_title : Optional[str], optional
            Add a title above the legend, by default ''

        save : bool, optional
            Whether to save the figure, by default False

        path_fig : str, optional
            Absolute path required to save the figure, by default 'cwd'
            When 'cwd', it will save the figure in the current working directory.
        """


        # Retrieve the data
        list_data = [x.T.values for x in self.delta(coordinates=coordinates, dose_unit=dose_unit)] 
        
        # Retrieve the metadata
        info = self.get_metadata()
        object_info = info.loc['object_type'].values[0]
        object_technique = info.loc['object_technique'][0]
        group_nb = info.loc['group'].values[0]
        group_descriptions = info.loc['group_description'].values
        group_description = group_descriptions[0]

        ids = [x for x in self.meas_ids]
        meas_nbs = [x.split('.')[-1] for x in ids]

        # Set the labels values
        if labels == 'default':                       
            labels = [f'{x}-{y}' for x,y in zip(meas_nbs, group_descriptions)] 

        elif labels == '':
            labels = []
        
        elif isinstance(labels, list):
            labels = labels
            '''
            labels_list = []
            for i,Id in enumerate(self.meas_ids):
                label = Id.split('.')[-1]
                for el in labels:
                    label = label + f'-{self.get_metadata().loc[el].values[i]}'
                labels_list.append(label)

            labels = labels_list
            '''

        # Add the initial values of the colorimetric coordinates
        if initial_values:
            initial_values = [x for x in list_data]

        # Set the color of the lines according to the sample
        if colors == 'sample':

            Lab = self.data_cielab(coordinates=['L*', 'a*', 'b*'])
            if self.stdev == True:                
                Lab = [df.loc[:, pd.IndexSlice[:,'mean']] for df in Lab]                       

            Lab_initial = [x.iloc[0,:].values for x in Lab]
            colors = list(colour.XYZ_to_sRGB(colour.Lab_to_XYZ(Lab_initial), self.set_illuminant()[0]).clip(0, 1))
            colors = colors * len(coordinates)
        
        # Whether to add a title or not
        if title == 'default':
            technique = 'MFT'            
        elif title == 'none':
            title = None
        else:
            title = title 

        # Define the saving folder in case the figure should be saved

        filename = ''
        if save:
            if path_fig == 'default':
                path_fig = self.get_dir(folder_type='figures') / filename                

            if path_fig == 'cwd':
                path_fig = f'{os.getcwd()}/{filename}' 
       
        
        plotting.delta(data=list_data, x_unit=dose_unit, y_unit=coordinates, labels=labels, initial_values=initial_values, colors=colors, lw=lw, title=title, fontsize=fontsize, legend_fontsize=legend_fontsize, legend_title=legend_title, save=save, path_fig=path_fig)


    def plot_sp(self, stds:Optional[bool] = False, spectra:Optional[str] = 'i', dose_unit:Optional[str] = 'He', dose_values:Union[int, float, list, tuple] = 'all', spectral_mode:Optional[str] = 'rfl', labels:Union[str,list] = 'default', title:Optional[str] = None, fontsize:Optional[int] = 24, fontsize_legend:Optional[int] = 24, legend_title='', wl_range:Optional[tuple] = None, colors:Union[str,list] = None, lw:Union[int, list] = 2, ls:Union[str, list] = '-', save=False, path_fig='cwd', derivation=False, smooth=False, smooth_params=[10,1], report:Optional[bool] = False):
        """Plot the reflectance spectra corresponding to the associated microfading analyses.

        Parameters
        ----------
        stds : list, bool
            Whether to show the standard deviation values, by default False

        spectra : Optional[str], optional
            Define which spectra to display, by default 'i'
            Use 'i' for initial spectral, 'f' for final spectra, 'i+f' for initial and final spectra, or 'all' for all the spectra.

        dose_unit : str, optional
            Unit of the light energy dose, by default 'He'
            Any of the following units can be used: 'He', 'Hv', 't'. Where 'He' corresponds to radiant energy (MJ/m2), 'Hv' to exposure dose (Mlxh), and 't' to times (sec)

        dose_values : Union[int, float, list, tuple], optional
            Values of the light dose energy, by default 'all'
            A single value (integer or float number), a list of multiple numerical values, or range values with a tuple (start, end, step) can be entered.
            When 'all', it takes the values found in the data. 

        spectral_mode : string, optional
            When 'rfl', it returns the reflectance spectra
            When 'abs', it returns the absorption spectra using the following equation: A = -log(R)

        labels : Union[str, list], optional
            A list of labels respective to each element given in the data parameter that will be shown in the legend. When the list is empty there is no legend displayed, by default 'default'
            When 'default', each label will composed of the Id number of the number followed by a short description

        title : str, optional
            Whether to add a title to the plot, by default None

        fontsize : int, optional
            Fontsize of the plot (title, ticks, and labels), by default 24

        fontsize_legend : int, optional
            Fontsize of the legend, by default 24

        legend_title : str, optional
            Add a title above the legend, by default ''

        wl_range : tuple, optional
            Define the wavelength range with a two-values tuple corresponding to the lowest and highest wavelength values, by default None

        colors : Union[str, list], optional
            Define the colors of the reflectance curves, by default None
            When 'sample', the color of each line will be based on srgb values computed from the reflectance values. Alternatively, a single string value can be used to define the color (see matplotlib colour values) or a list of matplotlib colour values can be used. 

        lw : Union[int, list], optional
            Define the width of the plot lines, by default 2
            It can be a single integer value that will apply to all the curves. Or a list of integers can be used where the number of integer elements should match the number of reflectance curves.

        ls : Union[str, list], optional
            Define the line style of the plot lines, by default '-'
            It can be a string ('-', '--', ':', '-.') that will apply to all the curves. Or a list of string can be used where the number of string elements should match the number of reflectance curves.

        save : bool, optional
            Whether to save the figure, by default False

        path_fig : str, optional
            Absolute path required to save the figure, by default 'cwd'
            When 'cwd', it will save the figure in the current working directory.

        derivation : bool, optional
            Wether to compute and display the first derivative values of the spectra, by default False

        smooth : bool, optional
            Whether to smooth the reflectance curves, by default False

        smooth_params : list, optional
            Parameters related to the Savitzky-Golay filter, by default [10,1]
            Enter a list of two integers where the first value corresponds to the window_length and the second to the polyorder value. 

        report : Optional[bool], optional
            Configure some aspects of the figure for use in a report, by default False

        Returns
        -------
        _type_
            It returns a figure that can be save as a png file.
        """

        # Retrieve the metadata
        info = self.get_metadata()
        object_info = info.loc['object_type'].values[0]
        object_technique = info.loc['object_technique'][0]
        group_nb = info.loc['group'].values[0]
        group_descriptions = info.loc['group_description'].values
        group_description = group_descriptions[0]

        ids = [x for x in self.meas_ids if 'BW' not in x]
        meas_nbs = [x.split('.')[-1] for x in ids]

        # Define the labels
        if labels == 'default':
            labels = [f'{x}-{y}' for x,y in zip(self.meas_ids,group_descriptions)]
            legend_title = 'Measurement $n^o$'

        # Select the spectral data
        if spectra == 'i':
            data_sp_all = self.data_sp(wl_range=wl_range)
            data_sp = [pd.DataFrame(x.iloc[:,0]) for x in data_sp_all]

            text = 'Initial spectra'

        elif spectra == 'f':
            data_sp_all = self.data_sp(wl_range=wl_range)
            data_sp = [pd.DataFrame(x.iloc[:,-1]) for x in data_sp_all]

            text = 'Final spectra'

        elif spectra == 'i+f':
            data_sp_all = self.data_sp(wl_range=wl_range)
            data_sp = [x.iloc[:,[0] + [-1]] for x in data_sp_all]

            ls = ['-', '--'] * len(data_sp)
            lw = [3,2] * len(data_sp)
            colors = [colors, 'k'] * len(data_sp)

            meas_labels = [f'{x}-{y}' for x,y in zip(self.meas_ids,group_descriptions)]
            none_labels = [None] * len(meas_labels)
            labels = [item for pair in zip(meas_labels, none_labels) for item in pair]

            text = 'Initial and final spectra (black dashed lines)'

        elif spectra == 'doses':
            data_sp = self.data_sp(wl_range=wl_range, dose_unit=dose_unit,dose_values=dose_values)

            
            dose_units = {'He': 'MJ/m2', 'Hv': 'Mlxh', 't': 'sec'}
            legend_title = f'Light dose values'
            labels = [f'{str(x)} {dose_units[dose_unit]}' for x in dose_values] * len(data_sp)

            text = ''
            
            ls_list = ['-','--','-.',':','-','--','-.',':','-','--','-.',':',]
            ls = ls_list[:len(dose_values)] * len(data_sp)        
            srgb_i = self.sRGB().iloc[0,:].values.reshape(-1, 3) 
            colors = np.repeat(srgb_i, 3, axis=0)          

        else:
            print(f'"{spectra}" is not an adequate value. Enter a value for the parameter "spectra" among the following list: "i", "f", "i+f", "doses".')
            return
            
        indices = [x.index for x in data_sp]        
        columns = [x.columns for x in data_sp] 


        # Whether to smooth the data
        if smooth:
                data_sp = [pd.DataFrame(savgol_filter(x.T, window_length=smooth_params[0], polyorder=smooth_params[1]).T, index=idx, columns=cols) for x,idx,cols in zip(data_sp,indices,columns)]       
                        
        # whether to compute the absorption spectra
        if spectral_mode == 'abs':
            data_sp = [np.log(x) * (-1) for x in data_sp]
        
        # Reset the index
        data = [x.reset_index() for x in data_sp]
               
        # Whether to compute the first derivative
        if derivation:
            data = [pd.concat([x.iloc[:,0], pd.DataFrame(np.gradient(x.iloc[:,1:], axis=0))], axis=1) for x in data]

        
        wanted_data = []

        for el in data:
            data_indexed = el.set_index(el.columns[0])
            data_values = [ (data_indexed.index,x) for x in data_indexed.T.values]
            wanted_data = wanted_data + data_values

        
        return plotting.spectra(data=wanted_data, stds=[], spectral_mode=spectral_mode, labels=labels, title=title, fontsize=fontsize, fontsize_legend=fontsize_legend, legend_title=legend_title, x_range=wl_range, colors=colors, lw=lw, ls=ls, text=text, save=save, path_fig=path_fig, derivation=derivation)
       

    def plot_sp_delta(self,spectra:Optional[tuple] = ('i','f'), dose_unit:Optional[str] = 'Hv', wl_range:Union[int,float,list,tuple] = 'all', spectral_mode:Optional[str] = 'rfl'):

        if spectra == ('i','f'):

            sp_data = [x.iloc[:,[0,-1]] for x in self.data_sp(wl_range=wl_range, spectral_mode=spectral_mode)]
            sp_delta = [x.iloc[:,1] - x.iloc[:,0] for x in sp_data]
            wanted_data = [(x.index, x.values) for x in sp_delta]

        elif spectra[0] == 'i':
            
            sp1 = [x.iloc[:,0] for x in self.data_sp(wl_range=wl_range, spectral_mode=spectral_mode)]
            sp2 = [x.values.flatten() for x in self.data_sp(dose_unit=dose_unit, dose_values=float(spectra[1]),wl_range=wl_range, spectral_mode=spectral_mode)]
            
            wanted_data = [(x.index,np.array(y)-np.array(x)) for x,y in zip(sp1,sp2)]

        elif spectra[1] == 'f':

            sp1 = [x.values.flatten() for x in self.data_sp(dose_unit=dose_unit, dose_values=float(spectra[0]), wl_range=wl_range, spectral_mode=spectral_mode)]            
            sp2 = [x.iloc[:,-1] for x in self.data_sp(wl_range=wl_range, spectral_mode=spectral_mode)]            
            
            wanted_data = [(y.index,np.array(y)-np.array(x)) for x,y in zip(sp1,sp2)]
        
        else:

            wavelengths = self.wavelength.T.values
            sp1 = [x.values.flatten() for x in self.data_sp(dose_unit=dose_unit, dose_values=float(spectra[0]),wl_range=wl_range, spectral_mode=spectral_mode)]
            sp2 = [x.values.flatten() for x in self.data_sp(dose_unit=dose_unit, dose_values=float(spectra[1]),wl_range=wl_range, spectral_mode=spectral_mode)]
            
            wanted_data = [(w,np.array(y)-np.array(x)) for w,x,y in zip(wavelengths,sp1,sp2)]   
                 
    
        plotting.spectra(data=wanted_data, spectral_mode=spectral_mode)


    def set_illuminant(self, illuminant:Optional[str] = 'D65', observer:Optional[str] = '10'):
        """Set the illuminant values

        Parameters
        ----------
        illuminant : Optional[str], optional
            Select the illuminant, by default 'D65'
            It can be any value within the following list: ['A', 'B', 'C', 'D50', 'D55', 'D60', 'D65', 'D75', 'E', 'FL1', 'FL2', 'FL3', 'FL4', 'FL5', 'FL6', 'FL7', 'FL8', 'FL9', 'FL10', 'FL11', 'FL12', 'FL3.1', 'FL3.2', 'FL3.3', 'FL3.4', 'FL3.5', 'FL3.6', 'FL3.7', 'FL3.8', 'FL3.9', 'FL3.10', 'FL3.11', 'FL3.12', 'FL3.13', 'FL3.14', 'FL3.15', 'HP1', 'HP2', 'HP3', 'HP4', 'HP5', 'LED-B1', 'LED-B2', 'LED-B3', 'LED-B4', 'LED-B5', 'LED-BH1', 'LED-RGB1', 'LED-V1', 'LED-V2', 'ID65', 'ID50', 'ISO 7589 Photographic Daylight', 'ISO 7589 Sensitometric Daylight', 'ISO 7589 Studio Tungsten', 'ISO 7589 Sensitometric Studio Tungsten', 'ISO 7589 Photoflood', 'ISO 7589 Sensitometric Photoflood', 'ISO 7589 Sensitometric Printer']

        observer : Optional[str], optional
            Standard observer in degree, by default '10'
            It can be either '2' or '10'

        Returns
        -------
        tuple
            It returns a tuple with two set of values: the chromaticity coordinates of the illuminants (CCS) and the spectral distribution of the illuminants (SDS).
        """

        observers = {
            '10': "cie_10_1964",
            '2' : "cie_2_1931"
        }
       
        CCS = colour.CCS_ILLUMINANTS[observers[observer]][illuminant]
        SDS = colour.SDS_ILLUMINANTS[illuminant]

        return CCS, SDS

     
    def set_observer(self, observer:Optional[str] = '10'):
        """Set the observer.

        Parameters
        ----------
        observer : Optional[str], optional
            Standard observer in degree, by default '10'
            It can be either '2' or '10'

        Returns
        -------        
            Returns the x_bar,  y_bar, z_bar spectra between 360 and 830 nm.
        """

        observers = {
            '10': "CIE 1964 10 Degree Standard Observer",
            '2' : "CIE 1931 2 Degree Standard Observer"
        }

        return colour.colorimetry.MSDS_CMFS_STANDARD_OBSERVER[observers[observer]]
    

    def sp_derivation(self):
        """Compute the first derivative values of reflectance spectra.

        Returns
        -------
        a list of pandas dataframes
            It returns the first derivative values of the reflectance spectra inside dataframes where each column corresponds to a single spectra.
        """

        sp = self.get_data(data='sp')                    

        sp_derivation = [pd.DataFrame(pd.concat([pd.DataFrame(np.gradient(x.iloc[:,:], axis=0), index=pd.Series(x.index), columns=x.columns)], axis=1),index=pd.Series(x.index), columns=x.columns) for x in sp]

        return sp_derivation
    

    def sRGB(self, illuminant='D65', observer='10'):
        """Compute the sRGB values. 

        Parameters
        ----------
        illuminant : (str, optional)  
            Reference *illuminant* ('D65', or 'D50'). by default 'D65'.
 
        observer : (str|int, optional)
            Reference *observer* in degree ('10' or '2'). by default '10'.

        Returns
        -------
        pandas dataframe
            It returns the sRGB values inside a dataframe where each column corresponds to a single file.
        """
        observer = str(observer)

        illuminants = {'D65':colour.SDS_ILLUMINANTS['D65'], 'D50':colour.SDS_ILLUMINANTS['D50']}
        observers = {
            '10': 'cie_10_1964',
            '2' : 'cie_2_1931',
        }
        cmfs_observers = {
            '10': colour.colorimetry.MSDS_CMFS_STANDARD_OBSERVER["CIE 1964 10 Degree Standard Observer"],
            '2': colour.colorimetry.MSDS_CMFS_STANDARD_OBSERVER["CIE 1931 2 Degree Standard Observer"] 
            }
        
        ccs_ill = colour.CCS_ILLUMINANTS[observers[observer]][illuminant]

        meas_ids = self.meas_ids                
        df_sp = self.get_data(data='sp')       
        df_srgb = []
        

        for df, meas_id in zip(df_sp, meas_ids):
            
            srgb_values = pd.DataFrame(index=['R','G','B']).T            

            for col in df.columns:
                
                sp = df[col]
                wl = df.index
                sd = colour.SpectralDistribution(sp,wl)                

                XYZ = colour.sd_to_XYZ(sd,cmfs_observers[observer], illuminant=illuminants[illuminant]) 
                srgb = np.round(colour.XYZ_to_sRGB(XYZ / 100, illuminant=ccs_ill), 4)                        
                srgb_values = pd.concat([srgb_values, pd.DataFrame(srgb, index=['R','G','B']).T], axis=0)
                srgb_values.index = np.arange(0,srgb_values.shape[0])

            srgb_values.columns = pd.MultiIndex.from_product([[meas_id], srgb_values.columns])
            df_srgb.append(srgb_values)

        return pd.concat(df_srgb, axis=1)


    @property
    def wavelength(self):
        """Return the wavelength range of the microfading measurements.
        """
        data = self.get_data(data='sp')

        wavelengths = pd.concat([pd.Series(x.index.values) for x in data], axis=1)
        wavelengths.columns = self.meas_ids

        return wavelengths


    def XYZ(self, illuminant:Optional[str] = 'D65', observer:Union[str,int] = '10'):
        """Compute the XYZ values. 

        Parameters
        ----------
        illuminant : (str, optional)  
            Reference *illuminant* ('D65', or 'D50'). by default 'D65'.
 
        observer : (str|int, optional)
            Reference *observer* in degree ('10' or '2'). by default '10'.

        Returns
        -------
        pandas dataframe
            It returns the XYZ values inside a dataframe where each column corresponds to a single file.
        """

        observer = str(observer)

        illuminants = {'D65':colour.SDS_ILLUMINANTS['D65'], 'D50':colour.SDS_ILLUMINANTS['D50']}
        
        cmfs_observers = {
            '10': colour.colorimetry.MSDS_CMFS_STANDARD_OBSERVER["CIE 1964 10 Degree Standard Observer"],
            '2': colour.colorimetry.MSDS_CMFS_STANDARD_OBSERVER["CIE 1931 2 Degree Standard Observer"] 
            }
        
        meas_ids = self.meas_ids                
        df_sp = self.get_data(data='sp')       
        df_XYZ = []
        

        for df, meas_id in zip(df_sp, meas_ids):
            
            XYZ_values = pd.DataFrame(index=['X','Y','Z']).T

            for col in df.columns:
                
                sp = df[col]
                wl = df.index
                sd = colour.SpectralDistribution(sp,wl)                

                XYZ = np.round(colour.sd_to_XYZ(sd,cmfs_observers[observer], illuminant=illuminants[illuminant]),3)
                XYZ_values = pd.concat([XYZ_values, pd.DataFrame(XYZ, index=['X','Y','Z']).T], axis=0)
                XYZ_values.index = np.arange(0,XYZ_values.shape[0])

            XYZ_values.columns = pd.MultiIndex.from_product([[meas_id], XYZ_values.columns])
            df_XYZ.append(XYZ_values)

        return pd.concat(df_XYZ, axis=1)


    def xy(self, illuminant:Optional[str] = 'D65', observer:Union[str, int] = '10'):
        """Compute the xy values. 

        Parameters
        ----------
        illuminant : (str, optional)  
            Reference *illuminant* ('D65', or 'D50'). by default 'D65'.
 
        observer : (str|int, optional)
            Reference *observer* in degree ('10' or '2'). by default '10'.

        Returns
        -------
        pandas dataframe
            It returns the xy values inside a dataframe where each column corresponds to a single file.
        """


        observer = str(observer)

        illuminants = {'D65':colour.SDS_ILLUMINANTS['D65'], 'D50':colour.SDS_ILLUMINANTS['D50']}        
        cmfs_observers = {
            '10': colour.colorimetry.MSDS_CMFS_STANDARD_OBSERVER["CIE 1964 10 Degree Standard Observer"],
            '2': colour.colorimetry.MSDS_CMFS_STANDARD_OBSERVER["CIE 1931 2 Degree Standard Observer"] 
            }
        
        meas_ids = self.meas_ids                
        df_sp = self.get_data(data='sp')       
        df_xy = []
        

        for df, meas_id in zip(df_sp, meas_ids):
            
            xy_values = pd.DataFrame(index=['x','y']).T           

            for col in df.columns:
                
                sp = df[col]
                wl = df.index
                sd = colour.SpectralDistribution(sp,wl)                

                XYZ = colour.sd_to_XYZ(sd,cmfs_observers[observer], illuminant=illuminants[illuminant])
                xy = np.round(colour.XYZ_to_xy(XYZ),4)
                xy_values = pd.concat([xy_values, pd.DataFrame(xy, index=['x','y']).T], axis=0)
                xy_values.index = np.arange(0,xy_values.shape[0])

            xy_values.columns = pd.MultiIndex.from_product([[meas_id], xy_values.columns])
            df_xy.append(xy_values)

        return pd.concat(df_xy, axis=1)




    

    