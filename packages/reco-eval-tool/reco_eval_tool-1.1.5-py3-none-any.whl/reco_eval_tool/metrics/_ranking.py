import pandas as pd
from sklearn.metrics import roc_auc_score, roc_curve
from ..utils import *
from ..path import *
from ..visualization import line_chart

GroundTruth = 'GroundTruth'
Predict = 'Predict'
DEFAULT_OUTPUT_FILE_NAME = 'ranking'


def calculate_auc(df, ground_truth_colunms, predict_columns, save_to_file=True, drop_na=True, output_file_name=None):
	"""
	Calculate the auc and draw the roc curve
	:param df: input dataframe
	:param ground_truth_colunms: ground truth columns
	:param predict_columns: predict columns
	:param drop_na: drop the rows with missing values in the ground_truth_colunms and predict_columns
	:param save_to_file: save the result to a csv file
	:param output_file_name: the name of the file to save the result
	:return: a dataframe with precision, recall, F1 of the prediction
	"""
	merged_auc = {}
	merged_roc_df = []
	fpr_columns = []
	tpr_columns = []
	# check the type of ground_truth_colunms and predict_columns if they are not list, convert them to list
	if not isinstance(ground_truth_colunms, list):
		ground_truth_colunms = [ground_truth_colunms]
	if not isinstance(predict_columns, list):
		predict_columns = [predict_columns]

	# check the length of ground_truth_colunms and predict_columns are the same
	assert len(ground_truth_colunms) == len(predict_columns), "The length of ground_truth_colunms and predict_columns should be the same"
	for i in range(len(ground_truth_colunms)):
		auc, roc_df = calculate_auc_single(df, ground_truth_colunms[i], predict_columns[i], drop_na=drop_na)
		merged_auc[f'{ground_truth_colunms[i]}_{predict_columns[i]}'] = auc
		merged_roc_df.append(roc_df)
		fpr_columns.append(f'{predict_columns[i]}_fpr')
		tpr_columns.append(f'{predict_columns[i]}_tpr')
	roc_df = merged_roc_df[0]
	for i in range(1, len(merged_roc_df)):
		roc_df = pd.merge(roc_df, merged_roc_df[i], on='thresholds', how='outer')
	roc_df = roc_df.reset_index(drop=True)
	# put thresholds column to the first column
	roc_df = roc_df[['thresholds'] + fpr_columns + tpr_columns]
	save_df_to_csv(roc_df, save_to_file, default_output_file_name=DEFAULT_OUTPUT_FILE_NAME, custom_output_file_name=output_file_name)
	merged_auc = pd.DataFrame(merged_auc, index=[0])
	save_df_to_csv(merged_auc, save_to_file, default_output_file_name=DEFAULT_OUTPUT_FILE_NAME, custom_output_file_name=output_file_name)
	line_chart(roc_df, fpr_columns, tpr_columns, title="ROC", labels=predict_columns, x_label="False positive ratio", y_label="True positive ratio", save_to_file=save_to_file, default_output_file_name=DEFAULT_OUTPUT_FILE_NAME, custom_output_file_name=output_file_name)
	return merged_auc, roc_df


def calculate_auc_single(df, ground_truth_colunm, predict_column, drop_na):
	"""
	Calculate the precision, recall, F1 of the prediction for a single group
	:param df: input dataframe
	:param ground_truth_colunm: ground truth column
	:param predict_column: predict column
	:param weight_column: weight for the calculation
	"""
	if drop_na:
		df = drop_na_raw(df, [ground_truth_colunm, predict_column])

	ground_truth = df[ground_truth_colunm].values.tolist()
	predict = df[predict_column].values.tolist()
	
	# calculate the auc
	auc = roc_auc_score(ground_truth, predict)
	fpr, tpr, thresholds = roc_curve(ground_truth, predict)
	roc_df = pd.DataFrame({f'{predict_column}_fpr': fpr, f'{predict_column}_tpr': tpr, 'thresholds': thresholds})
	return auc, roc_df


