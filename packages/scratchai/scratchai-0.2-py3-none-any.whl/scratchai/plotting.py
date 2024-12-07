import matplotlib.pyplot as plt
import numpy as np

def plot_loss_curve(losses, itertions):
    """
    Plot the losses over the number of iterations

    Args:
        losses (array): the training losses
        itertions (array): the number of iterations/epochs
    """
    plt.plot(itertions, losses, color = 'red')
    plt.xlabel('Number of Iterations/Epochs')
    plt.ylabel('Loss')
    plt.title('Loss Curve')
    plt.legend()
    plt.show()
    
def plot_generalization_curve(traning_lossses, testing_losses, iterations):
    """
    Plot the traning losses and the testing losses over the number of iterations

    Args:
        traning_lossses (array): the training losses
        testing_losses (array): the testing losses
        iterations (array): the number of iterations/epochs
    """
    plt.plot(iterations, traning_lossses, color = 'red')
    plt.plot(iterations, testing_losses, color = 'blue')
    plt.legend(['Training', 'Validation'])
    plt.title('Generalization Curve')
    plt.show()
    
def roc_metrics(y_true, y_prob, threshold):
    y_prob[y_prob >= threshold] = 1
    y_prob[y_prob < threshold] = 0
    
    tp = np.sum((y_true == 1) & (y_prob == 1))
    fp = np.sum((y_true == 0) & (y_prob == 1))
    
    tn = np.sum((y_true == 0) & (y_prob == 0))
    fn = np.sum((y_true == 1) & (y_prob == 0))
    
    tpr = tp / (fn + tp)
    fpr = fp / (tn + fp)
    
    return tpr, fpr
    
    
def plt_roc_cuve(y_true, y_prob):
    thresholds = [0,.05,.1,.15,.2,.25,.3,.35,.4,.45,.5,.55,.6,.65,.7,.75,.8,.85,.9,.95,1]
    
    # Calculate the tpr and fpr for threshold in thresholds
    tpr_points = []
    fpr_points = []
    for threshold in thresholds:
        tpr, fpr = roc_metrics(y_true, y_prob, threshold)
        tpr_points.append(tpr)
        fpr_points.append(fpr)
    
    # calculate the area ander the roc ruve
    auc = np.trapezoid(tpr_points, fpr_points)
    
    # plot the roc curve
    plt.plot(fpr_points, tpr_points, color = 'orange', lw = 2, label = f'AUC = {auc:.2f}')
    plt.plot([0, 1], [0, 1], color = 'blue', lw = 2, linestyle = '--', label = 'Random guess')
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
    plt.title('ROC curve')
    plt.legend(loc = 'lower right')
    plt.show()