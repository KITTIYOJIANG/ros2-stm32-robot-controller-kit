#ifndef ROBOT_CONTROLLER_MOTOR_DRIVER_H
#define ROBOT_CONTROLLER_MOTOR_DRIVER_H

#include <stdbool.h>

#include "../Config/error_code.h"

typedef struct {
    float left_speed;
    float right_speed;
    bool enabled;
    bool fault;
} rc_motor_driver_status_t;

void rc_motor_driver_init(void);

rc_error_code_t rc_motor_driver_set_speed(float left, float right);

void rc_motor_driver_stop(void);

bool rc_motor_driver_has_fault(void);

rc_motor_driver_status_t rc_motor_driver_get_status(void);

#endif /* ROBOT_CONTROLLER_MOTOR_DRIVER_H */
