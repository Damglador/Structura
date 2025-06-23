try:
    import ujson as json
except:
    print("using built in json, but that is much slower, consider installing ujson")
    import json
import os
import copy
import numpy as np

class render_controller:
    def __init__(self):
        self.rc={"format_version": "1.8.0"}
        self.rc["render_controllers"]={}
        self.rcname = "controller.render.armor_stand.ghost_blocks" 
        self.rc["render_controllers"][self.rcname] = {}
        materials = [{"*": "Material.ghost_blocks"}]
        self.rc["render_controllers"][self.rcname]["materials"]=materials
        
        self.geometry= "{}"
        self.textures = "{}"
        self.geometry_arrays={}
    def add_model(self,name_raw,big=False):
        name=name_raw.replace(" ","_").lower()
        default=f"geometry.ghost_blocks_{name}"
        new_geo = "query.get_name == '{}' ? array.ghost_blocks_{}[variable.armor_stand.pose_index] : ({})".format(name_raw,name,"{}")
        if big:
            default="geometry.default"
            new_geo=f"array.{name}[ variable.armor_stand.pose_index ]"
        self.geometry_arrays[f"array.ghost_blocks_{name}"]=[default]
        for i in range(12):
            self.geometry_arrays[f"array.ghost_blocks_{name}"].append(f"Geometry.ghost_blocks_{name}_{i}")
        
        self.geometry=self.geometry.format(new_geo)
        new_texture = "query.get_name == '{}' ? Texture.ghost_blocks_{} : ({})".format(name_raw,name,"{}")
        self.textures = self.textures.format(new_texture)
        
    def export(self, pack_name):
            
        self.geometry = self.geometry.format("Geometry.default")
        self.textures = self.textures.format("Texture.default")
        self.rc["render_controllers"][self.rcname]["arrays"] = {}
        self.rc["render_controllers"][self.rcname]["arrays"]["geometries"]=self.geometry_arrays
        self.rc["render_controllers"][self.rcname]["geometry"] = self.geometry
        self.rc["render_controllers"][self.rcname]["textures"] = [self.textures]
        
        rc = "armor_stand.ghost_blocks.render_controllers.json"
        rcpath = "{}/render_controllers/{}".format(pack_name, rc)
        os.makedirs(os.path.dirname(rcpath), exist_ok = True)
        
        with open(rcpath, "w+") as json_file:
            json.dump(self.rc, json_file, indent=2)
        
