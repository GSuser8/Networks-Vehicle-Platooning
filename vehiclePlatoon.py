import threading
import queue
import time
import random
import numpy as np

class Vehicle(threading.Thread):
    def __init__(self, vehicle_id, heartbeat_queue, congestion_queue, max_window_size=5):
        super().__init__()
        self.vehicle_id = vehicle_id
        self.heartbeat_queue = heartbeat_queue
        self.congestion_queue = congestion_queue
        self.cwnd = 1  # Initial congestion window size
        self.ssthresh = max_window_size // 2  # Slow start threshold
        self.max_window_size = max_window_size
        self.position = 0
        self.speed = random.uniform(40, 60)  # Initial speed in km/h
        self.synchronized = False
        self.running = True
        self.data_packets = []  # List to hold data packets

    def run(self):
        while self.running:
            try:
                # Receive heartbeat for synchronization
                heartbeat = self.heartbeat_queue.get(timeout=1)
                self.process_heartbeat(heartbeat)

                # Handle congestion control and data flow
                self.handle_congestion_control()

            except queue.Empty:
                print(f"Vehicle {self.vehicle_id}: No heartbeat received. Trying to resynchronize.")
                self.adjust_speed()

            time.sleep(1)

    def process_heartbeat(self, heartbeat):
        if heartbeat["sync"]:
            print(f"Vehicle {self.vehicle_id}: Received sync heartbeat. Adjusting speed and position.")
            self.synchronized = True
            self.speed = heartbeat["speed"]
            self.position += self.speed
        else:
            print(f"Vehicle {self.vehicle_id}: Non-sync heartbeat. Adjusting speed.")
            self.adjust_speed()

    def handle_congestion_control(self):
        # Simulate sending data with congestion control using RLNC
        if self.cwnd < self.ssthresh:
            # Slow start phase
            self.cwnd *= 2
            print(f"Vehicle {self.vehicle_id}: Slow Start, increasing cwnd to {self.cwnd}")
        else:
            # Congestion avoidance phase
            self.cwnd += 1
            print(f"Vehicle {self.vehicle_id}: Congestion Avoidance, increasing cwnd to {self.cwnd}")

        self.cwnd = min(self.cwnd, self.max_window_size)

        # Generate and encode packets using RLNC
        encoded_packets = self.rlnc_encode(self.data_packets, self.cwnd)

        for packet in encoded_packets:
            if random.choice([True, False]):  # Simulate packet loss
                print(f"Vehicle {self.vehicle_id}: Packet loss detected.")
                self.ssthresh = max(self.cwnd // 2, 1)
                self.cwnd = 1
                break

        # Simulate feedback to adjust congestion window size
        self.congestion_queue.put(self.cwnd)

    def rlnc_encode(self, packets, num_packets):
        """ Encode packets using RLNC. """
        if len(packets) == 0:
            return []

        num_original = len(packets)
        encoded_packets = []
        for _ in range(num_packets):
            coefficients = np.random.randint(0, 10, size=num_original)
            encoded_packet = sum(coeff * packet for coeff, packet in zip(coefficients, packets))
            encoded_packets.append(encoded_packet)
        return encoded_packets

    def adjust_speed(self):
        if not self.synchronized:
            self.speed += random.uniform(-5, 5)
            print(f"Vehicle {self.vehicle_id}: Adjusting speed to {self.speed:.2f} km/h to try to resync.")
        self.position += self.speed

    def stop(self):
        self.running = False

class LeadVehicle:
    def __init__(self, heartbeat_queue):
        self.heartbeat_queue = heartbeat_queue
        self.speed = 50  # Lead vehicle speed
        self.sync_interval = 3  # Heartbeat interval in seconds
        self.running = True  # Control flag for stopping the thread

    def send_heartbeat(self):
        while self.running:
            heartbeat = {
                "sync": True,  # Synchronization message
                "speed": self.speed
            }
            print("Lead Vehicle: Sending sync heartbeat.")
            self.heartbeat_queue.put(heartbeat)
            time.sleep(self.sync_interval)

    def start(self):
        self.thread = threading.Thread(target=self.send_heartbeat)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()  # Wait for the thread to finish

def run_simulation():
    heartbeat_queue = queue.Queue()
    congestion_queue = queue.Queue()

    # Create lead vehicle and start sending heartbeats
    lead_vehicle = LeadVehicle(heartbeat_queue)
    lead_vehicle.start()

    # Create a number of vehicles and start them
    vehicles = [Vehicle(vehicle_id=i, heartbeat_queue=heartbeat_queue, congestion_queue=congestion_queue) for i in range(5)]
    for vehicle in vehicles:
        vehicle.start()

    try:
        # Run the simulation for a certain period
        time.sleep(20)
    finally:
        # Stop all vehicles after the simulation ends
        for vehicle in vehicles:
            vehicle.stop()

        # Stop the lead vehicle's heartbeat thread
        lead_vehicle.stop()

# Run the simulation
run_simulation()
