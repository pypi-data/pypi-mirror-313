import time
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from ..path import *

def bar_plot(data, xlabel=None, ylabel=None, title=None, save_to_file=True, default_output_file_name=None, custom_output_file_name=None):
	"""Plot a bar plot."""
	if not save_to_file:
		return
	plt.clf()
	path = get_output_dir()
	if custom_output_file_name:
		path += f'/{custom_output_file_name}_bar_chart.png' 
	else:
		path += f'/{default_output_file_name}_bar_chart_{time.strftime("%Y%m%d%H%M%S")}.png'

	ax = sns.barplot(x=xlabel, y=ylabel, data=data)
	for p in ax.patches:
		p.set_height(p.get_height())
		ax.text(p.get_x() + p.get_width() / 2., p.get_height(), '%d' % int(p.get_height()), ha='center', va='bottom')
	plt.title(title)
	plt.savefig(path)
	print(f">>>> Plot saved at {path}")


def pie_plot(data, labels=None, sizes=None, title=None, save_to_file=True, default_output_file_name=None, custom_output_file_name=None):
	"""Plot a pie plot."""
	if not save_to_file:
		return
	plt.clf()
	path = get_output_dir()
	if custom_output_file_name:
		path += f'/{custom_output_file_name}_pie_chart.png'
	else:
		path += f'/{default_output_file_name}_pie_chart_{time.strftime("%Y%m%d%H%M%S")}.png'

	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
	ax1.axis('equal')
	plt.title(title)
	plt.savefig(path)
	print(f">>>> Plot saved at {path}")


def line_chart(data, x=None, y=None, title=None, labels=None, x_label=None, y_label=None, save_to_file=True, default_output_file_name=None, custom_output_file_name=None, if_clf=True):
	"""Plot a line chart."""
	if not save_to_file:
		return
	if if_clf:
		plt.clf()
	path = get_output_dir()
	if custom_output_file_name:
		path += f'/{custom_output_file_name}_line_chart.png'
	else:
		path += f'/{default_output_file_name}_line_chart_{time.strftime("%Y%m%d%H%M%S")}.png'

	# draw line chart for recall and precision
	if not isinstance(x, list):
		x = [x]
	if not isinstance(y, list):
		y = [y]
	if len(x) < len(y):
		if len(x) == 1:
			x = x * len(y)
	if labels is None:
		labels = y
	for x_, y_, label in zip(x, y, labels):
		plt.plot(data[x_], data[y_], label=label)
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	plt.title(title)
	plt.legend()
	plt.savefig(path)
	print(f">>>> Plot saved at {path}")


def pivot_bar_plot(data, index=None, columns=None, values=None, title=None, save_to_file=True, default_output_file_name=None, custom_output_file_name=None):
	"""Plot a bar plot."""
	if not save_to_file:
		return
	plt.clf()
	path = get_output_dir()
	if custom_output_file_name:
		path += f'/{custom_output_file_name}_pivot_bar_chart.png'
	else:
		path += f'/{default_output_file_name}_pivot_bar_chart_{time.strftime("%Y%m%d%H%M%S")}.png'

	data = data.pivot(index=index, columns=columns, values=values)
	ax = data.plot(kind='bar', stacked=False)
	for p in ax.patches:
		p.set_height(p.get_height())
		if 'ratio' in values.lower():
			ax.text(p.get_x() + p.get_width() / 2., p.get_height(), '%d%%' % int(p.get_height() * 100), ha='center', va='bottom')
		else:
			ax.text(p.get_x() + p.get_width() / 2., p.get_height(), '%d' % int(p.get_height()), ha='center', va='bottom')
	plt.title(title)
	plt.savefig(path)
	print(f">>>> Plot saved at {path}")



if __name__ == '__main__':
	import pandas as pd
	# data = {'Market': ['en_us', 'en_us', 'zh_cn'], 'Prediction': [0, 1, 0], 'Count': [1, 1, 2]}
	# df = pd.DataFrame(data)
	# # single_bar_plot(df, 'Prediction', 'Count', 'Distribution of Prediction', 'Prediction_distribution.png')
	# pivot_bar_plot(df, 'Market', 'Prediction', 'Distribution of Prediction', 'Prediction_distribution.png')


	data = {'threshold': [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], 
		 'recall': [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0], 
		 'precision': [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]}
	df = pd.DataFrame(data)

	# draw line chart for recall and precision
	line_chart(df, 'threshold', ['recall', 'precision'], 'Recall and Precision', 'Recall_Precision.png')