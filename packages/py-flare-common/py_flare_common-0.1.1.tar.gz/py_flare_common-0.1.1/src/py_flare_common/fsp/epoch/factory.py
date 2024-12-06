import time

from attrs import frozen

from .epoch import Epoch, RewardEpoch, VotingEpoch

__all__ = [
    "Factory",
    "VotingEpochFactory",
    "RewardEpochFactory",
]


@frozen
class Factory:
    first_epoch_epoc: int
    epoch_duration: int

    def make_epoch(self, id) -> Epoch:
        return Epoch(id, self)

    def duration(self) -> int:
        return self.epoch_duration

    def _from_timestamp(self, ts: int) -> int:
        return (ts - self.first_epoch_epoc) // self.epoch_duration

    def from_timestamp(self, ts: int) -> Epoch:
        return self.make_epoch(self._from_timestamp(ts))

    def now(self) -> Epoch:
        return self.from_timestamp(int(time.time()))

    def now_id(self) -> int:
        return self.now().id


@frozen
class VotingEpochFactory(Factory):
    ftso_reveal_deadline: int
    # Reward Epoch data
    reward_first_epoch_epoc: int
    reward_epoch_duration: int

    def make_epoch(self, id) -> VotingEpoch:
        return VotingEpoch(id, self)

    def make_reward_epoch(self, t: int):
        factory = RewardEpochFactory(
            self.reward_first_epoch_epoc,
            self.reward_epoch_duration,
            self.first_epoch_epoc,
            self.epoch_duration,
            self.ftso_reveal_deadline,
        )
        id = factory._from_timestamp(t)
        return factory.make_epoch(id)


@frozen
class RewardEpochFactory(Factory):
    # Voting Epoch data
    voting_first_epoch_epoc: int
    voting_epoch_duration: int
    voting_ftso_reveal_deadline: int

    def make_epoch(self, id) -> RewardEpoch:
        return RewardEpoch(id, self)

    def make_voting_epoch(self, t: int):
        factory = VotingEpochFactory(
            self.voting_first_epoch_epoc,
            self.voting_epoch_duration,
            self.voting_ftso_reveal_deadline,
            self.first_epoch_epoc,
            self.epoch_duration,
        )
        id = factory._from_timestamp(t)
        return factory.make_epoch(id)

    def from_voting_epoch(self, voting_epoch: VotingEpoch) -> RewardEpoch:
        if not (
            voting_epoch.factory.first_epoch_epoc == self.voting_first_epoch_epoc
            and voting_epoch.factory.epoch_duration == self.voting_epoch_duration
            and voting_epoch.factory.ftso_reveal_deadline
            == self.voting_ftso_reveal_deadline
            and voting_epoch.factory.reward_first_epoch_epoc == self.first_epoch_epoc
            and voting_epoch.factory.reward_epoch_duration == self.epoch_duration
        ):
            raise ValueError("VotingEpoch was made by wrong factory")
        return self.make_epoch(self._from_timestamp(voting_epoch.start_s))
