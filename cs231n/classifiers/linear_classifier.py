import numpy as np
from cs231n.classifiers.linear_svm import *
from cs231n.classifiers.softmax import *

class LinearClassifier:

    def __init__(self):
        self.W = None

    def train(self, X, y, learning_rate=1e-3, reg=1e-5, num_iters=300,
              batch_size=200, verbose=True):
        """
        Train this linear classifier using stochastic gradient descent.

        Inputs:
        - X: N x D array of training data. Each training point is a D-dimensional
             row.
        - y: 1-dimensional array of length N with labels 0...K-1, for K classes.
        - learning_rate: (float) learning rate for optimization.
        - reg: (float) regularization strength.
        - num_iters: (integer) number of steps to take when optimizing
        - batch_size: (integer) number of training examples to use at each step.
        - verbose: (boolean) If true, print progress during optimization.

        Outputs:
        A list containing the value of the loss function at each training iteration.
        """
        
        
        dim, num_train = X.shape
        
        num_classes = int(np.max(y) + 1)  # assume y takes values 0...K-1 
                                     # where K is number of classes

        # Lazy implementation allows for the initilized weights be created anew each time
        if self.W is None:
            # lazily initialize W
            self.W = np.random.randn(num_classes, dim) * 0.001

        # Run stochastic gradient descent to optimize W
        loss_history = []
        batch_start = 0
        
        for it in range(num_iters):

            X_batch = None
            y_batch = None

            #########################################################################
            # TODO:                                                                 #
            # Sample batch_size elements from the training data and their           #
            # corresponding labels to use in this round of gradient descent.        #
            # Store the data in X_batch and their corresponding labels in           #
            # y_batch; after sampling X_batch should have shape (dim, batch_size)   #
            # and y_batch should have shape (batch_size,)                           #
            #                                                                       #
            # Hint: Use np.random.choice to generate indices. Sampling with         #
            # replacement is faster than sampling without replacement.              #
            #########################################################################
            # print('\nTraining Linear Classifier, stochastic gradient descent...\n\n')
            
            # create a {batch_size} array of elements between 0 and {num_train}
            indices = np.random.choice(num_train, batch_size)
            
            # Create batch from dataset 
            X_batch = X[:, indices]
            y_batch = y[indices]
            
            #########################################################################
            #                       END OF YOUR CODE                                #
            #########################################################################

            # evaluate loss and gradient
            loss, grad = self.loss(X_batch, y_batch, reg)
            loss_history.append(loss)

            # perform parameter update
            #########################################################################
            # TODO:                                                                 #
            # Update the weights using the gradient and the learning rate.          #
            #########################################################################
            self.W += -learning_rate * grad

            #########################################################################
            #                       END OF YOUR CODE                                #
            #########################################################################

            if verbose and it % 100 == 0:
                print('iteration {} / {}: loss {:07.02f}'.format(it, num_iters, loss))

        return loss_history

    def predict(self, X):
        """
        Use the trained weights of this linear classifier to predict labels for
        data points.

        Inputs:
        - X: D x N array of training data. Each column is a D-dimensional point.

        Returns:
        - y_pred: Predicted labels for the data in X. y_pred is a 1-dimensional
          array of length N, and each element is an integer giving the predicted
          class.
        """
        y_pred = np.zeros(X.shape[1])
        ###########################################################################
        # TODO:                                                                   #
        # Implement this method. Store the predicted labels in y_pred.            #
        ###########################################################################
        
        y_pred = np.argmax(np.dot(self.W, X), axis=0)  # K x N array
        ###########################################################################
        #                           END OF YOUR CODE                              #
        ###########################################################################
        return y_pred
  
    def loss(self, X_batch, y_batch, reg):
        """
        Compute the loss function and its derivative. 
        Subclasses will override this.

        Inputs:
        - X_batch: D x N array of data; each column is a data point.
        - y_batch: 1-dimensional array of length N with labels 0...K-1, for K classes.
        - reg: (float) regularization strength.

        Returns: A tuple containing:
        - loss as a single float
        - gradient with respect to self.W; an array of the same shape as W
        """
        pass


class LinearSVM(LinearClassifier):
    """ A subclass that uses the Multiclass SVM loss function """

    def loss(self, X_batch, y_batch, reg):
        return svm_loss_vectorized(self.W, X_batch, y_batch, reg)


class Softmax(LinearClassifier):
    """ A subclass that uses the Softmax + Cross-entropy loss function """

    def loss(self, X_batch, y_batch, reg):
        return softmax_loss_vectorized(self.W, X_batch, y_batch, reg)
