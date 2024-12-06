from attrs import frozen

__all__ = ["calculate_median", "FtsoVote"]


@frozen
class FtsoVote:
    value: int
    weight: int


@frozen
class FtsoMedian:
    value: int
    first_quartile: int
    third_quartile: int
    sorted_votes: list[FtsoVote]


def calculate_median(votes: list[FtsoVote]) -> FtsoMedian | None:
    if len(votes) == 0:
        return None

    median = None
    quartile_1 = None
    quartile_3 = None

    # Sort the list by values if it is not already sorted.
    if not (all(votes[i].value <= votes[i + 1].value for i in range(len(votes) - 1))):
        votes.sort(key=lambda x: x.value)

    total_weight = sum([vote.weight for vote in votes])
    median_weight = total_weight // 2 + (total_weight % 2)
    quartile_weight = total_weight // 4
    current_weight_sum = 0

    for i, vote in enumerate(votes):
        current_weight_sum += vote.weight

        if quartile_1 is None and current_weight_sum > quartile_weight:
            quartile_1 = vote.value

        if current_weight_sum >= median_weight:
            if current_weight_sum == median_weight and total_weight % 2 == 0:
                next_vote = votes[i + 1]
                median = (vote.value + next_vote.value) // 2
                break
            else:
                median = vote.value
                break

    current_weight_sum = 0

    for i in range(len(votes) - 1, -1, -1):
        vote = votes[i]
        current_weight_sum += vote.weight

        if current_weight_sum > quartile_weight:
            quartile_3 = vote.value
            break

    assert median is not None
    assert quartile_1 is not None
    assert quartile_3 is not None

    return FtsoMedian(
        value=median,
        first_quartile=quartile_1,
        third_quartile=quartile_3,
        sorted_votes=votes,
    )
