#include <iostream>
#include <cmath>
#include <iomanip>

class LaneController {
private:
    // PID Gains (Tuned for stable steering)
    const double Kp = 0.5;   // Proportional gain (reacts to current error)
    const double Kd = 0.1;   // Derivative gain (reacts to rate of change)
    double previous_error = 0.0;

public:
    // Calculates the required steering angle based on lateral error (distance from lane center)
    double calculate_steering(double lateral_error, double dt) {
        // 1. Calculate derivative term (prevents overshooting)
        double error_derivative = (lateral_error - previous_error) / dt;
        
        // 2. Compute PID formula output
        double steering_output = -(Kp * lateral_error + Kd * error_derivative);
        
        // 3. Limit steering to max 30 degrees (expressed in radians) for realistic vehicle dynamics
        const double max_steering = 30.0 * M_PI / 180.0;
        if (steering_output > max_steering) steering_output = max_steering;
        if (steering_output < -max_steering) steering_output = -max_steering;
        
        // Save current error for the next computation step
        previous_error = lateral_error;
        return steering_output;
    }
};

int main() {
    LaneController controller;
    double dt = 0.1; // 100ms time step
    
    // Simulating a scenario where the car starts 1.5 meters left of the lane center
    double simulated_drift = -1.5; 
    
    std::cout << std::fixed << std::setprecision(3);
    std::cout << "[C++] Initializing Lane Tracking Controller..." << std::endl;
    
    // Simulate 3 correction steps
    for (int i = 1; i <= 3; ++i) {
        double steering_action = controller.calculate_steering(simulated_drift, dt);
        std::cout << "[C++] Step " << i << " | Lateral Drift: " << simulated_drift 
                  << "m | Action: Steering Command -> " << (steering_action * 180.0 / M_PI) << " degrees" << std::endl;
        
        // Simulating the vehicle slowly returning to the center line due to steering action
        simulated_drift += 0.4; 
    }
    
    return 0;
}
