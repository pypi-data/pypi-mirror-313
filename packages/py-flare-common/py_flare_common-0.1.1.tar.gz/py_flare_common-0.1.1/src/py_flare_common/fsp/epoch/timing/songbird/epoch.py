from ...epoch import RewardEpoch, VotingEpoch
from ...factory import RewardEpochFactory, VotingEpochFactory
from ..config import songbird_chain_config

__all__ = [
    "voting_epoch",
    "reward_epoch",
    "voting_epoch_factory",
    "reward_epoch_factory",
]

voting_epoch_factory = VotingEpochFactory(
    first_epoch_epoc=songbird_chain_config.voting_first_epoch_epoc,
    epoch_duration=songbird_chain_config.voting_epoch_duration,
    ftso_reveal_deadline=songbird_chain_config.voting_ftso_reveal_deadline,
    reward_first_epoch_epoc=songbird_chain_config.reward_first_epoch_epoc,
    reward_epoch_duration=songbird_chain_config.reward_epoch_duration,
)

reward_epoch_factory = RewardEpochFactory(
    first_epoch_epoc=songbird_chain_config.reward_first_epoch_epoc,
    epoch_duration=songbird_chain_config.reward_epoch_duration,
    voting_first_epoch_epoc=songbird_chain_config.voting_first_epoch_epoc,
    voting_epoch_duration=songbird_chain_config.voting_epoch_duration,
    voting_ftso_reveal_deadline=songbird_chain_config.voting_ftso_reveal_deadline,
)


def voting_epoch(id: int) -> VotingEpoch:
    return voting_epoch_factory.make_epoch(id)


def reward_epoch(id: int) -> RewardEpoch:
    return reward_epoch_factory.make_epoch(id)
