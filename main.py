import time
from src.diagnostic_server import VehicleInterfaceSystem
from src.powertrain_models import ICEPowertrain, EVPowertrain
from src.data_acquisition.import DiagnosticDataAcquisition

def run_dyno_test_cycle(vehicle_type, vehicle_id):
    print(f"=== INITIALIZING CHASSIS DYNO TESTING FOR: {vehicle_id.upper()} ===")
    vif = VehicleInterfaceSystem("config/vehicle_profiles.json")
    daq = DiagnosticDataAcquisition()
    
    profile = vif.load_vehicle_profile(vehicle_id)
    powertrain = ICEPowertrain(profile) if vehicle_type == "ICE" else EVPowertrain(profile)
    
    daq.start_da_session()
    start_time = time.time()
    
    # 5-step test profile simulating dynamic throttle alterations on a dyno bed
    test_steps = [(0.2, 50), (0.5, 120), (0.8, 200), (0.4, 150), (0.0, 30)]
    
    for idx, (throttle, load) in enumerate(test_steps):
        time.sleep(0.5) # Simulate time steps
        elapsed = time.time() - start_time
        
        raw_signals = powertrain.update(throttle, load)
        frame = daq.process_telemetry(elapsed, raw_signals)
        safety_status = vif.verify_safety_protocols(frame)
        
        print(f"[T+{elapsed:.2f}s] Safety: {safety_status} | Signals: {frame['signals']}")
        if "CRITICAL" in safety_status:
            print("DYNO RUN EMERGENCY STOP TRIGGERED.")
            break
            
    print(f"=== TEST RUN FOR {vehicle_id.upper()} COMPLETED. LOGGED {len(daq.log_buffer)} FRAMES ===\n")

if __name__ == "__main__":
    # Test execution for both ICE Powertrain emission cycles and EV test profiles
    run_dyno_test_cycle("ICE", "ice_suv")
    run_dyno_test_cycle("EV", "ev_suv")
  
