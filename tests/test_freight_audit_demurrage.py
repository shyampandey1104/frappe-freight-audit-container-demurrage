import unittest
from freight_audit_demurrage.engine import ContainerMovementTrack, FreightAuditDemurrageEngine

class TestFreightAuditDemurrageEngine(unittest.TestCase):
    def setUp(self):
        self.engine = FreightAuditDemurrageEngine()

    def test_overcharge_dispute(self):
        res = self.engine.audit_ocean_freight_invoice(
            billed_base_freight=2450.0, contracted_base_freight=2100.0,
            billed_baf=400.0, contracted_baf=300.0
        )
        self.assertEqual(res["audit_result"], "OVERCHARGE_DISPUTE_RAISED")
        self.assertEqual(res["total_overcharge_usd"], 450.0)

    def test_container_detention(self):
        cont = ContainerMovementTrack(
            container_number="MSCU9812401", shipping_line="MSC", port_of_discharge="JNPT",
            discharge_date="2026-03-01", gate_out_empty_return_date="2026-03-20", allowed_free_days=14, daily_detention_rate_usd=100.0
        )
        res = self.engine.compute_container_detention(cont)
        self.assertEqual(res["total_dwell_days"], 19)
        self.assertEqual(res["chargeable_days"], 5)
        self.assertEqual(res["detention_amount_usd"], 500.0)

if __name__ == "__main__":
    unittest.main()
