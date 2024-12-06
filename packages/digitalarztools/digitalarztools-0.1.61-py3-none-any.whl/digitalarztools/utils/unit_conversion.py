class FlowConverter:
    @staticmethod
    def cusecs_to_cumecs(cusecs):
        """
        Convert cubic feet per second (cusecs) to cubic meters per second (cumecs).

        :param cusecs: float, value in cusecs
        :return: float, value in cumecs
        """
        cumecs = cusecs * 0.0283168
        return cumecs

    @staticmethod
    def cumecs_to_cusecs(cumecs):
        """
        Convert cubic meters per second (cumecs) to cubic feet per second (cusecs).

        :param cumecs: float, value in cumecs
        :return: float, value in cusecs
        """
        cusecs = cumecs * 35.3147
        return cusecs


class TemperatureConverter:
    @staticmethod
    def kelvin_to_celsius(kelvin: float) -> float:
        """Convert Kelvin to Celsius."""
        return kelvin - 273.15

    @staticmethod
    def celsius_to_kelvin(celsius: float) -> float:
        """Convert Celsius to Kelvin."""
        return celsius + 273.15

    @staticmethod
    def kelvin_to_fahrenheit(kelvin: float) -> float:
        """Convert Kelvin to Fahrenheit."""
        celsius = TemperatureConverter.kelvin_to_celsius(kelvin)
        return TemperatureConverter.celsius_to_fahrenheit(celsius)

    @staticmethod
    def fahrenheit_to_kelvin(fahrenheit: float) -> float:
        """Convert Fahrenheit to Kelvin."""
        celsius = TemperatureConverter.fahrenheit_to_celsius(fahrenheit)
        return TemperatureConverter.celsius_to_kelvin(celsius)

    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        """Convert Celsius to Fahrenheit."""
        return (celsius * 9 / 5) + 32

    @staticmethod
    def fahrenheit_to_celsius(fahrenheit: float) -> float:
        """Convert Fahrenheit to Celsius."""
        return (fahrenheit - 32) * 5 / 9
