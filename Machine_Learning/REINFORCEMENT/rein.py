import numpy as np

# Q-table (4 states)
Q = np.zeros((4,4))

# Reward matrix
R = np.array([
    [-1, 0, 0, -1],
    [-1, -1, -1, 100],
    [-1, -1, -1, 100],
    [-1, -1, -1, 100]
])
                           
gamma = 0.9             
alpha = 0.1  

print(R)
print("--------------")
for episode in range(100):
    state = 0  # Start at A
    
    while state != 3:  # until reach D
        actions = np.where(R[state] >= 0)[0]
        action = np.random.choice(actions)
        
        next_state = action
        
        Q[state, action] = Q[state, action] + alpha * (
            R[state, action] + gamma * np.max(Q[next_state]) - Q[state, action]
        )
        
        state = next_state

print("Q-table:")
print(Q)