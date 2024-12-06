.. _user-function-plugins:

User Function plugins
---------------------

A **User Function plugin** can be defined by a **class** or a **function** in a python package.

A **user function plugin** defined by a **function** is a simple python function with one argument: `results` which contain a python dictionary of **ToolResults**.

This function **returns** a python dictionary with `x` and  `y` *(list)* data to plot , `title`, `bottom` and `left` *(string)* labels  `color` and `hvscolor` *(string)*  or *(int)* . For user plots with mutli-curves the python dictionary can contains `nrplots` *(int)* , `x_%i`,  `y_%i` *(list)* data to plot, `color_%i` and `hvscolor_%i` *(string)*  or *(int)* where `%i` runs from 1 to `nrplots`. If `y_%i` is set to ``None`` the previous plot will stay shown.
, e.g.

.. code-block:: python

    def positive(results):
	""" plot positive function values on the LineCut tool

	:param results: dictionary with tool results
	:type results: :obj:`dict`
	:returns: dictionary with user plot data
	:rtype: :obj:`dict`
	"""
	userplot = {}
	if "linecut_1" in results:
	    userplot = {"x": results["linecut_1"][0],
			"y": [max(0.0, yy) for yy in results["linecut_1"][1]]}
	return userplot


A **user function plugin** defined by a **class** it should have defined **__call__** method with one argument: `results`.

This **__call__** function returns a python dictionary with `x` and  `y` *list* data to plot  and optionally `title`, `bottom` and `left` *string* labels.

Moreover, the class *constructor* has one configuration string argument initialized by an initialization parameter, e.g.

.. code-block:: python

    class LineCutFlat(object):

	"""Flatten line cut"""

	def __init__(self, configuration=None):
	    """ constructor

	    :param configuration: JSON list with horizontal gap pixels to add
	    :type configuration: :obj:`str`
	    """
	    #: (:obj:`list` <:obj: `str`>) list of indexes for gap
	    self.__index = 1
	    try:
		self.__flat = float(configuration)
	    except Exception:
		self.__flat = 100000000.
		pass

	def __call__(self, results):
	    """ call method

	    :param results: dictionary with tool results
	    :type results: :obj:`dict`
	    :returns: dictionary with user plot data
	    :rtype: :obj:`dict`
	    """
	    userplot = {}
        if "tool" in results and results["tool"] == "linecut":
            try:
                nrplots = int(results["nrlinecuts"])
            except Exception:
                nrplots = 0
            userplot["nrplots"] = nrplots
            userplot["title"] = "Linecuts flatten at '%s'" % (self.__flat)

            for i in range(nrplots):
                xlabel = "x_%s" % (i + 1)
                ylabel = "y_%s" % (i + 1)
                label = "linecut_%s" % (i + 1)
                cllabel = "hsvcolor_%s" % (i + 1)
                if label in results:
                    userplot[xlabel] = results[label][0]
                    userplot[ylabel] = [min(yy, self.__flat)
                                        for yy in results[label][1]]
                    userplot[cllabel] = i/float(nrplots)
            if "unit" in results:
                userplot["bottom"] = results["unit"]
                userplot["left"] = "intensity"
	    return userplot

or

.. code-block:: python

    import json


    class DiffPDF(object):

	"""diffpy PDF user function"""

	def __init__(self, configuration=None):
	    """ constructor

	    :param configuration: JSON list with config file and diff index
	    :type configuration: :obj:`str`
	    """
	    #: (:obj:`list` <:obj: `str`>) list of indexes for gap
	    self.__configfile = None

	    config = None
	    try:
		config = json.loads(configuration)
		try:
		    self.__index = int(config[1])
		except Exception:
		    self.__index = 1
		self.__configfile = str(config[0])
	    except Exception:
		self.__index = 1
		self.__configfile = str(configuration)

	    from diffpy.pdfgetx import loadPDFConfig
	    self.__cfg = loadPDFConfig(self.__configfile)

	def __call__(self, results):
	    """ call method

	    :param results: dictionary with tool results
	    :type results: :obj:`dict`
	    :returns: dictionary with user plot data
	    :rtype: :obj:`dict`
	    """
	    userplot = {}
	    from diffpy.pdfgetx import PDFGetter
	    self.__pg = PDFGetter(config=self.__cfg)
	    label = "diff_%s" % self.__index
	    if label in results and self.__configfile:
		qq = results[label][0]
		df = results[label][1]
		data_gr = self.__pg(qq, df)
		x = data_gr[0]
		y = data_gr[1]

		userplot = {
		    "x": x, "y": y,
		    "title": "DiffPDF: %s with %s" % (label, self.__configfile)
		}
	    return userplot
    
	    
To configure filters see :ref:`user-function-plugins-settings`.
