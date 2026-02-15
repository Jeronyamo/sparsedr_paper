import matplotlib.pyplot as plt
import numpy as np

# Print barplot with iteration times
grid_equivalents = ('32³', '64³', '128³', '256³', '512³')

image_size = "(1024x1024)"
stage_times = {
    'Rendering': np.array([440.84, 476.96, 516.15, 668.85, 1169.08]),
    'Regularization': np.array([1, 1, 10, 10, 10]),
    'Optimizer': np.array([2.34,  2.44, 2.46, 2.57, 6.26]),
    'Redistancing': np.array([6.23, 6.19, 7.38, 14.54, 45.15]),
}
stage_times_ref = {
    'Rendering': np.array([1609.54,1616.62,1613.52,1620.31, 1660.60]),
    'Regularization': np.array([4.77 ,3.32,3.38,4.23 ,2.46]),
    'Optimizer': np.array([1.93,1.11,1.18,2.03,3.85]),
    'Redistancing': np.array([171.22,186.05,197.84,254.95,527.85]),
}
# image_size = "(512x512)"
# stage_times = {
#     'Rendering': np.array([180, 180, 340, 480, 760]),
#     'Regularization': np.array([1, 1, 10, 10, 100]),
#     'Optimizer': np.array([3, 3, 4, 10, 40]),
#     'Redistancing': np.array([9, 12, 24, 79, 318]),
# }
stage_colors = [ "royalblue", "limegreen", "gold", "tomato" ]

fig, ax = plt.subplots(layout='constrained')
bottom1 = np.zeros(5)
bottom2 = np.zeros(5)

x = np.arange(5)  # the label locations
width = 0.3  # the width of the bars
multiplier = 0.55

for i, stage in enumerate(stage_times.items()):
    stage = tuple([stage[0], stage[1], stage_times_ref[stage[0]]])
    offset = width * multiplier
    p = ax.bar(x + offset, stage[1], width, label=stage[0], bottom=bottom1, color=stage_colors[i])
    p = ax.bar(x - offset, stage[2], width, bottom=bottom2, color=stage_colors[i])
    bottom1 += stage[1]
    bottom2 += stage[2]

    # ax.bar_label(p, label_type='center')

# ax.set_title('Average time of 1 iteration ' + image_size)
# ax.set_xlabel("Equivalent grid size")
ax.set_ylabel("Time (ms)")
ax.set_xticks(range(len(grid_equivalents)))
ax.set_xticklabels(grid_equivalents)
ax.legend()
handles, labels = plt.gca().get_legend_handles_labels()
plt.legend(handles[::-1], labels[::-1])
plt.savefig("figures/time_1iter.eps")
plt.savefig("figures/time_1iter.png")


#Print plot showing loss for all iterations
##Parse output files for loss and time
def parse_sparsedr_output(fpath: str):
    scene_infos = {}
    with open(fpath) as ffile:
        for fline in ffile:
            if fline.startswith("Optimizing scene: "):
                scene_name = fline[len("Optimizing scene: "):].strip()
                scene_ckpt = 0
                scene_infos[scene_name] = { "scene_losses" : [], "scene_avg_time" : [[],], "scene_avg_psnr" : 0.0 }
            if fline.startswith("Iter:"):
                # print("HEEEEEERE:", fline, fline[fline.find(':', 5)+1:fline.find('+', fline.find(':', 5)+1)])
                scene_infos[scene_name]["scene_losses"].append(float(fline[fline.find(':', 5)+1:fline.find('+', fline.find(':', 5)+1)].strip()))
                scene_infos[scene_name]["scene_avg_time"][scene_ckpt].append([ float(val.strip())  for val in fline[fline.rfind('(')+1:fline.rfind(')')].split('+') ])
            if fline.startswith("Average PSNR"):
                scene_infos[scene_name]["scene_avg_psnr"] = float(fline[fline.find(':')+1:].strip())
            if fline.startswith("OptimizeGrid - Saved checkpoint: "):
                scene_ckpt = int(fline[fline.rfind('_')+1:fline.rfind('.')])
                scene_infos[scene_name]["scene_avg_time"].extend([ []  for _ in range(len(scene_infos[scene_name]["scene_avg_time"]), scene_ckpt+1) ])

    for scene in scene_infos:
        arr0, arr1, arr2, arr3 = [], [], [], []
        for i in range(len(scene_infos[scene]["scene_avg_time"])):
            avg_values = [0.0, 0.0, 0.0, 0.0]
            if len(scene_infos[scene]["scene_avg_time"][i]) == 0: continue
            for iter_infos in scene_infos[scene]["scene_avg_time"][i]:
                avg_values[0] += iter_infos[0]
                avg_values[1] += iter_infos[1]
                avg_values[2] += iter_infos[2]
                avg_values[3] += iter_infos[3]
            avg_values[0] /= max(1, len(scene_infos[scene]["scene_avg_time"][i]))
            avg_values[1] /= max(1, len(scene_infos[scene]["scene_avg_time"][i]))
            avg_values[2] /= max(1, len(scene_infos[scene]["scene_avg_time"][i]))
            avg_values[3] /= max(1, len(scene_infos[scene]["scene_avg_time"][i]))
            scene_infos[scene]["scene_avg_time"][i] = avg_values
            arr0.append(float(avg_values[0]))
            arr1.append(float(avg_values[1]))
            arr2.append(float(avg_values[2]))
            arr3.append(float(avg_values[3]))
        scene_infos[scene]["scene_avg_time"] = [np.array(arr0), np.array(arr1), np.array(arr2), np.array(arr3)]
    return scene_infos

all_scene_infos = parse_sparsedr_output("misc/dr_log_armadillo.txt")
all_scene_infos.update(parse_sparsedr_output("misc/dr_log_all_but_armadillo.txt"))

avg_arr0, avg_arr1, avg_arr2, avg_arr3 = np.array([0.,0.,0.,0.,0.,0.,0.]), np.array([0.,0.,0.,0.,0.,0.,0.]), np.array([0.,0.,0.,0.,0.,0.,0.]), np.array([0.,0.,0.,0.,0.,0.,0.])
scene_count = 0
for scene in all_scene_infos:
    if not scene.endswith("New1024"): continue
    scene_count += 1
    avg_arr0 += all_scene_infos[scene]["scene_avg_time"][0]
    avg_arr1 += all_scene_infos[scene]["scene_avg_time"][1]
    avg_arr2 += all_scene_infos[scene]["scene_avg_time"][2]
    avg_arr3 += all_scene_infos[scene]["scene_avg_time"][3]
avg_arr0 /= max(scene_count, 1)
avg_arr1 /= max(scene_count, 1)
avg_arr2 /= max(scene_count, 1)
avg_arr3 /= max(scene_count, 1)
# print(avg_arr0*0.5, avg_arr1, avg_arr2, avg_arr3)


fig, ax = plt.subplots(dpi=300, layout='constrained')

ax.plot(range(0,1000,2), all_scene_infos["NefertitiNew1024"]["scene_losses"])

ax.set_xlabel("Iterations")
ax.set_ylabel("MSE Loss")
plt.savefig("figures/loss_example.eps")
plt.savefig("figures/loss_example.png")

#Print model size plot
fig, ax = plt.subplots(dpi=300, layout='constrained')

grid_equivalents = ('32³', '64³', '128³', '256³', '512³', '1024³', '2048³')
arr_sizes = np.array([[32**3/1024/1024, 64**3/1024/1024, 128**3/1024/1024, 256**3/1024/1024, 512**3/1024/1024, 1024**3/1024/1024, 2048**3/1024/1024], [0.7,1.7,6.3,23.7,96.4,392.1, 1597.7]])
ax.plot(grid_equivalents, arr_sizes[0].T, label="Baseline", color=stage_colors[0])
ax.plot(grid_equivalents, arr_sizes[1].T, label="SparseDR", color=stage_colors[3])

# ax.set_xlabel("Iterations")
ax.set_ylabel("Size (MB)")
ax.set_yscale("log", base=2)
handles, labels = ax.get_legend_handles_labels()
ax.legend(fontsize=14)
plt.savefig("figures/size_comp.eps")
plt.savefig("figures/size_comp.png")


#Print PSNR bar plot
models = ("Armadillo", "Bunny", "Dragon", "Happy", "Nefertiti", "Teapot")
method_psnr = {
    'Baseline': (31., 35., 30., 31., 35., 36),
    'SparseDR': (all_scene_infos["ArmadilloNew1024"]["scene_avg_psnr"],
                 all_scene_infos[    "BunnyNew1024"]["scene_avg_psnr"],
                 all_scene_infos[   "DragonNew1024"]["scene_avg_psnr"],
                 all_scene_infos[    "HappyNew1024"]["scene_avg_psnr"],
                 all_scene_infos["NefertitiNew1024"]["scene_avg_psnr"],
                 all_scene_infos[   "TeapotNew1024"]["scene_avg_psnr"]),
}

x = np.arange(len(models))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0.5

fig, ax = plt.subplots(layout='constrained')
itr = 0
for attribute, measurement in method_psnr.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute, color=stage_colors[itr])
    ax.bar_label(rects, padding=3)
    multiplier += 1
    itr += 3

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('PSNR (dB)')
# ax.set_title('Penguin attributes by species')
ax.set_xticks(x + width, models)
ax.legend(loc='upper left', ncols=2, fontsize=14)
ax.set_ylim(0, 50)

plt.savefig("figures/psnr_comp.eps")
plt.savefig("figures/psnr_comp.png")