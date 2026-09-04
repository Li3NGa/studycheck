from __future__ import annotations
from dataclasses import dataclass
from .plans import Plan, FREE, PRO, FAMILY
from .limits import UsageLimit

PLANS: dict[str, Plan] = {p.name: p for p in (FREE, PRO, FAMILY)}

@dataclass
class Entitlement:
    user_id: str
    plan: str = FREE.name
    order_id: str | None = None
    active: bool = True

    def activate(self, plan: str, order_id: str | None = None) -> None:
        if plan not in PLANS: raise ValueError('unknown plan')
        self.plan = plan; self.order_id = order_id; self.active = True

def activate_paid(entitlement: Entitlement, plan: str, order_id: str, paid: bool) -> Entitlement:
    if not paid: raise PermissionError('order is not paid')
    entitlement.activate(plan, order_id); return entitlement

def plan_for(entitlement: Entitlement) -> Plan:
    return PLANS.get(entitlement.plan, FREE)

def plan_entitlements(plan: Plan = FREE, usage: UsageLimit | None = None) -> dict:
    usage = usage or UsageLimit(plan.daily_reviews)
    return {'plan':plan.name,'daily_reviews':plan.daily_reviews,'reviews_used':usage.reviews_today,'reviews_remaining':max(0,plan.daily_reviews-usage.reviews_today),'ai_explanations':plan.ai_explanations,'advanced_analytics':plan.advanced_analytics}

def require_feature(plan: Plan, feature: str) -> None:
    if not getattr(plan, feature, False): raise PermissionError(f'feature requires a paid plan: {feature}')
