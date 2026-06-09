import subprocess
import math
import time

def run_integrated_simulation():
    print("[SYSTEM] Compiling latest C++ controller code...")
    # Compile the C++ code automatically to ensure it is always up to date
    subprocess.run(["g++", "-O2", "lane_controller.cpp", "-o", "lane_controller"], check=True)
    
    print("[SYSTEM] Launching C++ Controller and Python Physics Engine Bridge...")
    # Start the compiled C++ controller as a background subprocess with piped communication channels
    process = subprocess.Popen(
        ["./lane_controller"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True # Ensures data is handled as text strings rather than raw binary bytes
    )

    # Simulated vehicle states
    lateral_drift = -2.0  # Starting 2 meters off-center to the left
    dt = 0.1             # 100ms time steps
    
    print("\n--- Starting Real-Time Closed-Loop Simulation ---")
    for step in range(1, 6):
        # 1. Send the current error metric to the C++ controller via stdin pipeline
        process.stdin.write(f"{lateral_drift} {dt}\n")
        process.stdin.flush()
        
        # 2. Read the calculation result back from C++ via stdout pipeline
        output_line = process.stdout.readline().strip()
        
        try:
            # Parse the numeric steering result from the controller stream
            steering_angle_rad = float(output_line)
            steering_angle_deg = math.degrees(steering_angle_rad)
        except ValueError:
            print(f"[ERROR] Step {step}: Could not parse controller output: '{output_line}'")
            break

        print(f"Step {step} | Current Drift: {lateral_drift:+.2f}m | C++ Output Steering Command: {steering_angle_deg:+.2f}°")
        
        # 3. Physics Simulation Update: Actuator movement alters physical orientation
        # If steering right (+), drift decreases. If steering left (-), drift increases.
        lateral_drift += (steering_angle_rad * 2.5) * dt 
        time.sleep(dt)

    # Clean up the process cleanly
    process.terminate()
    print("-------------------------------------------------")
    print("[SYSTEM] Simulation loop complete.")

if __name__ == "__main__":
    run_integrated_simulation()
