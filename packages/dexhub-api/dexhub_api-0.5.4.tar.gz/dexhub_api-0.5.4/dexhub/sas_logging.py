from typing import Dict, Any
from .data_types import Observation, Action, Transition, TransitionStorage
import os
from dexhub.upload import upload_file
import numpy as np 
import warnings
from datetime import datetime 
from .init import meta_data, transition_storage
# from .init import , viz
from typing import List
import io 
import pickle
import time 
import tempfile
import multiprocessing
import imageio
import mujoco 

def valid_checker(): 


    if meta_data["project"] is None:
        raise ValueError("Project name is not set.")
    if meta_data["robot"] is None:
        raise ValueError("Robot type is not set.")
    if meta_data["gripper"] is None:
        raise ValueError("Gripper type is not set.")
    if meta_data["teleoperation"] is None:
        raise ValueError("Teleoperation is not set.")
    if meta_data["task_description"] is None:
        # warning
        warnings.warn("Task description is not set.")


def log(obs: Observation, act: Action, data: mujoco.MjData = None) -> None:
    """
    Logs a transition to local memory using :class:`dexhub.data_types.TransitionStorage` class.

    :param obs: The observation data.
    :type obs: :class:`dexhub.data_types.Observation`
    :param act: The action data.
    :type act: :class:`dexhub.data_types.Action`
    :return: None
    :rtype: None

    Raises:
        :class:`TypeError`: If the types of `obs` or `act` are incorrect.

    """

    if not isinstance(obs, Observation):
        raise TypeError(f"Expected 'obs' to be of type Observation, got {type(obs).__name__}")
    
    if not isinstance(act, Action):
        raise TypeError(f"Expected 'act' to be of type Action, got {type(act).__name__}")

    transition = Transition(obs = obs, act = act)
    transition_storage.append(transition)

    # if data is not None: 

    #     info = [] 
    #     for obj in viz.bodies: 
    #         _obj = data.body(obj )
    #         info.append((obj, (_obj.xpos, _obj.xquat)))

        # viz.set_keypoints(info)

def save(success: bool = None, local_directory: str = None, task_description: str = None) -> None:

    """
    Saves the current transition data stored in `TransitionStorage` to a local directory 
    and triggers an upload process in a background process.

    This function handles the compression of transition data, saves it to a file in the local
    directory (defaulting to a temporary directory if none is specified), and uploads the data asynchronously.
    The metadata (such as success status) is updated before compression and uploading.

    :param success: An optional boolean value indicating whether the episode or task was successful. 
                    If provided, this value will be added to the metadata before saving the transition data.
    :type success: bool, optional
    :param local_directory: The directory path where the transition data should be saved locally. 
                            If not provided, the system's temporary directory is used by default.
    :type local_directory: str, optional
    :return: None

    Raises:
        :class:`OSError`: If there is an issue with creating the directory or writing to the file system.

    .. note::
        It compresses the transition data by creating an .mp4 file from the RGB images in the observation data using :meth:`TransitionStorage.compress`,
        while removing the RGB images from the transition data. The compressed bytes for the video is saved to a .dex file. 
        Use the :func:`dexhub.load` function to repopulate the RGB images from the compressed video file.

    .. note::
        If `success` is not provided, the metadata will not be updated for the success field.

    .. note::
        - The filename is generated based on the current date and time in the format `YYYY-MM-DD-HH-MM-SS.dex`.
    """

    cur_meta_data = meta_data.copy()

    if success is not None: 
        cur_meta_data["success"] = success

    if task_description is not None:
        cur_meta_data["task_description"] = task_description
    
    if not meta_data["sim"]: 
        transition_storage.compress()

    transition_storage.register_meta_data(cur_meta_data)

    if local_directory is None:
        local_directory = os.path.join(tempfile.gettempdir(), 'dexhub')

    os.makedirs(local_directory, exist_ok=True)

    filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    print(f"Saving transition data to {local_directory}/{filename}.dex")
    print(transition_storage)
    # save the transition data as a .dex file using pkl 
    with open(os.path.join(local_directory, f"{filename}.dex"), "wb") as f:
        print(f)
        print(transition_storage)
        pickle.dump(transition_storage, f)

    # Save the thumbnail as an mp4 file
    if not meta_data["sim"]:
        thumbnail_buffer = transition_storage.video_bytes["thumbnail"]
        thumbnail_buffer.seek(0)

        with open(os.path.join(local_directory, f"{filename}.mp4"), "wb") as f:
            f.write(thumbnail_buffer.read())

        buffer = io.BytesIO()
        pickle.dump(transition_storage, buffer)
        buffer.seek(0)
        thumbnail_buffer.seek(0)
        print("thumbnail buffer registered") 

    else: 
    #     html = viz.get_html() 

    #     # write above html (string) into a bytes buffer
    #     thumbnail_buffer = io.BytesIO()
    #     thumbnail_buffer.write(html.encode())

        # with open(os.path.join(local_directory, f"{filename}.html"), "wb") as f:
        #     f.write(thumbnail_buffer.getvalue())
        buffer = io.BytesIO()
        pickle.dump(transition_storage, buffer)
        buffer.seek(0)
        thumbnail_buffer = None
    

    p = multiprocessing.Process(target=upload_file, args=(buffer, filename + '.dex', cur_meta_data, thumbnail_buffer), daemon=True)
    p.start()

    transition_storage.clear()




def load(path: str) -> TransitionStorage:
    """
    Loads a compressed transition file from the specified path and decompresses the data.

    This function retrieves a transition file saved in `.dex` format, which was previously saved
    using the `save` function. It loads the transition data, decompresses it using the 
    `decompress` method of `TransitionStorage`, and returns the resulting object for further use.

    :param path: The file path to the `.dex` file containing the saved transition data.
    :type path: str
    :return: A `TransitionStorage` object containing the decompressed transition data.
    :rtype: :class:`dexhub.data_types.TransitionStorage`

    Raises:
        :class:`FileNotFoundError`: If the file at the provided `path` does not exist.
        :class:`OSError`: If there are issues reading the file from the file system.
        :class:`TypeError`: If the loaded data is not of the expected `TransitionStorage` type.
    
    Example usage:
        >>> transitions = load('/path/to/file.dex')

    Notes:
        - This function assumes that the transition file was saved in a compressed format and will
          attempt to decompress it before returning the data.
        - The `allow_pickle=True` parameter is used when loading the `.dex` file for compatibility
          with custom Python objects serialized using `pickle`.
    """

    data: TransitionStorage = pickle.load(open(path, "rb"))
    data.decompress()

    return data


def get_sim(data: TransitionStorage) -> mujoco.MjModel: 


    return mujoco.MjModel.from_xml_string(data.mjcf_data["xml"] , data.mjcf_data["assets"])