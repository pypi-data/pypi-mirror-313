import pandas as pd
from pathlib import Path
from typing import Optional
import json
import os
from ipywidgets import Layout
import ipywidgets as ipw
from IPython.display import display, clear_output

style = {"description_width": "initial"}


class DB:
    def __init__(self, config_file=Path(__file__).parent / 'db_config.json') -> None:
        self.config_file =  config_file
        self.folder_db = Path(self.load_folder_db())


    def add_new_object(self):
        """Add a new object in the DB_objects.csv file"""

        db_projects = self.get_db(db='projects')
        projects_list = ['noProject'] + list(db_projects['project_id'].values)

        db_objects = self.get_db(db='objects')
        existing_columns = list(db_objects.columns)

        creators_file = open(self.folder_db / r'object_creators.txt', 'r').read()
        creators = creators_file.split("\n")
        
        types_file = open(self.folder_db / r'object_types.txt', 'r').read()
        types = types_file.split("\n")        

        techniques_file = open(self.folder_db / r'object_techniques.txt', 'r').read()
        techniques = techniques_file.split("\n")        

        supports_file = open(self.folder_db  / r'object_supports.txt', 'r').read()
        supports = supports_file.split("\n")        

        owners_file = open(self.folder_db / r'institutions.txt', 'r').read()
        owners = owners_file.split("\n")
               

        # Define ipython widgets

        project_id = ipw.Combobox(
            #value = ' ',
            placeholder='Project',
            options = projects_list,
            description = 'Project id',
            ensure_option=False,
            disabled=False,
            layout=Layout(width="99%", height="30px"),
            style=style,
        )

        object_id = ipw.Text(        
            value='',
            placeholder='Inv. N°',
            description='Id',
            disabled=False,
            layout=Layout(width="99%", height="30px"),
            style=style,   
        )

        object_category = ipw.Dropdown(
            options=['heritage','model','reference','sample'],
            value='heritage',
            description='Category',
            disabled=False,
            layout=Layout(width="99%", height="30px"),
            style=style,
        )    

        object_creator = ipw.Combobox(
            placeholder = 'Surname, Name',
            options = creators,
            description = 'Creator',
            ensure_option=False,
            disabled=False,
            layout=Layout(width="99%", height="30px"),
            style=style,
        ) 

        object_date = ipw.Text(
            value='',
            placeholder='Enter a date',
            description='Date',
            disabled=False,
            layout=Layout(width="99%", height="30px"),
            style=style,         
        )  

        object_owner = ipw.Combobox(
            placeholder = 'Enter an institution/owner',
            options = owners,
            description = 'Object owner',
            ensure_option = False,
            disabled = False,
            layout=Layout(width='99%',height="30px"),
            style = style

        )

        object_title = ipw.Textarea(        
            value='',
            placeholder='Enter the title',
            description='Title',
            disabled=False,
            layout=Layout(width='99%',height="100%"),
            style=style,   
        )  

        object_name = ipw.Text(        
            value='',
            placeholder='Enter a short object name without space',
            description='Name',
            disabled=False,
            layout=Layout(width='99%',height="30px"),
            style=style,   
        )

        object_type = ipw.Combobox(
            placeholder = 'General classification',
            options = types,
            description = 'Type',
            ensure_option=False,
            disabled=False,
            layout=Layout(width="99%", height="30px"),
            style=style,
        )

        object_technique = ipw.SelectMultiple(
            placeholder = 'Enter techniques/materials',
            options = techniques,
            description = 'Technique',
            ensure_option=False,
            disabled=False,
            layout=Layout(width="99%", height="160px"),
            style=style,
        )   

        object_support = ipw.Combobox(
            placeholder = 'Enter a material',
            options = supports,
            description = 'Support',
            ensure_option=False,
            disabled=False,
            layout=Layout(width="99%", height="30px"),
            style=style,
        )

        recording = ipw.Button(
            description='Create record',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click me',
            #layout=Layout(width="50%", height="30px"),
            #style=style,
            #icon='check' # (FontAwesome names without the `fa-` prefix)
        )        
        

        button_record_output = ipw.Output()       
    

        object_color = ipw.Combobox(
            description = 'Color',
            placeholder = 'Optional',
            ensure_option=False,
            disabled=False,
            layout=Layout(width="99%", height="30px"),
            style=style,
        )        
                
        # Combobox for additional parameters (if any)
        additional_params = [col for col in existing_columns if col not in [
            'project_id',
            'object_id',
            'object_category',
            'object_type',
            'object_technique',
            'object_title',
            'object_name',
            'object_creator',
            'object_date',
            'object_owner',
            'object_support']]

        additional_param_widgets = {}
        for param in additional_params:
            additional_param_widgets[param] = ipw.Combobox(
                description=param,
                options=[],  # You can populate this with options if needed
                placeholder=f"Enter {param} value"
            )        


        def button_record_pressed(b):
            """
            Save the object info in the object database file (DB_objects.csv).
            """

            with button_record_output:
                button_record_output.clear_output(wait=True)

                db_objects_file = self.folder_db / 'DB_objects.csv'
                db_objects = pd.read_csv(db_objects_file)                

                creators_file = open(self.folder_db  / r'object_creators.txt', 'r').read().splitlines()
                creators = creators_file 

                owners_file = open(self.folder_db  / r'institutions.txt', 'r').read().splitlines()
                owners = owners_file             

                types_file = open(self.folder_db / r'object_types.txt', 'r').read().splitlines()
                types = types_file       

                techniques_file = open(self.folder_db / r'object_techniques.txt', 'r').read().splitlines()
                techniques = techniques_file        

                supports_file = open(self.folder_db  / r'object_supports.txt', 'r').read().splitlines()
                supports = supports_file                        

                new_row = pd.DataFrame({                    
                    'project_id': project_id.value,
                    'object_id' : object_id.value,                   
                    'object_category': object_category.value, 
                    'object_type': object_type.value, 
                    "object_technique": "_".join(object_technique.value),
                    "object_title": object_title.value,
                    'object_name': object_name.value,
                    'object_creator': object_creator.value,                        
                    'object_date': object_date.value,
                    'object_owner': object_owner.value,
                    'object_support': object_support.value},                       
                    index=[0] 
                    ) 


                if object_creator.value not in creators:
                    creators.append(str(object_creator.value))
                    creators = sorted(creators, key=str.casefold) 
                    
                    with open(self.folder_db / 'object_creators.txt', 'w') as f:
                        f.write('\n'.join(creators).strip())
                    f.close()

                if object_owner.value not in owners:                       
                    owners.append(str(object_owner.value))         
                    owners = sorted(owners)   

                    with open(self.folder_db / 'institutions.txt', 'w') as f:
                        f.write('\n'.join(owners).strip())  
                    f.close() 

                
                if object_support.value not in supports:
                    supports.append(str(object_support.value))
                    supports = sorted(supports, key=str.casefold)                    

                    with open(self.folder_db / 'object_supports.txt', 'w') as f:
                        f.write('\n'.join(supports).strip()) 
                    f.close()

                if object_type.value not in types:
                    types.append(str(object_type.value))
                    types = sorted(types, key=str.casefold)

                    with open(self.folder_db / 'object_types.txt', 'w') as f:
                        f.write('\n'.join(types).strip())
                    f.close()                                 
                

                # Add additional parameters to the new record
                for param, widget in additional_param_widgets.items():
                    new_row[param] = widget.value

                db_objects_new = pd.concat([db_objects, new_row],)
                db_objects_new.to_csv(db_objects_file, index= False)
                print(f'Object {object_id.value} added to database.')

        recording.on_click(button_record_pressed)

        display(ipw.HBox([ipw.VBox([object_id,project_id,object_creator,object_date,object_owner,object_title, object_name],layout=Layout(width="40%", height="300px"), style=style,),
                        ipw.VBox([object_category,object_type,object_technique,object_support,object_color],layout=Layout(width="40%", height="300px"), style=style),
                        ]))  

        display(*[widget for widget in additional_param_widgets.values()])
        display(ipw.HBox([recording, button_record_output]))
        

    def add_new_person(self):
        """Record a new person in the persons.txt file
        """

        # Function to get the existing initials from the file
        def get_existing_initials(file_path):
            try:
                with open(file_path, 'r') as file:
                    # Reading the file line by line and storing the initials in a set
                    existing_initials = set()
                    for line in file:
                        initials = line.strip().split(' : ')[1]
                        existing_initials.add(initials)
                    return existing_initials
            except FileNotFoundError:
                # If the file does not exist, return an empty set
                return set()
            
        # Function to update the text file if the initials are unique
        def update_text_file(file_path, name, surname, initials):
            # Check if the initials already exist
            existing_initials = get_existing_initials(file_path)
            
            if initials in existing_initials:
                print(f"Initials '{initials}' already exist. Please use different initials.")
            else:
                # If the initials are unique, add the new entry
                with open(file_path, 'a') as file:
                    file.write(f"{name}, {surname} : {initials}\n")
                print(f"Added: {name}, {surname} : {initials}")


        # Define ipython widgets
        name_widget = ipw.Text(        
            value='',
            placeholder='Enter a name',
            description='Name',               
        )

        surname_widget = ipw.Text(        
            value='',
            placeholder='Enter a surname',
            description='Surname',             
        )
        
        initials_widget = ipw.Text(        
            value='',
            placeholder='Enter initials in capital letters',
            description='Initials',             
        )

        recording = ipw.Button(
            description='Create record',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click me',            
        )        
        

        button_record_output = ipw.Output()

        def button_record_pressed(b):
            """
            Save the person info in the persons.txt file.
            """

            button_record_output.clear_output(wait=True)

            name = name_widget.value.strip()
            surname = surname_widget.value.strip()
            initials = initials_widget.value.strip()

            with button_record_output:

                if name and surname and initials: # ensure all fields are filled
                    update_text_file(self.folder_db / 'persons.txt', name, surname, initials)
                else:
                    
                    print("Please enter all fields (Name, Surname, Initials)")

            

        recording.on_click(button_record_pressed)

        display(name_widget,surname_widget,initials_widget)
        display(ipw.HBox([recording, button_record_output]))


    def add_new_project(self):
        """Add a new project in the DB_projects.csv file"""

        db_projects = self.get_db(db='projects')
        existing_columns = list(db_projects.columns)
        institutions = sorted(set(db_projects['institution']))
        
        with open(self.folder_db / 'persons.txt') as f:
            persons = f.read().splitlines()
            f.close()

        persons = [x.split(':')[0] for x in persons]

        # Define ipython widgets
        project_Id = ipw.Text(        
            value='',
            placeholder='Type something',
            description='Project Id',
            disabled=False,
            layout=Layout(width="95%", height="30px"),
            style=style,   
        )

        institution = ipw.Combobox(
            placeholder = 'Enter an institution',
            options = institutions,  
            description = 'Institution',
            ensure_option=False,
            disabled=False,
            layout=Layout(width="95%", height="30px"),
            style=style,
        )
        
        startDate = ipw.DatePicker(
            description='Start date',
            disabled=False,
            layout=Layout(width="90%", height="30px"),
            style=style,
        )

        endDate = ipw.DatePicker(
            description='End date',
            disabled=False,
            layout=Layout(width="90%", height="30px"),
            style=style,
        )

        PL = ipw.Dropdown(
            options=persons,
            value=persons[0],
            description='Project leader',
            disabled=False,
            layout=Layout(width="90%", height="30px"),
            style=style,
        )
        

        recording = ipw.Button(
            description='Create record',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click me',
            #layout=Layout(width="50%", height="30px"),
            #style=style,
            #icon='check' # (FontAwesome names without the `fa-` prefix)
        )
        

        project_keyword = ipw.Text(
            placeholder = 'Describe project in 1 or 2 words',
            description = 'Project keywords',
            disabled = False,
            layout=Layout(width="95%", height="40px"),
            style = style,
        )

        # Combobox for additional parameters (if any)
        additional_params = [col for col in existing_columns if col not in ['project_id', 'institution', 'start_date', 'end_date', 'project_leader', 'keywords']]
        additional_param_widgets = {}
        for param in additional_params:
            additional_param_widgets[param] = ipw.Combobox(
                description=param,
                options=[],  # You can populate this with options if needed
                placeholder=f"Enter {param} value"
            )

        button_record_output = ipw.Output()


        def button_record_pressed(b):
            """
            Save the project info in the project database file (DB_projects.csv).
            """

            with button_record_output:
                button_record_output.clear_output(wait=True)

                Projects_DB_file = self.folder_db / 'DB_projects.csv'
                Projects_DB = pd.read_csv(Projects_DB_file)  

                institutions = open(self.folder_db  / r'institutions.txt', 'r').read().splitlines()
                
                new_row = pd.DataFrame({'project_id':project_Id.value,
                        'institution':institution.value, 
                        'start_date':startDate.value, 
                        'end_date':endDate.value,
                        'project_leader':PL.value,                        
                        'keywords':project_keyword.value},                       
                        index=[0] 
                        )  
                
                if institution.value not in institutions:                       
                    institutions.append(str(institution.value))         
                    institutions = sorted(institutions)   

                    with open(self.folder_db / 'institutions.txt', 'w') as f:
                        f.write('\n'.join(institutions).strip())  
                    f.close()                
                

                # Add additional parameters to the new record
                for param, widget in additional_param_widgets.items():
                    new_row[param] = widget.value

                Projects_DB_new = pd.concat([Projects_DB, new_row],)
                Projects_DB_new.to_csv(Projects_DB_file, index= False)
                print(f'Project {project_Id.value} added to database.')

        recording.on_click(button_record_pressed)


        # Display the widgets
        display(ipw.HBox([
            ipw.VBox([
                ipw.HBox([
                    ipw.VBox([project_Id,institution, project_keyword],layout=Layout(width="60%", height="95%")),
                    ipw.VBox([startDate,endDate, PL],layout=Layout(width="60%", height="95%")),
                    ]),                
                ], layout=Layout(width="50%", height="100%")),                        
            ], layout=Layout(width="100%", height="110%"))
        ) 

        display(*[widget for widget in additional_param_widgets.values()])
        display(ipw.HBox([recording, button_record_output]))


    def create_db(self, folder_path):      

        self.folder_db = folder_path
        self.save_folder_db(folder_path)

        # create the project database
        db_project = pd.DataFrame(columns=['project_id','institution','start_date','end_date','project_leader','keywords'])
        db_project.to_csv(Path(folder_path) / 'DB_projects.csv', index=False)

        # create the object database
        db_object = pd.DataFrame(columns=['object_id','object_category','object_type','object_technique','object_title','object_name','object_creator','object_date','object_owner','object_support','colorants','colorants_name','binding','ratio','thickness_um','color','status','project_id'])
        db_object.to_csv(Path(folder_path) / 'DB_objects.csv', index=False)

        print(f'DB_projects.csv and DB_objects.csv created in the following folder: {folder_path}')

        # create several text files
        with open(Path(folder_path) / 'object_creators.txt', 'w') as f:
            pass

        with open(Path(folder_path) / 'object_techniques.txt', 'w') as f:
            f.write("China ink\n")
            f.write("acrylinc\n")
            f.write("aquatinte\n")
            f.write("black ink\n")
            f.write("black pencil\n")
            f.write("chalk\n")
            f.write("charcoal\n")
            f.write("monotypie\n")
            f.write("dye\n")
            f.write("felt-tip ink\n")
            f.write("frescoe\n")
            f.write("gouache\n")
            f.write("ink\n")
            f.write("linoleum print\n")
            f.write("lithograh\n")
            f.write("mezzotinte\n")
            f.write("oil paint\n")
            f.write("pastel\n")
            f.write("tin-glazed\n")
            f.write("watercolor\n")
            f.write("wood block print\n")        

        with open(Path(folder_path) / 'object_types.txt', 'w') as f:            
            f.write("banknote\n")
            f.write("book\n")
            f.write("BWS\n")       
            f.write("ceramic\n")
            f.write("colorchart\n")
            f.write("drawing\n")
            f.write("notebook\n")
            f.write("paint-out\n")
            f.write("painting\n")
            f.write("photograph\n")
            f.write("print\n")
            f.write("sculpture\n")
            f.write("seals\n")
            f.write("spectralon\n")
            f.write("tapistry\n")
            f.write("textile\n")
            f.write("wallpainting\n")

        with open(Path(folder_path) / 'object_supports.txt', 'w') as f:
            f.write("blue paper\n")
            f.write("canvas\n")
            f.write("cardboard\n")
            f.write("ceramic\n")
            f.write("coloured paper\n")
            f.write("cotton\n")
            f.write("Japanese paper\n")
            f.write("none\n")
            f.write("opacity chart\n")
            f.write("paper\n")
            f.write("parchment\n")
            f.write("rag paper\n")
            f.write("stone\n")
            f.write("transparent paper\n")
            f.write("wax\n")
            f.write("wood\n")
            f.write("woodpulp paper\n")
            f.write("wool\n")            

        with open(Path(folder_path) / 'institutions.txt', 'w') as f:
            pass

        with open(Path(folder_path) / 'persons.txt', 'w') as f:
            pass


    def save_folder_db(self, folder_path):
        # Save folder path in a JSON file
        with open(self.config_file, 'w') as file:
            json.dump({"folder_db": folder_path}, file)


    def load_folder_db(self):
        # Load folder path from JSON file if it exists
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                config = json.load(file)
                return config.get("folder_db")
            
        else:
            print('Databases have not been created or were deleted.')
            return None
    

    def get_db(self, db:Optional[str] = 'all'):

        if (Path(self.folder_db) / 'DB_projects.csv').exists():
            db_projects = pd.read_csv(Path(self.folder_db) / 'DB_projects.csv')
        else:
            print(f'The DB_projects.csv file is not existing. Make sure to create one by running the function "create_DB" from the microfading package.')
            return
        
        if (Path(self.folder_db) / 'DB_objects.csv').exists():        
            db_objects = pd.read_csv(Path(self.folder_db) / 'DB_objects.csv')
        else:
            print(f'The DB_objects.csv file is not existing. Make sure to create one by running the function "create_DB" from the microfading package.')
            return

        if db == 'all':
            return db_projects, db_objects
        
        elif db == 'projects':
            return db_projects
        
        elif db == 'objects':
            return db_objects


    def update_db_projects(self, new: str, old:Optional[str] = None):

        if (Path(self.folder_db) / 'DB_projects.csv').exists():
            
            db_projects = self.get_db(db='projects')
            db_projects[new] = ''
            
            if old != None:
                if old in db_projects.columns:
                    db_projects.drop(old, axis=1, inplace=True)
                else:
                    print(f'The column {old} cannot be removed because it does not exist.')

            db_projects.to_csv(Path(self.folder_db) / 'DB_projects.csv',index=False)
            print('DB_projects successfully updated.')

        else:
            print('No databases have been created yet.')
        

    def update_db_objects(self, new: str, old:Optional[str] = None):

        if (Path(self.folder_db) / 'DB_objects.csv').exists():
            
            db_objects = self.get_db(db='objects')
            db_objects[new] = ''
            
            if old != None:
                if old in db_objects.columns:
                    db_objects.drop(old, axis=1, inplace=True)
                else:
                    print(f'The column {old} cannot be removed because it does not exist.')

            db_objects.to_csv(Path(self.folder_db) / 'DB_objects.csv',index=False)
            print('DB_projects successfully updated.')

        else:
            print('No databases have been created yet.')
