def classification_accuracy(y_true, y_pred):
    assert len(y_true) == len(y_pred)
    return sum([1 if true == pred else 0 for pred, true in zip(y_pred, y_true)]) / len(
        y_true
    )
