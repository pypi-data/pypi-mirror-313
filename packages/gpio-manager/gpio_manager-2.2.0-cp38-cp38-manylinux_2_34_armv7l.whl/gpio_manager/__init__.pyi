"""
gpio_manager

A comprehensive library for managing GPIO operations, including input/output control,
PWM management, I2C communication, and support for edge-triggered callbacks with debounce.
Suitable for all Raspberry Pi models.

Classes:

- GPIOManager: Manages GPIO pins, including input and output configurations, and supports callback assignments.

- PWMManager: Controls Pulse Width Modulation (PWM) functionality for GPIO pins.

- I2CManager: Provides I2C communication functions for interacting with I2C devices.

- Enums: Defines enums such as PinState, LogicLevel, InternPullResistorState, and TriggerEdge for easy configuration
of pin states and edge triggers.

Example usage:
    from gpio_manager import GPIOManager
    gpio = GPIOManager()
    gpio.add_input_pin(pin_num=4)
    gpio.assign_callback(pin_num=4, callback=my_callback)
"""


class InternPullResistorState:
    """Enum representing the GPIO pin state types for input pins."""
    PULLUP: 'InternPullResistorState'
    """
    Pulls the pin up to VCC.
    """
    PULLDOWN: 'InternPullResistorState'
    """
    Pulls the pin down to ground.
    """
    EXTERNAL: 'InternPullResistorState'
    """
    Don't use the internal pull resistor.
    """
    AUTO: 'InternPullResistorState'
    """
    Automatically picks the pull resistor based on the pin logic level (Default).
    """


class PinState:
    """Enum representing the GPIO pin state types for output pins. The state represents the logic state of the pin. The voltage will be set based on the logic level."""
    HIGH: 'PinState'
    """
    Sets the pin to Logic HIGH.
    """
    LOW: 'PinState'
    """
    Sets the pin to Logic LOW.
    """


class LogicLevel:
    """Enum representing the logic levels of the pins."""
    HIGH: 'LogicLevel'
    """
    Logic high, when the voltage is close to VCC (Default).
    """
    LOW: 'LogicLevel'
    """
    Logic high, when the voltage is close to ground.
    """


class TriggerEdge:
    """Enum representing the trigger edge types. Triggers are based off logic level changes"""
    RISING: 'TriggerEdge'
    """
    Trigger on the rising edge. (from Logic LOW to Logic HIGH)
    """
    FALLING: 'TriggerEdge'
    """
    Trigger on the falling edge. (from Logic HIGH to Logic LOW)
    """
    BOTH: 'TriggerEdge'
    """
    Trigger on both edges (Default).
    """

class I2CManager:
    """I2CManager provides methods to manage I2C communication."""

    def __init__(self) -> None:
        """Initializes a new I2CManager instance."""
        ...

    def open(self, bus: Optional[int] = 1) -> None:
        """
        Opens the I2C bus.

        :param bus: The I2C bus number to open (default is 1).
        """
        ...

    def close(self) -> None:
        """
        Closes the I2C bus.
        """
        ...

    def write_byte(self, addr: int, data: int) -> None:
        """
        Writes a single byte to the I2C slave device.

        :param addr: The I2C slave address.
        :param data: The byte to write.
        """
        ...

    def block_write_byte(self, addr: int, command: int, data: int) -> None:
        """
        Writes a single byte with a command to the I2C slave device.

        :param addr: The I2C slave address.
        :param command: The command to send.
        :param data: The byte to write.
        """
        ...

    def read_byte(self, addr: int) -> int:
        """
        Reads a single byte from the I2C slave device.

        :param addr: The I2C slave address.
        :return: The byte read.
        """
        ...

    def block_read_byte(self, addr: int, command: int) -> int:
        """
        Reads a single byte with a command from the I2C slave device.

        :param addr: The I2C slave address.
        :param command: The command to send before reading.
        :return: The byte read.
        """
        ...

    def write(self, addr: int, data: bytes) -> None:
        """
        Writes data to the I2C slave device.

        :param addr: The I2C slave address.
        :param data: The bytes to write.
        """
        ...

    def block_write(self, addr: int, command: int, data: bytes) -> None:
        """
        Writes data with a command to the I2C slave device.

        :param addr: The I2C slave address.
        :param command: The command to send.
        :param data: The bytes to write.
        """
        ...

    def read(self, addr: int, length: int) -> bytes:
        """
        Reads data from the I2C slave device.

        :param addr: The I2C slave address.
        :param length: The number of bytes to read.
        :return: The bytes read.
        """
        ...

    def block_read(self, addr: int, command: int, length: int) -> bytes:
        """
        Reads data with a command from the I2C slave device.

        :param addr: The I2C slave address.
        :param command: The command to send before reading.
        :param length: The number of bytes to read.
        :return: The bytes read.
        """
        ...

    def write_read(self, addr: int, write_data: bytes, read_length: int) -> bytes:
        """
        Performs a write followed by a read operation.

        :param addr: The I2C slave address.
        :param write_data: The bytes to write.
        :param read_length: The number of bytes to read.
        :return: The bytes read.
        """
        ...

    def block_write_read(self, addr: int, command: int, write_data: bytes, read_length: int) -> bytes:
        """
        Performs a block write followed by a block read operation.

        :param addr: The I2C slave address.
        :param command: The command to send.
        :param write_data: The bytes to write.
        :param read_length: The number of bytes to read.
        :return: The bytes read.
        """
        ...

class PWMManager:
    """PWMManager provides methods to manage PWM channels."""

    def __init__(self) -> None:
        """Initializes a new PWMManager instance."""
        ...

    def setup_pwm_channel(self, channel_num: int, frequency_hz: Optional[float] = None,
                          duty_cycle: Optional[float] = None, period_ms: Optional[float] = None,
                          pulse_width_ms: Optional[float] = None,
                          logic_level: Optional['LogicLevel'] = LogicLevel.HIGH) -> None:
        """
        Sets up a PWM channel with the specified parameters.
        The value of frequency_hz and duty_cycle overwrites period_ms and pulse_width_ms if they are set.
        If neither frequency_hz and duty_cycle nor period_ms and pulse_width_ms are set, the default value of 1000 hz
        and a duty_cycle of 0 are used.

        :param channel_num: The PWM channel number (0 or 1).
        :param frequency_hz: The frequency in Hertz.
        :param duty_cycle: The duty cycle (0 to 100).
        :param period_ms: The period in milliseconds.
        :param pulse_width_ms: The pulse width in milliseconds.
        :param logic_level: The Logic level of the PWM signal (set using LogicLevel.[NORMAL or INVERSE]).
        """
        ...

    def start_pwm_channel(self, channel_num: int) -> None:
        """
        Starts the PWM signal on the specified channel.

        :param channel_num: The PWM channel number (0 or 1).
        """
        ...

    def stop_pwm_channel(self, channel_num: int) -> None:
        """
        Stops the PWM signal on the specified channel.

        :param channel_num: The PWM channel number (0 or 1).
        """
        ...

    def reset_pwm_channel(self, channel_num: int) -> None:
        """
        resets the PWM channel and removes it from the manager.

        :param channel_num: The PWM channel number (0 or 1).
        """
        ...

    def set_duty_cycle(self, channel_num: int, duty_cycle: float) -> None:
        """
        Sets the duty cycle for the specified PWM channel.

        :param channel_num: The PWM channel number (0 or 1).
        :param duty_cycle: The new duty cycle (0 to 100).
        """
        ...

    def set_frequency(self, channel_num: int, frequency_hz: float) -> None:
        """
        Sets the frequency for the specified PWM channel.

        :param channel_num: The PWM channel number (0 or 1).
        :param frequency_hz: The new frequency in Hertz.
        """
        ...

    def set_period(self, channel_num: int, period_ms: float) -> None:
        """
        Sets the period for the specified PWM channel in milliseconds.

        :param channel_num: The PWM channel number (0 or 1).
        :param period_ms: The new period in seconds.
        """

    ...

    def set_pulse_width(self, channel_num: int, pulse_width_ms: float) -> None:
        """
        Sets the pulse width for the specified PWM channel in milliseconds.

        :param channel_num: The PWM channel number (0 or 1).
        :param pulse_width_ms: The new pulse width in ms.
        """
        ...

    def get_frequency(self, channel_num: int) -> float:
        """
        Gets the current frequency of the specified PWM channel.

        :param channel_num: The PWM channel number (0 or 1).
        :return: The current frequency in Hertz.
        """
        ...

    def get_duty_cycle(self, channel_num: int) -> float:
        """
        Gets the current duty cycle of the specified PWM channel.

        :param channel_num: The PWM channel number (0 or 1).
        :return: The current duty cycle (0 to 100).
        """
        ...

    def get_period(self, channel_num: int) -> float:
        """
        Gets the current period of the specified PWM channel.

        :param channel_num: The PWM channel number (0 or 1).
        :return: The current period in milliseconds.
        """
        ...

    def get_pulse_width(self, channel_num: int) -> float:
        """
        Gets the current pulse width of the specified PWM channel.

        :param channel_num: The PWM channel number (0 or 1).
        :return: The current pulse width in milliseconds.
        """
        ...

    def cleanup(self) -> None:
        """
        Sets all PWM channels to the disabled state and clears them from the set list
        """

from typing import Optional, Tuple, Callable


class GPIOManager:
    """GPIOManager provides methods to manage GPIO pins and register callbacks."""

    def __init__(self) -> None:
        """Initializes a new GPIOManager instance."""
        ...

    def add_input_pin(self, pin_num: int,
                      pull_resistor_state: Optional[InternPullResistorState] = InternPullResistorState.AUTO,
                      logic_level: Optional[LogicLevel] = LogicLevel.HIGH) -> None:
        """
        Sets up an input pin but does not assign a callback yet.

        :param pin_num: The GPIO pin to configure as input.
        :param pull_resistor_state: The pin state (set it by using gpio_manager.InternPullResistorState.[PULLUP, PULLDOWN, EXTERNAL, or AUTO]).
        :param logic_level: The logic level of the pin (set it by using gpio_manager.LogicLevel.[HIGH or LOW]).
        """
        ...

    def assign_callback(self, pin_num: int, callback: Callable[..., None], trigger_edge: Optional[TriggerEdge] =
    TriggerEdge.BOTH, debounce_time_ms: Optional[int] = 2, args: Optional[Tuple] = None, include_trigger_time: Optional[bool] = False,
                        include_trigger_edge: Optional[bool] = False) -> None:
        """
        Assigns a callback to an input pin. If enabled, TriggerTime is a float representing the time the trigger occurred since unix time epoch. TriggerEdge is an enum representing the edge that triggered the
        callback (gpio_manager.TriggerEdge.[RISING, FALLING]).

        :param pin_num: The GPIO pin.
        :param callback: The callback function to be invoked on pin change.
        :param trigger_edge: The edge trigger type (set using gpio_manager.TriggerEdge.[RISING, FALLING, BOTH]).
        :param args: The arguments to pass to the callback function.
        :param debounce_time_ms: The debounce time in milliseconds.
        :param include_trigger_time: Whether to include the trigger time in the callback. (Will be the first argument)
        :param include_trigger_edge: Whether to include the trigger edge in the callback. (Will be the second argument if include_trigger_time is True, otherwise the first
        argument)
        """
        ...

    def add_output_pin(self, pin_num: int, pin_state: Optional[PinState] = PinState.LOW,
                       logic_level: Optional[LogicLevel] = LogicLevel.HIGH) -> None:
        """
        Sets up an output pin.

        :param pin_num: The GPIO pin to configure as output.
        :param pin_state: The initial state of the pin (set it by using gpio_manager.PINState.[HIGH or LOW]).
        :param logic_level: The logic level of the pin (set it by using gpio_manager.LogicLevel.[HIGH or LOW]).
        """
        ...

    def set_output_pin(self, pin_num: int, pin_state: PinState) -> None:
        """
        Sets the state of an output pin.

        :param pin_num: The GPIO pin.
        :param pin_state: The desired state (set it by using gpio_manager.PINState.[HIGH or LOW]).
        """
        ...

    def get_pin(self, pin_num: int) -> PinState:
        """
        Polls the current state of an input pin.

        :param pin_num: The GPIO pin to get.
        :return: The current state of the pin (check it by using gpio_manager.PINState.[HIGH or LOW]).
        """
        ...

    def unassign_callback(self, pin_num: int) -> None:
        """
        Unassigns a callback from an input pin.

        :param pin_num: The GPIO pin whose callback is to be reset.
        """
        ...

    def wait_for_edge(self, pin_num: int, trigger_edge: Optional[TriggerEdge] = TriggerEdge.BOTH, timeout_ms:
    Optional[int] = None) -> None:
        """
        Waits for an edge on the assigned pin. This function block for the given timeout, or waits forever if it is 
        set to a negative number or None.

        :param pin_num: The GPIO pin.
        :param trigger_edge: The trigger type (set using gpio_manager.TriggerEdge.[RISING, FALLING, BOTH]).
        :param timeout_ms: Timeout in milliseconds.
        """
        ...

    def setup_pwm(self, pin_num, frequency_hz: Optional[float] = None, duty_cycle: Optional[float] = None,
                  period_ms: Optional[float] = None,
                  pulse_width_ms: Optional[float] = None, logic_level: Optional[LogicLevel] = LogicLevel.HIGH) -> None:
        """
        Sets up a PWM signal on the given pin. If The pin must be set up as an output pin before calling this
        function, the values for the logic level and current state will be preserved otherwise the default values
        will be used when setting up pwm for the pin (initial output low and logic high).

        The value of frequency_hz and duty_cycle overwrites period_ms and pulse_width_ms if they are set.
        If neither frequency_hz and duty_cycle nor period_ms and pulse_width_ms are set, the default value of 1000 hz
        and a duty_cycle of 0 are used.

        :param pin_num: The GPIO pin.
        :param frequency_hz: The period of the pwm signal in hertz.
        :param duty_cycle: The pulse width of the pwm signal as a percentage of the frequency (Duty cycle must be between 0 and 100).
        :param period_ms: The period in milliseconds.
        :param pulse_width_ms: The pulse width in milliseconds.
        :param logic_level: The logic level of the pin (set it by using gpio_manager.LogicLevel.[HIGH or LOW]).
        """
        ...

    def set_pwm_duty_cycle(self, pin_num: int, duty_cycle: float) -> None:
        """
        Sets the PWM signal's duty cycle.
        :param pin_num: The GPIO pin.
        :param duty_cycle: The pulse width of the pwm signal as a percentage of the frequency (Duty cycle must be between 0 and 100).
        """
        ...

    def set_pwm_frequency(self, pin_num: int, frequency_hz: float) -> None:
        """
        Sets the PWM signal's frequency.
        :param pin_num: The GPIO pin.
        :param frequency_hz: The period of the pwm signal in hertz.
        """
        ...

    def set_pwm_period(self, pin_num: int, period_ms: float) -> None:
        """
        Sets the PWM signal's period.
        :param pin_num: The GPIO pin.
        :param period_ms: The period in milliseconds.
        """
        ...

    def set_pwm_pulse_width(self, pin_num: int, pulse_width_ms: float) -> None:
        """
        Sets the PWM signal's pulse width.
        :param pin_num: The GPIO pin.
        :param pulse_width_ms: The pulse width in milliseconds.
        """
        ...

    def start_pwm(self, pin_num: int) -> None:
        """
        Starts the PWM signal.
        :param pin_num: The GPIO pin.
        """
        ...

    def stop_pwm(self, pin_num: int) -> None:
        """
        Stops the PWM signal.
        :param pin_num: The GPIO pin.
        """
        ...

    def reset_pin(self, pin_num: int) -> None:
        """
        Resets the given pin so it can set to either input or output.
        :param pin_num: The GPIO pin.
        """

    ...

    def cleanup(self) -> None:
        """
        Cleans up the GPIO pins by setting all output pins to low and clearing all interrupts.
        """
        ...

