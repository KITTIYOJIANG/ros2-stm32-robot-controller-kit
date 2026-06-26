#ifndef ROBOT_CONTROLLER_ERROR_CODE_H
#define ROBOT_CONTROLLER_ERROR_CODE_H

#include <stdint.h>

typedef enum {
    RC_ERR_OK = 0x0000,
    RC_ERR_BAD_COMMAND = 0x0001,
    RC_ERR_BAD_ARGUMENT = 0x0002,
    RC_ERR_COMMAND_TIMEOUT = 0x0003,
    RC_ERR_MOTOR_FAULT = 0x0100,
    RC_ERR_IMU_NOT_READY = 0x0200,
    RC_ERR_ENCODER_FAULT = 0x0300,
    RC_ERR_PROTOCOL_CRC = 0x0400,
} rc_error_code_t;

static inline const char *rc_error_code_name(rc_error_code_t code)
{
    switch (code) {
    case RC_ERR_OK:
        return "ERR_OK";
    case RC_ERR_BAD_COMMAND:
        return "ERR_BAD_COMMAND";
    case RC_ERR_BAD_ARGUMENT:
        return "ERR_BAD_ARGUMENT";
    case RC_ERR_COMMAND_TIMEOUT:
        return "ERR_COMMAND_TIMEOUT";
    case RC_ERR_MOTOR_FAULT:
        return "ERR_MOTOR_FAULT";
    case RC_ERR_IMU_NOT_READY:
        return "ERR_IMU_NOT_READY";
    case RC_ERR_ENCODER_FAULT:
        return "ERR_ENCODER_FAULT";
    case RC_ERR_PROTOCOL_CRC:
        return "ERR_PROTOCOL_CRC";
    default:
        return "ERR_UNKNOWN";
    }
}

static inline uint16_t rc_error_code_value(rc_error_code_t code)
{
    return (uint16_t)code;
}

#endif /* ROBOT_CONTROLLER_ERROR_CODE_H */
