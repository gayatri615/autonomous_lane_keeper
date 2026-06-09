import time
import math

class VehicleSimulation:
    def __init__(self):
        # Initial State: X position, Y position, Orientation Angle (Heading in radians)
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.velocity = 0.0  # meters per second
        self.steering_angle = 0.0  # radians

    def update_physics(self, dt):
        """ Simple Kinematic Bicycle Model for Vehicle Physics """
        # Update positions based on velocity and current heading direction
        self.x += self.velocity * math.cos(self.theta) * dt
        self.y += self.velocity * math.sin(self.theta) * dt
        # Update orientation based on steering inputs
        self.theta += self.velocity * math.tan(self.steering_angle) * dt

        print(f"[SIM] Pos: ({self.x:.2f}, {self.y:.2f}) | Heading: {math.degrees(self.theta):.1f}° | Speed: {self.velocity:.1f} m/s")

if __name__ == "__main__":
    sim = VehicleSimulation()
    sim.velocity = 5.0  # Set moving speed to 5 m/s (~18 km/h)
    sim.steering_angle = math.radians(5)  # Slight right turn of 5 degrees
    
    print("Starting physics engine loop for 5 steps...")
    dt = 0.1  # Time step of 100 milliseconds
    for _ in range(5):
        sim.update_physics(dt)
        time.sleep(dt)
