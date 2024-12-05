import grpc
import time
import cv2
import dexhub.avp.grpc_msg.dexterity_pb2 as dexterity_pb2
import dexhub.avp.grpc_msg.dexterity_pb2_grpc as dexterity_pb2_grpc

class RobotClientforAVP:
    """
    RobotClient is responsible for connecting to a remote gRPC server hosted on Apple Vision Pro,
    streaming stereo image data, and receiving hand tracking updates.
    """
    
    def __init__(self, host="vision-pro-host-ip", port=12350):
        """
        Initializes the RobotClient with the server host and port and sets up video capture.

        Args:
            host (str): The IP address of the gRPC server hosted on the Apple Vision Pro.
            port (int): The port number of the gRPC server. Defaults to 12350.
        """
        self.host = host
        self.port = port
        self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')
        self.stub = dexterity_pb2_grpc.HandTrackingServiceStub(self.channel)

        self.left_image = None
        self.right_image = None


    def _return_latest_stereo_image(self):
        """
        Captures stereo image data from the camera and returns it encoded as JPEG.

        Returns:
            dexterity_pb2.StereoImage: A stereo image message with left and right images encoded in JPEG.
        """
        
        if self.left_image is None or self.right_image is None:
            return None
        
        # Split stereo image into left and right
        left_image = self.left_image
        right_image = self.right_image

        # Encode images as JPEG
        _, left_buffer = cv2.imencode('.jpg', left_image)
        _, right_buffer = cv2.imencode('.jpg', right_image)

        # Create StereoImage message
        stereo_image = dexterity_pb2.StereoImage(
            left_image=left_buffer.tobytes(),
            right_image=right_buffer.tobytes()
        )

        return stereo_image



    def generate_stereo_image_stream(self):
        """
        Generator function to capture and yield stereo images in a continuous stream.
        """
        while True:
            stereo_image = self._return_latest_stereo_image()
            if stereo_image:
                yield stereo_image
            time.sleep(0.1)

    def stream_stereo_images_and_get_hand_updates(self):
        """
        Streams stereo images to the gRPC server and listens for hand updates.
        """
        try:

            # Call the gRPC method and process hand updates
            response_iterator = self.stub.StreamStereoImagesandGetHandUpdates(self.generate_stereo_image_stream())

            for hand_update in response_iterator:
                print("Received hand update:")
                print(f"Left hand wrist: {hand_update.left_hand.wristMatrix}")
                print(f"Right hand wrist: {hand_update.right_hand.wristMatrix}")
                print(f"Head: {hand_update.Head}")

        except grpc.RpcError as e:
            print(f"gRPC error: {e}")

    def check_health(self):
        """
        Checks the health of the gRPC server.
        """
        try:
            response = self.stub.Check(dexterity_pb2.HealthCheckRequest())
            if response.status == dexterity_pb2.HealthCheckResponse.SERVING:
                print("Server is healthy and serving.")
            else:
                print("Server is not serving.")
        except grpc.RpcError as e:
            print(f"Health check failed: {e}")

    def stop(self):
        """
        Releases resources used by the client, including camera capture.
        """
        if self.cap:
            self.cap.release()
            print("Released camera resources")


if __name__ == '__main__':
    # Create an instance of the client and start streaming stereo images
    client = RobotClientforAVP(host="vision-pro-host-ip", port=12350)  # Replace with actual host IP and port
    client.check_health()  # Optional: Check if the server is healthy
    client.stream_stereo_images_and_get_hand_updates()
    client.stop()  # Ensure cleanup of resources when done
