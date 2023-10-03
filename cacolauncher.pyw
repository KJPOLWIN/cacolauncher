import PySimpleGUI as sg
import subprocess
import json

data = None

with open("savedvalues.json", "r") as read_file:
    data = json.load(read_file)

mods = data["mods"]

mods_to_run = {

}

print(data["gzdoom_path"])

gzdoom_path = data["gzdoom_path"]

available_files_column = [
    [
        sg.Text("Available packages: ")
    ],
    [   
        sg.Listbox(values=list(mods.keys()), enable_events=True, size=(40, 20), key="available_packages")
    ]
]

torun_files_column = [
    [
        sg.Text("Packages to run: ")
    ],
    [
        sg.Listbox(
        values=[], enable_events=True, size=(40, 20), key="packages_to_run")
    ]
    
]

layout = [
    [
        [
            sg.Text("GZDoom filepath: "),
            sg.Input(gzdoom_path, size=(25, 1), enable_events=True, key="gzdoom_path"),
            sg.FileBrowse(key="gzdoom_path_choose")
        ]
    ],
    [
        sg.HorizontalSeparator()
    ],
    [
        [
            sg.Text("File name: "), 
            sg.Input(size=(25, 1), enable_events=True, key="new_filename"), 
            sg.FileBrowse()
        ],
        [
            sg.Text("Package name: "), 
            sg.Input(size=(25, 1), enable_events=True,
            key="new_pkg_name")
        ],
        [
            sg.Button("Save"),
            sg.Button("Cancel")
        ]
    ], 
    [
        sg.HorizontalSeparator()
    ],
    [
        sg.Column(available_files_column), 
        sg.Column(torun_files_column)
    ], 
    [
        sg.Button("Clear"), 
        sg.Button("Run")
    ],
]

window = sg.Window("CacoLauncher", layout)

while True:
    event, values = window.read()
    print(values)
    
    if event == sg.WIN_CLOSED:
        """dataToSave = {
            "gzdoom_path": gzdoom_path,
            "mods": mods
        }
        
        with open("savedvalues.json", "w") as write_file:
            json.dump(dataToSave, write_file)"""
        break;
    
    if event == "Cancel":
        window["new_filename"].update("")
        window["new_pkg_name"].update("")
    
    if event == "Save":
        mods.update({values["new_pkg_name"]: values["new_filename"]})
        
        window["new_filename"].update("")
        window["new_pkg_name"].update("")
        
        window["available_packages"].update(mods)
        
        dataToSave = {
            "gzdoom_path": gzdoom_path,
            "mods": mods
        }
        
        with open("savedvalues.json", "w") as write_file:
            json.dump(dataToSave, write_file)
    
    if event == "available_packages":
        if len(values["available_packages"]) > 0:
            mods_to_run.update({values["available_packages"][0]: mods.get(values["available_packages"][0])})
    
        window["packages_to_run"].update(mods_to_run)
        
    if event == "packages_to_run":
        mods_to_run.pop(values["packages_to_run"][0])
        window["packages_to_run"].update(mods_to_run)
    
    if event == "Clear":
        mods_to_run.clear()
        window["packages_to_run"].update(mods_to_run)

    if event == "gzdoom_path" or "gzdoom_path_choose":
        print(values)
        print(event)
        print(values["gzdoom_path"])
        gzdoom_path = values["gzdoom_path"]
        
        dataToSave = {
            "gzdoom_path": gzdoom_path,
            "mods": mods
        }
        
        with open("savedvalues.json", "w") as write_file:
            json.dump(dataToSave, write_file)
        
    if event == "Run":
        mods_filenames = list(mods_to_run.values())
        
        subprocess.run([gzdoom_path, "-file"] + mods_filenames)
        
window.close()