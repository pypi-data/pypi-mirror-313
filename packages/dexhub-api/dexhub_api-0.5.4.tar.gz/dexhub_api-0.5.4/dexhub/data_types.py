import dexhub 
import numpy as np
from dataclasses import dataclass, field
import scipy 
from typing import *
from enum import Enum
import scipy.spatial
import time 
from datetime import datetime
import warnings 
import io 
import imageio 
import mujoco 
from dm_control import mjcf 


@dataclass
class SE3: 

    """
    A class representing a 3D rigid body transformation (SE3).

    This class encapsulates a 3D position and a 3D rotation, and provides methods to convert between transformation matrices and SE3 representations.

    Attributes:
        pos (np.ndarray): A 3D position vector represented as a numpy array of shape (3,).
        rot (scipy.spatial.transform.Rotation): A rotation represented as a `scipy.spatial.transform.Rotation` object. 
    """

    pos: np.ndarray
    rot: scipy.spatial.transform.Rotation


    def __post_init__(self):
        if self.pos.shape != (3,):
            raise ValueError(f"Position must be a 3D vector, got {self.pos.shape}")
        if not isinstance(self.rot, scipy.spatial.transform.Rotation):
            raise TypeError(f"Rotation must be a scipy.spatial.transform.Rotation object, got {type(self.rot)}")
        
    def get_matrix(self):
        """
        Converts the SE3 object to a 4x4 homogeneous transformation matrix.

        :return: A 4x4 numpy array representing the homogeneous transformation matrix.
        :rtype: np.ndarray
        """

        matrix = np.eye(4)
        matrix[:3, :3] = self.rot.as_matrix()
        matrix[:3, 3] = self.pos
        return matrix
    
    def get_posquat(self, scalar_first=True): 
        """
        Converts the SE3 object to a position-quaternion representation.

        :param scalar_first: Whether to return the quaternion in scalar-first (w, x, y, z) or scalar-last (x, y, z, w) format.
        :type scalar_first: bool
        :return: A numpy array of shape (7,) representing the position and quaternion.
        :rtype: np.ndarray
        """
        quat = self.rot.as_quat(scalar_first = scalar_first) 
        return np.concatenate([self.pos, quat])
        
    @classmethod
    def from_matrix(cls, matrix: np.ndarray):
        """
        Class method to create an SE3 object from a 4x4 transformation matrix.

        :param matrix: A 4x4 homogeneous transformation matrix.
        :type matrix: np.ndarray
        :return: An SE3 object representing the transformation encoded in the matrix.
        :rtype: SE3
        :raises ValueError: If the input matrix is not of shape (4, 4).
        """
        if matrix.shape != (4, 4):
            raise ValueError(f"Matrix must be a 4x4 homogeneous transformation matrix, got {matrix.shape}")

        # Extract rotation matrix (top-left 3x3) and position vector (top-right 3x1)
        rotation_matrix = matrix[:3, :3]
        position = matrix[:3, 3]

        # Create a Rotation object from the rotation matrix
        rotation = scipy.spatial.transform.Rotation.from_matrix(rotation_matrix)

        return cls(pos=position, rot=rotation)

@dataclass
class Observation: 
    """
    Represents an observation in the robot's environment, containing sensory and positional data.

    :param rgbs: A dictionary of RGB images captured from different camera views. The keys are strings (camera names), and the values are numpy arrays representing the images.
    :type rgbs: Dict[str, np.ndarray]
    
    :param qpos: The robot's joint positions. If it's single arm, directly pass the numpy array. If it's dual arm, pass a dictionary with keys (e.g. "left" and "right") and joint position values as numpy arrays.
    :type qpos: np.ndarray or Dict[str, np.ndarray]
    
    :param gripper_qpos: The positions of the gripper joints. If it's single arm, directly pass the numpy array. If it's dual arm, pass a dictionary with keys (e.g. "left" and "right") and gripper joint position values as numpy arrays.
    :type gripper_qpos: np.ndarray or Dict[str, np.ndarray]
    
    :param ee_pose: The end-effector pose, represented by an SE3 object. If it's single arm, directly pass the SE3 object. If it's dual arm, pass a dictionary with keys (e.g. "left" and "right") and SE3 values.
    :type ee_pose: SE3 or Dict[str, SE3]
    
    :param depths: Optional dictionary of depth images captured from different camera views. The keys are strings (camera names), and the values are numpy arrays representing depth maps.
    :type depths: Optional[Dict[str, np.ndarray]]
    
    :param qvel: Optional array of joint velocities for the robot. If it's single arm, directly pass the numpy array. If it's dual arm, pass a dictionary with keys (e.g. "left" and "right") and joint velocity values as numpy arrays.
    :type qvel: Optional[np.ndarray] or Optional[Dict[str, np.ndarray]]

    :param mj_qpos: Optional array of MuJoCo qpos values for a given simulation scene. 
    :type mj_qpos: Optional[np.ndarray]

    :param mj_qvel: Optional array of MuJoCo qvel values for a given simulation scene.
    :type mj_qvel: Optional[np.ndarray]
    
    :raises TypeError: If any of the input parameters are not of the expected type.
    :raises ValueError: If any of the RGB images in `rgbs` do not have the expected shape (width, height, 3).
    
        
    .. warning::
        We require both `qpos` and `ee_pose` fields to be present in the observation. 
        Logging of both is essential us to post-process every loggings, ensuring consistent axis conventions and frame transformations. 
        The post-processing step is performed by :func:`dexhub.utils.sanity_checker`.
    .. note::
        We are expecting RGB images to be in the shape (width, height, 3) and depth images to be in the shape (width, height).

    Example usage::

        obs = Observation(
            rgbs={"head": front_rgb, "left_wrist": left_rgb, "right_wrist": right_rgb},
            qpos={"left": left_qpos, "right": right_qpos},
            gripper_qpos={"left": left_gripper_qpos, "right": right_gripper_qpos},
            ee_pose={"left": left_ee_pose, "right": right_ee_pose},
        }

    """
    rgbs: Optional[Dict[str, np.ndarray]] = field(default_factory=dict)
    qpos: Optional[Dict[str, np.ndarray]] = field(default_factory=dict)
    gripper_qpos: Optional[Dict[str, np.ndarray]] = field(default_factory=dict)
    ee_pose: Optional[Dict[str, SE3]] = field(default_factory=dict)
    depths: Optional[Dict[str, np.ndarray]] = field(default_factory=dict)
    qvel: Optional[Dict[str, np.ndarray]] = field(default_factory=dict)
    mj_qpos: Optional[Dict[str, np.ndarray]] = field(default_factory=dict)
    mj_qvel: Optional[Dict[str, np.ndarray]] = field(default_factory=dict)

    def __init__(
        self,
        rgbs=None,
        qpos=None,
        gripper_qpos=None,
        ee_pose=None,
        depths=None,
        qvel=None,
        mj_qpos=None,
        mj_qvel=None,
    ):
        # Direct type validation in the constructor
        self.rgbs = self._validate_dict(rgbs, np.ndarray, "rgbs")
        self.qpos = self._validate_dict(qpos, np.ndarray, "qpos")
        self.gripper_qpos = self._validate_dict(gripper_qpos, np.ndarray, "gripper_qpos")
        self.ee_pose = self._validate_dict(ee_pose, SE3, "ee_pose")
        self.depths = self._validate_dict(depths, np.ndarray, "depths")
        self.qvel = self._validate_dict(qvel, np.ndarray, "qvel")
        self.mj_qpos = self._validate_dict(mj_qpos, np.ndarray, "mj_qpos")
        self.mj_qvel = self._validate_dict(mj_qvel, np.ndarray, "mj_qvel")

    def _validate_dict(self, data, expected_type, name):
        if isinstance(data, expected_type):  # Handle single-arm case
            return data
        if data is not None and not isinstance(data, dict):
            raise TypeError(f"{name} must be a dictionary or a single {expected_type.__name__}, got {type(data)}")
        if data is not None:
            for key, value in data.items():
                if not isinstance(value, expected_type):
                    raise TypeError(f"Each value in {name} must be of type {expected_type}, got {type(value)}")
        return data
    
    @property
    def qpos(self):
        # Concatenate left and right if both exist
        return self._qpos


    @qpos.setter
    def qpos(self, value):
        self._qpos = self._validate_dict(value, np.ndarray, "qpos")

    @property
    def qvel(self):
        # Concatenate left and right if both exist
        if "left" in self._qvel and "right" in self._qvel:
            return np.concatenate([self._qvel["left"], self._qvel["right"]])
        elif "left" in self._qvel:
            return self._qvel["left"]
        elif "right" in self._qvel:
            return self._qvel["right"]
        return None

    @qvel.setter
    def qvel(self, value):
        self._qvel = self._validate_dict(value, np.ndarray, "qvel")

    @property
    def ee_pose(self):
        return self._ee_pose

    @ee_pose.setter
    def ee_pose(self, value):
        self._ee_pose = self._validate_dict(value, SE3, "ee_pose")

    @property
    def gripper_qpos(self):
        return self._gripper_qpos

    @gripper_qpos.setter
    def gripper_qpos(self, value):
        self._gripper_qpos = self._validate_dict(value, np.ndarray, "gripper_qpos")

    @property
    def mj_qpos(self):
        return self._mj_qpos

    @mj_qpos.setter
    def mj_qpos(self, value):
        self._mj_qpos = self._validate_dict(value, np.ndarray, "mj_qpos")

    @property
    def mj_qvel(self):
        return self._mj_qvel

    @mj_qvel.setter
    def mj_qvel(self, value):
        self._mj_qvel = self._validate_dict(value, np.ndarray, "mj_qvel")


@dataclass
class ObservationChunk:
    """
    Represents a chunk of observations stacked along the first dimension. :meth:`from_observations` can be used to create an `ObservationChunk` object from a list of `Observation` objects.
    """

    rgbs: Optional[Dict[str, np.ndarray]] = field(default_factory=dict)
    qpos: Optional[Dict[str, np.ndarray]] = field(default_factory=dict)
    gripper_qpos: Optional[Dict[str, np.ndarray]] = field(default_factory=dict)
    ee_pose: Optional[Dict[str, np.ndarray]] = field(default_factory=dict)
    depths: Optional[Dict[str, np.ndarray]] = field(default_factory=dict)
    qvel: Optional[Dict[str, np.ndarray]] = field(default_factory=dict)
    mj_qpos: Optional[Dict[str, np.ndarray]] = field(default_factory=dict)
    mj_qvel: Optional[Dict[str, np.ndarray]] = field(default_factory=dict)

    @classmethod
    def from_observations(cls, observations: List[Observation]) -> "ObservationChunk":
        """
        Creates an ObservationChunk from a list of Observation objects.

        :param observations: A list of Observation objects to combine into an ObservationChunk.
        :type observations: List[Observation]
        :return: An ObservationChunk object with stacked data from the observations.
        :rtype: ObservationChunk
        """
        def stack_dict(data_list, keys, axis=0):
            """
            Helper function to stack dictionaries with the same keys across a list of observations.
            """
            print(keys, data_list)
            return {key: np.stack([data[key] for data in data_list], axis=axis) for key in keys}

        # Stack RGB dictionaries
        stacked_rgbs = stack_dict(
            [obs.rgbs for obs in observations], observations[0].rgbs.keys()
        ) if all(obs.rgbs for obs in observations) else None

        # Stack qpos dictionaries
        stacked_qpos = stack_dict(
            [obs.qpos for obs in observations], observations[0].qpos.keys()
        ) if all(obs.qpos for obs in observations) else None

        # Stack gripper_qpos dictionaries
        stacked_gripper_qpos = stack_dict(
            [obs.gripper_qpos for obs in observations], observations[0].gripper_qpos.keys()
        ) if all(obs.gripper_qpos for obs in observations) else None

        # Stack ee_pose dictionaries
        stacked_ee_pose = stack_dict(
            {key: obs.ee_pose[key].get_matrix() for obs in observations for key in obs.ee_pose.keys()},
            observations[0].ee_pose.keys()
        ) if all(obs.ee_pose for obs in observations) else None

        # Stack depth dictionaries
        stacked_depths = stack_dict(
            [obs.depths for obs in observations], observations[0].depths.keys()
        ) if all(obs.depths for obs in observations) else None

        # Stack qvel dictionaries
        stacked_qvel = stack_dict(
            [obs.qvel for obs in observations], observations[0].qvel.keys()
        ) if all(obs.qvel for obs in observations) else None

        # Stack mj_qpos dictionaries
        stacked_mj_qpos = stack_dict(
            [obs.mj_qpos for obs in observations], observations[0].mj_qpos.keys()
        ) if all(obs.mj_qpos for obs in observations) else None

        # Stack mj_qvel dictionaries
        stacked_mj_qvel = stack_dict(
            [obs.mj_qvel for obs in observations], observations[0].mj_qvel.keys()
        ) if all(obs.mj_qvel for obs in observations) else None

        return cls(
            rgbs=stacked_rgbs,
            qpos=stacked_qpos,
            gripper_qpos=stacked_gripper_qpos,
            ee_pose=stacked_ee_pose,
            depths=stacked_depths,
            qvel=stacked_qvel,
            mj_qpos=stacked_mj_qpos,
            mj_qvel=stacked_mj_qvel,
        )
    

@dataclass
class Action:
    """
    Represents an action taken by the robot in the environment, including control inputs for joints, end-effectors, and grippers.

    :param qpos: Joint positions for one or more arms. If it's single arm, directly pass the numpy array. If it's multi-arm, pass a dictionary with keys (e.g., "left", "right") and joint position values as numpy arrays.
    :type qpos: np.ndarray or Dict[str, np.ndarray]
    
    :param qvel: Joint velocities for one or more arms. Follows the same structure as `qpos`.
    :type qvel: Optional[np.ndarray] or Optional[Dict[str, np.ndarray]]
    
    :param qtorque: Joint torques for one or more arms. Follows the same structure as `qpos`.
    :type qtorque: Optional[np.ndarray] or Optional[Dict[str, np.ndarray]]
    
    :param ee_pose: End-effector poses represented by an SE3 object. If it's single arm, directly pass the SE3 object. If it's multi-arm, pass a dictionary with keys (e.g., "left", "right") and SE3 values.
    :type ee_pose: Optional[SE3] or Optional[Dict[str, SE3]]
    
    :param gripper_qpos: Positions of gripper joints. Follows the same structure as `qpos`.
    :type gripper_qpos: Optional[np.ndarray] or Optional[Dict[str, np.ndarray]]
    
    :param gripper_qvel: Velocities of gripper joints. Follows the same structure as `qpos`.
    :type gripper_qvel: Optional[np.ndarray] or Optional[Dict[str, np.ndarray]]
    
    :param mj_ctrl: Control inputs for MuJoCo simulations, such as actuator controls.
    :type mj_ctrl: Optional[np.ndarray] or Optional[Dict[str, np.ndarray]]

    :raises TypeError: If any of the input parameters are not of the expected type.
    :raises ValueError: If any parameter does not match the expected shape or structure.

    Example usage::

        act = Action(
            qpos={"left": np.random.rand(7), "right": np.random.rand(7)},
            qvel={"left": np.random.rand(7), "right": np.random.rand(7)},
            qtorque={"left": np.random.rand(7), "right": np.random.rand(7)},
            ee_pose={"left": SE3(pos=np.random.rand(3), rot=scipy.spatial.transform.Rotation.random())},
            gripper_qpos={"left": np.random.rand(2), "right": np.random.rand(2)},
        )
    """

    qpos: Optional[Dict[str, np.ndarray]] = field(default_factory=dict)
    qvel: Optional[Dict[str, np.ndarray]] = field(default_factory=dict)
    qtorque: Optional[Dict[str, np.ndarray]] = field(default_factory=dict)
    ee_pose: Optional[Dict[str, SE3]] = field(default_factory=dict)
    gripper_qpos: Optional[Dict[str, np.ndarray]] = field(default_factory=dict)
    gripper_qvel: Optional[Dict[str, np.ndarray]] = field(default_factory=dict)
    mj_ctrl: Optional[Dict[str, np.ndarray]] = field(default_factory=dict)

    def __init__(
        self,
        qpos=None,
        qvel=None,
        qtorque=None,
        ee_pose=None,
        gripper_qpos=None,
        gripper_qvel=None,
        mj_ctrl=None,
    ):
        # Direct type validation in the constructor
        self.qpos = self._validate_dict(qpos, np.ndarray, "qpos")
        self.qvel = self._validate_dict(qvel, np.ndarray, "qvel")
        self.qtorque = self._validate_dict(qtorque, np.ndarray, "qtorque")
        self.ee_pose = self._validate_dict(ee_pose, SE3, "ee_pose")
        self.gripper_qpos = self._validate_dict(gripper_qpos, np.ndarray, "gripper_qpos")
        self.gripper_qvel = self._validate_dict(gripper_qvel, np.ndarray, "gripper_qvel")
        self.mj_ctrl = self._validate_dict(mj_ctrl, np.ndarray, "mj_ctrl")

    def _validate_dict(self, data, expected_type, name):
        if isinstance(data, expected_type):  # Handle single-arm case
            return data 
        if data is not None and not isinstance(data, dict):
            raise TypeError(f"{name} must be a dictionary or a single {expected_type.__name__}, got {type(data)}")
        if data is not None:
            for key, value in data.items():
                if not isinstance(value, expected_type):
                    raise TypeError(f"Each value in {name} must be of type {expected_type}, got {type(value)}")
        return data

    @property
    def qpos(self):
        return self._qpos

    @qpos.setter
    def qpos(self, value):
        self._qpos = self._validate_dict(value, np.ndarray, "qpos")

    @property
    def qvel(self):
        return self._qvel

    @qvel.setter
    def qvel(self, value):
        self._qvel = self._validate_dict(value, np.ndarray, "qvel")

    @property
    def qtorque(self):
        return self._qtorque

    @qtorque.setter
    def qtorque(self, value):
        self._qtorque = self._validate_dict(value, np.ndarray, "qtorque")

    @property
    def ee_pose(self):
        return self._ee_pose

    @ee_pose.setter
    def ee_pose(self, value):
        self._ee_pose = self._validate_dict(value, SE3, "ee_pose")

    @property
    def gripper_qpos(self):
        return self._gripper_qpos

    @gripper_qpos.setter
    def gripper_qpos(self, value):
        self._gripper_qpos = self._validate_dict(value, np.ndarray, "gripper_qpos")

    @property
    def gripper_qvel(self):
        return self._gripper_qvel

    @gripper_qvel.setter
    def gripper_qvel(self, value):
        self._gripper_qvel = self._validate_dict(value, np.ndarray, "gripper_qvel")

    @property
    def mj_ctrl(self):
        return self._mj_ctrl

    @mj_ctrl.setter
    def mj_ctrl(self, value):
        self._mj_ctrl = self._validate_dict(value, np.ndarray, "mj_ctrl")


@dataclass
class ActionChunk:
    """
    A dataclass to represent a chunk of actions, useful for policy training.  
    Shares the same attributes as :class:`dexhub.data_types.Action` but with batch dimensions as the first axis.
    """
    
    qpos: Optional[np.ndarray] = None
    qvel: Optional[np.ndarray] = None
    qtorque: Optional[np.ndarray] = None
    ee_pose: Optional[np.ndarray] = None
    gripper_qpos: Optional[np.ndarray] = None
    gripper_qvel: Optional[np.ndarray] = None



@dataclass
class Transition: 
    """
    A data class representing a transition, which consists of an observation-action pair.

    Attributes:
        obs (Observation): The observation at the current time step.
        act (Action): The action taken based on the observation.
    """

    obs: Observation
    act: Action


class arms(Enum):
    """
    Enum representing different robotic arms.

    :cvar UR3E: Universal Robots UR3e arm.
    :cvar UR5E: Universal Robots UR5e arm.
    :cvar FR3: Franka Research 3 arm.
    :cvar PANDA: Franka Emika Panda arm.
    :cvar JACO: Kinova Jaco robotic arm.
    :cvar KINOVAGen3: Kinova Gen3 robotic arm.
    """

    UR3E = "UR3e"
    UR5E = "UR5e"
    FR3 = "Franka  Research 3"
    PANDA = "Franka Emika Panda"
    JACO = "Jaco"
    KINOVAGen3 = "Kinova Gen3"

class grippers(Enum):
    """
    Enum representing different robotic grippers.

    :cvar ROBOTIQ_2F85: Robotiq 2F-85 gripper.
    :cvar ROBOTIQ_2F140: Robotiq 2F-140 gripper.
    :cvar PANDA_HAND: Panda Hand gripper.
    """

    ROBOTIQ_2F85 = "Robotiq 2F-85"
    ROBOTIQ_2F140 = "Robotiq 2F-140"
    PANDA_HAND = "Panda Hand"

class hands(Enum):
    """
    Enum representing different multifingered robotic hands.

    :cvar SHADOW_HAND: Shadow Dexterous Hand.
    :cvar ALLEGRO_HAND: Allegro Hand.
    :cvar LEAP_HAND: Leap Hand.
    """
    SHADOW_HAND = "Shadow Dexterous Hand"
    ALLEGRO_HAND = "Allegro Hand"
    LEAP_HAND = "Leap Hand"


class control_modes(Enum):
    """
    Enum representing different control modes for robotic arms and hands.

    :cvar POSITION: Position control mode for direct control of joint positions.
    :cvar EEPOSE: End-effector pose control mode.
    :cvar VELOCITY: Velocity control mode for controlling joint velocities.
    """

    POSITION = "Position"
    EEPOSE = "End-Effector Pose"
    VELOCITY = "Velocity"


class TransitionStorage:
    """
    A class to store the logged transitions in memory and perform post-processing tasks like
    creating videos from RGB observations, compressing data, and checking the consistency of logged transitions.

    The `TransitionStorage` class stores a sequence of transitions along with timestamps, provides methods
    to append transitions, remove unnecessary data, and perform compression and decompression before saving
    and after loading.

    Attributes:
        data (List[Transition]): A list that holds the logged transitions.
        time_stamp (List[datetime]): A list that holds the timestamps for each logged transition.
        video_bytes (Dict[str, io.BytesIO]): A dictionary that stores video data (in bytes) for each camera.
        meta_data (Dict[str, Any]): A dictionary that stores metadata associated with the project.
        mjmodel_bytes (Dict[str, Optional[io.BytesIO]]): A dictionary that stores the MuJoCo model files (XML and asset files) as byte streams.
    """
    
    def __init__(self):
        """
        Initializes the `TransitionStorage` with empty lists for storing transitions and timestamps, 
        and initializes an empty dictionary for storing video buffers.
        """
        self.data: List[Transition] = []
        self.time_stamp: List[datetime] = []
        self.video_bytes: Dict[str, io.BytesIO] = {}
        self.meta_data: Dict[str, Any] = {}
        self.mjcf_data = {
            "xml": None,
            "assets": None, 
        }  
    
    def append(self, transition: Transition):
        """
        Appends a transition to the storage and records the current timestamp.

        :param transition: The transition to be added to the storage.
        :type transition: Transition
        """
        self.data.append(transition)
        self.time_stamp.append(datetime.now())

    def get_mjmodel(self):
        """
        Loads the MuJoCo model from the stored byte streams.
        """
        return mujoco.MjModel.from_xml_string(self.mjcf_data["xml"], self.mjcf_data["assets"])
    
    def register_meta_data(self, meta_data: Dict[str, Any]):
        """
        Registers the metadata associated with the project.

        :param meta_data: A dictionary containing the project metadata.
        :type meta_data: Dict[str, Any]
        """
        self.meta_data = meta_data

    def _remove_rgb(self):
        """
        Removes RGB images from the stored transitions to save memory during the compression process.

        This method replaces all RGB image data in the transitions with `None` to reduce the storage size
        after video encoding is done.
        """
        for transition in self.data:
            for key in transition.obs.rgbs.keys():
                transition.obs.rgbs[key] = None 
    
    def compress(self):
        """
        Compresses the logged transitions by creating videos from the RGB observations and
        removing the original RGB data from the transitions.

        This method first creates video files from the logged RGB frames for each camera, stores them
        in the `video_bytes` attribute, and then removes the raw RGB data to reduce memory usage.
        """
        self._make_video()
        self._make_thumbnail_video()
        self._remove_rgb()

    def _make_thumbnail_video(self):
        """
        Creates a thumbnail video from the logged RGB transitions: for multiple camera view points, 
        things are stacked vertically to create a vertically long video like Youtube shorts form. 
        """

        buffer = io.BytesIO()
        writer = imageio.get_writer(buffer, format='mp4', fps=30, codec='libx264', macro_block_size=4)

        for transition in self.data:
            # concatenate all the images vertically
            rgb = np.concatenate([transition.obs.rgbs[key] for key in transition.obs.rgbs.keys()], axis = 0)
            writer.append_data(rgb)

        writer.close()
        # actually write the buffer to a file
        buffer.seek(0)
        self.video_bytes["thumbnail"] = buffer

    def decompress(self):
        """
        Decompresses the logged transitions by decoding video files and restoring RGB frames.

        This method reads the video data stored in `video_bytes`, decodes it back into individual frames,
        and restores the RGB images into their corresponding transitions.
        """
        self._decode_video()
    
    def _realtime_check(self):
        """
        Checks if the transitions are logged at uniform time intervals.

        This method calculates the time intervals between consecutive transitions and issues a warning 
        if the intervals deviate by more than 10% from the mean time interval.

        :raises Warning: If transitions are not logged in uniform time intervals.
        """
        time_intervals = [self.time_stamp[i+1] - self.time_stamp[i] for i in range(len(self.time_stamp) - 1)]
        mean_time_interval = sum(time_intervals) / len(time_intervals)

        # Allow 10% deviation from mean time interval
        if not all(abs(t - mean_time_interval) < 0.1 * mean_time_interval for t in time_intervals):
            warnings.warn("Transitions are not logged in uniform time intervals.")

    def sanity_check(self):
        """
        Checks the logged transitions for consistency and correctness by solving an optimization problem
        to correct joint ordering and end-effector frame conventions.

        The optimization aligns joint ordering and end-effector frames by searching over permutations and 
        end-effector frame conventions using brute force and gradient descent, respectively.

        .. math::
            \min_{\\text{perm},\mathbf{T}} \sum  \| f(\\text{perm}(\\theta )) \cdot \mathbf{T} - \mathbf{T}^{ee} \|

        The brute-force search is performed for joint permutations, and the end-effector frame conventions
        are optimized using a differentiable forward kinematics layer.
        """
        # Optimization logic goes here

    def _make_video(self):
        """
        Creates videos from the logged RGB transitions and stores them as byte streams.

        This method loops through the RGB frames for each camera in the logged transitions, creates a video
        using the `libx264` codec, and stores the video in the `video_bytes` dictionary as a byte stream.

        :raises ValueError: If the RGB data for any camera is missing or invalid.
        """
        obs = self.data[0].obs
        camera_names = sorted(obs.rgbs.keys())

        self.video_bytes = {}

        for camera_name in camera_names:
            buffer = io.BytesIO()
            # Use libx264 codec with macro_block_size option for efficient encoding
            with imageio.get_writer(buffer, format='mp4', fps=30, codec='libx264', macro_block_size=4) as writer:
                for transition in self.data:
                    rgb = transition.obs.rgbs.get(camera_name)
                    if rgb is None:
                        raise ValueError(f"RGB data for camera '{camera_name}' is missing in some transitions.")
                    writer.append_data(rgb)
            
            buffer.seek(0)
            self.video_bytes[camera_name] = buffer

    def _decode_video(self) -> Dict[str, np.ndarray]:
        """
        Decodes the stored video byte streams into individual RGB frames and restores them in the transitions.

        This method reads the video files stored in the `video_bytes` dictionary, decodes them into individual
        frames, and restores the frames to the corresponding transitions for each camera.

        :raises ValueError: If any video file cannot be read or decoded.
        """
        for camera_name, buffer in self.video_bytes.items():
            buffer.seek(0)  # Ensure we're at the start of the buffer

            # Read the video data using imageio
            video = imageio.get_reader(buffer, format='mp4')

            # Convert the video to a list of frames (numpy arrays)
            frames = [frame for frame in video]

            if len(frames) != len(self.data):
                raise ValueError(f"Mismatch between the number of frames and transitions for camera '{camera_name}'.")

            for i, frame in enumerate(frames): 
                self.data[i].obs.rgbs[camera_name] = np.array(frame)


    def get_chunks(self, obs_chunk_size: int, act_chunk_size: int) -> List[Tuple[ObservationChunk, ActionChunk]]:
        """
        Splits the logged transitions into overlapping chunks of observations and actions.

        This method creates chunks of observations and actions, where the observation chunks and action chunks
        overlap. The chunk sizes for observations and actions are determined by `obs_chunk_size` and `act_chunk_size`.

        For example, with `obs_chunk_size=3` and `act_chunk_size=5`, and given the logged transitions:

        .. code-block:: python

            Observations: o1, o2, o3, o4, o5, o6, o7, o8, o9, o10, ...
            Actions     : a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, ...

        The method will return the following chunks:

        .. code-block:: python

            [
                ((o1, o2, o3), (a3, a4, a5, a6, a7)), 
                ((o2, o3, o4), (a4, a5, a6, a7, a8)),
                ((o3, o4, o5), (a5, a6, a7, a8, a9)),
                ((o4, o5, o6), (a6, a7, a8, a9, a10)),
                ...
            ]

        The observation chunks will consist of consecutive `obs_chunk_size` observations, and the action chunks
        will be created starting from the middle of the observation chunk (at index `obs_chunk_size // 2`) and
        extending to `act_chunk_size`.

        :param obs_chunk_size: The number of consecutive observations to include in each observation chunk.
        :type obs_chunk_size: int
        :param act_chunk_size: The number of consecutive actions to include in each action chunk.
        :type act_chunk_size: int
        :return: A list of tuples, where each tuple contains an observation chunk and an action chunk.
        :rtype: List[Tuple[ObservationChunk, ActionChunk]]
                
        :raises ValueError: If the number of logged transitions is less than the chunk sizes.
        """
        if len(self.data) < max(obs_chunk_size, act_chunk_size):
            raise ValueError("The number of logged transitions is less than the chunk sizes.")

        chunk_pairs = [] 

        for i in range(len(self.data) - obs_chunk_size + 1):
            obs_chunk = [self.data[j].obs for j in range(i, i + obs_chunk_size)]
            
            # Action chunks start from the middle of the observation chunk and extend to the specified length.
            action_start = i + (obs_chunk_size // 2)
            action_end = min(action_start + act_chunk_size, len(self.data))
            act_chunk = [self.data[j].act for j in range(action_start, action_end)]

            obs_chunk = ObservationChunk.from_observations(obs_chunk)
            act_chunk = self._batchify_actions(act_chunk)

            chunk_pairs.append((obs_chunk, act_chunk))

        return chunk_pairs

    def _batchify_observations(self, observations: List[Observation]) -> ObservationChunk:
        """
        Combines a list of Observation objects into a single ObservationChunk
        by stacking the numpy arrays along axis=0.

        :param observations: A list of Observation objects to be combined.
        :type observations: List[Observation]
        :return: A single ObservationChunk object where the numpy arrays have been stacked along axis=0.
        :rtype: ObservationChunk
        """
        def stack_dict(data_list, keys, axis=0):
            """
            Helper function to stack dictionaries with the same keys across a list of observations.
            """
            return {key: np.stack([data[key] for data in data_list], axis=axis) for key in keys}

        # Stack RGB dictionaries
        if all(obs.rgbs for obs in observations):
            stacked_rgbs = stack_dict(
                [obs.rgbs for obs in observations], observations[0].rgbs.keys()
            )
        else:
            stacked_rgbs = None

        # Stack qpos dictionaries
        if all(obs.qpos for obs in observations):
            stacked_qpos = stack_dict(
                [obs.qpos for obs in observations], observations[0].qpos.keys()
            )
        else:
            stacked_qpos = None

        # Stack gripper_qpos dictionaries
        if all(obs.gripper_qpos for obs in observations):
            stacked_gripper_qpos = stack_dict(
                [obs.gripper_qpos for obs in observations], observations[0].gripper_qpos.keys()
            )
        else:
            stacked_gripper_qpos = None

        # Stack ee_pose dictionaries (assuming SE3 objects are numpy-compatible)
        if all(obs.ee_pose for obs in observations):
            stacked_ee_pose = {
                key: np.stack([obs.ee_pose[key].get_matrix() for obs in observations], axis=0)
                for key in observations[0].ee_pose.keys()
            }
        else:
            stacked_ee_pose = None

        # Stack depth dictionaries
        if all(obs.depths for obs in observations):
            stacked_depths = stack_dict(
                [obs.depths for obs in observations], observations[0].depths.keys()
            )
        else:
            stacked_depths = None

        # Stack qvel dictionaries
        if all(obs.qvel for obs in observations):
            stacked_qvel = stack_dict(
                [obs.qvel for obs in observations], observations[0].qvel.keys()
            )
        else:
            stacked_qvel = None

        # Stack mj_qpos dictionaries
        if all(obs.mj_qpos for obs in observations):
            stacked_mj_qpos = stack_dict(
                [obs.mj_qpos for obs in observations], observations[0].mj_qpos.keys()
            )
        else:
            stacked_mj_qpos = None

        # Stack mj_qvel dictionaries
        if all(obs.mj_qvel for obs in observations):
            stacked_mj_qvel = stack_dict(
                [obs.mj_qvel for obs in observations], observations[0].mj_qvel.keys()
            )
        else:
            stacked_mj_qvel = None

        # Create a new ObservationChunk object with stacked data
        return ObservationChunk(
            rgbs=stacked_rgbs,
            qpos=stacked_qpos,
            gripper_qpos=stacked_gripper_qpos,
            ee_pose=stacked_ee_pose,
            depths=stacked_depths,
            qvel=stacked_qvel,
            mj_qpos=stacked_mj_qpos,
            mj_qvel=stacked_mj_qvel,
        )

    def _batchify_actions(actions: List[Action]) -> ActionChunk:
        """
        Combines a list of Action objects into a single ActionChunk by stacking the numpy arrays along axis=0.

        :param actions: A list of Action objects to be combined.
        :type actions: List[Action]
        :return: A single ActionChunk object where the numpy arrays have been stacked along axis=0.
        :rtype: ActionChunk
        """
        
        # Stack qpos arrays
        if all(action.qpos is not None for action in actions):
            stacked_qpos = np.stack([action.qpos for action in actions], axis=0)
        else:
            stacked_qpos = None

        # Stack qvel arrays
        if all(action.qvel is not None for action in actions):
            stacked_qvel = np.stack([action.qvel for action in actions], axis=0)
        else:
            stacked_qvel = None

        # Stack qtorque arrays
        if all(action.qtorque is not None for action in actions):
            stacked_qtorque = np.stack([action.qtorque for action in actions], axis=0)
        else:
            stacked_qtorque = None

        # Stack ee_pose arrays (assuming SE3 is numpy-compatible)
        if all(action.ee_pose is not None for action in actions):
            stacked_ee_pose = np.stack([action.ee_pose for action in actions], axis=0)
        else:
            stacked_ee_pose = None

        # Stack gripper_qpos arrays
        if all(action.gripper_qpos is not None for action in actions):
            stacked_gripper_qpos = np.stack([action.gripper_qpos for action in actions], axis=0)
        else:
            stacked_gripper_qpos = None

        # Stack gripper_qvel arrays
        if all(action.gripper_qvel is not None for action in actions):
            stacked_gripper_qvel = np.stack([action.gripper_qvel for action in actions], axis=0)
        else:
            stacked_gripper_qvel = None

        # Return the batchified ActionChunk
        return ActionChunk(
            qpos=stacked_qpos,
            qvel=stacked_qvel,
            qtorque=stacked_qtorque,
            ee_pose=stacked_ee_pose,
            gripper_qpos=stacked_gripper_qpos,
            gripper_qvel=stacked_gripper_qvel
        )


    def clear(self):
        """
        Clears the stored transitions, timestamps, and video buffers.

        This method is automatically called after saving the transitions, clearing all logged data in the
        `TransitionStorage` object, including the transitions, timestamps, and video byte streams.
        """
        self.data = []
        self.time_stamp = []
        self.video_bytes = {}
        self.meta_data = {}


if __name__ == "__main__": 

    dexhub.init("test", dexhub.arms.FR3, dexhub.grippers.PANDA_HAND, dexhub.control_modes.POSITION)
    from dexhub.data_types import Observation, Action, SE3
    from dexhub.init import transition_storage

    obs = Observation(
        rgbs={"front": np.random.rand(100, 100, 3), "side": np.random.rand(100, 100, 3)},
        qpos={"left": np.random.rand(7), "right": np.random.rand(7)},
        gripper_qpos={"left": np.random.rand(2), "right": np.random.rand(2)},
        ee_pose={"left": SE3(pos=np.random.rand(3), rot=scipy.spatial.transform.Rotation.random()),
                 "right": SE3(pos=np.random.rand(3), rot=scipy.spatial.transform.Rotation.random())},
        depths={"front": np.random.rand(100, 100), "side": np.random.rand(100, 100)},
        qvel=np.random.rand(7),
    )

    act = Action(
        ee_pose={"left": SE3(pos=np.random.rand(3), rot=scipy.spatial.transform.Rotation.random()),
                 "right": SE3(pos=np.random.rand(3), rot=scipy.spatial.transform.Rotation.random())},
        gripper_qpos={"left": np.random.rand(2), "right": np.random.rand(2)},
    )

    for _ in range(100): 
        dexhub.log(obs, act)

    transition_storage.get_chunks(3, 5)