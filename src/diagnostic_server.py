import json

class VehicleInterfaceSystem:
    """Manages the configuration handshake and system diagnostics"""
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.profiles = json.load(f)

    def load_vehicle_profile(self, vehicle_id):
        if vehicle_id not in self.profiles:
            raise ValueError(f"Vehicle ID '{vehicle_id}' not found in profiles.")
        return self.profiles[vehicle_id]

    def verify_safety_protocols(self, telemetry_frame):
        # Emulates safety checklist routines prior to and during dyno runs
        signals = telemetry_frame["signals"]
        if "coolant_temperature_c" in signals and signals["coolant_temperature_c"] > 110:
            return "CRITICAL_ERROR: ENGINE_OVERHEATING_ABORT_RUN"
        if "inverter_temperature_c" in signals and signals["inverter_temperature_c"] > 80:
            return "CRITICAL_ERROR: INVERTER_THERMAL_RUNAWAY_ABORT_RUN"
        return "SYSTEMS_NORMAL"
      
