import matplotlib.pyplot as plt
import numpy as np

# Print barplot with iteration times
grid_equivalents = ('32³', '64³', '128³', '256³', '512³')

image_size = "(1024x1024)"
stage_times = {
    'Rendering': np.array([447, 501, 584, 838, 1693]),
    'Regularization': np.array([1, 1, 10, 10, 100]),
    'Optimizer': np.array([3, 3, 4, 10, 40]),
    'Redistancing': np.array([9, 12, 24, 79, 318]),
}
# image_size = "(512x512)"
# stage_times = {
#     'Rendering': np.array([180, 180, 340, 480, 760]),
#     'Regularization': np.array([1, 1, 10, 10, 100]),
#     'Optimizer': np.array([3, 3, 4, 10, 40]),
#     'Redistancing': np.array([9, 12, 24, 79, 318]),
# }
stage_colors = [ "royalblue", "limegreen", "gold", "tomato" ]
width = 0.6  # the width of the bars: can also be len(x) sequence


fig, ax = plt.subplots(dpi=300)
bottom = np.zeros(5)

for i, stage in enumerate(stage_times.items()):
    p = ax.bar(grid_equivalents, stage[1], width, label=stage[0], bottom=bottom, color=stage_colors[i])
    bottom += stage[1]

    # ax.bar_label(p, label_type='center')

ax.set_title('Average time of 1 iteration ' + image_size)
ax.set_xlabel("Equivalent grid size")
ax.set_ylabel("Time, ms")
ax.legend()
plt.savefig("figures/time_1iter.eps")