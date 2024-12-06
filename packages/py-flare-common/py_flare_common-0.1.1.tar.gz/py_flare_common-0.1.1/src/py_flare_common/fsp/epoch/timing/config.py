from attrs import frozen

__all__ = []


@frozen
class ChainConfig:
    voting_first_epoch_epoc: int
    voting_epoch_duration: int
    voting_ftso_reveal_deadline: int
    reward_first_epoch_epoc: int
    reward_epoch_duration: int


# flare
flare_chain_config = ChainConfig(
    voting_first_epoch_epoc=1658430000,
    voting_epoch_duration=90,
    voting_ftso_reveal_deadline=45,
    reward_first_epoch_epoc=1658430000,
    reward_epoch_duration=302400,
)

# songbird
songbird_chain_config = ChainConfig(
    voting_first_epoch_epoc=1658429955,
    voting_epoch_duration=90,
    voting_ftso_reveal_deadline=45,
    reward_first_epoch_epoc=1658429955,
    reward_epoch_duration=302400,
)

# coston
coston_chain_config = ChainConfig(
    voting_first_epoch_epoc=1658429955,
    voting_epoch_duration=90,
    voting_ftso_reveal_deadline=45,
    reward_first_epoch_epoc=1658429955,
    reward_epoch_duration=21600,
)

# coston2
coston2_chain_config = ChainConfig(
    voting_first_epoch_epoc=1658430000,
    voting_epoch_duration=90,
    voting_ftso_reveal_deadline=45,
    reward_first_epoch_epoc=1658430000,
    reward_epoch_duration=21600,
)
