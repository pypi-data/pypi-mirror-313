import grpc
import time
import numpy as np
from dexhub.avp.grpc_msg import dexterity_pb2, dexterity_pb2_grpc

# Function to create a random 4x4 matrix
def create_random_matrix():
    return dexterity_pb2.Matrix4x4(
        m00=np.random.random(), m01=np.random.random(), m02=np.random.random(), m03=np.random.random(),
        m10=np.random.random(), m11=np.random.random(), m12=np.random.random(), m13=np.random.random(),
        m20=np.random.random(), m21=np.random.random(), m22=np.random.random(), m23=np.random.random(),
        m30=np.random.random(), m31=np.random.random(), m32=np.random.random(), m33=np.random.random(),
    )

# Function to create a random Skeleton with 24 joint matrices
def create_random_skeleton():
    skeleton = dexterity_pb2.Skeleton()
    for _ in range(24):
        skeleton.jointMatrices.append(create_random_matrix())
    return skeleton

# Function to create a random HandUpdate
def create_random_hand_update():
    left_hand = dexterity_pb2.Hand(
        wristMatrix=create_random_matrix(),
        skeleton=create_random_skeleton()
    )
    right_hand = dexterity_pb2.Hand(
        wristMatrix=create_random_matrix(),
        skeleton=create_random_skeleton()
    )
    head = create_random_matrix()

    return dexterity_pb2.HandUpdate(
        left_hand=left_hand,
        right_hand=right_hand,
        Head=head
    )

# Mock client class to stream hand updates to the server
class MockHandTrackingClient:
    def __init__(self, server_address='localhost:12350'):
        self.channel = grpc.insecure_channel(server_address)
        self.stub = dexterity_pb2_grpc.HandTrackingServiceStub(self.channel)

    def stream_hand_updates(self):
        try:
            # Stream random hand updates to the server
            for response in self.stub.StreamHandUpdatesandGetSimStates(self.generate_hand_updates()):
                print(f"Received sim states: {response}")
        except grpc.RpcError as e:
            print(f"gRPC error: {e}")

    def generate_hand_updates(self):
        while True:
            hand_update = create_random_hand_update()
            yield hand_update

    def check_health(self):
        try:
            response = self.stub.Check(dexterity_pb2.HealthCheckRequest())
            print(f"Health check status: {response.status}")
        except grpc.RpcError as e:
            print(f"gRPC error: {e}")

# Usage example
if __name__ == '__main__':
    client = MockHandTrackingClient()
    
    # Perform a health check
    client.check_health()
    
    # Start streaming hand updates
    client.stream_hand_updates()
