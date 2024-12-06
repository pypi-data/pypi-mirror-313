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
