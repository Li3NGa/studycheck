from __future__ import annotations
from .api import StudyCheckService
from .entitlements import plan_entitlements

def current_plan(service:StudyCheckService)->dict:
    return plan_entitlements(service.plan,service.usage)
