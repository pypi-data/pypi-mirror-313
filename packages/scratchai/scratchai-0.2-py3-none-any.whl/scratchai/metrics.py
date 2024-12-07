import numpy as np

def cross_entropy(y_pred, y):
    """
    calculates the cross entropy loss using batchs from y and y_pred for performance

    Args:
        y_pred (array): the model predicted values
        y (array): the actual values

    Returns:
        int: the calculated model loss from y and y_pred
    """
    total_cost = 0
    batch_size = 100
    
    for i in range(0, len(y), batch_size):
        y_batch = y[i: i + batch_size]
        y_pred_batch = y_pred[i: i + batch_size]
        
        total_cost += np.sum(-y_batch * np.log(y_pred_batch) - (1 - y_batch) * np.log(1 - y_pred_batch))
        
    return total_cost / len(y)

def recall(y_true, y_pred):
    """
    Calculate the reall(True positive rate)

    Args:
        y_true (array): the actucal values
        y_pred (array): the predicted values

    Returns:
        int: the number of true positives over the number of actual positives
    """
    true_positives = 0
    actual_positives = 0
    for i in range(0, len(y_true), 100):
        y_true_batch = y_true[i:i + 100]
        y_pred_batch = y_pred[i:i + 100]
        
        true_positives += np.sum((y_true_batch == 1) & (y_pred_batch == 1))
        actual_positives += np.sum(y_true_batch == 1)
        
    return true_positives / actual_positives

def precision(y_true, y_pred):
    """
    Calculate the precision

    Args:
        y_true (array): the actual values
        y_pred (array): the predicted values

    Returns:
        int: the number of true positives over the number of classsified positives
    """
    true_positives = 0
    calassified_possitives = 0
    for i in range(0, len(y_true), 100):
        y_true_batch = y_true[i:i + 100]
        y_pred_batch = y_pred[i:i + 100]
        
        true_positives += np.sum((y_true_batch == 1) & (y_pred_batch == 1))
        calassified_possitives += np.sum(y_pred_batch == 1)
        
    return true_positives / calassified_possitives

def accuracy(y_true, y_pred):
    """
    calculate the accuracy

    Args:
        y_true (array): the actual values
        y_pred (array): the predicted values

    Returns:
        int: None
    """
    total_acurracy = 0
    for i in range(0, len(y_true), 100):
        y_true_batch = y_true[i:i + 100]
        y_pred_batch = y_pred[i:i + 100]
        total_acurracy += np.sum(y_true_batch == y_pred_batch)
        
    return total_acurracy / len(y_true)

def confusion_matrix(y_true, y_pred):
    true_positives = np.sum((y_true == 1) & (y_pred == 1))
    false_positives = np.sum((y_true == 0) & (y_pred == 1))
    true_negatives = np.sum((y_true == 0) & (y_pred == 0))
    false_negatives = np.sum((y_true == 1) & (y_pred == 0))
    return np.array([[true_positives, false_positives], [true_negatives, false_negatives]])

def mean_absolute_error(y_true, y_pred):
    return np.sum(np.abs(y_pred - y_true)) / len(y_true)

def mean_squared_error(y_true, y_pred):
    return np.sum((y_pred - y_true) ** 2) / len(y_true)