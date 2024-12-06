from time import time
import json
from typing import List, Optional

from pydantic import BaseModel, Extra, Field, NonNegativeFloat, root_validator, validator

from chaiverse.schemas.date_range_schema import BoundedDateRange, DateRange


class CompetitionChatRouting(BaseModel):
    percentage: NonNegativeFloat = Field(default=100)

    @validator('percentage')
    def validate_percentage(cls, value):
        assert value <= 100, 'percentage more than 100'
        return value


class Competition(BaseModel, extra=Extra.allow):
    display_name: str

    submission_date_range: Optional[DateRange]
    leaderboard_format: Optional[str]
    leaderboard_should_use_feedback: Optional[bool]
    evaluation_date_range: Optional[BoundedDateRange]
    chat_routing: Optional[CompetitionChatRouting]
    enrolled_submission_ids: Optional[List[str]]

    @property
    def submission_start_time(self) -> float:
        date_range = self.submission_date_range or DateRange()
        return date_range.start_epoch_time

    @property
    def submission_end_time(self) -> float:
        date_range = self.submission_date_range or DateRange()
        return date_range.end_epoch_time

    @property
    def evaluation_start_time(self) -> Optional[float]:
        return self.evaluation_date_range.start_epoch_time if self.evaluation_date_range else None
        
    @property
    def evaluation_end_time(self) -> Optional[float]:
        return self.evaluation_date_range.end_epoch_time if self.evaluation_date_range else None

    @property
    def is_submitting(self):
        is_submitting = self.submission_start_time <= time() < self.submission_end_time
        return is_submitting

    @property
    def is_evaluating(self):
        is_evaluating = self.evaluation_start_time <= time() < self.evaluation_end_time
        return is_evaluating

    @validator('enrolled_submission_ids')
    def validate_enrolled_submission_ids(cls, enrolled_submission_ids):
        if enrolled_submission_ids:
            enrolled_submission_ids = list({}.fromkeys(enrolled_submission_ids))
        return enrolled_submission_ids

    @root_validator
    def validate_date_ranges(cls, values: dict):
        submission_date_range = values.get('submission_date_range') or DateRange()
        evaluation_date_range = values.get('evaluation_date_range')
        if evaluation_date_range:
            assert evaluation_date_range.start_epoch_time >= submission_date_range.end_epoch_time, 'evaluation starts before submission completes'
        return values

    def get_enrolled_submission_ids(self):
        return self.enrolled_submission_ids or []

    # pydantic 2.x implements model_dump. Existing dict() in pydantic 1.x doesn't serialize recursively
    def model_dump(self):
        return json.loads(self.json())
