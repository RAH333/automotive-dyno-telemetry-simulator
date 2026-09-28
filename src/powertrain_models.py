import random

class ICEPowertrain:
    def __init__(self, profile):
        self.p = profile
        self.rpm = self.p["idle_rpm"]
        self.coolant_temp = 25.0  # Celsius

    def update(self, throttle, dyno_load_nm):
        # Calculate dynamic RPM updates based on throttle and simulated dynamometer load
        rpm_delta = (throttle * 1500) - (dyno_load_nm * 2.5)
        self.rpm = max(self.p["idle_rpm"], min(self.p["max_rpm"], self.rpm + rpm_delta))
        
        # Simulate engine thermal behavior
        if self.coolant_temp < 90.0:
            self.coolant_temp += 0.05 * (self.rpm / 1000.0)
        else:
            self.coolant_temp += random.uniform(-0.2, 0.2)

        # Basic emissions scaling function relative to RPM and load conditions
        co2_emission = (self.p["base_co2_g_km"] / 100.0) * (self.rpm / 2000.0) * (1.0 + throttle)
        nox_emission = 0.05 * (self.coolant_temp / 90.0) * (throttle * 1.5)

        return {
            "engine_rpm": round(self.rpm, 1),
            "coolant_temperature_c": round(self.coolant_temp, 1),
            "co2_g_km": round(co2_emission, 2),
            "nox_g_km": round(nox_emission, 4),
            "exhaust_gas_temp_c": round(200 + (self.rpm * 0.12), 1)
        }

class EVPowertrain:
    def __init__(self, profile):
        self.p = profile
        self.motor_rpm = 0
        self.soc = 100.0  # State of Charge %
        self.inverter_temp = 25.0

    def update(self, throttle, dyno_load_nm):
        rpm_delta = (throttle * 3000) - (dyno_load_nm * 1.8)
        self.motor_rpm = max(0, min(self.p["max_motor_rpm"], self.motor_rpm + rpm_delta))
        
        # Simulate battery drainage and inverter thermal load
        current_draw = (throttle * 350) + (dyno_load_nm * 0.5)
        self.soc = max(0.0, self.soc - (current_draw * 0.0001))
        self.inverter_temp = max(25.0, min(85.0, 25.0 + (current_draw * 0.12)))

        return {
            "motor_rpm": round(self.motor_rpm, 1),
            "battery_soc_pct": round(self.soc, 2),
            "inverter_temperature_c": round(self.inverter_temp, 1),
            "current_draw_a": round(current_draw, 1),
            "co2_g_km": 0.00,
            "nox_g_km": 0.0000
        }
      
