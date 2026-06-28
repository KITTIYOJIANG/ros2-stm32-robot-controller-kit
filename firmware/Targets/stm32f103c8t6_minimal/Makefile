TARGET := c8t6_minimal
BUILD_DIR := build
FIRMWARE_ROOT := ../..

CC := arm-none-eabi-gcc
OBJCOPY := arm-none-eabi-objcopy
SIZE := arm-none-eabi-size

CPU_FLAGS := -mcpu=cortex-m3 -mthumb
CFLAGS := $(CPU_FLAGS) -std=c11 -Os -Wall -Wextra -ffunction-sections -fdata-sections
CFLAGS += -fno-builtin -fno-unwind-tables -fno-asynchronous-unwind-tables
CFLAGS += -I$(FIRMWARE_ROOT)
LDFLAGS := $(CPU_FLAGS) -nostdlib -Wl,--gc-sections -Wl,-Map=$(BUILD_DIR)/$(TARGET).map
LDFLAGS += -T linker/stm32f103c8t6.ld

SOURCES := \
	src/startup_stm32f103c8t6.c \
	src/main.c

OBJECTS := $(SOURCES:%.c=$(BUILD_DIR)/%.o)

.PHONY: all clean flash size

all: $(BUILD_DIR)/$(TARGET).elf $(BUILD_DIR)/$(TARGET).bin size

$(BUILD_DIR)/$(TARGET).elf: $(OBJECTS) linker/stm32f103c8t6.ld
	$(CC) $(OBJECTS) $(LDFLAGS) -o $@

$(BUILD_DIR)/$(TARGET).bin: $(BUILD_DIR)/$(TARGET).elf
	$(OBJCOPY) -O binary $< $@

$(BUILD_DIR)/%.o: %.c
	mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -c $< -o $@

size: $(BUILD_DIR)/$(TARGET).elf
	$(SIZE) $<

flash: $(BUILD_DIR)/$(TARGET).elf
	openocd -f flash_openocd.cfg -c "program $(BUILD_DIR)/$(TARGET).elf verify reset exit"

clean:
	rm -rf $(BUILD_DIR)
