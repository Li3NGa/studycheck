from __future__ import annotations
from .plans import Plan, FREE
from .limits import UsageLimit

def plan_entitlements(plan:Plan=FREE,usage:UsageLimit|None=None)->dict:
    usage=usage or UsageLimit(plan.daily_reviews)
    return {'plan':plan.name,'daily_reviews':plan.daily_reviews,'reviews_used':usage.reviews_today,'reviews_remaining':max(0,plan.daily_reviews-usage.reviews_today),'ai_explanations':plan.ai_explanations,'advanced_analytics':plan.advanced_analytics}

def require_feature(plan:Plan,feature:str)->None:
    if not getattr(plan,feature,False): raise PermissionError(f'feature requires a paid plan: {feature}')
