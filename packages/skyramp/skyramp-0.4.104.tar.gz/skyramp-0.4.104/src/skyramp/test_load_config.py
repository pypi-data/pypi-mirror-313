"""
Contains helpers for configuring load test parameters
"""
from typing import Optional

class _LoadTestConfig:
    def __init__(self,
                 target_rps: Optional[int] = None,
                 at_once: Optional[int] = None,
                 count: Optional[int] = None,
                 duration: Optional[str] = None,
                 rampup_interval: Optional[str] = None,
                 rampup_duration: Optional[str] = None,
                 stop_on_failure: Optional[bool] = False,
                 ) -> None:

        self.target_rps = target_rps
        self.at_once = at_once
        self.count = count
        self.duration = duration
        self.rampup_interval = rampup_interval
        self.rampup_duration = rampup_duration
        self.stop_on_failure = stop_on_failure

    @staticmethod
    def from_kwargs(**kwargs):
        """
        convert kwargs into loadTestConfig object
        """
        target_rps = kwargs.get('target_rps', None)
        at_once = kwargs.get('at_once', None)
        count = kwargs.get('count', None)
        duration = kwargs.get('duration', None)
        rampup_interval = kwargs.get('rampup_interval', None)
        rampup_duration = kwargs.get('rampup_duration', None)
        stop_on_failure = kwargs.get('stop_on_failure', False)
        return _LoadTestConfig(target_rps,
                               at_once,
                               count,
                               duration,
                               rampup_interval,
                               rampup_duration,
                               stop_on_failure)

    def apply_to_dict(self, pattern: dict):
        """
        apply load test values to dictionary
        """
        if self.target_rps is not None:
            pattern["targetRPS"] = self.target_rps
        if self.at_once is not None:
            pattern["atOnce"] = self.at_once
        if self.duration is not None:
            pattern["duration"] = self.duration
        if self.count is not None:
            pattern["count"] = self.count
        if self.rampup_interval is not None or self.rampup_duration is not None:
            pattern["rampUp"] = {}
            if self.rampup_interval is not None:
                pattern["rampUp"]["interval"] = self.rampup_interval
            if self.rampup_duration is not None:
                pattern["rampUp"]["duration"] = self.rampup_duration
        if self.stop_on_failure is True:
            pattern["stopOnFailure"] = True
