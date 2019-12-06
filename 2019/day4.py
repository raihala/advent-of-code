LOWER_BOUND = 234208
UPPER_BOUND = 765869


def enumerate_passwords(num_digits=6, allowed_digits=range(10),
                        lower_bound=0, upper_bound=999999, repeats_allowed=True):
    """
    Recursively determines how many numbers meet the given criteria:
    * have the given number of digits
    * only use the allowed digits (NB: allowed_digits must be range(n, 10) for some value 0 <= n <= 9)
    * between the given bounds, inclusive on both ends
    * have all digits, left to right, either nondecreasing or
        strictly increasing based on the value of repeats_allowed
    """
    # base cases
    if num_digits == 0:
        return 1
    elif len(allowed_digits) == 0:
        return 0

    # eg lower bound = 123456 => digit = 1, remainder = 23456
    # but if allowed digits are eg 3-9, then:
    #   actual lower bound = 300000 => digit = 3, remainder = 0
    # on the other hand if allowed digits are 3-9 but lower bound is 400000,
    #   then allowed digits are actually 4-9
    lower_bound_digit, lower_bound_remainder = divmod(lower_bound, 10**(num_digits-1))
    if lower_bound_digit < allowed_digits[0]:
        lower_bound_digit = allowed_digits[0]
        lower_bound_remainder = 0
    elif lower_bound_digit > allowed_digits[0]:
        allowed_digits = range(lower_bound_digit, 10)

    # if for whatever reason the upper bound is on an excessively
    # large order of magnitude, go ahead and clip it
    upper_bound = min(upper_bound, 10**num_digits - 1)
    upper_bound_digit, upper_bound_remainder = divmod(upper_bound, 10**(num_digits-1))
    # eg if upper bound is 2xxxxxx but allowed digits are 3-9, there are no possible solutions
    if upper_bound_digit < allowed_digits[0]:
        return 0

    res = 0

    # recursive case where we pick the lower bound digit.
    # if bounds are 225000 and 300000, and we pick the digit 2,
    # then the recursive bounds are 25000 and 99999. but if the
    # bounds are 225000 and 275000 and we pick the digit 2,
    # the recursive bounds will be 25000 and 75000.
    res += enumerate_passwords(
        num_digits=num_digits-1,
        allowed_digits=allowed_digits if repeats_allowed else allowed_digits[1:],
        lower_bound=lower_bound_remainder,
        upper_bound=upper_bound_remainder if lower_bound_digit == upper_bound_digit else 10**(num_digits-1) - 1,
        repeats_allowed=repeats_allowed
    )

    # if the bounds start with the same digit, we're already done. otherwise
    # there are more options we need to consider picking.
    if lower_bound_digit != upper_bound_digit:
        # recursive case where we pick the upper bound digit. this time
        # we will need to update the allowed digits.
        res += enumerate_passwords(
            num_digits=num_digits-1,
            allowed_digits=range(upper_bound_digit, 10) if repeats_allowed else range(upper_bound_digit + 1, 10),
            lower_bound=0,
            upper_bound=upper_bound_remainder,
            repeats_allowed=repeats_allowed
        )

        # recursive cases where we pick a digit strictly between the two
        # bounds, such that neither of the bounds are relevant
        for digit in range(lower_bound_digit+1, upper_bound_digit):
            res += enumerate_passwords(
                num_digits=num_digits - 1,
                allowed_digits=range(digit, 10) if repeats_allowed else range(digit+1, 10),
                lower_bound=0,
                upper_bound=10**(num_digits-1) - 1,
                repeats_allowed=repeats_allowed
            )

    return res


with_or_without_repeats = enumerate_passwords(lower_bound=LOWER_BOUND, upper_bound=UPPER_BOUND)
without_repeats = enumerate_passwords(lower_bound=LOWER_BOUND, upper_bound=UPPER_BOUND, repeats_allowed=False)
with_repeats = with_or_without_repeats - without_repeats

print(with_repeats)
