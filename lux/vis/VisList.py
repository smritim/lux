from __future__ import annotations
from lux.vislib.altair.AltairRenderer import AltairRenderer
from lux.utils.utils import check_import_lux_widget
from typing import List, Union, Callable, Dict
from lux.vis.Vis import Vis
from lux.vis.Clause import Clause
import warnings
class VisList():
	'''
	VisList is a list of Vis objects. 
	'''
	def __init__(self,input_lst:Union[List[Vis],List[Clause]],source=None):
		# Overloaded Constructor
		self.source = source 
		self._input_lst = input_lst
		if len(input_lst)>0:
			if (self._is_vis_input()):
				self.collection = input_lst
				self.intent = []
			else:
				self.intent = input_lst
				self.collection = []
		else:
			self.collection = []
			self.intent = []
		self.widget = None
		if (source is not None): self.refresh_source(source)
	def set_intent(self, intent:List[Clause]) -> None:
		"""
		Sets the intent of the VisList and refresh the source based on the new clause

		Parameters
		----------
		intent : List[Clause]
			Query specifying the desired VisList
		"""		
		self.intent = intent
		self.refresh_source(self.source)
	def get_exported(self) -> VisList:
		"""
		Get selected visualizations as exported Vis List

		Notes
        -----
		Convert the _exportedVisIdxs dictionary into a programmable VisList
		Example _exportedVisIdxs : 
			{'Vis List': [0, 2]}
		
		Returns
		-------
		VisList
		 	return a VisList of selected visualizations. -> VisList(v1, v2...)
		"""        
		if not hasattr(self,"widget"):
			warnings.warn(
						"\nNo widget attached to the VisList."
						"Please assign VisList to an output variable.\n"
						"See more: https://lux-api.readthedocs.io/en/latest/source/guide/FAQ.html#troubleshooting-tips"
						, stacklevel=2)
			return []
		exported_vis_lst =self.widget._exportedVisIdxs
		if (exported_vis_lst=={}):
			warnings.warn(
				"\nNo visualization selected to export.\n"
				"See more: https://lux-api.readthedocs.io/en/latest/source/guide/FAQ.html#troubleshooting-tips"
				,stacklevel=2)
			return []
		else:
			exported_views = VisList(list(map(self.__getitem__, exported_vis_lst["Vis List"])))
			return exported_views
	def remove_duplicates(self) -> None:
		"""
		Removes duplicate visualizations in Vis List
		"""		
		self.collection = list(set(self.collection))
	def _is_vis_input(self):
		if (type(self._input_lst[0])==Vis):
			return True
		elif (type(self._input_lst[0])==Clause):
			return False
	def __getitem__(self, key):
		return self.collection[key]
	def __setitem__(self, key, value):
		self.collection[key] = value
	def __len__(self):
		return len(self.collection)
	def __repr__(self):
		if len(self.collection) == 0:
			return str(self._input_lst)
		x_channel = ""
		y_channel = ""
		largest_mark = 0
		largest_filter = 0
		for vis in self.collection: #finds longest x attribute among all visualizations
			filter_spec = None
			for clause in vis._inferred_intent:
				if clause.value != "":
					filter_spec = clause

				if (clause.aggregation != "" and clause.aggregation is not None):
					attribute = clause._aggregation_name.upper() + "(" + clause.attribute + ")"
				elif clause.bin_size > 0:
					attribute = "BIN(" + clause.attribute + ")"
				else:
					attribute = clause.attribute

				if clause.channel == "x" and len(x_channel) < len(attribute):
					x_channel = attribute
				if clause.channel == "y" and len(y_channel) < len(attribute):
					y_channel = attribute
			if len(vis.mark) > largest_mark:
				largest_mark = len(vis.mark)
			if filter_spec and len(str(filter_spec.value)) + len(filter_spec.attribute) > largest_filter:
				largest_filter = len(str(filter_spec.value)) + len(filter_spec.attribute) 
		vis_repr = []
		largest_x_length = len(x_channel)
		largest_y_length = len(y_channel)
		for vis in self.collection: #pads the shorter visualizations with spaces before the y attribute
			filter_spec = None
			x_channel = ""
			y_channel = ""
			additional_channels = []
			for clause in vis._inferred_intent:
				if clause.value != "":
					filter_spec = clause

				if (clause.aggregation != "" and clause.aggregation is not None and vis.mark!='scatter'):
					attribute = clause._aggregation_name.upper() + "(" + clause.attribute + ")"
				elif clause.bin_size > 0:
					attribute = "BIN(" + clause.attribute + ")"
				else:
					attribute = clause.attribute

				if clause.channel == "x":
					x_channel = attribute.ljust(largest_x_length)
				elif clause.channel == "y":
					y_channel = attribute
				elif clause.channel != "":
					additional_channels.append([clause.channel, attribute])
			if filter_spec:
				y_channel = y_channel.ljust(largest_y_length)
			elif largest_filter != 0:
				y_channel = y_channel.ljust(largest_y_length + largest_filter + 9)
			else:
				y_channel = y_channel.ljust(largest_y_length + largest_filter)
			if x_channel != "":
				x_channel = "x: " + x_channel + ", "
			if y_channel != "":
				y_channel = "y: " + y_channel
			aligned_mark = vis.mark.ljust(largest_mark)
			str_additional_channels = ""
			for channel in additional_channels:
				str_additional_channels += ", " + channel[0] + ": " + channel[1]
			if filter_spec:
				aligned_filter = " -- [" + filter_spec.attribute + filter_spec.filter_op + str(filter_spec.value) + "]"
				aligned_filter = aligned_filter.ljust(largest_filter + 8)
				vis_repr.append(f" <Vis  ({x_channel}{y_channel}{str_additional_channels} {aligned_filter}) mark: {aligned_mark}, score: {vis.score:.2f} >") 
			else:
				vis_repr.append(f" <Vis  ({x_channel}{y_channel}{str_additional_channels}) mark: {aligned_mark}, score: {vis.score:.2f} >") 
		return '['+',\n'.join(vis_repr)[1:]+']'
	def map(self,function):
		# generalized way of applying a function to each element
		return map(function, self.collection)
	
	def get(self,field_name):
		# Get the value of the field for all objects in the collection
		def get_field(d_obj):
			field_val = getattr(d_obj,field_name)
			# Might want to write catch error if key not in field
			return field_val
		return self.map(get_field)

	def set(self,field_name,field_val):
		return NotImplemented
	def set_plot_config(self,config_func:Callable):
		"""
		Modify plot aesthetic settings to the Vis List
		Currently only supported for Altair visualizations

		Parameters
		----------
		config_func : typing.Callable
			A function that takes in an AltairChart (https://altair-viz.github.io/user_guide/generated/toplevel/altair.Chart.html) as input and returns an AltairChart as output
		"""
		for vis in self.collection:
			vis.plot_config = config_func
	def clear_plot_config(self):
		for vis in self.collection:
			vis.plot_config = None
	def sort(self, remove_invalid=True, descending = True):
		# remove the items that have invalid (-1) score
		if (remove_invalid): self.collection = list(filter(lambda x: x.score!=-1,self.collection))
		# sort in-place by “score” by default if available, otherwise user-specified field to sort by
		self.collection.sort(key=lambda x: x.score, reverse=descending)

	def topK(self,k):
		#sort and truncate list to first K items
		self.sort(remove_invalid=True)
		return VisList(self.collection[:k])
	def bottomK(self,k):
		#sort and truncate list to first K items
		self.sort(descending=False,remove_invalid=True)
		return VisList(self.collection[:k])
	def normalize_score(self, invert_order = False):
		max_score = max(list(self.get("score")))
		for dobj in self.collection:
			dobj.score = dobj.score/max_score
			if (invert_order): dobj.score = 1 - dobj.score
	def _repr_html_(self):
		self.widget =  None
		from IPython.display import display
		from lux.luxDataFrame.LuxDataframe import LuxDataFrame
		recommendation = {"action": "Vis List",
					  "description": "Shows a vis list defined by the intent"}
		recommendation["collection"] = self.collection

		check_import_lux_widget()
		import luxWidget
		recJSON = LuxDataFrame.rec_to_JSON([recommendation])
		self.widget =  luxWidget.LuxWidget(
				currentVis={},
				recommendations=recJSON,
				intent=""
			)
		display(self.widget)	
	
	def refresh_source(self, ldf) :
		"""
		Loading the source into the visualizations in the VisList, then populating each visualization 
		based on the new source data, effectively "materializing" the visualization collection.

		Parameters
		----------
		ldf : LuxDataframe
			Input Dataframe to be attached to the VisList

		Returns
		-------
		VisList
			Complete VisList with fully-specified fields
		
		See Also
		--------
		lux.vis.Vis.refresh_source

		Note
		----
		Function derives a new _inferred_intent by instantiating the intent specification on the new data
		"""		
		from lux.compiler.Parser import Parser
		from lux.compiler.Validator import Validator
		from lux.compiler.Compiler import Compiler
		from lux.executor.PandasExecutor import PandasExecutor #TODO: temporary (generalize to executor)
		self.source = ldf
		if len(self._input_lst)>0:
			if (self._is_vis_input()):
				for vis in self.collection:
					vis._inferred_intent = Parser.parse(vis.intent)
					Validator.validate_spec(vis._inferred_intent,ldf)
				self.collection = Compiler.compile(ldf,ldf.intent,self,enumerate_collection=False)
			else:
				self._inferred_intent = Parser.parse(self.intent)
				Validator.validate_spec(self._inferred_intent,ldf)
				self.collection = Compiler.compile(ldf,self._inferred_intent,self)
			ldf.executor.execute(self.collection,ldf)
