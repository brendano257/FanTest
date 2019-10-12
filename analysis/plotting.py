"""
Preferred plotting method is seconds from start of experiment -- since all experiments are conducted via scripts, the
start and end times are reliable down to a second or two.
"""

from pathlib import Path


def plot(title, filepath: Path, limits=None, minor_ticks=None, major_ticks=None,
		 x_label_str='Seconds', y_label_str='Temperature (\xb0C)',
		 vertical_annotations=(), horizontal_annotations=(),
		 color_set = ('#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf'),
		 **kwargs):
	"""
	Plots x, y coordinates with a single y-axis as a line graph with optional axis labels, tick control and a default
	color scheme.

	:param str title: title to be displayed on the plot
	:param Path filepath: pathlib Path where file will be saved, can relative to dir function is called in, or absolute
	:param dict limits: optional dictionary of limits including ['top','bottom','right','left']
	:param list minor_ticks: list of values along x-axis at which to place minor ticks
	:param list major_ticks: list of values along x-axis at which to place major ticks
	:param str x_label_str: label to be placed below x-axis
	:param str y_label_str: label to be placed below y-axis
	:param tuple vertical_annotations: any vertical lines to be plotted in the form (('name', x), ...)
	:param tuple horizontal_annotations: any horizontal lines to be plotted in the form (('name', y), ...)
	:param iterable color_set: iterable containing valid matplotlib colors;
		default scheme courtesy of Color Brewer (http://colorbrewer2.org/#type=qualitative&scheme=Set1&n=8)
	:param kwargs: kwarg pairs of {'name of parameter': (x, y)}
	:return:
	"""
	from matplotlib import pyplot as plt

	color_set = (c for c in color_set)  # convert to an iterable to allow multiple sources to pull the next color

	f1 = plt.figure()
	ax = f1.gca()

	if limits:
		ax.set_xlim(right=limits.get('right'))
		ax.set_xlim(left=limits.get('left'))
		ax.set_ylim(top=limits.get('top'))
		ax.set_ylim(bottom=limits.get('bottom'))

	if major_ticks:
		ax.set_xticks(major_ticks, minor=False)
	if minor_ticks:
		ax.set_xticks(minor_ticks, minor=True)

	legend_keys = [key for key in kwargs]

	for name, (x, y) in kwargs.items():
		ax.plot(x, y, color=next(color_set))

	if vertical_annotations:
		for line in vertical_annotations:
			ax.axvline(line[1], color=next(color_set))  # plot line across the axis
			legend_keys.append(line[0])  # add name to legend

	if horizontal_annotations:
		for line in horizontal_annotations:
			ax.axhline(line[1], color=next(color_set))  # plot line across the axis
			legend_keys.append(line[0])  # add name to legend

	[i.set_linewidth(2) for i in ax.spines.values()]
	ax.tick_params(axis='both', which='major', size=8, width=2, labelsize=15)
	f1.set_size_inches(8, 4.5)  # same as 16:9, ie widescreen

	ax.set_ylabel(y_label_str, fontsize=20)
	ax.set_xlabel(x_label_str, fontsize=20)
	ax.set_title(title)
	ax.legend(legend_keys)

	f1.subplots_adjust(bottom=.20)
	f1.savefig(filepath, dpi=150)
	plt.close(f1)


def plotyy(title, filepath: Path, limits_y1=None, limits_y2=None, minor_ticks=None, major_ticks=None,
		 x_label_str='Seconds', y1_label_str='Temperature (\xb0C)', y2_label_str='Temperature (\xb0C)',
		 vertical_annotations=(), horizontal_annotations_y1=(), horizontal_annotations_y2=(),
		 color_set_y1 = ('#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf'),
		 color_set_y2 = ('#66c2a5','#fc8d62','#8da0cb','#e78ac3','#a6d854','#ffd92f','#e5c494','#b3b3b3'),
		 **kwargs):
	"""
	Plots x, y coordinates with a single y-axis as a line graph with optional axis labels, tick control and a default
	color scheme.

	:param str title: title to be displayed on the plot
	:param Path filepath: pathlib Path where file will be saved, can relative to dir function is called in, or absolute
	:param dict limits: optional dictionary of limits including ['top','bottom','right','left']
	:param list minor_ticks: list of values along x-axis at which to place minor ticks
	:param list major_ticks: list of values along x-axis at which to place major ticks
	:param str x_label_str: label to be placed below x-axis
	:param str y_label_str: label to be placed below y-axis
	:param tuple vertical_annotations: any vertical lines to be plotted in the form (('name', x), ...)
	:param tuple horizontal_annotations: any horizontal lines to be plotted in the form (('name', y), ...)
	:param generator color_set: generator containing valid matplotlib colors;
		default scheme courtesy of Color Brewer (http://colorbrewer2.org/#type=qualitative&scheme=Dark2&n=8)
	:param kwargs: kwarg pairs of {'name of parameter': (x, y, axis: int)}
	:return:
	"""
	from matplotlib import pyplot as plt

	color_set_y1 = (c for c in color_set_y1)  # convert to a generator to allow multiple sources to pull the next color
	color_set_y2 = (c for c in color_set_y2)

	f1 = plt.figure()
	ax1 = f1.gca()
	ax2 = ax1.twinx()

	for limits, axis in zip((limits_y1, limits_y2), (ax1, ax2)):  # apply limits to axes separately
		if limits:
			axis.set_xlim(right=limits.get('right'))
			axis.set_xlim(left=limits.get('left'))
			axis.set_ylim(top=limits.get('top'))
			axis.set_ylim(bottom=limits.get('bottom'))

	if major_ticks:
		ax1.set_xticks(major_ticks, minor=False)
	if minor_ticks:
		ax1.set_xticks(minor_ticks, minor=True)

	legend_keys_ax1 = []
	legend_keys_ax2 = []

	for name, (x, y, axis) in kwargs.items():
		if axis is 1:
			ax1.plot(x, y, color=next(color_set_y1))
			legend_keys_ax1.append(name)

		if axis is 2:
			ax2.plot(x, y, color=next(color_set_y2))
			legend_keys_ax2.append(name)

	if vertical_annotations:
		for line in vertical_annotations:
			ax1.axvline(line[1], color=next(color_set_y1))  # plot line across the axis
			legend_keys_ax1.append(line[0])  # add name to legend

	if horizontal_annotations_y1:
		for line in horizontal_annotations_y1:
			ax1.axhline(line[1], color=next(color_set_y1))  # plot line across the axis
			legend_keys_ax1.append(line[0])  # add name to legend

	if horizontal_annotations_y2:
		for line in horizontal_annotations_y2:
			ax2.axhline(line[1], color=next(color_set_y2))  # plot line across the axis
			legend_keys_ax2.append(line[0])  # add name to legend

	ax1.tick_params(axis='both', which='major', size=8, width=2, labelsize=15)
	ax2.tick_params(axis='both', which='major', size=8, width=2, labelsize=15)

	[i.set_linewidth(2) for i in ax1.spines.values()]

	f1.set_size_inches(8, 5)  # same as 16:9, ie widescreen

	ax1.set_ylabel(y1_label_str, fontsize=15)
	ax2.set_ylabel(y2_label_str, fontsize=15)

	ax1.set_xlabel(x_label_str, fontsize=15)
	ax1.set_title(title, fontsize=20)

	ax1.legend(legend_keys_ax1, loc='lower left')
	ax2.legend(legend_keys_ax2, loc='upper right')

	ax1.set_zorder(-1)

	f1.subplots_adjust(bottom=.20)
	plt.tight_layout()
	f1.savefig(filepath, dpi=150)
	plt.close(f1)


def plot_gpu_and_cpu(path: Path):
	pass


if __name__ == '__main__':
	from math import ceil

	from parse_files_to_json import load_from_json

	all_measurements = load_from_json(Path('/home/brendan/FanTest/analysis/json/2019_10_12_13_17_run_log.json'))

	data_pairs = [
		(m.get('date'), m.get('GPU'), m.get('GPU Fan'), m.get('CPU-0'),
		 m.get('CPU-1'), m.get('CPU-2'), m.get('CPU-3'), m.get('CPU-4'), m.get('CPU-5'))
		for m in all_measurements if m.get('date')]

	dates = [d[0] for d in data_pairs]
	GPU_temps = [d[1] for d in data_pairs]
	GPU_fan = [d[2] for d in data_pairs]
	CPU0 = [d[3] for d in data_pairs]
	CPU1 = [d[4] for d in data_pairs]
	CPU2 = [d[5] for d in data_pairs]
	CPU3 = [d[6] for d in data_pairs]
	CPU4 = [d[7] for d in data_pairs]
	CPU5 = [d[8] for d in data_pairs]

	seconds = [(d - dates[0]).total_seconds() for d in dates]

	right_lim = ceil(seconds[-1] / 200) * 200  # hacky right limit by rounding to nearest >= 200s

	plot('GPU Over Time', Path('/home/brendan/FanTest/analysis/plots/gpu.png'),
		 limits={'top': 90, 'bottom': 25, 'left': 0, 'right': right_lim},
		 vertical_annotations=(('Stressing Stopped', 600),),
		 **{'GPU': (seconds, GPU_temps)})

	plot('CPU Over Time', Path('/home/brendan/FanTest/analysis/plots/cpu.png'),
		 limits={'top': 90, 'bottom': 25, 'left': 0, 'right': right_lim},
		 vertical_annotations=(('Stressing Stopped', 600),),
		 **{
			 'CPU 0': (seconds, CPU0),
			 'CPU 1': (seconds, CPU1),
			 'CPU 2': (seconds, CPU2),
			 'CPU 3': (seconds, CPU3),
			 'CPU 4': (seconds, CPU4),
			 'CPU 5': (seconds, CPU5),
		 })

	plotyy('GPU Temperature and Fan Speed', Path('/home/brendan/FanTest/analysis/plots/gpu_YY.png'),
		   limits_y1={'top': 90, 'bottom': 25, 'left': 0, 'right': right_lim},
		   y2_label_str= 'Rotations Per Minute (RPM)',
		   vertical_annotations=(('Stressing Stopped', 600),),
		   **{'GPU': (seconds, GPU_temps, 1),
			  'GPU Fan': (seconds, GPU_fan, 2)})


