"""A set of aggregators

@author Rory Byrne <rory@rory.bio>
"""
from abc import abstractmethod, ABC
from dataclasses import dataclass
from itertools import groupby
from typing import Generic, TypeVar, List

from msr.model import Result, MT, MeasuredUrl, MeasuredDomain, Measurement

OT = TypeVar('OT', MeasuredUrl, MeasuredDomain)


class Aggregator(ABC, Generic[MT, OT]):

    @abstractmethod
    def __call__(self, result: Result[MT], *args, **kwargs) -> Result[OT]:
        raise NotImplementedError()


class Identity(Generic[MT], Aggregator[MT, MT]):

    def __call__(self, result: Result[MT], *args, **kwargs) -> Result[MT]:
        return result


@dataclass
class Group:
    key: str
    measurements: List[Measurement]


class AverageByDomain(Aggregator[MeasuredUrl, MeasuredDomain]):

    def __call__(self, result: Result[MeasuredUrl], *args, **kwargs) -> Result[MeasuredDomain]:
        data = sorted(result.data, key=lambda item: item.url.domain)
        group_generator = groupby(data, key=lambda item: item.url.domain)
        groups: List[Group] = [Group(k, [x.measurement for x in v]) for k, v in group_generator]

        aggregated_data = [MeasuredDomain(g.key, self._average(g.measurements)) for g in groups]

        return Result(aggregated_data)

    @staticmethod
    def _average(measurements: List[Measurement]) -> Measurement:
        raw_values = [m.value for m in measurements]

        return Measurement(sum(raw_values)/len(raw_values), measurements[0].dimension)
