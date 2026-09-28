import unittest
from src.powertrain_models import ICEPowertrain

class TestAutomotivePowertrain(unittest.TestCase):
    def setUp(self):
        self.mock_ice_profile = {
            "type": "ICE",
            "idle_rpm": 800,
            "max_rpm": 4500,
            "base_co2_g_km": 172
        }
        self.engine = ICEPowertrain(self.mock_ice_profile)

    def test_idle_constraints(self):
        # Engine should stay at or above its target idle value
        metrics = self.engine.update(throttle=0.0, dyno_load_nm=200)
        self.assertGreaterEqual(metrics["engine_rpm"], 800)

    def test_emission_trends(self):
        # Emissions should rise proportionally with engine throttle increases
        low_throttle_metrics = self.engine.update(throttle=0.1, dyno_load_nm=50)
        high_throttle_metrics = self.engine.update(throttle=0.9, dyno_load_nm=50)
        self.assertGreater(high_throttle_metrics["co2_g_km"], low_throttle_metrics["co2_g_km"])

if __name__ == "__main__":
    unittest.main()
  
