from functools import total_ordering
from typing import TYPE_CHECKING, Self

from attrs import frozen

if TYPE_CHECKING:
    from .factory import (
        Factory,
        RewardEpochFactory,
        VotingEpochFactory,
    )


__all__ = [
    "Epoch",
    "VotingEpoch",
    "RewardEpoch",
]


@total_ordering
@frozen
class Epoch:
    id: int
    factory: "Factory"

    def __lt__(self, other: Self) -> bool:
        if not isinstance(other, self.__class__) or self.factory != other.factory:
            return NotImplemented
        return self.id < other.id

    def __contains__(self, time: int):
        return self.start_s <= time < self.end_s

    @property
    def next(self) -> Self:
        return type(self)(self.id + 1, self.factory)

    @property
    def previous(self) -> Self:
        return type(self)(self.id - 1, self.factory)

    @property
    def start_s(self) -> int:
        return self.factory.first_epoch_epoc + self.id * self.factory.epoch_duration

    @property
    def end_s(self) -> int:
        return self.next.start_s


@frozen
class VotingEpoch(Epoch):
    factory: "VotingEpochFactory"

    def to_reward_epoch(self) -> "RewardEpoch":
        return self.factory.make_reward_epoch(self.start_s)

    def reveal_deadline(self) -> int:
        return self.start_s + self.factory.ftso_reveal_deadline


@frozen
class RewardEpoch(Epoch):
    factory: "RewardEpochFactory"

    def to_first_voting_epoch(self) -> VotingEpoch:
        return self.factory.make_voting_epoch(self.start_s)
