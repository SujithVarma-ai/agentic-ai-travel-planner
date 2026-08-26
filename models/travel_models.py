from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TravelRequest:
    origin: str
    destination: str
    duration_days: int
    travelers: int
    budget: float
    interests: List[str] = field(default_factory=list)
    travel_dates: Optional[str] = None


@dataclass
class TransportOption:
    mode: str
    provider: str
    price: float
    duration: str
    details: str = ""


@dataclass
class AccommodationOption:
    name: str
    price_per_night: float
    location: str
    rating: float
    details: str = ""


@dataclass
class ActivityOption:
    name: str
    location: str
    price: float
    duration: str
    category: str
    details: str = ""


@dataclass
class BudgetResult:
    transport_cost: float
    accommodation_cost: float
    activity_cost: float
    food_cost: float
    total_cost: float
    remaining_budget: float
    within_budget: bool


@dataclass
class TravelPlan:
    destination: str
    summary: str
    transport: List[TransportOption] = field(default_factory=list)
    accommodation: List[AccommodationOption] = field(default_factory=list)
    activities: List[ActivityOption] = field(default_factory=list)
    budget: Optional[BudgetResult] = None
    itinerary: List[str] = field(default_factory=list)