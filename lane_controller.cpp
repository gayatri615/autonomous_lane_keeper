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
    double lateral_drift;
    double dt;

    // Continuously listen to incoming data from the Python process pipeline
    while (std::cin >> lateral_drift >> dt) {
        double steering_action = controller.calculate_steering(lateral_drift, dt);
        // Print ONLY the pure numerical result to stdout for Python to parse cleanly
        std::cout << steering_action << std::endl;
    }
    return 0;
}
