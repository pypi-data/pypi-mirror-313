import meshcat
import meshcat.geometry as g
import meshcat.transformations as tf
import os
import mujoco 
from scipy.spatial.transform import Rotation as R
import numpy as np 
from meshcat.animation import Animation
from dm_control import mjcf
from io import BytesIO

class MJCMeshcat: 

    def __init__(self): 

        # Create a new visualizer
        self.vis = meshcat.Visualizer()
        self.base_t = dict() 
        self.materials = dict() 
        self.meshes = dict()

        self.anim = Animation()
        self.cnt = 0 

    def parse_mjcf(self, mjcf: mjcf.Element): 

        for material in mjcf.asset.find_all("material"):
            name = material.full_identifier 
            rgba = material.rgba
            texture = material.texture

            if texture is not None and texture != "grid": 
                texture_contents = BytesIO(texture.file.contents)
            else: 
                texture_contents = None
            
            self.register_material(name, texture_contents, rgba)

        for mesh in mjcf.asset.find_all("mesh"):

            print(mesh)
            input_io = BytesIO(mesh.file.contents)

            try: 
                scale = mesh.scale[0]
            except:
                scale = 1.0

            # print(mesh.name, mesh.file.extension, scale)
            self.register_mesh(mesh.name, mesh.file.extension, input_io, scale)


        for body in mjcf.worldbody.find_all("body"):
            if body.geom is None: 
                continue
            for geom in body.geom:
                # print(dir(geom))
                # print(geom.__class__)
                # for method in dir(geom):
                #     print(method, ':', str(getattr(geom, method)))
                if "collision" in str(geom.dclass): 
                    pass
                else:
                    try: 
                        if geom.material is None: 
                            # print(str(geom.dclass))
                            material = geom.dclass.geom.material 
                        else:
                            material = geom.material
                        self.register_geom(body.full_identifier, geom.mesh.name, material.full_identifier, geom.pos, geom.quat)
                    except Exception as e:
                        # print(body.full_identifier, geom.name, e)
                        pass 


    def register_material(self, material_name, texture_content, rgba):


        if texture_content is None and rgba is not None: 
            # convert rgba to hex like 0xffffff
            import matplotlib.colors as mcolors
            hex = mcolors.to_hex(rgba)
            hex = hex.replace("#", "0x")

            self.materials[material_name] = g.MeshLambertMaterial(color=hex)

        elif texture_content is not None and rgba is None:
            self.materials[material_name] = g.MeshLambertMaterial(
                map=g.ImageTexture(g.PngImage.from_stream(texture_content))
            )


    def register_mesh(self, mesh_name, mesh_type, mesh_content, mesh_scale = 1.0):

        # Load the mesh
        if "stl" in mesh_type: 
            mesh = g.StlMeshGeometry.from_stream(mesh_content)
        elif "obj" in mesh_type:
            mesh = g.ObjMeshGeometry.from_stream(mesh_content)
        else: 
            mesh = g.MeshGeometry()

        self.meshes[mesh_name] = {
            "mesh": mesh,
            "scale": mesh_scale, 
        }


        
    def register_geom(self, body_name, mesh_name, material_name, pos, quat):
        

        # Get the mesh
        mesh = self.meshes[mesh_name]["mesh"]
        scale = self.meshes[mesh_name]["scale"]

        # Get the material
        if material_name not in self.materials: 
            material = None 
            
        else:
            material = self.materials[material_name]

        # Get the position and orientation
        mat = np.eye(4)
        if quat is not None:    
            mat[:3, :3] = R.from_quat(quat, scalar_first=True).as_matrix()
        if pos is not None: 
            mat[:3, -1] = pos
        
        mat[:3, :3] *= scale

        self.base_t[f"{body_name}/{mesh_name}"] = mat


        # Create the geometry

        self.vis[f"{body_name}/{mesh_name}"].set_object(mesh, material)
        # geom.set_transform(tf.quaternion_matrix(quat))
        self.vis[f"{body_name}/{mesh_name}"].set_transform(self.base_t[f"{body_name}/{mesh_name}"])

        # # Add the geometry to the visualizer
        print(f"Added {body_name}/{mesh_name} to the visualizer")


    def set_body_transform(self, body_name, pos, quat, frame): 

        if frame is None: 
            frame = self.vis 

        mat = np.eye(4)
        if quat is not None:    
            mat[:3, :3] = R.from_quat(quat, scalar_first=True).as_matrix()
        if pos is not None: 
            mat[:3, -1] = pos

        frame[body_name].set_transform(mat)


    @property
    def bodies(self): 
        # return the list of bodies
        # you can extract it from self.vis keys which are {body_name}/{geom_name}

        d =  [] 
        for key in self.base_t.keys(): 
            c1, c2, c3 = key.split("/")
            d.append(f"{c1}/{c2}")

        return d
        

    def set_keypoints(self, body_transforms):

        with self.anim.at_frame(self.vis, self.cnt) as frame:
            for transform in body_transforms: 
                body_name, (pos, quat) = transform
                self.set_body_transform(body_name, pos, quat, frame)

        self.cnt += 1

    def get_html(self): 
        self.vis.set_cam_pos([0, 0.75, 0.5])
        self.vis.set_cam_target([0, 0, 0])

        self.vis.set_animation(self.anim, play=True, repetitions = 100) 

        html = self.vis.static_html()
        # image = self.vis.get_image()
        # save the image as a file
        # with open("./thumbnail.png", "wb") as f:
        #     f.write(image)
        return html 





if __name__ == "__main__":

    mjc = MJCMeshcat()