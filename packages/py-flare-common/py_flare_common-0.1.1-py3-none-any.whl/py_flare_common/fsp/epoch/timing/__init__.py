from .coston.epoch import reward_epoch as coston_reward_epoch
from .coston.epoch import reward_epoch_factory as coston2_reward_epoch_factory
from .coston.epoch import reward_epoch_factory as coston_reward_epoch_factory
from .coston.epoch import reward_epoch_factory as flare_reward_epoch_factory
from .coston.epoch import reward_epoch_factory as songbird_reward_epoch_factory
from .coston.epoch import voting_epoch as coston_voting_epoch
from .coston.epoch import voting_epoch_factory as coston2_voting_epoch_factory
from .coston.epoch import voting_epoch_factory as coston_voting_epoch_factory
from .coston.epoch import voting_epoch_factory as flare_voting_epoch_factory
from .coston.epoch import voting_epoch_factory as songbird_voting_epoch_factory
from .coston2.epoch import reward_epoch as coston2_reward_epoch
from .coston2.epoch import voting_epoch as coston2_voting_epoch
from .flare.epoch import reward_epoch as flare_reward_epoch
from .flare.epoch import voting_epoch as flare_voting_epoch
from .songbird.epoch import reward_epoch as songbird_reward_epoch
from .songbird.epoch import voting_epoch as songbird_voting_epoch

__all__ = [
    "coston_voting_epoch",
    "coston_reward_epoch",
    "coston_voting_epoch_factory",
    "coston_reward_epoch_factory",
    "coston2_voting_epoch",
    "coston2_reward_epoch",
    "coston2_voting_epoch_factory",
    "coston2_reward_epoch_factory",
    "songbird_voting_epoch",
    "songbird_reward_epoch",
    "songbird_voting_epoch_factory",
    "songbird_reward_epoch_factory",
    "flare_voting_epoch",
    "flare_reward_epoch",
    "flare_voting_epoch_factory",
    "flare_reward_epoch_factory",
]
