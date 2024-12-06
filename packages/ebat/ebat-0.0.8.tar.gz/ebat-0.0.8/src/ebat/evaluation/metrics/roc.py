def false_acceptance_rate(y_true, y_pred):
    assert len(y_true) == len(y_pred)
    return sum(
        [1 if not true and pred else 0 for true, pred in zip(y_true, y_pred)]
    ) / len(y_true)


def false_rejection_rate(y_true, y_pred):
    assert len(y_true) == len(y_pred)
    return sum(
        [1 if true and not pred else 0 for true, pred in zip(y_true, y_pred)]
    ) / len(y_true)


if __name__ == "__main__":
    print(
        false_acceptance_rate(
            [False, False, False, False], [False, False, False, False]
        ),
    )
    print(
        false_acceptance_rate(
            [False, False, False, False], [False, False, False, True]
        ),
    )
    print(
        false_acceptance_rate([False, False, False, False], [False, False, True, True]),
    )
    print(
        false_acceptance_rate([False, False, False, False], [False, True, True, True]),
    )
    print(
        false_acceptance_rate([False, False, False, False], [True, True, True, True]),
    )
