import subprocess
import math
import time
import matplotlib.pyplot as plt

def run_visual_simulation():
    # 1. Compile C++ binary automatically
    subprocess.run(["g++", "-O2", "lane_controller.cpp", "-o", "lane_controller"], check=True)
    
    # 2. Launch the C++ controller subprocess pipeline
    process = subprocess.Popen(
        ["./lane_controller"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True
    )

    # Simulation variables
    lateral_drift = -2.5  # Start 2.5 meters off-center to the left
    dt = 0.1
    time_steps = []
    drift_history = []
    
    # Set up interactive plotting
    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 4))
    
    print("\n--- Running Visualization Engine ---")
    for step in range(1, 21): # Run for 20 steps to map a full correction curve
        # Send data to C++ controller
        process.stdin.write(f"{lateral_drift} {dt}\n")
        process.stdin.flush()
        
        # Read steering response from C++
        output_line = process.stdout.readline().strip()
        try:
            steering_angle_rad = float(output_line)
        except ValueError:
            break

        # Log history for graphing
        time_steps.append(step * dt)
        drift_history.append(lateral_drift)
        
        # Update vehicle physics position loop
        lateral_drift += (steering_angle_rad * 3.0) * dt 
        
        # Clear previous frame and redraw updating plot
        ax.clear()
        ax.plot(time_steps, drift_history, 'b-o', label='Vehicle Path')
        ax.axhline(0, color='r', linestyle='--', label='Lane Center Line')
        ax.set_title("Real-Time Autonomous Lane Correction (C++ Control Logic)")
        ax.set_xlabel("Time (Seconds)")
        ax.set_ylabel("Lateral Position Drift (Meters)")
        ax.set_ylim(-3.0, 1.0)
        ax.grid(True)
        ax.legend()
        
        plt.draw()
        plt.pause(0.05) # Pauses briefly to render the animation frame smoothly

    process.terminate()
    plt.ioff() # Turn off interactive plotting mode
    
    # Save the final trajectory curve graph as an asset for your GitHub Readme
    plt.savefig('lane_tracking_trajectory.png')
    print("[SYSTEM] Simulation complete. Chart asset saved as 'lane_tracking_trajectory.png'")
    plt.show()

if __name__ == "__main__":
    run_visual_simulation()
