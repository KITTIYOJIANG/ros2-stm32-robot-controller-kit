#ifndef ROBOT_CONTROLLER_PROTOCOL_H
#define ROBOT_CONTROLLER_PROTOCOL_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#include "../Config/error_code.h"

#define RC_PROTOCOL_MAX_LINE_LENGTH 128
#define RC_PROTOCOL_MAX_RESPONSE_LENGTH 160

typedef enum {
    RC_PROTOCOL_COMMAND_UNKNOWN = 0,
    RC_PROTOCOL_COMMAND_PING,
    RC_PROTOCOL_COMMAND_GET_VERSION,
    RC_PROTOCOL_COMMAND_GET_STATUS,
    RC_PROTOCOL_COMMAND_SET_MOTOR,
    RC_PROTOCOL_COMMAND_STOP,
    RC_PROTOCOL_COMMAND_READ_IMU,
    RC_PROTOCOL_COMMAND_READ_ENCODER,
} rc_protocol_command_t;

typedef struct {
    rc_protocol_command_t command;
    float left_speed;
    float right_speed;
} rc_protocol_message_t;

typedef struct {
    const char *state;
    rc_error_code_t last_error;
    uint32_t uptime_ms;
    bool motor_fault;
    bool imu_ready;
    bool encoder_ready;
} rc_protocol_status_t;

typedef struct {
    float ax;
    float ay;
    float az;
    float gx;
    float gy;
    float gz;
} rc_protocol_imu_sample_t;

typedef struct {
    int32_t left;
    int32_t right;
} rc_protocol_encoder_sample_t;

rc_error_code_t rc_protocol_parse_line(const char *line, rc_protocol_message_t *message);

size_t rc_protocol_format_ack(
    rc_protocol_command_t command,
    char *buffer,
    size_t buffer_size);

size_t rc_protocol_format_error(
    rc_error_code_t code,
    const char *message,
    char *buffer,
    size_t buffer_size);

size_t rc_protocol_format_version(char *buffer, size_t buffer_size);

size_t rc_protocol_format_status(
    const rc_protocol_status_t *status,
    char *buffer,
    size_t buffer_size);

size_t rc_protocol_format_imu(
    const rc_protocol_imu_sample_t *sample,
    char *buffer,
    size_t buffer_size);

size_t rc_protocol_format_encoder(
    const rc_protocol_encoder_sample_t *sample,
    char *buffer,
    size_t buffer_size);

const char *rc_protocol_command_name(rc_protocol_command_t command);

#endif /* ROBOT_CONTROLLER_PROTOCOL_H */
