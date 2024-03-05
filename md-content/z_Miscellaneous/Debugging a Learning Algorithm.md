# Debugging a Learning Algorithm

You've implemented regularized linear regression on housing prices, but it makes unacceptably large errors in predictions. What do you try next?

- **Get more training examples** — This can help fix high variance.
- **Try smaller sets of features** — This can help fix high variance.
- **Try getting additional features** — This can help fix high bias.
- **Try adding polynomial features** — This can help fix high bias. Examples of polynomial features include \(x_1^2\), \(x_2^2\), \(x_1 \times x_2\), etc.
- **Try decreasing \(\lambda\)** — This can help fix high bias.
- **Try increasing \(\lambda\)** — This can help fix high variance.

The cost function for regularized linear regression is given by:

\[ J(\vec{w}, b) = \frac{1}{2m} \sum_{i=1}^{m} (f_{\vec{w},b}(\vec{x}^{(i)}) - y^{(i)})^2 + \frac{\lambda}{2m} \sum_{j=1}^{n} w_j^2 \]

- The first term measures how well the model \(f_{\vec{w},b}\) fits the training data.
- The second term penalizes the complexity of the model by adding the squared magnitude of the weights multiplied by the regularization parameter \(\lambda\).

## Bias and Variance

High bias and high variance describe two different issues related to the performance of machine learning models on training and validation (or test) datasets.

- **High Bias**: High bias occurs when a model has insufficient complexity to capture the underlying patterns of the data, leading to poor performance on both the training and validation datasets. This situation is indicative of underfitting, where the model is too simple to accurately represent the data. High bias is characterized by a significant error on the training set, suggesting that the model is not even fitting the training data well.

- **High Variance**: High variance occurs when a model is too complex, capturing not only the underlying patterns but also the noise in the training dataset. This leads to a model that performs well on the training data but poorly on unseen data (validation or test dataset), indicative of overfitting. High variance is characterized by a significant difference between the training error and the validation error, where the model's performance on the training set is much better than on the validation set.

In summary, if the training error differs significantly from the validation error, with much lower error on the training set, it's a sign of high variance, not high bias. High variance suggests that the model is overfitting the training data and not generalizing well to unseen data.
