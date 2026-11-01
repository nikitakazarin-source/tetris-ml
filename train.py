import random
from collections import deque
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from main import TetrisEngine


class DQN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(4, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        return self.net(x)


class DQNAgent:
    def __init__(self):
        self.model = DQN()
        self.optimizer = optim.Adam(self.model.parameters(), lr=1e-3)
        self.criterion = nn.MSELoss()
        self.memory = deque(maxlen=20000)

        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.001
        self.epsilon_decay = 0.995
        self.batch_size = 512

    def select_action(self, next_states):
        if random.random() <= self.epsilon:
            return random.choice(list(next_states.keys()))

        actions = list(next_states.keys())
        states_tensor = torch.FloatTensor(np.array(list(next_states.values())))

        self.model.eval()
        with torch.no_grad():
            predictions = self.model(states_tensor).squeeze()
        self.model.train()

        best_idx = torch.argmax(predictions).item()
        return actions[best_idx]

    def remember(self, state, reward, next_state, done):
        self.memory.append((state, reward, next_state, done))

    def replay(self):
        if len(self.memory) < self.batch_size:
            return

        batch = random.sample(self.memory, self.batch_size)
        states, rewards, next_states, dones = zip(*batch)

        states_t = torch.FloatTensor(np.array(states))
        rewards_t = torch.FloatTensor(rewards).unsqueeze(1)
        next_states_t = torch.FloatTensor(np.array(next_states))
        dones_t = torch.FloatTensor(dones).unsqueeze(1)

        with torch.no_grad():
            next_q = self.model(next_states_t)
            targets = rewards_t + (1 - dones_t) * self.gamma * next_q

        current_q = self.model(states_t)
        loss = self.criterion(current_q, targets)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


if __name__ == "__main__":
    env = TetrisEngine()
    agent = DQNAgent()
    episodes = 2000
    best_score = 0

    for ep in range(1, episodes + 1):
        state = env.reset()
        done = False

        while not done:
            next_states = env.get_next_states()
            if not next_states:
                break

            action = agent.select_action(next_states)
            next_state = next_states[action]
            reward, done = env.step_ai(action)

            agent.remember(state, reward, next_state, done)
            state = next_state

        agent.replay()

        if env.score > best_score:
            best_score = env.score
            torch.save(agent.model.state_dict(), "best_tetris_model.pth")

        if ep % 50 == 0:
            print(f"Episode: {ep} | Score: {env.score} | Lines: {env.lines_cleared} | Best: {best_score} | Epsilon: {agent.epsilon:.3f}")