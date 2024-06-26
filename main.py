import random
from itertools import chain, combinations
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def powerset(iterable):
    """计算幂集（所有子集的集合）。"""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def is_inside_circle(point, circle_center, radius):
    """检查点是否在圆内。"""
    x, y = point
    cx, cy = circle_center
    return (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2


def monte_carlo_net_area(main_R, main_coord, main_influence, other_Rs, other_coords, other_influence,
                         num_samples=100000):
    """使用蒙特卡洛方法计算主要公司和其他公司影响范围的净面积。"""

    # 计算样本点可能出现的最大和最小坐标
    max_x = max([main_coord[0] + main_R] + [coord[0] + R for coord, R in zip(other_coords, other_Rs)])
    min_x = min([main_coord[0] - main_R] + [coord[0] - R for coord, R in zip(other_coords, other_Rs)])
    max_y = max([main_coord[1] + main_R] + [coord[1] + R for coord, R in zip(other_coords, other_Rs)])
    min_y = min([main_coord[1] - main_R] + [coord[1] - R for coord, R in zip(other_coords, other_Rs)])

    # 生成所有圆的组合的幂集
    circle_list = list(range(len(other_Rs)))
    powersets = powerset(circle_list)

    # 计算点落在各种组合内的次数
    count_inside_main = 0
    count_inside = {}
    influence = {}
    for i in powersets:
        count_inside[i] = 0
        influence[i] = main_influence
        for j in i:
            influence[i] += other_influence[j]
    for _ in range(num_samples):
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)

        if is_inside_circle((x, y), main_coord, main_R):
            count_inside_main += 1
            i = 0
            sets = ()
            for coord, R in zip(other_coords, other_Rs):
                if is_inside_circle((x, y), coord, R):
                    sets = sets + (i,)
                i += 1
            count_inside[sets] += 1

    # 计算净影响面积
    area = 0
    for i in powerset(circle_list):
        area += (main_influence / influence[i]) * (count_inside[i] / num_samples) * (max_x - min_x) * (max_y - min_y)

    return area


def visualize_influence(main_R, main_coord, other_Rs, other_coords):
    """可视化主公司和其他公司的影响范围。"""
    fig, ax = plt.subplots(figsize=(10, 10))

    # 绘制主要公司的圆
    main_circle = patches.Circle(main_coord, main_R, fc='blue', alpha=0.5)
    ax.add_patch(main_circle)

    # 绘制其他公司的圆
    for R, coord in zip(other_Rs, other_coords):
        other_circle = patches.Circle(coord, R, fc='red', alpha=0.5)
        ax.add_patch(other_circle)

    # 设置图形的边界
    max_radius = max([main_R] + other_Rs)
    ax.set_xlim(-max_radius, max_radius)
    ax.set_ylim(-max_radius, max_radius)

    # 设置网格和纵横比
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


# 输入值
main_R = float(input("输入您公司圆的半径："))
main_coord = (0, 0)
main_influence = float(input("输入您公司的影响力："))

num_other_circles = int(input("输入其他竞争公司的数量："))
other_Rs = []
other_coords = []
other_influence = []

for i in range(num_other_circles):
    R = float(input(f"输入第{i + 1}个公司的半径："))
    x = float(input(f"输入第{i + 1}个公司圆心的X坐标："))
    y = float(input(f"输入第{i + 1}个公司圆心的Y坐标："))
    influence = float(input(f"输入第{i + 1}个公司的影响力："))

    other_Rs.append(R)
    other_coords.append((x, y))
    other_influence.append(influence)

# 使用蒙特卡洛方法计算净面积
area = monte_carlo_net_area(main_R, main_coord, main_influence, other_Rs, other_coords, other_influence)
print(f"净影响面积: {area}")

# 可视化影响范围
visualize_influence(main_R, main_coord, other_Rs, other_coords)


# exit(0)
