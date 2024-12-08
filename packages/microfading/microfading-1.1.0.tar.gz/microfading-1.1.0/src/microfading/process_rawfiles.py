import pandas as pd
import numpy as np
import colour
from math import pi
from pathlib import Path
from typing import Optional, Union
import scipy.interpolate as sip
from scipy.interpolate import RegularGridInterpolator


from . import databases
from . import MFT_info_template


def MFT_fotonowy(files: list, filenaming:Optional[str] = 'none', folder:Optional[str] = '.', db:Optional[bool] = False, comment:Optional[str] = '', authors:Optional[str] = 'XX', interpolation:Optional[str] = 'He', step:Optional[float | int] = 0.1, average:Optional[int] = 20, background:Optional[str] = 'black'):

            
    # check whether the objects and projects databases have been created
    if db:
        DB = databases.DB()

        if DB.folder_db is None:
            return 'Databases have not been created. Please, create databases by running the function "create_DB" from the microfading package.'
        
        else:            
            db_projects, db_objects = DB.get_db()
    
    else:
        filenaming = 'none'
   
    # define parameters for colorimetric calculations
    D65 = colour.SDS_ILLUMINANTS["D65"]
    d65 = colour.CCS_ILLUMINANTS["cie_10_1964"]["D65"]
    cmfs = colour.colorimetry.MSDS_CMFS_STANDARD_OBSERVER["CIE 1964 10 Degree Standard Observer"] 

    # wanted wavelength range
    wanted_wl = pd.Index(np.arange(380,781), name='wavelength_nm')
    
    # retrieve counts spectral files to be processed
    raw_files_counts = [Path(file) for file in files if 'spect_convert.txt' in Path(file).name]
 
    
    # process each spectral file
    for raw_file_counts in raw_files_counts:

                
        # retrieve the corresponding colorimetric file
        raw_file_cl = Path(str(raw_file_counts).replace('-spect_convert.txt', '.txt'))
        stemName = raw_file_cl.stem.replace(" ", "_")                                 

        # upload raw files into dataframes
        raw_df_counts = pd.read_csv(raw_file_counts, sep='\t', skiprows = 1)
        raw_df_cl = pd.read_csv(raw_file_cl, sep='\t', skiprows = 8)        

        # round up the first and last wavelength values
        raw_df_counts.rename(index={380.024:380},inplace=True)
        raw_df_counts.rename(index={779.910:780},inplace=True)

        # select white and dark spectral references (first and second columns respectively)
        white_ref = raw_df_counts.iloc[:,0].values
        dark_ref = raw_df_counts.iloc[:,1].values
        
        # remove the white and dark ref        
        df_counts = raw_df_counts.iloc[:,2:-1]  
        df_counts.columns = raw_df_counts.columns[3:] 

        # rename the index column
        df_counts.index.name = 'wavelength_nm'               

        # create an empty dataframe for the spectral reflectance values        
        raw_df_sp = pd.DataFrame(index=raw_df_counts.index)
        raw_df_sp.index.name = 'wavelength_nm'        

        # drop the before last column of df_counts
        df_counts = df_counts.drop(df_counts.iloc[:,-2].name,axis=1)
        
        # compute the reflectance values
        for col in df_counts.columns:  
            counts = df_counts[col].values
            sp = pd.Series(counts / white_ref, index=df_counts.index, name=col[15:])
            raw_df_sp = pd.concat([raw_df_sp,sp], axis=1)   
                
        # retrieve the times and energy values        
        times = raw_df_cl['#Time']
        interval_sec = int(np.round(times.values[3] - times.values[2],0))
        numDataPoints = len(times)        
        duration_min = np.round(times.values[-1] /60, 2)
        He = raw_df_cl['Watts']       # in MJ/m²
        Hv = raw_df_cl['Lux']         # in Mlxh
        total_He = He.values[-1]
        total_Hv = Hv.values[-1]
        ill = (60 * total_Hv) / duration_min
        irr = (total_He*1e6) / (duration_min * 60)
         
        
        # interpolate the data
        if interpolation == 'none':   
            df_sp = raw_df_sp
            df_sp.columns = [float(col[:-3]) for col in df_sp.columns]

            df_cl = np.round(raw_df_cl,3)
            df_cl = df_cl[['Watts', 'Lux', '#Time', 'L','a','b','dE76','dE2000']]
            df_cl.columns = ['He_MJ/m2', 'Hv_Mlxh','t_sec', 'L*', 'a*','b*', 'dE76', 'dE00']  

            LCh = np.round(colour.Lab_to_LCHab(df_cl[['L*','a*','b*']].values).T,3)

            df_cl['C*'] = LCh[1]
            df_cl['h'] = LCh[2]

            df_cl = df_cl[['He_MJ/m2', 'Hv_Mlxh','t_sec', 'L*','a*','b*','C*','h','dE76','dE00']]
                                 
        else:
            # define abscissa units
            abs_scales = {'He': He, 'Hv': Hv, 't': times}
            abs_scales_name = {'He': 'He_MJ/m2', 'Hv': 'Hv_Mlxh', 't': 't_sec'}           

            #  define the abscissa range according to the choosen step value
            wanted_x = np.arange(0, abs_scales[interpolation].values[-1], step)            
                          
            # create a dataframe for the energy and time on the abscissa axis        
            df_abs = pd.DataFrame({'t_sec':times, 'He_MJ/m2': He,'Hv_Mlxh': Hv})
            df_abs = df_abs.set_index(abs_scales_name[interpolation])

            # create an interp1d function for each column of df_abs
            abs_interp_functions = [sip.interp1d(df_abs.index, df_abs[col], kind='linear', fill_value='extrapolate') for col in df_abs.columns]            

            # interpolate all columns of df_abs simultaneously
            interpolated_abs_data = np.vstack([f(wanted_x) for f in abs_interp_functions]).T

            # Create a new DataFrame with the interpolated data
            interpolated_df = pd.DataFrame(interpolated_abs_data, index=wanted_x, columns=df_abs.columns)

            interpolated_df.index.name = abs_scales_name[interpolation]
            interpolated_df = interpolated_df.reset_index()            
            
            # modify the columns names according to the choosen abscissa unit
            raw_df_sp.columns = abs_scales[interpolation]
            
            # interpolate the reflectance values according to the wavelength and the abscissa range
            interp = RegularGridInterpolator((raw_df_sp.index,raw_df_sp.columns), raw_df_sp.values)

            pw, px = np.meshgrid(wanted_wl, wanted_x, indexing='ij')     
            interp_data = interp((pw, px))    
            df_sp_interp = pd.DataFrame(interp_data, index=wanted_wl, columns=wanted_x)
                            
            # name the columns
            df_sp_interp.columns.name = abs_scales_name[interpolation] 

            # empty list to store XYZ values
            XYZ = []

            # calculate the LabCh values
            for col in df_sp_interp.columns:
                sd = colour.SpectralDistribution(df_sp_interp[col], wanted_wl)
                XYZ.append(colour.sd_to_XYZ(sd, cmfs, illuminant=D65))        

            XYZ = np.array(XYZ)

            Lab = np.array([colour.XYZ_to_Lab(d / 100, d65) for d in XYZ])
            LCh = np.array([colour.Lab_to_LCHab(d) for d in Lab])
                    
            L = []
            a = []
            b = []
            C = []
            h = []

            [L.append(np.round(i[0],3)) for i in Lab]
            [a.append(np.round(i[1],3)) for i in Lab]
            [b.append(np.round(i[2],3)) for i in Lab]
            [C.append(np.round(i[1],3)) for i in LCh]
            [h.append(np.round(i[2],3)) for i in LCh]

                
            # compute the delta E values
            dE76 = np.round(np.array([colour.delta_E(Lab[0], d, method="CIE 1976") for d in Lab]),3)
            dE00 = np.round(np.array([colour.delta_E(Lab[0], d) for d in Lab]),3)

            # calculate dR_VIS and dR
            dR_vis = []                                                            # empty list to store the dRvis values                                   
            df_sp_vis = df_sp_interp.loc[400:740]                                  # reflectance spectra in the visible range
            sp_initial = (df_sp_vis.iloc[:,0].values) * 100                        # initial spectrum
        
            for col in df_sp_vis.columns:
                sp = df_sp_vis[col]
                dR_val = np.sum(np.absolute(sp*100-sp_initial)) / len(sp_initial)           
                dR_vis.append(np.round(dR_val,2))      
                        
            # create the colorimetric dataframe
            df_cl = pd.DataFrame({'L*': L,
                                'a*': a,
                                'b*': b,
                                'C*': C,
                                'h': h,
                                'dE76': dE76,
                                'dE00': dE00,
                                'dR_vis': dR_vis
                                })                
            
            # concatenate the energy values with df_cl
            df_cl = pd.concat([interpolated_df,df_cl], axis=1)

            # rename spectral dataframe
            df_sp = df_sp_interp


            ###### CREATE INFO DATAFRAME ####### 

            # retrieve the information about the analysis        
            lookfor = '#Time'
            file_raw_cl = open(raw_file_cl).read()

            infos = file_raw_cl[:file_raw_cl.index(lookfor)].splitlines()
            dic_infos = {}

            for i in infos:             
                key = i[2:i.index(':')]
                value = i[i.index(':')+2:]              
                dic_infos[key]=[value]

            df_info = pd.DataFrame.from_dict(dic_infos).T 
            

            if db == False:          

                df_info.loc['duration_min'] = duration_min
                df_info.loc['interval_sec'] = interval_sec
                df_info.loc['numDataPoints'] = numDataPoints 
                df_info.loc['totalDose_MJ/m2'] = np.round(total_He, 3)
                df_info.loc['totalDose_Mlxh'] = np.round(total_Hv, 3)
                df_info.loc['illuminance_Mlx'] = np.round(ill, 4)
                df_info.loc['irradiance_W/m2'] = int(irr)

                current = int(df_info.loc['Curr'].values[0].split(' ')[0])
                df_info.loc['Curr'] = current
                df_info = df_info.rename(index={'Curr': 'current_mA'})

                df_info.index.name = 'parameters'
                df_info.columns = ['values']  

            else:
                
                if 'project_id' in db_objects.columns:
                    db_objects = db_objects.drop('project_id', axis=1)
                
                info_parameters = [
                "[SINGLE MICROFADING ANALYSIS]",
                "authors",
                "date_time",
                "comment",
                "[PROJECT INFO]"] + list(db_projects.columns) + ["[OBJECT INFO]"] + list(db_objects.columns) + MFT_info_template.device_info + MFT_info_template.analysis_info + MFT_info_template.beam_info

                date_time = pd.to_datetime(df_info.loc['Date'].values[0])
                date = date_time.date()
                project_id = raw_file_cl.stem.split(' ')[0]
                object_id = raw_file_cl.stem.split(' ')[1]
                project_info = list(db_projects.query(f'project_id == "{project_id}"').values[0])
                object_info = list(db_objects.query(f'object_id == "{object_id}"').values[0])


                # device info values
                device = 'Fotonowy-MFT'
                LED_nb = df_info.loc['LED'].values[0]
                device_info = [
                    " ",
                    device, 
                    'none',
                    'none',
                    'none',
                    '0° : 45°',
                    'unknown',
                    'unknown',
                    'none',
                    'none',
                    'Thorlabs, FT030',
                    f'LED{LED_nb}',
                    'none',
                    'none',
                    'none',
                    'Fotonowy fotolon PTFE'
                ]


                # analysis info values
                
                meas_nb = '01'
                meas_id = f'MF.{object_id}.{meas_nb}'
                spec_comp = 'SCE_excluded'

                int_time = df_info.loc['Sample integration time [ms]'].values[0]
                fwhm = MFT_info_template.beam_FWHM[LED_nb]

                area = pi * (((fwhm/1e6)/2)**2)
                power = np.round((irr * area) * 1e3, 3)
                lum = np.round(area * (ill * 1e6),3)
                current = int(df_info.loc['Curr'].values[0].split(' ')[0])
                
                group = ""
                group_description = ""
                

                analysis_info = [
                    " ",
                    meas_id,
                    group, 
                    group_description,
                    background,
                    spec_comp,
                    int_time,
                    average, 
                    duration_min, 
                    interval_sec,
                    "1",
                    "D65",
                    "10deg",
                ]

                # beam info                

                beam_info = [
                    " ",
                    'none',
                    'none',
                    fwhm,
                    current,
                    power,
                    lum,
                    np.int32(irr),
                    np.round(ill,3)                    
                ]

                info_values = [
                    " ",
                    authors,
                    date_time,
                    comment,
                    " "] + project_info + [" "] + object_info + device_info + analysis_info + beam_info

                df_info = pd.DataFrame({'parameters':info_parameters})
                df_info["values"] = pd.Series(info_values)

            df_info = df_info.set_index('parameters')

            # define the output filename
            if filenaming == 'none':
                filename = stemName

            elif filenaming == 'auto':
                group = stemName.split('_')[2]
                group_description = stemName.split('_')[3]
                object_type = df_info.loc['object_type']['values']
                filename = f'{project_id}_{meas_id}_{group}_{group_description}_{object_type}_{date}'

            elif isinstance(filenaming, list):                
                filename = "_".join([df_info.loc[x]['values'] for x in filenaming])
               
               
            # export the dataframes to an excel file
            with pd.ExcelWriter(Path(folder) / f'{filename}.xlsx') as writer:

                df_info.to_excel(writer, sheet_name='info', index=True)
                df_cl.to_excel(writer, sheet_name="CIELAB", index=False)

                if interpolation == 'none':
                    df_sp.to_excel(writer, sheet_name="spectra", index=True, index_label=f'wl-nm_t-sec')

                else:
                    df_sp.to_excel(writer, sheet_name="spectra", index=True, index_label=f'wl-nm_{abs_scales_name[interpolation].replace("_", "-")}')

            return 
        



