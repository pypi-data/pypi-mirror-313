
r'''
# DexHub: Central Data Hub for Robot Manipulation Learning

`DexHub` is a designed to be a central open-sourced data hub for robot learning, primarily focused on manipulation. 
It provides a simple API to **log every robot interactions** to an open-sourced cloud database, 
where anyone can **download our ever-growing dataset** for training robot policies. 

DexHub isn't starting from scratch; thanks to many wonderful projects such as [Open-X Embodiment](), [RH20T](), [Bridge](), and [DROID](), DexHub starts with a
vast source of real-world datasets containing over 1M transitions, which will continually grow over time, **thanks to you!**

## Three ways to contribute to DexHub

You can either be a **Generator** or a **Discriminator**. 

- Being a **Generator** means you are contributing new robot data to DexHub.
    1. Real-world:  Insert `dexhub.log` to any of your existing robot script. Think like an `wandb` for robots; instead of training logs, you are logging robot interactions.

        ```python
        import dexhub
        dexhub.log(obs, act)
        ```

    2. Simulation: If you have an Apple Vision Pro, you can use [DART]() to teleoperate robots in simulation. It automatically logs data to DexHub. 

- Being a **Discriminator** means you are contributing by labeling the recorded robot interactions. 
    1. [DexHub-Labeler](): Download the app on your iPhone, and start swiping left and right to **label** successful, and failed robot interactions. 
    2. [DexHub-Portal](https://dexhub.ai/): You can also label the data on the web portal for more detailed labeling, including task descriptions and video annotations.



## Quick Start 
1. Retreive your API token from our [DexHub Portal](https://dexhub.ai/). 
2. Export the API token as an environment variable. Also add it to your `.bashrc` or `.zshrc` file.
    ```bash
    export DEXHUB_API_TOKEN=...
    ```
3. Install the `dexhub-api` package using pip.
    ```bash
    pip install dexhub-api
    ```
4. **Contribute** a new robot data with `dexhub.logging.log`

    ```python
    import dexhub  # automatically registers the API token from the environment variable
    import my_teleop_interface as teleop
    dexhub.init("my_first_teleop", robot=dexhub.Arms.FR3, 
                gripper=dexhub.Grippers.PandaHand, teleoperation=True)
    
    while True:
        try:
            # get observation from your robot
            obs = robot.get_observation()
            # get action from your teleoperation interface
            action = teleop.get_action() 

            # log the transition to DexHub! 
            dexhub.log(obs, action)

            # step the robot with the action
            robot.step(action)

        except KeyboardInterrupt:
            dexhub.close()
    ```
    Your log data goes through an **automated sanity checker**, `dexhub.utils.sanity_checker`, ensuring every joint orderings, end-effector frame conventions, timestamps, and data types are correct.
    You can see how your logged data is processed in [DexHub Portal](https://dexhub.ai/), and if it passes the sanity check, it will be added to the global dataset.
    You can also download your own dataset from the portal.


5. **Download and train** with our ever-growing robot dataset with `dexhub.download.my_dataset` or `dexhub.download.global_dataset`.

    ```python
    import dexhub
    from dexhub.utils import DexHubDataset
    
    # get your dataset for training! 
    data = dexhub.download_dataset(uuid="xxxxxx") 

    # Wrap it up as a PyTorch Dataset 
    dataset = DexHubDataset(data)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

    # Train your robot policy!
    for epoch in range(n_epochs):
        for batch in dataloader:
            obs1, action, obs2 = batch
            # train your policy here!
            ...
    ```

'''

__docformat__ = "markdown"  # explicitly disable rST processing in the examples above.
__version__ = "14.7.0"  # this is read from setup.py



from .init import init, register_sim
from .sas_logging import log, save, load, get_sim
from .download import download_dataset, get_dataset_uuids
from .data_types import arms, grippers, hands, control_modes
from .data_types import Observation, Action, Transition, SE3
from scipy.spatial.transform import Rotation


"""
DexHub Main API

Functions:
    - init: Initialize the DexHub module
    - log: Log data in DexHub
    - save: Save DexHub logs
"""

__all__ = ['init', 'log', 'save', 'arms', 'grippers', 'hands', 'control_modes']
