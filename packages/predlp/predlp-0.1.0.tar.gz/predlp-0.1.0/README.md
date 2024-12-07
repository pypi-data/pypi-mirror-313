# PredLP
Prediction probabilities with a linear programming constraint during label assignment.

## Usage
Example label contraint imposed using the package *predlp* via this code:
```python
from predlp.solver import pred_prob_lp

# ML outputs feed into predlp constraints
class_names = ['label_a', 'label_b', 'label_c']
label_counts = {'label_a': 2, 'label_b': 1, 'label_c': 1}
pred_probs = [
    [0.6*, 0.3,  0.1],
    [0.2,  0.5*, 0.3],
    [0.8*, 0.1,  0.1],
    [0.5,  0.1,  0.4*]
]

# Run through solver and optimize for probability scores
pred_after_lp = pred_prob_lp(class_names=class_names, label_counts= label_counts, pred_probs=pred_probs)

# Output of predlp, highlighted in array (*)
pred_after_lp == ['label_a', 'label_b', 'label_a', 'label_c']
```

## Parameters
- **class_names** (list):  The list should be in the order that matches the pred_prob array. So if class 0 is ‘linear’ and class 1 is ‘programming’, then class_names = ['linear', 'programming'].
- **label_counts** (dict): A dictionary specifying the expected count for each label. The keys represent the class (N), and the values (K) constraints.
- **pred_probs** (np.array): A 2D array of shape (N, K) containing the model predicted probabilities for each label. Each row corresponds to a class, corresponding to the class_name parameter, and the columns represent probabilities for classes {0, 1, ..., K-1}.

## Returns
- **pred_lp** (list): A list of predicted labels, with a total length of N. The list satisfies the constraints defined by label_counts and is optimized to maximize the total probability score across all predictions.

## Citation and related publications

Here are relevant papers to cite if you use this package:

<details><summary><a href="https://www.statcan.gc.ca/en/conferences/symposium2024/program">Life in the FastText Lane: Harnessing Linear Programming Constrained Machine Learning for Classifications Revision</a> (<b>click to show bibtex</b>) </summary>

    @inproceedings{
        title={Life in the FastText Lane: Harnessing Linear Programming Constrained Machine Learning for Classifications Revision},
        author={Justin Evans, Laura Wile},
        conference={Statistics Canada's International Methodology Symposium: The Future of Official Statistics},
        year={2024}
    }

</details>