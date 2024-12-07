
import matplotlib.pyplot as plt
import numpy as np

import barcode as bc

def plot_barcode_lines(lines, name, show = False, save = False):
	# Количество объектов
	np.random.seed(0)  # Для повторяемости результатов
	# Уникальные цвета для каждого объекта
	colors = []
	for i in range(30):
		r = np.round(np.random.rand(),1)
		g = np.round(np.random.rand(),1)
		b = np.round(np.random.rand(),1)

		colors.append([r,g,b])

	separateFig, ax = plt.subplots(1, 1)
	ax.grid(True)

	ax.set_xlabel('Brightness')
	ax.set_ylabel('Component number')

	k = 1
	for line in lines:
		x_coords = [line[0], line[1]]
		heights = [k, k]
		ax.plot(x_coords, heights, linestyle='-', color=colors[k % len(colors)], linewidth= 1)
		k += 1

	if show:
		plt.show()

	if save:
		plt.savefig(f"{name}.png", dpi=300)
		plt.savefig(f"{name}.svg")




def plot_3d_list(item : bc.Baritem):
    bar = item.getBarcodeLines()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    n = 100

    kn=0
    for bl in bar:
        vals = bl.get3dList()

        for i in range(0,len(vals),5):
            ax.scatter(kn, vals[i].value, vals[i].count, marker='o')
        kn+=1

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.show()