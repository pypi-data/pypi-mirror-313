__all__ = ["encode_update_array"]


def encode_update_array(deltas: list[int]) -> list[int]:
    update_array = []

    for number in deltas:
        if not (0 <= number <= 255):
            raise ValueError("The number must be between 0 and 255, inclusive.")
        for shift in range(7, -1, -2):
            sign_bit = (number >> shift) & 1
            value_bit = (number >> (shift - 1)) & 1
            update_array.append(-value_bit if sign_bit == 1 else value_bit)

    return update_array
