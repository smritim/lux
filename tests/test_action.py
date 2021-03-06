from .context import lux
import pytest
import pandas as pd

from lux.vis.Vis import Vis
def test_vary_filter_val():
	df = pd.read_csv("lux/data/olympic.csv")
	vis = Vis(["Height","SportType=Ball"],df)
	df.set_intent_as_vis(vis)
	df._repr_html_()
	assert len(df.recommendation["Filter"]) == len(df["SportType"].unique())-1

def test_generalize_action():
	#test that generalize action creates all unique visualizations
	df = pd.read_csv("lux/data/car.csv")
	df["Year"] = pd.to_datetime(df["Year"], format='%Y') # change pandas dtype for the column "Year" to datetype
	df.set_intent(["Acceleration", "MilesPerGal", "Cylinders", "Origin=USA"])
	df.show_more()
	assert(len(df.recommendation['Generalize']) == 4)
	v1 = df.recommendation['Generalize'][0]
	v2 = df.recommendation['Generalize'][1]
	v3 = df.recommendation['Generalize'][2]
	v4 = df.recommendation['Generalize'][3]

	for clause in v4._inferred_intent: 
		assert clause.value==""  #No filter value
	assert v4.title =='Overall'
  
	check1 = v1 != v2 and v1 != v3 and v1 != v4
	check2 = v2 != v3 and v2 != v4
	check3 = v3 != v4
	assert(check1 and check2 and check3)

def test_row_column_group():
	df = pd.read_csv("lux/data/state_timeseries.csv")
	df["Date"] = pd.to_datetime(df["Date"])
	tseries = df.pivot(index="State",columns="Date",values="Value")
	# Interpolating missing values
	tseries[tseries.columns.min()] = tseries[tseries.columns.min()].fillna(0)
	tseries[tseries.columns.max()] = tseries[tseries.columns.max()].fillna(tseries.max(axis=1))
	tseries = tseries.interpolate('zero',axis=1)
	tseries._repr_html_()
	assert list(tseries.recommendation.keys() ) == ['Row Groups','Column Groups']

def test_groupby():
	df = pd.read_csv("lux/data/college.csv")
	groupbyResult = df.groupby("Region").sum()
	groupbyResult._repr_html_()
	assert list(groupbyResult.recommendation.keys() ) == ['Column Groups']

def test_crosstab():
	# Example from http://www.datasciencemadesimple.com/cross-tab-cross-table-python-pandas/
	d = {
		'Name':['Alisa','Bobby','Cathrine','Alisa','Bobby','Cathrine',
				'Alisa','Bobby','Cathrine','Alisa','Bobby','Cathrine'],
		'Exam':['Semester 1','Semester 1','Semester 1','Semester 1','Semester 1','Semester 1',
				'Semester 2','Semester 2','Semester 2','Semester 2','Semester 2','Semester 2'],
		
		'Subject':['Mathematics','Mathematics','Mathematics','Science','Science','Science',
				'Mathematics','Mathematics','Mathematics','Science','Science','Science'],
	'Result':['Pass','Pass','Fail','Pass','Fail','Pass','Pass','Fail','Fail','Pass','Pass','Fail']}
	
	df = pd.DataFrame(d,columns=['Name','Exam','Subject','Result'])
	result = pd.crosstab([df.Exam],df.Result)
	result._repr_html_()
	assert list(result.recommendation.keys() ) == ['Row Groups','Column Groups']

def test_custom_aggregation():
	import numpy as np
	df = pd.read_csv("lux/data/college.csv")
	df.set_intent(["HighestDegree",lux.Clause("AverageCost",aggregation=np.ptp)])
	df._repr_html_()
	assert list(df.recommendation.keys()) ==['Enhance', 'Filter', 'Generalize']