#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#include "Config/error_code.h"
#include "Config/version.h"

#define PERIPH_BASE 0x40000000u
#define APB2PERIPH_BASE (PERIPH_BASE + 0x00010000u)
#define AHBPERIPH_BASE (PERIPH_BASE + 0x00018000u)

#define GPIOA_BASE (APB2PERIPH_BASE + 0x00000800u)
#define GPIOC_BASE (APB2PERIPH_BASE + 0x00001000u)
#define USART1_BASE (APB2PERIPH_BASE + 0x00003800u)
#define RCC_BASE (AHBPERIPH_BASE + 0x00001000u)

#define SYST_CSR (*(volatile uint32_t *)0xE000E010u)
#define SYST_RVR (*(volatile uint32_t *)0xE000E014u)
#define SYST_CVR (*(volatile uint32_t *)0xE000E018u)

#define HSI_CLOCK_HZ 8000000u
#define UART_BAUDRATE 115200u

#define RCC_APB2ENR_AFIOEN (1u << 0)
#define RCC_APB2ENR_IOPAEN (1u << 2)
#define RCC_APB2ENR_IOPCEN (1u << 4)
#define RCC_APB2ENR_USART1EN (1u << 14)

#define USART_SR_RXNE (1u << 5)
#define USART_SR_TXE (1u << 7)
#define USART_CR1_RE (1u << 2)
#define USART_CR1_TE (1u << 3)
#define USART_CR1_UE (1u << 13)

#define SYST_CSR_ENABLE (1u << 0)
#define SYST_CSR_TICKINT (1u << 1)
#define SYST_CSR_CLKSOURCE (1u << 2)

#define LED_PIN 13u
#define LED_PIN_MASK (1u << LED_PIN)
#define LINE_BUFFER_SIZE 64u

typedef struct {
    volatile uint32_t CR;
    volatile uint32_t CFGR;
    volatile uint32_t CIR;
    volatile uint32_t APB2RSTR;
    volatile uint32_t APB1RSTR;
    volatile uint32_t AHBENR;
    volatile uint32_t APB2ENR;
    volatile uint32_t APB1ENR;
    volatile uint32_t BDCR;
    volatile uint32_t CSR;
} rcc_registers_t;

typedef struct {
    volatile uint32_t CRL;
    volatile uint32_t CRH;
    volatile uint32_t IDR;
    volatile uint32_t ODR;
    volatile uint32_t BSRR;
    volatile uint32_t BRR;
    volatile uint32_t LCKR;
} gpio_registers_t;

typedef struct {
    volatile uint32_t SR;
    volatile uint32_t DR;
    volatile uint32_t BRR;
    volatile uint32_t CR1;
    volatile uint32_t CR2;
    volatile uint32_t CR3;
    volatile uint32_t GTPR;
} usart_registers_t;

#define RCC ((rcc_registers_t *)RCC_BASE)
#define GPIOA ((gpio_registers_t *)GPIOA_BASE)
#define GPIOC ((gpio_registers_t *)GPIOC_BASE)
#define USART1 ((usart_registers_t *)USART1_BASE)

static volatile uint32_t g_millis;
static volatile uint32_t g_led_tick_count;
static char g_line_buffer[LINE_BUFFER_SIZE];
static size_t g_line_length;

static void board_clock_init(void);
static void led_init(void);
static void led_toggle(void);
static void systick_init(void);
static void usart1_init(void);
static void uart_write_char(char value);
static void uart_write(const char *text);
static void uart_write_line(const char *text);
static int uart_read_char_nonblocking(void);
static void command_process_char(char value);
static void command_handle_line(const char *line);
static bool string_equals(const char *left, const char *right);
static const char *error_name(rc_error_code_t code);
static const char *error_value(rc_error_code_t code);

int main(void)
{
    board_clock_init();
    led_init();
    usart1_init();
    systick_init();

    while (1) {
        int value = uart_read_char_nonblocking();
        if (value >= 0) {
            command_process_char((char)value);
        }
    }
}

void SysTick_Handler(void)
{
    g_millis++;
    g_led_tick_count++;
    if (g_led_tick_count >= 500u) {
        g_led_tick_count = 0u;
        led_toggle();
    }
}

static void board_clock_init(void)
{
    RCC->APB2ENR |= RCC_APB2ENR_AFIOEN | RCC_APB2ENR_IOPAEN |
                    RCC_APB2ENR_IOPCEN | RCC_APB2ENR_USART1EN;
}

static void led_init(void)
{
    GPIOC->CRH &= ~(0xFu << 20u);
    GPIOC->CRH |= (0x2u << 20u);
    GPIOC->BSRR = LED_PIN_MASK;
}

static void led_toggle(void)
{
    if ((GPIOC->ODR & LED_PIN_MASK) != 0u) {
        GPIOC->BRR = LED_PIN_MASK;
    } else {
        GPIOC->BSRR = LED_PIN_MASK;
    }
}

static void systick_init(void)
{
    SYST_RVR = (HSI_CLOCK_HZ / 1000u) - 1u;
    SYST_CVR = 0u;
    SYST_CSR = SYST_CSR_CLKSOURCE | SYST_CSR_TICKINT | SYST_CSR_ENABLE;
}

static void usart1_init(void)
{
    GPIOA->CRH &= ~((0xFu << 4u) | (0xFu << 8u));
    GPIOA->CRH |= (0xAu << 4u) | (0x4u << 8u);

    USART1->CR1 = 0u;
    USART1->BRR = (HSI_CLOCK_HZ + (UART_BAUDRATE / 2u)) / UART_BAUDRATE;
    USART1->CR1 = USART_CR1_UE | USART_CR1_TE | USART_CR1_RE;
}

static void uart_write_char(char value)
{
    while ((USART1->SR & USART_SR_TXE) == 0u) {
    }
    USART1->DR = (uint32_t)(uint8_t)value;
}

static void uart_write(const char *text)
{
    while (*text != '\0') {
        uart_write_char(*text++);
    }
}

static void uart_write_line(const char *text)
{
    uart_write(text);
    uart_write("\r\n");
}

static int uart_read_char_nonblocking(void)
{
    if ((USART1->SR & USART_SR_RXNE) == 0u) {
        return -1;
    }
    return (int)(USART1->DR & 0xFFu);
}

static void command_process_char(char value)
{
    if (value == '\r' || value == '\n') {
        if (g_line_length > 0u) {
            g_line_buffer[g_line_length] = '\0';
            command_handle_line(g_line_buffer);
            g_line_length = 0u;
        }
        return;
    }

    if (g_line_length >= (LINE_BUFFER_SIZE - 1u)) {
        g_line_length = 0u;
        uart_write_line("ERROR code=0x0002 name=ERR_BAD_ARGUMENT message=\"line too long\"");
        return;
    }

    g_line_buffer[g_line_length++] = value;
}

static void command_handle_line(const char *line)
{
    if (string_equals(line, "PING")) {
        uart_write_line("ACK PING");
        return;
    }

    if (string_equals(line, "GET_VERSION")) {
        uart_write("VERSION firmware=");
        uart_write(ROBOT_CONTROLLER_FIRMWARE_VERSION_STRING);
        uart_write(" protocol=");
        uart_write(ROBOT_CONTROLLER_PROTOCOL_VERSION_STRING);
        uart_write(" board=");
        uart_write(ROBOT_CONTROLLER_BOARD_NAME);
        uart_write("\r\n");
        return;
    }

    if (string_equals(line, "STOP")) {
        uart_write_line("ACK STOP");
        return;
    }

    uart_write("ERROR code=");
    uart_write(error_value(RC_ERR_BAD_COMMAND));
    uart_write(" name=");
    uart_write(error_name(RC_ERR_BAD_COMMAND));
    uart_write_line(" message=\"unknown command\"");
}

static bool string_equals(const char *left, const char *right)
{
    while (*left != '\0' && *right != '\0') {
        if (*left != *right) {
            return false;
        }
        left++;
        right++;
    }
    return *left == '\0' && *right == '\0';
}

static const char *error_name(rc_error_code_t code)
{
    switch (code) {
    case RC_ERR_BAD_COMMAND:
        return "ERR_BAD_COMMAND";
    case RC_ERR_BAD_ARGUMENT:
        return "ERR_BAD_ARGUMENT";
    case RC_ERR_OK:
    case RC_ERR_COMMAND_TIMEOUT:
    case RC_ERR_MOTOR_FAULT:
    case RC_ERR_IMU_NOT_READY:
    case RC_ERR_ENCODER_FAULT:
    case RC_ERR_PROTOCOL_CRC:
    default:
        return "ERR_UNKNOWN";
    }
}

static const char *error_value(rc_error_code_t code)
{
    switch (code) {
    case RC_ERR_BAD_COMMAND:
        return "0x0001";
    case RC_ERR_BAD_ARGUMENT:
        return "0x0002";
    case RC_ERR_OK:
    case RC_ERR_COMMAND_TIMEOUT:
    case RC_ERR_MOTOR_FAULT:
    case RC_ERR_IMU_NOT_READY:
    case RC_ERR_ENCODER_FAULT:
    case RC_ERR_PROTOCOL_CRC:
    default:
        return "0xFFFF";
    }
}
