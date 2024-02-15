# The Boundary of Neural Network Trainability is Fractal

https://arxiv.org/html/2402.06184v1

This paper by Jascha Sohl-Dickstein explores the intriguing similarities between the generation of certain fractals (like the Mandelbrot and Julia sets) and the training of neural networks. Both processes involve iterating a function and observing the divergent or convergent behavior of the resultant series based on the hyperparameters chosen. The study specifically investigates the boundary between hyperparameters that lead to stable versus divergent neural network training outcomes, revealing that this boundary exhibits fractal characteristics across a wide range of scales and configurations.

The research demonstrates that iterating a complex function with neural networks, influenced by random factors from weight initialization and training data, results in fractal patterns that resemble more organic structures, lacking the repeated symmetry seen in traditional fractals. This phenomenon is observed across various experimental conditions, including different nonlinearities (tanh, ReLU, identity), training methods (full batch, minibatch), and hyperparameters (learning rates, initialization parameters).

Significantly, the paper discusses the implications of these findings for understanding neural network training dynamics, meta-learning, and the optimization of hyperparameters. It suggests that the fractal nature of the boundary between convergent and divergent training conditions may explain the sensitivity and chaotic behavior of neural network training outcomes in response to small hyperparameter adjustments. This insight is particularly relevant for meta-learning, where navigating the complex landscape of hyperparameters is crucial for optimizing neural network performance.

The study also touches on the aesthetic and engaging aspect of fractals, noting the personal enjoyment derived from the project and its appeal to a broader audience, including the author's daughter. This highlights the unique intersection of mathematical beauty, theoretical research, and practical implications for neural network training and optimization.

## References

- Boyd, S. P., & Vandenberghe, L. (2004). *Convex optimization*. Cambridge University Press.
- Brooks, R., & Matelski, J. P. (1981). The dynamics of 2-generator subgroups of psl (2, c). In *Riemann surfaces and related topics: Proceedings of the 1978 Stony Brook Conference* (Vol. 1). Princeton University Press Princeton, New Jersey.
- Chen, X., Balasubramanian, K., Ghosal, P., & Agrawalla, B. (2023). From stability to chaos: Analyzing gradient descent dynamics in quadratic regression. arXiv preprint arXiv:2310.01687.
- Gostick, J. T., Khan, Z. A., Tranter, T. G., Kok, M. D. R., Agnaou, M., Sadeghi, M., & Jervis, R. J. (2019). Porespy: A python toolkit for quantitative analysis of porous media images. *Journal of Open Source Software*, 4(37), 1296.
- Julia, G. (1918). Mémoire sur l’itération des fonctions rationnelles. *Journal de mathématiques pures et appliquées*, 1, 47–245.
- Kong, L., & Tao, M. (2020). Stochasticity of deterministic gradient descent: Large learning rate for multiscale objective function. *Advances in Neural Information Processing Systems*, 33, 2625–2638.
- Mandelbrot, B. B. (1982). *The fractal geometry of nature* (Vol. 1). WH Freeman New York.
- Markus, M., & Hess, B. (1998). Lyapunov exponents of the logistic map with periodic forcing. In *Chaos and Fractals* (pp. 73–78). Elsevier.
- Mei, S., Montanari, A., & Nguyen, P.-M. (2018). A mean field view of the landscape of two-layer neural networks. *Proceedings of the National Academy of Sciences*, 115(33), E7665–E7671.
- Metz, L., Maheswaranathan, N., Nixon, J., Freeman, D., & Sohl-Dickstein, J. (2019). Understanding and correcting pathologies in the training of learned optimizers. In *International Conference on Machine Learning* (pp. 4556–4565). PMLR.
- Metz, L., Harrison, J., Freeman, C. D., Merchant, A., Beyer, L., Bradbury, J., Agrawal, N., Poole, B., Mordatch, I., Roberts, A., & Sohl-Dickstein, J. (2022). Velo: Training versatile learned optimizers by scaling up.
- Michelitsch, T. M., & Rössler, O. E. (1992). The “burning ship” and its quasi-julia sets. *Computers & Graphics*, 16(4), 435–438.
- Milnor, J. (2011). *Dynamics in One Complex Variable.(AM-160):(AM-160)-* (Vol. 160). Princeton University Press.
- Tatham, S. Fractals derived from Newton–Raphson. http://www.chiark.greenend.org.uk/~sgtatham/newton/.
