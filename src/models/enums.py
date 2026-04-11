from enum import Enum


class CompoundingFrequency(str, Enum):
    ANNUALLY = "annually"
    SEMI_ANNUALLY = "semi_annually"
    QUARTERLY = "quarterly"
    MONTHLY = "monthly"
    DAILY = "daily"
    CONTINUOUS = "continuous"

    @property
    def periods_per_year(self) -> int:
        mapping = {
            "annually": 1,
            "semi_annually": 2,
            "quarterly": 4,
            "monthly": 12,
            "daily": 365,
            "continuous": 0,
        }
        return mapping[self.value]


class AnnuityType(str, Enum):
    ORDINARY = "ordinary"  # payments at end of period
    DUE = "due"  # payments at beginning of period


class LoanType(str, Enum):
    HOME = "home"
    CAR = "car"
    PERSONAL = "personal"
    EDUCATION = "education"
    GOLD = "gold"
    OTHER = "other"


class RiskProfile(str, Enum):
    CONSERVATIVE = "conservative"
    MODERATELY_CONSERVATIVE = "moderately_conservative"
    MODERATE = "moderate"
    MODERATELY_AGGRESSIVE = "moderately_aggressive"
    AGGRESSIVE = "aggressive"


class BondType(str, Enum):
    GOVERNMENT = "government"
    CORPORATE = "corporate"
    ZERO_COUPON = "zero_coupon"
    FLOATING_RATE = "floating_rate"


class ReturnMethod(str, Enum):
    ABSOLUTE = "absolute"
    ANNUALIZED = "annualized"
    CAGR = "cagr"
    XIRR = "xirr"
