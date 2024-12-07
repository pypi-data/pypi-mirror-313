import numpy as np
from pulp import LpProblem, LpVariable, lpSum, LpMaximize

def pred_prob_lp(class_names: list, label_counts: dict, pred_probs: np.array) -> list:
    """ An LP solver for prediction probabilities

    Args:
        class_names (list):  The list should be in the order that matches the pred_prob array. So if class 0 is ‘linear’ and class 1 is ‘programming’, then class_names = ['linear', 'programming'].
        label_counts (dict): A dictionary specifying the expected count for each label. The keys represent the class (N), and the values (K) constraints.
        pred_probs (np.array): A 2D array of shape (N, K) containing the model predicted probabilities for each label. Each row corresponds to a class, corresponding to the class_name parameter, and the columns represent probabilities for classes {0, 1, ..., K-1}.
    Returns:
        pred_lp (list): A list of predicted labels, with a total length of N. The list satisfies the constraints defined by label_counts and is optimized to maximize the total probability score across all predictions.
    
    """
    
    # Create a linear programming problem
    lp_model = LpProblem(name="Label_Optimization", sense=LpMaximize)

    # Create binary variables for label assignment
    x = LpVariable.dicts("label_assignment", ((i, j) for i in range(len(pred_probs)) for j in class_names), cat='Binary')

    # Objective function: maximize the probability scores
    lp_model += lpSum(x[i, j] * pred_probs [i][class_names.index(j)] for i in range(len(pred_probs)) for j in class_names)

    # Constraints: label count constraints
    for j in class_names:
        lp_model += lpSum(x[i, j] for i in range(len(pred_probs))) == label_counts[j]

    # Constraint: each score array (ie. record) can only be selected once
    for i in range(len(pred_probs)):
        lp_model += lpSum(x[i, j] for j in class_names) == 1

    # Solve the problem
    lp_model.solve()

    # Return the results
    pred_lp = []
    for i in range(len(pred_probs)):
        for j in class_names:
            if x[i, j].value() == 1:
                # print(f"Data Point {i+1}: {j}")
                pred_lp.append(j)

    print("Optimal Score:", lp_model.objective.value())

    return pred_lp