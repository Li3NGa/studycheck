from __future__ import annotations
from dataclasses import dataclass
from datetime import date

@dataclass
class UsageLimit:
    daily_reviews:int=20
    reviews_today:int=0
    day:date=date.today()

    def consume_review(self)->None:
        today=date.today()
        if self.day!=today:self.day=today; self.reviews_today=0
        if self.reviews_today>=self.daily_reviews:raise PermissionError('daily review limit reached')
        self.reviews_today+=1
