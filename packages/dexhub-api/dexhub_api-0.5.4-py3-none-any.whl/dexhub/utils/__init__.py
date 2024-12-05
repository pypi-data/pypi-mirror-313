
import os 
import numpy as np 
import zmq 
from threading import Thread
from queue import Queue
import matplotlib.pyplot as plt
import time
from PIL import Image
import math
from scipy.spatial.transform import Rotation as R
from typing import * 

class time_profiler:

    def __init__(self): 
        """
        class that profiles the time taken by different functions 
        
        it'll be called as follows: 
        profiler = time_profiler()
        profiler.start("function_name")
        # do something
        profiler.end("function_name") <-- and this will print the time taken by the function 
        """
        self.timings = {}
        self.start_time = 0

    def start(self, name):
        self.start_time = time.time()
        self.timings[name] = 0

    def end(self, name):
        self.timings[name] = time.time() - self.start_time
        if os.getenv("MJ_DEBUG", False):
            print(f"{name} took {self.timings[name]}")

def pprint(msg, time): 

    if os.getenv("MJ_DEBUG", False):
        print(msg, time)

YUP2ZUP = np.array([[1, 0, 0, 0], 
                    [0, 0, -1, 0], 
                    [0, 1, 0, 0],
                    [0, 0, 0, 1]], dtype = np.float64)

def segmentation_mask_to_rgb(mask, color_map=None):
    """
    Convert a segmentation mask to an RGB image for debugging.
    
    Args:
        mask (numpy.ndarray): 2D array with segmentation mask values.
        color_map (dict): Optional. A dictionary mapping mask values to RGB tuples. 
                          If None, a default color map will be generated.
                          
    Returns:
        PIL.Image.Image: The RGB image.
    """
    # Generate a color map if none is provided
    if color_map is None:
        unique_values = np.unique(mask)
        np.random.seed(42)  # For reproducibility
        color_map = {val: tuple(np.random.randint(0, 256, 3).tolist()) for val in unique_values}
     
    # Create an RGB image using the color map
    rgb_image = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
    
    for val, color in color_map.items():
        rgb_image[mask == val] = color

    return Image.fromarray(rgb_image)


def data_receiver(socket, data_queue):
    while True:
        msg = socket.recv_pyobj()  # Receive the image data
        data_queue.put(msg)

def image_rendering_process(addr):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(addr)
    socket.setsockopt(zmq.SUBSCRIBE, b'')

    data_queue = Queue()

    # Start the data receiving thread
    receiver_thread = Thread(target=data_receiver, args=(socket, data_queue))
    receiver_thread.daemon = True
    receiver_thread.start()

    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()

    # Initialize the image plot with some dummy data
    img = np.zeros((480, 1280, 3), dtype=np.uint8)  # Assuming a 480x640 RGB image
    im_plot = ax.imshow(img)

    plt.tight_layout()

    while True:
        while not data_queue.empty():
            img_data = data_queue.get()
            print("here", img_data.shape)

            # Update the image plot with the new image data
            im_plot.set_data(img_data)

            # If you want to adjust the color limits, you can do it like this:
            # im_plot.set_clim(vmin=-1, vmax=2)  # Adjust these limits based on your data

            ax.draw_artist(im_plot)
            fig.canvas.flush_events()  # Update the plot

        time.sleep(0.01)  # Small sleep to prevent overloading the CPU


def get_random_perturbed_pose(
    old_pose: np.ndarray,
    reset_spec: Dict[str, Any],
) -> np.ndarray:
    new_pose = old_pose.copy()
    
    # perturb position
    min_pos = np.array(reset_spec['min_pos'])
    max_pos = np.array(reset_spec['max_pos'])
    new_pose[:3] = old_pose[:3] + np.random.rand(3) * (max_pos - min_pos) + min_pos

    # get angle perturbation as euler angles
    max_euler = np.array(reset_spec['max_rot'])
    min_euler = np.array(reset_spec['min_rot'])
    euler_perturbation = np.random.rand(3) * (max_euler - min_euler) + min_euler

    # perturb orientation by euler angles
    r = R.from_euler('xyz', euler_perturbation, degrees=True)
    old_rot = R.from_quat(old_pose[3:])
    new_rot = r * old_rot
    new_pose[3:] = new_rot.as_quat()

    return new_pose



def convert_to_z_up(quaternion_str, table_height):
    # Parse the input string
    x, y, z, rw, rx, ry, rz = map(float, quaternion_str.split(','))

    mat = np.eye(4)
    mat[:3, :3] = R.from_quat([rw, rx, ry, rz], scalar_first=True).as_matrix()
    mat[:3, -1] = np.array([x, y, z])

    new_mat = YUP2ZUP @ mat 

    new_pos = new_mat[:3, -1]
    new_pos[2] -= table_height
    new_quat = R.from_matrix(new_mat[:3, :3]).as_quat(scalar_first=True)

    result = np.concatenate((new_pos, new_quat))

    return result

# Define rotation matrices for each axis
def rot_x(angle):
    angle = math.radians(angle)
    return np.array([[1, 0, 0, 0],
                     [0, math.cos(angle), -math.sin(angle), 0],
                     [0, math.sin(angle), math.cos(angle), 0],
                     [0, 0, 0, 1]])#.type(np.float64)

def rot_y(angle):
    angle = math.radians(angle)
    return np.array([[math.cos(angle), 0, math.sin(angle), 0],
                     [0, 1, 0, 0],
                     [-math.sin(angle), 0, math.cos(angle), 0],
                     [0, 0, 0, 1]])#.astype(np.float64)

def rot_z(angle):
    angle = math.radians(angle)
    return np.array([[math.cos(angle), -math.sin(angle), 0, 0],
                    [math.sin(angle), math.cos(angle), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])#.astype(np.float64)

def sm2mat(sm_state, type = "right"): 
    # convert roll pitch yaw to rotation matrix

    if type == "right": 
        roll = - sm_state.roll * 0.1
        pitch = - sm_state.pitch * 0.1
        yaw = - sm_state.yaw * 0.1
        
        rot_mat = rot_z(yaw) @ rot_y(pitch) @ rot_x(roll)

    else:
        roll = - sm_state.roll * 0.1
        pitch = - sm_state.pitch * 0.1
        yaw = - sm_state.yaw * 0.1
        
        rot_mat = rot_z(yaw) @ rot_y(- roll) @ rot_x(pitch)

    mat = np.eye(4)
    mat[:3, :3] = rot_mat[:3, :3]
    # translations 
    mat[:3, -1] = np.array([sm_state.x * 0.001, sm_state.y* 0.001, sm_state.z* 0.001])

    return mat

