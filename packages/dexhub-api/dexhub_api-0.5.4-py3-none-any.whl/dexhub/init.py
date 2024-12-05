import dexhub
from dm_control import mjcf  
import warnings 
from dexhub.data_types import TransitionStorage
from dexhub.utils.meshcat_viz import MJCMeshcat
from copy import deepcopy

transition_storage = TransitionStorage() 

meta_data = { 
    "project_name": None, 
    "arm": None, 
    "hand": None,
    "teleop": False,
    "task_description": None,
    "control_mode": None, 
    "sim": False, 
}

mjcf_data: mjcf.Element = None  
# viz: MJCMeshcat = MJCMeshcat() 


def init(project_name, arm, hand, control_mode, teleop = False, \
         task_description = None):
    """
    Initializes the DexHub logging system. Call this function at the beginning of your script to set up the project metadata.

    :param project_name: The name of the project for logging and metadata.
    :type project_name: str
    
    :param arm: The robotic arm being used.
    :type arm: :class:`dexhub.types.arms`
    
    :param hand: The gripper or hand being used.
    :type hand: :class:`dexhub.types.grippers`
    
    :param control_mode: The control mode for the robot, such as position, velocity, or torque control.
    :type control_mode: :class:`dexhub.types.control_modes`
    
    :param teleop: Specifies whether teleoperation is enabled. Defaults to `False`.
    :type teleop: bool
    
    :param task_description: An optional string that describes the task being performed. If not provided, a warning will be issued, recommending its inclusion for better data organization.
    :type task_description: Optional[str]
    
    :raises Warning: If `task_description` is not set.
    
    This function initializes the DexHub system by populating the metadata with relevant project details such as the robot arm, gripper, control mode, and task description. It prints out the initialized values for verification.

    Example usage::

        dexhub.init("my_cool_robot_teleop", arms.FR3, grippers.PANDA_HAND, 
                    control_modes.POSITION, teleop=True, 
                    task_description="Pick and place operation with small objects")

    Output:

    .. code-block::

        DexHub Initialized:
        -------------------
        Project Name      : my_cool_robot_teleop
        Robot Arm         : Franka Emika Panda
        Gripper           : Panda Gripper
        Teleoperation     : True
        Control Mode      : POSITION
        Task Description  : Pick and place operation with small objects
        -------------------

    .. note::
        The `task_description` parameter is optional but highly recommended for better data organization.

    """
    meta_data["project_name"] = project_name
    meta_data["arm"] = arm
    meta_data["hand"] = hand
    meta_data["teleop"] = teleop
    meta_data["task_description"] = task_description
    meta_data["control_mode"] = control_mode

    warnings.warn("Task description is not set. We highly recommend setting a task description for better data organization.")

    # Pretty-printed output
    print(f"""
    DexHub Initialized:
    -------------------
    Project Name      : {project_name}
    Robot Arm         : {arm}
    Gripper           : {hand}
    Teleoperation     : {teleop}
    Control Mode      : {control_mode}
    Task Description  : {task_description if task_description else 'N/A'}
    -------------------
    """)


def register_sim(input_mjcf: mjcf.Element): 

    """
    
    Registers the MuJoCo model with the DexHub system for logging and data collection.
    
    :param mjcf: The MuJoCo model file or XML string.
    :type mjcf: :class:`dm_control.mjcf.Element`
    """

    print("here", input_mjcf)

    transition_storage.mjcf_data = {
        "xml": input_mjcf.to_xml_string(), 
        "assets": input_mjcf.get_assets(), 
    }   
    meta_data["sim"] =  True 

    # viz.parse_mjcf(input_mjcf)

    print("Simulation registered with DexHub.")