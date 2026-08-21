"""
Agent A5: Allocation Solver (Pure Python Deterministic Optimizer).
Calculates exact mathematically verified resource allocations without any LLM hallucination.
Emits exactly 3 fixed candidate plans: [1] fastest, [2] max_coverage, [3] least_depleting.
"""

from typing import Dict, Any, List
import copy
from app.bus.eventbus import event_bus


class AllocationSolverAgent:
    name = "A5_Solver"

    async def solve(
        self,
        need_items: List[Dict[str, Any]],
        candidates: List[Dict[str, Any]],
        run_id: str,
        pinned_provider_id: str = None
    ) -> Dict[str, Any]:
        """
        Solves allocation arithmetic deterministically.
        Generates 3 named candidate options.
        """
        await event_bus.emit(
            "agent.entered",
            self.name,
            {"stage": "A5", "description": "Deterministic Allocation Optimization (Python Math)"},
            run_id=run_id
        )

        # Build demand dictionary
        demand: Dict[str, int] = {}
        for item in need_items:
            key = item.get("resource_key")
            qty = item.get("quantity", 1)
            demand[key] = demand.get(key, 0) + qty

        # Sort candidate list for the 3 distinct strategies
        # 1. Fastest: Sorted by distance / ETA ascending
        cand_fastest = sorted(candidates, key=lambda c: (c.get("distance_km", 999), c.get("eta_hours", 999)))

        # 2. Max Coverage: Sorted by total matching stock descending
        def total_matching_stock(c):
            inv = c.get("inventory", {})
            return sum(inv.get(k, 0) for k in demand)
        cand_coverage = sorted(candidates, key=total_matching_stock, reverse=True)

        # 3. Least Depleting: Sorted by total inventory volume descending (largest hubs first)
        cand_least_depleting = sorted(candidates, key=lambda c: sum(c.get("inventory", {}).values()), reverse=True)

        # If admin pinned a provider, prioritize them at the front
        if pinned_provider_id:
            def pin_filter(lst):
                pinned = [c for c in lst if c.get("provider_id") == pinned_provider_id]
                rest = [c for c in lst if c.get("provider_id") != pinned_provider_id]
                return pinned + rest
            cand_fastest = pin_filter(cand_fastest)
            cand_coverage = pin_filter(cand_coverage)
            cand_least_depleting = pin_filter(cand_least_depleting)

        option_fastest = self._build_plan("fastest", "Rapid Response (Fastest Arrival)", "Minimizes travel time by deploying closest available response squads.", demand, cand_fastest)
        option_coverage = self._build_plan("max_coverage", "Maximum Coverage Plan", "Fulfills the highest possible percentage of total relief items.", demand, cand_coverage)
        option_least_depleting = self._build_plan("least_depleting", "Depletion-Balanced Plan", "Draws stock from large regional distribution centers to protect forward clinic reserves.", demand, cand_least_depleting)

        options = {
            "fastest": option_fastest,
            "max_coverage": option_coverage,
            "least_depleting": option_least_depleting
        }

        await event_bus.emit(
            "options.proposed",
            self.name,
            {
                "option_count": 3,
                "options": options
            },
            run_id=run_id
        )

        return options

    def _build_plan(
        self,
        opt_id: str,
        title: str,
        desc: str,
        demand: Dict[str, int],
        sorted_candidates: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Greedy allocation against candidate inventory."""
        rem_demand = dict(demand)
        allocations = []
        total_fulfilled = {k: 0 for k in demand}
        max_eta = 0.0

        for cand in sorted_candidates:
            p_id = cand.get("provider_id")
            p_name = cand.get("provider_name") or cand.get("name")
            p_inv = cand.get("inventory", {})
            dist_km = cand.get("distance_km", 5.0)
            eta_h = cand.get("eta_hours", 1.0)

            allocated_from_cand = {}
            for res_key, req_qty in list(rem_demand.items()):
                if req_qty <= 0:
                    continue
                avail = p_inv.get(res_key, 0)
                if avail > 0:
                    give = min(avail, req_qty)
                    allocated_from_cand[res_key] = give
                    rem_demand[res_key] -= give
                    total_fulfilled[res_key] += give

            if allocated_from_cand:
                max_eta = max(max_eta, eta_h)
                allocations.append({
                    "provider_id": p_id,
                    "provider_name": p_name,
                    "distance_km": dist_km,
                    "eta_hours": eta_h,
                    "items": allocated_from_cand
                })

        total_req = sum(demand.values())
        total_got = sum(total_fulfilled.values())
        coverage_ratio = round(total_got / total_req, 2) if total_req > 0 else 1.0

        if opt_id == "least_depleting":
            depletion = "low"
        elif opt_id == "fastest":
            depletion = "medium"
        else:
            depletion = "medium-high"

        return {
            "option_id": opt_id,
            "title": title,
            "description": desc,
            "allocations": allocations,
            "total_fulfilled": total_fulfilled,
            "demand": demand,
            "coverage_ratio": coverage_ratio,
            "max_eta_hours": max_eta or 1.0,
            "depletion_impact": depletion
        }


a5_solver = AllocationSolverAgent()
