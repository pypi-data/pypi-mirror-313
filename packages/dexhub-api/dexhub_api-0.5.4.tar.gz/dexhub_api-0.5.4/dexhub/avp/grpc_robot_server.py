import grpc
from concurrent import futures
import time
import threading
import numpy as np
from dexhub.avp.grpc_msg import * 
from dexhub.avp.utils.grpc_utils import * 
from PIL import Image
import io 
import cv2 
from dexhub.utils import rot_x

YUP2ZUP = np.array([[[1, 0, 0, 0], 
                    [0, 0, -1, 0], 
                    [0, 1, 0, 0],
                    [0, 0, 0, 1]]], dtype = np.float64)

ZUP2YUP = np.array([[1, 0, 0, 0],
                    [0, 0, 1, 0],
                    [0, -1, 0, 0],
                    [0, 0, 0, 1]], dtype = np.float64)


class RobotServerforAVP:
    """
    RobotServer is responsible for handling hand tracking data and stereo image streams,
    transforming them, and sending them to connected clients.
    """

    def __init__(self, port=12350):
        """
        Initializes the RobotServer with the specified port and sets up the video capture and initial state.

        Args:
            port (int): The port number for the server to listen on. Defaults to 12350.
        """

        self.port = port
        self.latest = None
        self.axis_transform = YUP2ZUP
        self.sim_states = dexterity_pb2.SimStates()
        self.sim_states.matrices["left_hand"].CopyFrom(matrix4x4_to_proto(np.eye(4)))

        self.cap = cv2.VideoCapture(0) # MODIFY TO CORRECT PORT
        resolution = (1280, 480)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

        ret = False
        while not ret: 

            ret, image = self.cap.read() # reads frame that has stereo images side by side
            if not ret:
                print("failed to grab")
                return 
            
            image = cv2.rotate(image, cv2.ROTATE_180)
            # print("real_image:", image.shape)
            w = image.shape[1]//2
            h = image.shape[0]
            im_left = image[:, :w]
            im_right = image[:, w:2*w]
            
            _, buffer = cv2.imencode('.jpg', im_left)
            _, buffer2 = cv2.imencode('.jpg', im_right)
            # print("encoded both")
            
            # # Here, the server will yield the current stereo images that are set
            self.stereo_image = dexterity_pb2.StereoImage(left_image = buffer.tobytes(), right_image = buffer2.tobytes())


    def start(self):

        """
        Starts the gRPC server to listen for incoming hand updates and stream responses.
        """
        
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
        dexterity_pb2_grpc.add_HandTrackingServiceServicer_to_server(
            self.HandTrackingServicer(self), self.server)
        self.server.add_insecure_port(f'[::]:{self.port}')
        self.server.start()
        print(f"Server started, listening on port {self.port}")
        threading.Thread(target=self._keep_alive, daemon=True).start()

    def stop(self):

        """
        Stops the gRPC server.
        """
        
        if self.server:
            self.server.stop(0)
            print("Server stopped")

    def _keep_alive(self):
        try:
            while True:
                time.sleep(86400)
        except KeyboardInterrupt:
            self.stop()

    def get_latest(self):

        """
        Returns the latest transformations received by the server.

        Returns:
            dict: Latest transformation data for hands and head.
        """
        
        return self.latest

    class HandTrackingServicer(dexterity_pb2_grpc.HandTrackingServiceServicer):

        """
        HandTrackingServicer handles incoming hand updates and processes them to return simulation states
        or stereo images to the client.
        """
        
        def __init__(self, outer):
            print("HandTrackingServicer init")
            self.outer = outer

        def StreamHandUpdatesandGetSimStates(self, request_iterator, context):

            """
            Processes a stream of hand updates and returns the corresponding simulation states.

            Args:
                request_iterator (iterator): Iterator of HandUpdate messages.
                context (grpc.Context): The context of the gRPC call.

            Yields:
                SimStates: The current simulated states based on hand updates.
            """
            
            for hand_update in request_iterator:
                try: 
                    start_transformation_time = time.time()
                    # print(f"Transformation started at: {start_transformation_time} seconds")
                    transformations = {
                        "left_wrist": self.outer.axis_transform @ process_matrix(hand_update.left_hand.wristMatrix),
                        "right_wrist": self.outer.axis_transform @ process_matrix(hand_update.right_hand.wristMatrix),
                        "left_fingers": process_matrices(hand_update.left_hand.skeleton.jointMatrices),
                        "right_fingers": process_matrices(hand_update.right_hand.skeleton.jointMatrices),
                        "head": rotate_head(self.outer.axis_transform @ process_matrix(hand_update.Head)),
                        "left_pinch_distance": get_pinch_distance(hand_update.left_hand.skeleton.jointMatrices),
                        "right_pinch_distance": get_pinch_distance(hand_update.right_hand.skeleton.jointMatrices),
                    }
                    transformations["right_wrist_roll"] = get_wrist_roll(transformations["right_wrist"])
                    transformations["left_wrist_roll"] = get_wrist_roll(transformations["left_wrist"])

                    self.outer.latest = transformations
                    end_transformation_time = time.time()
                    # print(f"Transformation ended at: {end_transformation_time} seconds")
                    elapsed_time = end_transformation_time - start_transformation_time
                    # print(f"Elapsed time: {elapsed_time * 1000} ms")
                    
                    # You can add any processing here to fill sim_states based on transformations
                    yield self.outer.sim_states

                except Exception as e: 
                    print(e)


        def StreamHandUpdatesandGetStereoImages(self, request_iterator, context):

            """
            Processes a stream of hand updates and returns the corresponding stereo images.

            Args:
                request_iterator (iterator): Iterator of HandUpdate messages.
                context (grpc.Context): The context of the gRPC call.

            Yields:
                StereoImage: The current stereo images based on hand updates.
            """
            
            for hand_update in request_iterator:
                try:

                    # print(f"Transformation started at: {start_transformation_time} seconds")
                    transformations = {
                        "left_wrist": self.outer.axis_transform @ process_matrix(hand_update.left_hand.wristMatrix),
                        "right_wrist": self.outer.axis_transform @ process_matrix(hand_update.right_hand.wristMatrix),
                        "left_fingers": process_matrices(hand_update.left_hand.skeleton.jointMatrices),
                        "right_fingers": process_matrices(hand_update.right_hand.skeleton.jointMatrices),
                        "head": rotate_head(self.outer.axis_transform @ process_matrix(hand_update.Head)  @ rot_x(60)),
                        "left_pinch_distance": get_pinch_distance(hand_update.left_hand.skeleton.jointMatrices),
                        "right_pinch_distance": get_pinch_distance(hand_update.right_hand.skeleton.jointMatrices),
                    }
                    transformations["right_wrist_roll"] = get_wrist_roll(transformations["right_wrist"])
                    transformations["left_wrist_roll"] = get_wrist_roll(transformations["left_wrist"])

                    self.outer.latest = transformations

                    # print("real_image:", image.shape)
                    # w = image.shape[1]//2
                    # h = image.shape[0]
                    # im_left = image[:, :w]
                    # im_right = image[:, w:2*w]
                    
                    # _, buffer = cv2.imencode('.jpg', im_left)
                    # _, buffer2 = cv2.imencode('.jpg', im_right)
                    # print("encoded both")
                    
                    # # Here, the server will yield the current stereo images that are set
                    # yield dexterity_pb2.StereoImage(left_image = buffer.tobytes(), right_image = buffer2.tobytes())

                    yield self.outer.stereo_image

                except Exception as e:
                    print(f"Error streaming stereo images: {e}")


        def Check(self, request, context):
            response = dexterity_pb2.HealthCheckResponse()
            response.status = dexterity_pb2.HealthCheckResponse.SERVING
            return response

    def set_sim_states(self, sim_dict):
        """
        Sets the latest simulation states using the provided dictionary.

        Args:
            sim_dict (dict): A dictionary containing the simulation states with matrix data.
        """
        for key, value in sim_dict.items(): 
            self.sim_states.matrices[key].CopyFrom(matrix4x4_to_proto(ZUP2YUP @ value))

    # Method to update stereo images, automatically applying JPEG encoding
    def set_image_states(self, stereo_image_np, stereo = False):
        """
        Sets the latest stereo image states with JPEG encoding, based on the input image array.

        Args:
            stereo_image_np (numpy.ndarray): The stereo image as a numpy array.
            stereo (bool): Flag indicating whether the image is a stereo pair. Defaults to False.
        """

        # Extract the numpy arrays from the input dictionary
        image = stereo_image_np
        # convert rgb to bgr
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if stereo: 
            w = image.shape[1] // 2
            h = image.shape[0]
            print("sim_image:", image.shape)

            # Split the image into left and right
            im_left = image[:,:w]
            im_right = image[:,w:2*w]

            _, buffer_left = cv2.imencode('.jpg', im_left)
            _, buffer_right = cv2.imencode('.jpg', im_right)


        else:

            # Encode both images as JPEG using OpenCV
            _, buffer_left = cv2.imencode('.jpg', image)
            _, buffer_right = cv2.imencode('.jpg', image)

        # Create and set the StereoImage message
        stereo_image = dexterity_pb2.StereoImage(left_image = buffer_left.tobytes(), right_image = buffer_right.tobytes())

        self.stereo_image = stereo_image

        # ret, image = self.cap.read() # reads frame that has stereo images side by side
        # if not ret:
        #     print("failed to grab")
        #     return 

        # # split image in half
        # image = cv2.rotate(image, cv2.ROTATE_180)
        # w = image.shape[1]//2
        # h = image.shape[0]
        # im_left = image[:, :w]
        # im_right = image[:, w:2*w]
        
        # _, buffer = cv2.imencode('.jpg', im_left)
        # _, buffer2 = cv2.imencode('.jpg', im_right)
        # print("encoded both")

        # self.stereo_image.left_image = buffer.tobytes()
        # self.stereo_image.right_image = buffer2.tobytes()
        # pass 



    def _encode_jpeg(self, image):
        """Encodes a PIL image to JPEG format."""
        try:
            output = io.BytesIO()
            image.save(output, format='JPEG')
            jpeg_data = output.getvalue()

            return jpeg_data
        
        except Exception as e:
            print(f"JPEG encoding error: {e}")
            return None



# Usage example
if __name__ == '__main__':


    server = RobotServerforAVP()
    server.start()

    try:
        while True:
            latest = server.get_latest()
            if latest:
                pass
                # print(f"Latest head position: {latest['head'][0, :3, 3]}")
    except KeyboardInterrupt:
        server.stop()