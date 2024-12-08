import torch
import torch.nn as nn
import torch.optim as optim

class TreeNode(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(TreeNode, self).__init__()
        self.fc = nn.Linear(input_size * 2, hidden_size)
        self.activation = nn.ReLU()

    def forward(self, left, right):
        combined = torch.cat((left, right), dim=1)
        output = self.fc(combined)
        output = self.activation(output)
        return output

class TreeRNN(nn.Module):
    def __init__(self, leaf_size, hidden_size):
        super(TreeRNN, self).__init__()
        self.leaf_size = leaf_size
        self.hidden_size = hidden_size
        self.node = TreeNode(leaf_size, hidden_size)            
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, tree):
        if isinstance(tree, int):
            # Leaf node
            return torch.tensor([tree], dtype=torch.float32).view(1, -1)
        else:
            left, right = tree
            left_vector = self.forward(left)
            right_vector = self.forward(right)
            node_vector = self.node(left_vector, right_vector)
            return node_vector

    def predict(self, tree):
        root_vector = self.forward(tree)
        score = self.fc(root_vector)
        return score

# Example tree: ((1, 2), (3, ))
tree = ((1, 2), (3, ))

# Initialize model, loss function, and optimizer
model = TreeRNN(leaf_size=1, hidden_size=10)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# Training data (example)
train_trees = [((1, 2), (3, )), ((1,), (2,)), ((5,), (6,)), ((1, 2, 3), (4,)), ((1, 2, 3, 4), (5, 6))]
train_scores = [5.0, 3.0, 6.0, 8.0, 10.0]

# Training loop
for epoch in range(100):
    for tree, score in zip(train_trees, train_scores):
        optimizer.zero_grad()
        prediction = model.predict(tree)
        loss = criterion(prediction, torch.tensor([score], dtype=torch.float32))
        loss.backward()
        optimizer.step()

# Predicting for a new tree
new_tree = ((1, 2), (3, ))
predicted_score = model.predict(new_tree)
print(predicted_score.item())
