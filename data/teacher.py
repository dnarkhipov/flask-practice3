from dataclasses import dataclass


@dataclass
class Teacher:
    id: int
    name: str
    about: str
    rating: float
    picture: str
    price: int
    goals: str
    free: dict

    @staticmethod
    def _keep_free_time(schedule):
        # Keep only free hours in schedule
        return [f'0{h}'[-5:] for h, v in schedule.items() if v]

    @property
    def free_days_in_week(self):
        return {day: self._keep_free_time(sched) for day, sched in self.free.items()}
