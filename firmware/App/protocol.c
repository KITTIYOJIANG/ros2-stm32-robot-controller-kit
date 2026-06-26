#include "protocol.h"

#include <stdio.h>
#include <string.h>

#include "../Config/version.h"

static bool is_speed_in_range(float value)
{
    return value >= -1.0f && value <= 1.0f;
}

const char *rc_protocol_command_name(rc_protocol_command_t command)
{
    switch (command) {
    case RC_PROTOCOL_COMMAND_PING:
        return "PING";
    case RC_PROTOCOL_COMMAND_GET_VERSION:
        return "GET_VERSION";
    case RC_PROTOCOL_COMMAND_GET_STATUS:
        return "GET_STATUS";
    case RC_PROTOCOL_COMMAND_SET_MOTOR:
        return "SET_MOTOR";
    case RC_PROTOCOL_COMMAND_STOP:
        return "STOP";
    case RC_PROTOCOL_COMMAND_READ_IMU:
        return "READ_IMU";
    case RC_PROTOCOL_COMMAND_READ_ENCODER:
        return "READ_ENCODER";
    case RC_PROTOCOL_COMMAND_UNKNOWN:
    default:
        return "UNKNOWN";
    }
}

rc_error_code_t rc_protocol_parse_line(const char *line, rc_protocol_message_t *message)
{
    if (line == NULL || message == NULL) {
        return RC_ERR_BAD_ARGUMENT;
    }

    message->command = RC_PROTOCOL_COMMAND_UNKNOWN;
    message->left_speed = 0.0f;
    message->right_speed = 0.0f;

    if (strcmp(line, "PING") == 0) {
        message->command = RC_PROTOCOL_COMMAND_PING;
        return RC_ERR_OK;
    }

    if (strcmp(line, "GET_VERSION") == 0) {
        message->command = RC_PROTOCOL_COMMAND_GET_VERSION;
        return RC_ERR_OK;
    }

    if (strcmp(line, "GET_STATUS") == 0) {
        message->command = RC_PROTOCOL_COMMAND_GET_STATUS;
        return RC_ERR_OK;
    }

    if (strcmp(line, "STOP") == 0) {
        message->command = RC_PROTOCOL_COMMAND_STOP;
        return RC_ERR_OK;
    }

    if (strcmp(line, "READ_IMU") == 0) {
        message->command = RC_PROTOCOL_COMMAND_READ_IMU;
        return RC_ERR_OK;
    }

    if (strcmp(line, "READ_ENCODER") == 0) {
        message->command = RC_PROTOCOL_COMMAND_READ_ENCODER;
        return RC_ERR_OK;
    }

    if (strncmp(line, "SET_MOTOR", 9) == 0) {
        float left = 0.0f;
        float right = 0.0f;
        int matched = sscanf(line, "SET_MOTOR left=%f right=%f", &left, &right);
        if (matched != 2) {
            return RC_ERR_BAD_ARGUMENT;
        }
        if (!is_speed_in_range(left) || !is_speed_in_range(right)) {
            return RC_ERR_BAD_ARGUMENT;
        }
        message->command = RC_PROTOCOL_COMMAND_SET_MOTOR;
        message->left_speed = left;
        message->right_speed = right;
        return RC_ERR_OK;
    }

    return RC_ERR_BAD_COMMAND;
}

size_t rc_protocol_format_ack(
    rc_protocol_command_t command,
    char *buffer,
    size_t buffer_size)
{
    int written = snprintf(
        buffer,
        buffer_size,
        "ACK %s",
        rc_protocol_command_name(command));
    return written < 0 ? 0u : (size_t)written;
}

size_t rc_protocol_format_error(
    rc_error_code_t code,
    const char *message,
    char *buffer,
    size_t buffer_size)
{
    int written = snprintf(
        buffer,
        buffer_size,
        "ERROR code=0x%04X name=%s message=\"%s\"",
        rc_error_code_value(code),
        rc_error_code_name(code),
        message == NULL ? "" : message);
    return written < 0 ? 0u : (size_t)written;
}

size_t rc_protocol_format_version(char *buffer, size_t buffer_size)
{
    int written = snprintf(
        buffer,
        buffer_size,
        "VERSION firmware=%s protocol=%s board=%s",
        ROBOT_CONTROLLER_FIRMWARE_VERSION_STRING,
        ROBOT_CONTROLLER_PROTOCOL_VERSION_STRING,
        ROBOT_CONTROLLER_BOARD_NAME);
    return written < 0 ? 0u : (size_t)written;
}

size_t rc_protocol_format_status(
    const rc_protocol_status_t *status,
    char *buffer,
    size_t buffer_size)
{
    if (status == NULL) {
        return rc_protocol_format_error(
            RC_ERR_BAD_ARGUMENT,
            "missing status",
            buffer,
            buffer_size);
    }

    int written = snprintf(
        buffer,
        buffer_size,
        "STATUS state=%s error=%s uptime_ms=%lu motor_fault=%u imu_ready=%u encoder_ready=%u",
        status->state == NULL ? "UNKNOWN" : status->state,
        rc_error_code_name(status->last_error),
        (unsigned long)status->uptime_ms,
        status->motor_fault ? 1u : 0u,
        status->imu_ready ? 1u : 0u,
        status->encoder_ready ? 1u : 0u);
    return written < 0 ? 0u : (size_t)written;
}

size_t rc_protocol_format_imu(
    const rc_protocol_imu_sample_t *sample,
    char *buffer,
    size_t buffer_size)
{
    if (sample == NULL) {
        return rc_protocol_format_error(
            RC_ERR_IMU_NOT_READY,
            "missing imu sample",
            buffer,
            buffer_size);
    }

    int written = snprintf(
        buffer,
        buffer_size,
        "IMU ax=%.3f ay=%.3f az=%.3f gx=%.3f gy=%.3f gz=%.3f",
        sample->ax,
        sample->ay,
        sample->az,
        sample->gx,
        sample->gy,
        sample->gz);
    return written < 0 ? 0u : (size_t)written;
}

size_t rc_protocol_format_encoder(
    const rc_protocol_encoder_sample_t *sample,
    char *buffer,
    size_t buffer_size)
{
    if (sample == NULL) {
        return rc_protocol_format_error(
            RC_ERR_ENCODER_FAULT,
            "missing encoder sample",
            buffer,
            buffer_size);
    }

    int written = snprintf(
        buffer,
        buffer_size,
        "ENCODER left=%ld right=%ld",
        (long)sample->left,
        (long)sample->right);
    return written < 0 ? 0u : (size_t)written;
}
