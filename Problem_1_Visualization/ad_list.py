import matplotlib.pyplot as plt
import random

# 사용자로부터 입력 받은 인접 리스트
adj_list_input = {}
num_nodes = int(input("노드 개수를 입력하세요: "))
for i in range(num_nodes):
    node = input(f"{i+1}번째 노드의 이름을 입력하세요: ")
    neighbors = input(f"{node}의 이웃 노드를 입력하세요 (쉼표로 구분하여 입력): ").split(',')
    adj_list_input[node] = [neighbor.strip() for neighbor in neighbors]  # 공백 제거하여 저장

# 각 노드의 좌표를 랜덤으로 정의
pos = {node: (random.uniform(0, 10), random.uniform(0, 10)) for node in adj_list_input.keys()}

# 그래프 그리기
plt.figure(figsize=(6, 4))

# 각 노드를 그리기
for node, neighbors in adj_list_input.items():
    plt.scatter(pos[node][0], pos[node][1], color='purple', s=200, zorder=5)  # 노드를 그리기
    plt.text(pos[node][0], pos[node][1], node, fontsize=12, ha='center', va='center', color='white', zorder=10)  # 노드 이름 표시
    for neighbor in neighbors:
        plt.plot([pos[node][0], pos[neighbor][0]], [pos[node][1], pos[neighbor][1]], color='black', zorder=1)  # 간선을 그리기


plt.title('Graph Visualization')
plt.axis('off')  # 축을 비활성화
plt.show()
