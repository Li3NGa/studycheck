from __future__ import annotations
from .billing import Subscription
from .usage import Usage,consume_generation
from .billing import LIMITS

def charge_generation(subscription:Subscription,usage:Usage)->Usage:
    limit=LIMITS[subscription.plan]['generations']
    if not subscription.allows('generations',usage.generations):
        raise PermissionError('subscription does not allow another generation')
    return consume_generation(usage,limit)
