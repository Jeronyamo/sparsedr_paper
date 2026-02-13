import matplotlib.pyplot as plt
import numpy as np

# Print barplot with iteration times
grid_equivalents = ('32³', '64³', '128³', '256³', '512³')
stage_times = {
    'Rendering': np.array([180, 180, 340, 480, 760]),
    'Regularization': np.array([1, 1, 10, 10, 100]),
    'Redistancing': np.array([1, 3, 12, 70, 110]),
}
stage_colors = [ "orangered", "royalblue", "springgreen" ]
width = 0.6  # the width of the bars: can also be len(x) sequence


fig, ax = plt.subplots(dpi=300)
bottom = np.zeros(5)

for i, stage in enumerate(stage_times.items()):
    p = ax.bar(grid_equivalents, stage[1], width, label=stage[0], bottom=bottom, color=stage_colors[i])
    bottom += stage[1]

    # ax.bar_label(p, label_type='center')

ax.set_title('Average time of 1 iteration')
ax.set_xlabel("Grid equivalent")
ax.set_ylabel("Time, ms")
ax.legend()
plt.savefig("figures/time_1iter.png")