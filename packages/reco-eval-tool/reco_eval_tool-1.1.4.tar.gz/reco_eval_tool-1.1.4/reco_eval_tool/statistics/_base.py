import os
import pandas as pd
import numpy as np
from ..visualization import *
from ..path import *
from ..utils import *
from ..metrics import *

COUNT = 'Count'
RATIO = 'Ratio'
SHIFT = 'Shift'
GROUP_TOTAL = 'group_total'
GROUP_RATIO = 'group_ratio'
TOTAL_RATIO = 'total_ratio'
COLUMN1_COLUMN2 = 'column1_column2'

def single_feature_analysis(df, column, drop_na=True, save_to_file=True, output_file_name=None):
	"""
	Analyze the single feature
	:param df: DataFrame
	:param column: column name
	:param drop_na: drop the rows with no value
	:param save_to_file: save the result to files
	:param output_file_name: the name of the file to save the result
	:return: analysis
	"""
	default_output_file_name = f'{column}_distribution'

	if drop_na:
		df = drop_na_raw(df, [column])

	feature_analysis = df.groupby(column)[column].value_counts().reset_index(name=COUNT)
	total_count = feature_analysis[COUNT].sum()
	feature_analysis[RATIO] = feature_analysis[COUNT] / total_count

	bar_plot(data=feature_analysis, xlabel=column, ylabel=COUNT, title=f'Distribution of {column}', save_to_file=save_to_file, default_output_file_name=default_output_file_name, custom_output_file_name=output_file_name)
	pie_plot(data=feature_analysis, labels=feature_analysis[column], sizes=feature_analysis[COUNT], title=f'Distribution of {column}', save_to_file=save_to_file, default_output_file_name=default_output_file_name, custom_output_file_name=output_file_name)
	save_df_to_csv(feature_analysis, save_to_file, default_output_file_name=default_output_file_name, custom_output_file_name=output_file_name)
	return feature_analysis


def pivot_table(df, column1, column2, drop_na=True, save_to_file=True, output_file_name=None):
	"""
	Create a pivot table for two columns
	:param df: DataFrame
	:param column1: column name
	:param column2: column name
	:param drop_na: drop the rows with no value
	:param save_to_file: save the result to files
	:param output_file_name: the name of the file to save the result
	:return: analysis
	"""
	default_output_file_name = f'{column1}_{column2}_pivot_table'
	count_default_output_file_name = f'{column1}_{column2}_pivot_table_count'
	group_ratio_default_output_file_name = f'{column1}_{column2}_pivot_table_group_ratio'
	count_custom_output_file_name = None if not output_file_name else output_file_name + "_pivot_table_count"
	group_ratio_custom_output_file_name = None if not output_file_name else output_file_name + "_pivot_table_group_ratio"
	
	if drop_na:
		df = drop_na_raw(df, [column1, column2])

	pivot_analysis = df.groupby([column1, column2]).size().reset_index(name=COUNT)
	pivot_analysis = pivot_analysis.sort_values(by=COUNT, ascending=False)
	total_count = pivot_analysis[COUNT].sum()
	pivot_analysis[TOTAL_RATIO] = pivot_analysis[COUNT] / total_count

	column1_df = pivot_analysis.groupby([column1])[COUNT].sum().reset_index()
	column1_df = column1_df.rename(columns={COUNT: GROUP_TOTAL})
	pivot_analysis = pd.merge(pivot_analysis, column1_df, on=column1, how='left')
	pivot_analysis[GROUP_RATIO] = pivot_analysis[COUNT] / pivot_analysis[GROUP_TOTAL]

	group_pivot_analysis = pivot_analysis.copy()
	group_pivot_analysis[COLUMN1_COLUMN2] = group_pivot_analysis[column1].astype(str) + "&" + group_pivot_analysis[column2].astype(str)

	pivot_bar_plot(data=pivot_analysis, index=column1, columns=column2, values=COUNT, title=f'Count of {column1} and {column2}', save_to_file=save_to_file, default_output_file_name=count_default_output_file_name, custom_output_file_name=count_custom_output_file_name)
	pivot_bar_plot(data=pivot_analysis, index=column1, columns=column2, values=GROUP_RATIO, title=f'Group Ratio  {column2}', save_to_file=save_to_file, default_output_file_name=group_ratio_default_output_file_name, custom_output_file_name=group_ratio_custom_output_file_name)
	pie_plot(data=group_pivot_analysis, labels=group_pivot_analysis[COLUMN1_COLUMN2], sizes=group_pivot_analysis[COUNT], title=f'Total Ratio of {column1} + {column2}', save_to_file=save_to_file, default_output_file_name=default_output_file_name, custom_output_file_name=output_file_name)
	save_df_to_csv(pivot_analysis, save_to_file, default_output_file_name=default_output_file_name, custom_output_file_name=output_file_name)
	return pivot_analysis


def feature_shift_analysis(df, column1, column2, gen_pivot_table=True, drop_na=True, save_to_file=True, output_file_name=None):
	"""
	Analyze the shift of two columns
	:param df: DataFrame
	:param column1: column name
	:param column2: column name
	:param gen_pivot_table: generate pivot table
	:param drop_na: drop the rows with no value
	:param save_to_file: save the result to files
	:param output_file_name: the name of the file to save the result
	:return: analysis
	"""
	default_output_file_name = f'{column1}_{column2}_shift'
	if gen_pivot_table:
		pivot_table(df, column1, column2, drop_na, save_to_file, output_file_name)

	if drop_na:
		df = drop_na_raw(df, [column1, column2])

	df[SHIFT] = df[column1] != df[column2]
	overall_shift = df[SHIFT].value_counts().reset_index(name=COUNT)
	overall_shift[RATIO] = overall_shift[COUNT] / overall_shift[COUNT].sum()

	pie_plot(data=overall_shift, labels=overall_shift[SHIFT], sizes=overall_shift[COUNT], title=f'Shift of {column1} and {column2}', save_to_file=save_to_file, default_output_file_name=default_output_file_name, custom_output_file_name=output_file_name)
	save_df_to_csv(overall_shift, save_to_file, default_output_file_name=default_output_file_name, custom_output_file_name=output_file_name)
	return overall_shift


def feature_correlation_coefficient(df, column, drop_na=True, save_to_file=True, output_file_name=None):
	"""
	Calculate the correlation coefficient of the column with other columns
	:param df: DataFrame
	:param column: column name
	:param drop_na: drop the rows with no value
	:param save_to_file: save the result to files
	:param output_file_name: the name of the file to save the result
	:return: correlation coefficient
	"""
	default_output_file_name = f'{column}_correlation_coefficient'
	if drop_na:
		df = drop_na_raw(df, [column])
	
	# filter the columns with numeric values
	df = df.select_dtypes(include=[np.number])

	correlation_coefficient = df.corr()[column].reset_index()
	correlation_coefficient = correlation_coefficient.rename(columns={column: 'correlation_coefficient'})
	correlation_coefficient = correlation_coefficient.sort_values(by='correlation_coefficient', ascending=False)
	save_df_to_csv(correlation_coefficient, save_to_file, default_output_file_name=default_output_file_name, custom_output_file_name=output_file_name)
	return correlation_coefficient


def threshold_selection(df, ground_truth_column, predict_column, need_sigmoid=True, threshold_list=None,  line_chart_metrics=None, save_to_file=True, output_file_name=None):
	"""
	Analyze the threshold of the prediction
	:param df: DataFrame
	:param ground_truth_column: ground truth column
	:param predict_column: predict column
	:param need_sigmoid: whether need sigmoid
	:param threshold_list: threshold list, the default value is np.linspace(0, 1, 21)
	:param line_chart_metrics: line chart metrics, the default value is ['recall', 'precision', 'f1', 'FPR']
	:param save_to_file: save the result to files
	:param output_file_name: the name of the file to save the result
	"""
	default_output_file_name = f'{ground_truth_column}_{predict_column}_threshold_selection'
	optimum_thresholds_default_output_file_name = f'{default_output_file_name}_optimum_thresholds'
	optimum_thresholds_output_file_name = None if not output_file_name else output_file_name + "_optimum_thresholds" 

	# check the value of ground_truth_column are in [0, 1], predict_column are float
	assert set(df[ground_truth_column].unique()) == {0, 1}, f"The value of {ground_truth_column} should be in [0, 1]"
	assert df[predict_column].dtype == float, f"The value of {predict_column} should be float"
	if need_sigmoid:
		df[predict_column] = df[predict_column].apply(lambda x: np.exp(x) / (1 + np.exp(x)))
		print(f">>>> IMPORTANT!!!! The sigmoid function is applied to {predict_column}")

	df = drop_na_raw(df, [ground_truth_column, predict_column])

	if threshold_list is None:
		threshold_list = np.linspace(0, 1, 21)
		print(f">>>> The default threshold list is {threshold_list}")
	threshold_list = [round(threshold, 2) for threshold in threshold_list]

	df = df[[ground_truth_column, predict_column]]
	merge_df = []
	for threshold in threshold_list:
		tmp_df = df.copy()
		tmp_df['threshold'] = threshold
		tmp_df[predict_column] = df[predict_column] > threshold
		merge_df.append(tmp_df)
	merge_df = pd.concat(merge_df)
	prf_df = calculate_prf(merge_df, ground_truth_column, predict_column, breakdown_column='threshold', save_to_file=save_to_file, output_file_name=output_file_name)
	
	print(f">>>> line chart metrics should be in {prf_df.columns}")
	if line_chart_metrics is None:
		line_chart_metrics = ['recall', 'precision', 'f1', 'FPR']
		print(f">>>> The default line chart metrics are {line_chart_metrics}")

	line_chart(prf_df, 'threshold', line_chart_metrics, title=f'{",".join(line_chart_metrics)} vs {predict_column} Threshold', x_label="threshold", y_lable="value",  save_to_file=save_to_file, default_output_file_name=default_output_file_name, custom_output_file_name=output_file_name)
	
	optimum_thresholds = {"Metrics": [], "Metrics_Value": [], "Threshold": []}
	for metric in line_chart_metrics:
		optimum_thresholds["Metrics"].append(metric)
		optimum_thresholds["Metrics_Value"].append(prf_df[metric].max())
		optimum_thresholds["Threshold"].append(prf_df[prf_df[metric] == prf_df[metric].max()]['threshold'].values[0])
	optimum_thresholds = pd.DataFrame(optimum_thresholds)

	save_df_to_csv(optimum_thresholds, save_to_file, default_output_file_name=optimum_thresholds_default_output_file_name, custom_output_file_name=optimum_thresholds_output_file_name)
	return prf_df







	
