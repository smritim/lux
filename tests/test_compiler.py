from .context import lux
import pytest
import pandas as pd
def test_underspecifiedSingleVis():
	df = pd.read_csv("lux/data/car.csv")
	df.setContext([lux.Spec(attribute = "MilesPerGal"),lux.Spec(attribute = "Weight")])
	assert len(df.viewCollection)==1
	assert df.viewCollection[0].mark == "scatter"
	for attr in df.viewCollection[0].specLst: assert attr.dataModel=="measure"
	for attr in df.viewCollection[0].specLst: assert attr.dataType=="quantitative"

def test_underspecifiedVisCollection():
	df = pd.read_csv("lux/data/car.csv")
	df["Year"] = pd.to_datetime(df["Year"], format='%Y') # change pandas dtype for the column "Year" to datetype
	df.setContext([lux.Spec(attribute = ["Horsepower","Weight","Acceleration"]),lux.Spec(attribute = "Year")])
	assert len(df.viewCollection)==3
	assert df.viewCollection[0].mark == "line" 
	for vc in df.viewCollection: 
		assert (vc.getObjFromChannel("x")[0].attribute == "Year")
	df.setContext([lux.Spec(attribute = "?"),lux.Spec(attribute = "Year")])
	assert len(df.viewCollection) == len(df.columns)
	for vc in df.viewCollection: 
		assert (vc.getObjFromChannel("x")[0].attribute == "Year")
	df.setContext([lux.Spec(attribute = "?",dataType="quantitative"),lux.Spec(attribute = "Year")])
	assert len(df.viewCollection) == len([view.getObjByDataType("quantitative") for view in df.viewCollection]) # should be 5

	df.setContext([lux.Spec(attribute = "?", dataModel="measure"),lux.Spec(attribute="MilesPerGal",channel="y")])
	for vc in df.viewCollection: 
		print (vc.getObjFromChannel("y")[0].attribute == "MilesPerGal")
	
	df.setContext([lux.Spec(attribute = "?", dataModel="measure"),lux.Spec(attribute = "?", dataModel="measure")])
	assert len(df.viewCollection) == len([view.getObjByDataModel("measure") for view in df.viewCollection]) #should be 25 
def test_parse():
	df = pd.read_csv("lux/data/car.csv")
	df.setContext([lux.Spec("Origin=?"),lux.Spec(attribute = "MilesPerGal")])
	assert len(df.viewCollection)==3

	df = pd.read_csv("lux/data/car.csv")
	df.setContext([lux.Spec("Origin=?"),lux.Spec("MilesPerGal")])
	assert len(df.viewCollection)==3
def test_underspecifiedVisCollection_Zval():
	# check if the number of charts is correct
	df = pd.read_csv("lux/data/car.csv")
	df.setContext([lux.Spec(attribute = "Origin", filterOp="=",value="?"),lux.Spec(attribute = "MilesPerGal")])
	assert len(df.viewCollection)==3


# 	dobj = lux.DataObj(dataset,[lux.Column("Horsepower"),lux.Column("Brand"),lux.Row("Origin",["Japan","USA"])])
# 	assert type(dobj.compiled).__name__ == "DataObjCollection"
# 	assert len(dobj.compiled.collection) == 2

# 	dobj = lux.DataObj(dataset,[lux.Column(["Horsepower","Weight"]),lux.Column("Brand"),lux.Row("Origin",["Japan","USA"])])
# 	assert len(dobj.compiled.collection) == 4

# 	# test ? command
# 	dobj = lux.DataObj(dataset,[lux.Column(["Horsepower","Weight"]),lux.Column("Brand"),lux.Row("Origin","?")])
# 	assert len(dobj.compiled.collection) == 6

# 	# test if z axis has been filtered correctly
# 	dobj = lux.DataObj(dataset,[lux.Column(["Horsepower","Weight"]),lux.Column("Brand"),lux.Row("Origin",["Japan","USA"])])
# 	chartTitles = list(dobj.compiled.get("title"))
# 	assert "Origin=USA" and "Origin=Japan" in chartTitles
# 	assert "Origin=Europe" not in chartTitles

# 	# test number of data points makes sense
# 	dobj = lux.DataObj(dataset,[lux.Column(["Horsepower"]),lux.Column("Brand"),lux.Row("Origin","?")])
# 	def getNumDataPoints(dObj):
# 		numRows = getattr(dObj, "dataset").df.shape[0]
# 		# Might want to write catch error if key not in field
# 		return numRows
# 	totalNumRows= sum(list(dobj.compiled.map(getNumDataPoints)))
# 	assert totalNumRows == 392

# def test_underspecifiedVisCollection_Zattr():
# 	dataset = lux.Dataset("lux/data/cars.csv",schema=[{"Year":{"dataType":"date"}}])
# 	dobj = lux.DataObj(dataset,[lux.Column(["Horsepower"]),lux.Column("Weight"),lux.Row(["Origin","Cylinders"],"?")])
# 	assert len(dobj.compiled.collection) == 8 

# def test_specifiedChannelEnforcedVisCollection():
# 	dataset = lux.Dataset("lux/data/cars.csv",schema=[{"Year":{"dataType":"date"}}])
# 	dobj = lux.DataObj(dataset,[lux.Column("?",dataModel="measure"),lux.Column("MilesPerGal",channel="x")])
# 	for di in dobj.compiled.collection:
# 		assert di.getByColumnName("MilesPerGal")[0].channel == "x"
# def test_autoencodingScatter():
# 	# No channel specified
# 	dataset = lux.Dataset("lux/data/cars.csv",schema=[{"Year":{"dataType":"date"}}])
# 	dobj = lux.DataObj(dataset,[lux.Column("MilesPerGal"),lux.Column("Weight")])
# 	assert dobj.compiled.getByColumnName("MilesPerGal")[0].channel == "x"
# 	assert dobj.compiled.getByColumnName("Weight")[0].channel == "y"
# 	# Partial channel specified
# 	dobj = lux.DataObj(dataset,[lux.Column("MilesPerGal", channel="y"),lux.Column("Weight")])
# 	assert dobj.compiled.getByColumnName("MilesPerGal")[0].channel == "y"
# 	assert dobj.compiled.getByColumnName("Weight")[0].channel == "x"

# 	# Full channel specified
# 	dobj = lux.DataObj(dataset,[lux.Column("MilesPerGal", channel="y"),lux.Column("Weight", channel="x")])
# 	assert dobj.compiled.getByColumnName("MilesPerGal")[0].channel == "y"
# 	assert dobj.compiled.getByColumnName("Weight")[0].channel == "x"
# 	# Duplicate channel specified
# 	with pytest.raises(ValueError):
# 		# Should throw error because there should not be columns with the same channel specified
# 		dobj = lux.DataObj(dataset,[lux.Column("MilesPerGal", channel="x"),lux.Column("Weight", channel="x")])

	
# def test_autoencodingHistogram():
# 	dataset = lux.Dataset("lux/data/cars.csv",schema=[{"Year":{"dataType":"date"}}])
	
# 	# Partial channel specified
# 	dobj = lux.DataObj(dataset,[lux.Column("MilesPerGal",channel="y")])
# 	assert dobj.compiled.getByColumnName("MilesPerGal")[0].channel == "y"

# 	dobj = lux.DataObj(dataset,[lux.Column("MilesPerGal", channel="x")])
# 	assert dobj.compiled.getByColumnName("MilesPerGal")[0].channel == "x"
# 	assert dobj.compiled.getByColumnName("count()")[0].channel == "y"

# def test_autoencodingLineChart():
# 	dataset = lux.Dataset("lux/data/cars.csv",schema=[{"Year":{"dataType":"date"}}])
# 	dobj = lux.DataObj(dataset,[lux.Column("Year"),lux.Column("Acceleration")])
# 	checkAttributeOnChannel(dobj,"Year","x")
# 	checkAttributeOnChannel(dobj,"Acceleration","y")
# 	# Partial channel specified
# 	dobj = lux.DataObj(dataset,[lux.Column("Year", channel="y"),lux.Column("Acceleration")])
# 	checkAttributeOnChannel(dobj,"Year","y")
# 	checkAttributeOnChannel(dobj,"Acceleration","x")

# 	# Full channel specified
# 	dobj = lux.DataObj(dataset,[lux.Column("Year", channel="y"),lux.Column("Acceleration", channel="x")])
# 	checkAttributeOnChannel(dobj,"Year","y")
# 	checkAttributeOnChannel(dobj,"Acceleration","x")
# 	# Duplicate channel specified
# 	with pytest.raises(ValueError):
# 		# Should throw error because there should not be columns with the same channel specified
# 		dobj = lux.DataObj(dataset,[lux.Column("Year", channel="x"),lux.Column("Acceleration", channel="x")])

# def test_autoencodingColorLineChart():
# 	dataset = lux.Dataset("lux/data/cars.csv",schema=[{"Year":{"dataType":"date"}}])
# 	dobj = lux.DataObj(dataset,[lux.Column("Year"),lux.Column("Acceleration"),lux.Column("Origin")])
# 	checkAttributeOnChannel(dobj,"Year","x")
# 	checkAttributeOnChannel(dobj,"Acceleration","y")
# 	checkAttributeOnChannel(dobj,"Origin","color")
# def test_autoencodingColorScatterChart():
# 	dataset = lux.Dataset("lux/data/cars.csv",schema=[{"Year":{"dataType":"date"}}])
# 	dobj = lux.DataObj(dataset,[lux.Column("Horsepower"),lux.Column("Acceleration"),lux.Column("Origin")])
# 	checkAttributeOnChannel(dobj,"Origin","color")
# 	dobj = lux.DataObj(dataset,[lux.Column("Horsepower"),lux.Column("Acceleration",channel="color"),lux.Column("Origin")])
# 	checkAttributeOnChannel(dobj,"Acceleration","color")
# def test_populateOptions():
# 	from lux.compiler.Compiler import Compiler
# 	dataset = lux.Dataset("lux/data/cars.csv",schema=[{"Year":{"dataType":"date"}}])
# 	dobj = lux.DataObj(dataset,[lux.Column("?"),lux.Column("MilesPerGal")])
# 	colLst = list(map(lambda x: x.columnName, Compiler.populateOptions(dobj, dobj.spec[0])))
# 	assert listEqual(colLst, list(dobj.dataset.df.columns))
# 	dobj = lux.DataObj(dataset,[lux.Column("?",dataModel="measure"),lux.Column("MilesPerGal")])
# 	colLst = list(map(lambda x: x.columnName, Compiler.populateOptions(dobj, dobj.spec[0])))
# 	assert listEqual(colLst,['Acceleration','Weight','Horsepower','MilesPerGal','Displacement'])

# def listEqual(l1,l2):
#     l1.sort()
#     l2.sort()
#     return l1==l2
# def checkAttributeOnChannel(dobj,attrName,channelName):
# 	assert dobj.compiled.getByColumnName(attrName)[0].channel == channelName
