"""Ocean Freight Bill Audit & Container Detention/Demurrage Engine."""
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Dict, Any, Optional

@dataclass
class ContainerMovementTrack:
    container_number: str
    shipping_line: str
    port_of_discharge: str
    discharge_date: str
    gate_out_empty_return_date: str
    allowed_free_days: int = 14
    daily_detention_rate_usd: float = 120.0

class FreightAuditDemurrageEngine:
    def __init__(self):
        self.containers: Dict[str, ContainerMovementTrack] = {}

    def audit_ocean_freight_invoice(self, billed_base_freight: float, contracted_base_freight: float, billed_baf: float, contracted_baf: float) -> Dict[str, Any]:
        freight_variance = round(billed_base_freight - contracted_base_freight, 2)
        baf_variance = round(billed_baf - contracted_baf, 2)
        total_overcharge = round(max(0.0, freight_variance) + max(0.0, baf_variance), 2)
        
        return {
            "freight_variance_usd": freight_variance,
            "baf_variance_usd": baf_variance,
            "total_overcharge_usd": total_overcharge,
            "audit_result": "OVERCHARGE_DISPUTE_RAISED" if total_overcharge > 0 else "AUDIT_CLEARED"
        }

    def compute_container_detention(self, cont: ContainerMovementTrack) -> Dict[str, Any]:
        d1 = datetime.strptime(cont.discharge_date, "%Y-%m-%d").date()
        d2 = datetime.strptime(cont.gate_out_empty_return_date, "%Y-%m-%d").date()
        total_days = (d2 - d1).days

        chargeable_days = max(0, total_days - cont.allowed_free_days)
        detention_cost = round(chargeable_days * cont.daily_detention_rate_usd, 2)

        return {
            "container_number": cont.container_number,
            "total_dwell_days": total_days,
            "free_days": cont.allowed_free_days,
            "chargeable_days": chargeable_days,
            "detention_amount_usd": detention_cost
        }
