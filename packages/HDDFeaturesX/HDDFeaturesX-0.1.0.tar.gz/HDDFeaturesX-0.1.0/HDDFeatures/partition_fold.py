import numpy as np

def partition_fold(data, k, max_iterations=100):
    """
    Function to partition the dataset into k parts using the Grey Wolf Optimizer.
    
    Parameters:
    data (np.array): The dataset to be divided.
    k (int): The desired number of parts.
    max_iterations (int): The number of iterations for the Grey Wolf Optimizer.
    
    Returns:
    list of np.array: A list containing k parts of the dataset.
    """
    def objective_function(indices):
        # Reshape indices into k parts
        parts = [indices[i::k] for i in range(k)]
        # Calculate the objective (e.g., variance of parts)
        variances = [np.var(data[part], axis=0).sum() for part in parts]
        return np.mean(variances)
    
    def initialize_positions(n_agents, dim):
        return np.random.randint(0, dim, (n_agents, dim))

    def gwo_optimize(dim, n_agents, max_iterations):
        alpha_pos = np.zeros(dim)
        alpha_score = float('inf')

        beta_pos = np.zeros(dim)
        beta_score = float('inf')

        delta_pos = np.zeros(dim)
        delta_score = float('inf')

        positions = initialize_positions(n_agents, dim)

        for iteration in range(max_iterations):
            for i in range(n_agents):
                fitness = objective_function(positions[i])

                if fitness < alpha_score:
                    alpha_score = fitness
                    alpha_pos = positions[i].copy()

                elif fitness < beta_score:
                    beta_score = fitness
                    beta_pos = positions[i].copy()

                elif fitness < delta_score:
                    delta_score = fitness
                    delta_pos = positions[i].copy()

            a = 2 - iteration * (2 / max_iterations)

            for i in range(n_agents):
                for j in range(dim):
                    r1, r2 = np.random.rand(2)
                    A1 = 2 * a * r1 - a
                    C1 = 2 * r2
                    D_alpha = abs(C1 * alpha_pos[j] - positions[i][j])
                    X1 = alpha_pos[j] - A1 * D_alpha

                    r1, r2 = np.random.rand(2)
                    A2 = 2 * a * r1 - a
                    C2 = 2 * r2
                    D_beta = abs(C2 * beta_pos[j] - positions[i][j])
                    X2 = beta_pos[j] - A2 * D_beta

                    r1, r2 = np.random.rand(2)
                    A3 = 2 * a * r1 - a
                    C3 = 2 * r2
                    D_delta = abs(C3 * delta_pos[j] - positions[i][j])
                    X3 = delta_pos[j] - A3 * D_delta

                    # Weights based on long-tail distribution (alpha > beta > delta)
                    weights = np.abs(np.random.pareto(a=2.5, size=3))  
                    weights /= np.sum(weights) 

                 
                    new_position = weights[0] * X1 + weights[1] * X2 + weights[2] * X3
                    positions[i][j] = np.clip(new_position, 0, dim - 1)  

        return alpha_pos


    num_samples = data.shape[0]
    num_agents = 20  # You can adjust this based on the problem size
    optimal_indices = gwo_optimize(num_samples, num_agents, max_iterations)
    optimal_indices = optimal_indices.astype(int)

    # Partition the data using the optimized indices
    parts = [data[optimal_indices[i::k], :] for i in range(k)]
    
    return parts
