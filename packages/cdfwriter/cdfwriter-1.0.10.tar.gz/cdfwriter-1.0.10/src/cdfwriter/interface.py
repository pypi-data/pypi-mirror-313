"""High level Object-Oriented interface methods for the CDFWriter package."""

__author__ = "Joey Mukherjee <joey@swri.org>"

import os
import random
import numpy as np
from collections import OrderedDict
# from collections import Sequence
from collections.abc import Sequence
from spacepy import pycdf
import datetime


class CDFWriter (object):
    """
    A class used to hold information that is needed in order to create
    a common set of CDF files that are similar.

    This class uses spacepy.pycdf to generate the CDFs.

    There are 2 kinds of variables that can be defined:
    1) plot - integer or real numbers that are plottable
    2) support - integer or real "attached" variables (e.g. constants)

    For this class, the name of the time variable is assumed to be
    "Epoch".

    Attributes
    ----------
    _prefix : str
        A string added at the beginning of the filename for every CDF
        file generated
    _outputDirectory : str
        The name of the directory in which the CDF file is to placed

        If the directory does not already exists, it will be created.
    _cdf_temp_name : str
        A temporary CDF filename used as the CDF file is being created
    _cdf : Python object representing a CDF file
        The handle to the CDF file being created
    _last_cdf_filename : str
        The name of the last CDF file created
    _file_naming_convention : str
        The time range string as default for naming files (default: "%Y%m%d%H%M00")
    _version : str
        The version number of the CDF file created
    _doNotSplit : Boolean
        Flag which specifies if the CDF file is to be split on a time boundary
    _boundary = datetime.timedelta
        Time interval at which the CDF file is to be split
    _variables : dictionary
        The variables defined for the CDF file
    _constants : dictionary
        The constants defined for the CDF file
    _global_attrs : dictionary
        The global attributes defined for the CDF file
    _variable_attrs : dictionary
        The attributes associated with the variables defined for the CDF file
    _firstTime : CDF Epoch data type
        The time associated with the first record in the CDF file
    _lastTime : CDF Epoch data type
        The time associated with the last record in the CDF file
    _data : dictionary
        The data associated with the plot variables defined for the CDF file
    _constantData : dictionary
        The data associated with the constants defined for the CDF file
    """

    def __init__(self, prefix, outputdir='./'):
        """
        Create CDF files with a "common" look.

        Parameters
        ----------
        prefix : str
            String prefix which is prepended to every CDF file generated.
        outputdir : str, optional
            The location where the CDF file is to be placed (default is the current directory).
        """

        self._prefix = prefix

        pycdf.lib.set_backward(False)
        if not outputdir.endswith(('/', '\\')):
            outputdir += '/'
        self._outputDirectory = outputdir

        # Make sure directory exists or pycdf creates error

        if not os.path.exists(self._outputDirectory):
            os.makedirs(self._outputDirectory)

        self._cdf_temp_name = outputdir + '__tmp' + str(os.getpid()) + '_' + str(random.randint(1, 65535)) + '.cdf'
        self._cdf = pycdf.CDF(self._cdf_temp_name, '')
        self._last_cdf_filename = None
        self._version = "0.0.0"
        self._file_naming_convention = "%Y%m%d%H%M00"
        self._doNotSplit = True
        self._boundary = datetime.timedelta(hours=6)

        self._variables = []
        self._constants = []
        self._global_attrs = OrderedDict()
        self._variable_attrs = {}

        self._firstTime = None
        self._lastTime = None
        self._data = {}
        self._constantData = {}

    def __repr__(self):
        """Define the string representation of the CDFWriter class object.

        Parameters
        ----------
        No parameters defined.

        Returns
        -------
        str
            The string representation of the key-value pairs of the CDFWriter
            attributes.
        """

        values = {k: repr(v) for (k, v) in self.__dict__.items()}

        return ('CDFWriter(name={_name}, prefix={_prefix}, outputdir={_outputdir})').format(**values)

    def __iter__(self):
        """Define the iterator for the CDFWriter class object.

        Parameters
        ----------
        No parameters defined.

        Returns
        -------
        iterator
            The CDFWriter custom iterator object
        """

        return iter([('name', self._name), ('prefix', self._prefix), ('outputdir', self._outputDirectory)])

# Add an attributes which is global in nature (i.e. covers entire CDF file)
    def addGlobalAttribute(self, name, value):
        """Define an attribute to be added to the global part of the CDF file.

        Parameters
        ----------
        name : str
            The string identifier for the global attribute.
        value : CDF_Data_Type
            The value to be assigned to the attribute being defined.

            CDF_Data_Type refers to the list of data types supported by CDF
            and used in pycdf.

        Raises
        ------
        TypeError
            If one of the arguments is not of the correct type.
        """

        if not isinstance(name, str):
            raise TypeError('name parameter must be a str')

        self._global_attrs[name] = value
        return

# Add an attribute which is tied to a single variable (plot or support)
    def addVariableAttribute(self, attribute_name, variable_name, value):
        """Define an attribute to be added to a variable in the CDF file.

        Parameters
        ----------
        attribute_name : str
            The string identifier for the variable attribute.
        variable_name : str
            The string identifier for the variable.
        value : CDF_Data_Type
            The value to be assigned to the variable attribute.

            CDF_Data_Type refers to the list of data types supported by CDF
            and used in pycdf.
        """

        # Before we store the value of the attribute, make sure this
        # variable has a place within the dictionary of variables with
        # attributes.

        if variable_name not in self._variable_attrs:
            self._variable_attrs[variable_name] = OrderedDict()
        self._variable_attrs[variable_name][attribute_name] = value
        return

# Add a variable to the CDF
    def addVariable(self, name, dataType, sizes=None,
                    dimVariances=None, variance=True, num_elements=1,
                    compression=pycdf.const.GZIP_COMPRESSION,
                    compression_param=5, sparse=False):
        """Define a variable to be included in the CDF file.

        pycdf.const refers to the list of constants supported by CDF
        when specifying a CDF data type for a variable.

        Parameters
        ----------
        name : str
            The string identifier for the variable.
        dataType : pycdf.const
            The data type of the variable.
        sizes : int, optional
            A python list which holds the size of each dimension defined
            for the constant.  The size must be greater than zero
            (default is None).
        dimVariances : pycdf.const, optional
            A python list which holds the dimension variance for each
            dimension defined for the variable (default is None).
        variance : Boolean, optional
            The record variance defined for the variable (default is True).
        num_elements : int, optional
            The number of elements of the data type for the variable
            (default is 1).
        compression : pycdf.const, optional
            The type of compression for the variable
            (default is pycdf.const.GZIP_COMPRESSION).
        compression_param : pycdf.const or int, optional
            The parameter value associated with the type of compression
            selected for the variable (default is 5).
        sparse: Boolean, optional
            Whether or not to set the sparse flag of the variable

        Raises
        ------
        TypeError
            If one of the arguments is not of the correct type.
        """

        if not isinstance(name, str):
            raise TypeError('name parameter must be a str')

        self._variables.append({'name': name, 'dataType': dataType,
                                'sizes': sizes, 'dimVariances': dimVariances,
                                'variance': variance,
                                'num_elements': num_elements,
                                'compression': compression,
                                'compression_param': compression_param,
                                'sparse': sparse,
                                })
        return

# Add data to an already defined variable to the CDF
# There are competing interests:
# [NOTE: 1 cdf record and ALL cdf records are handled. Partial set of cdf
#       records NOT handled. We may not want to handle partial sets.
# ]
#   1) input variable may be scalar or array
#   2) array may contain 1 cdf record [or many cdf records] or all cdf records.
#      As an example, Epoch is either a single, scalar value = 1 cdf record or
#                     an array of single, scalar values = many cdf records.
#                     These many records [can be a partial set of epochs or]
#                     will represent all epochs.
#                     Counts_per_accum is a vector = 1 cdf record or
#                     an array of vectors = many cdf records.
#
# If input is scalar, then can set [variable_name] = data or [data]
#                     and can append data or [data]
# If input is array:
#   For new variable_name: if array is 1 cdf record: must set = [data]
#                          if array is many cdf records: set = data
#                                                       but can set = [data]
#                          [if array is partial set, set = [data]]
#   For old variable: if array is 1 cdf record: append ( ,[data], axis=0)
#                     if array is many cdf records, append ( ,data, axis=0)
#                     [if array is partial set, append [data]]

    def addVariableData(self, variable_name, data, all_values=False):
        """Add data to the specified variable defined in the CDF file.

        Parameters
        ----------
        variable_name : str
            The name of the variable to which data is being added -
            case sensitive.
        data : CDF_Data_Type
            The data to be added to the constant variable.

            CDF_Data_Type refers to the list of data types supported by CDF
            and used in pycdf.
        all_values : Boolean, optional
            A flag which tells if the data contains values for all
            CDF records (default is False).

            True means data contains values for all CDF records.
            False means data contains values for a single CDF record.

        Raises
        ------
        TypeError
            If one of the arguments is not of the correct type.
        ValueError
            If the variable name has not been previously defined
            (a call to addVariable() has not been made)
        """

# for a variable called Epoch (assume this is the name of the time variable!)

        if not isinstance(variable_name, str):
            raise TypeError('variable_name parameter must be a str')
        if not isinstance(all_values, bool):
            raise TypeError('all_values parameter must be a bool')

        # Make sure variable has already been defined before we try to 
        # add the data.

        list_of_all_variables = []
        definedVariables = self._variables

        for variable in definedVariables:
            list_of_all_variables.append(variable['name'])

        if variable_name not in list_of_all_variables:
            raise ValueError('variable_name {0} must be one of {valids}'.format(
                variable_name, valids=repr(list_of_all_variables)))

        if variable_name == 'Epoch':
            if not isinstance(data, (Sequence, np.ndarray)):
                times = [data]
            else:
                times = data
            if self._firstTime is None:
                self._firstTime = times[0]
            self._lastTime = times[-1]

        if all_values:
           assert variable_name not in self._data
           self._data[variable_name] = data
        else:
           if variable_name not in self._data:
              self._data[variable_name] = [data]
           else:
              self._data[variable_name].append (data)

        return

# Add a constant to the CDF
    def addConstant(self, name, dataType, sizes):
        """Define a constant to be included in the CDF file.

        Parameters
        ----------
        name : str
            The string identifier for the constant.
        dataType : pycdf.const
            The data type of the constant.

            pycdf.const refers to the list of constants supported by CDF
            when specifying a CDF data type for a variable.
        sizes : int
            A python list which holds the size of each dimension defined for
            the constant.  Each size must be greater than zero (0).

        Raises
        ------
        TypeError
            If one of the arguments is not of the correct type.
        """

        if not isinstance(name, str):
            raise TypeError('name parameter must be a str')

        self._constants.append({'name': name, 'dataType': dataType, 'sizes': sizes})
        return

# Add data to an already defined constant to the CDF
    def addConstantData(self, constant_name, data):
        """Add data to the specified constant defined in the CDF file.

        Parameters
        ----------
        constant_name : str
            The name of the constant variable to which data is being added -
            case sensitive.
        data : CDF_Data_Type
            The data to be added to the constant variable.

            CDF_Data_Type refers to the list of data types supported by CDF
            and used in pycdf.

        Raises
        ------
        TypeError
            If one of the arguments is not of the correct type.
        ValueError
            If the constant variable named has not been previously defined
            (a call to addConstant() has not been made)
        """

        if not isinstance(constant_name, str):
            raise TypeError('constant_name parameter must be a str')

        # Make sure constant have already been defined before we try to 
        # add the data.

        list_of_all_constants = []
        definedConstants = self._constants

        for constant in definedConstants:
            list_of_all_constants.append(constant['name'])

        if constant_name not in list_of_all_constants:
            raise ValueError('constant_name {0} must be one of {valids}'.format(
                constant_name, valids=repr(list_of_all_constants)))

        # First time data being added?

        if constant_name not in self._constantData:
            self._constantData[constant_name] = [data]
        else:
            self._constantData[constant_name].append (data)

        return

    def _writeData(self):
        """Write the data to the CDF file.

        Parameters
        ----------
        No parameters defined.
        """

        # Transfer the global attributes defined.

        for name, value in self._global_attrs.items():
            self._cdf.attrs[name] = value

        # Transfer the constants defined.

        for constant in self._constants:
            if constant ['dataType'] == pycdf.const.CDF_CHAR:
               n_elems = len (max(self._constantData[constant['name']][0], key=len))
            else:
               n_elems = 1

            self._cdf.new(constant['name'], type=constant['dataType'], n_elements=n_elems,
                          dims=constant['sizes'], dimVarys=None, recVary=False,
                          compress=pycdf.const.NO_COMPRESSION)
            if constant['name'] in self._variable_attrs:
                for name, value in self._variable_attrs[constant['name']].items():
                    self._cdf[constant['name']].attrs[name] = value
            if constant['name'] in self._constantData:
                self._cdf[constant['name']] = self._constantData[constant['name']][0]

        # Transfer the variables defined.

        for variable in self._variables:
            try:
                self._cdf.new(variable['name'], type=variable['dataType'],
                              dims=variable['sizes'],
                              dimVarys=variable['dimVariances'],
                              recVary=variable['variance'],
                              compress=variable['compression'],
                              compress_param=variable['compression_param'],
                              sparse=variable ['sparse'])
            except:
                print ("Can't add", variable['name'], "to CDF - already exists")
            if variable['name'] in self._variable_attrs:
                for name, value in self._variable_attrs[variable['name']].items():
                    try:
                        self._cdf[variable['name']].attrs[name] = value
                    except:
                        print ("Can't add attribute", value, "to attribute", name, "on", variable['name'])
            if variable['name'] in self._data:
                try:
                    self._cdf[variable['name']] = self._data[variable['name']]
                except:
                    print ("Can't add", self._data[variable['name']], "to variable", variable['name'])

    def cloneVariable (self, zVar, name=None, cloneData=False, newType=None, newAttrs = []):
        """Define a new variable to be included in the CDF file which is a copied from the named input variable 

        Parameters
        ----------
        zVar : pycdf.Var
            The name of the variable to copy from (clone) for the new variable being defined.

            pycdf.Var refers a class which defines CDF variables of the type zVariable.
        name : str, optional
            The string identifier for the new variable being defined (default is None so the name value is cloned).
        cloneData : Boolean, optional
            A flag which tells if the data from the named variable (zVar) is to be copied to the new variable 
            being defined (default is False).
        newType : pycdf.const, optional
            The data type of the new variable being defined (default is None so the data type value is cloned).

            pycdf.const refers to the list of constants supported by CDF
            when specifying a CDF data type for a variable.
        newAttrs : CDF_Data_Type, optional
            The list of attributes to be defined for the new variable, overwriting any of the attributes 
            cloned from the named variable zVar (default is an empty list).
        """

        if name is None:
           name = zVar.name()
        if newType is None:
           newType = zVar.type()

        self._variables.append({'name': name, 'dataType': newType,
                                'sizes': zVar._dim_sizes(), 'dimVariances': zVar.dv(),
                                'variance': zVar.rv(),
                                'num_elements': zVar.nelems(),
                                'compression': zVar.compress()[0],
                                'compression_param': zVar.compress()[1],
                                'sparse': zVar.sparse (),
                               })
        self._variable_attrs [name] = OrderedDict ()
        attrs = zVar.attrs.items ()
        for k, v in attrs:
            self._variable_attrs [name][k] = v
        for k, v in newAttrs:  # overwrite any new ones
            self._variable_attrs [name][k] = v

        if cloneData:
           self._data[name] = zVar [...]
        return

    def close(self):
        """Close the CDF file currently being processed.

        If data for any of the variables within the CDF was added,
        the CDF file is moved to the output directory specified.

        Parameters
        ----------
        No parameters defined.
        """

        self.addGlobalAttribute('Generation_date',
                                datetime.datetime.now().strftime("%Y%m%d"))
        self.addGlobalAttribute('Data_version', "v" + self._version)
        self.addGlobalAttribute('Logical_source', self._prefix)

        if self._firstTime is not None:
            new_filename = self._prefix + '_' + self._firstTime.strftime(self._file_naming_convention) + '_v' + self._version + '.cdf'
            self.addGlobalAttribute('Logical_file_id', self._prefix + '_' + self._firstTime.strftime(self._file_naming_convention))
        else:
            new_filename = self._prefix + '_v' + self._version + '.cdf'

        if self._data:
            self._writeData()

        self._cdf.close()

        # Moves the CDF file from the temporary to the permanent location
        # with the correct filename.

        if os.path.exists (self._outputDirectory + new_filename):
            raise RuntimeError(self._outputDirectory + new_filename, 'already exists!')
        else:
            os.rename(self._cdf_temp_name, self._outputDirectory + new_filename)
        if not self._data:
            os.unlink(self._outputDirectory + new_filename)
        else:
            self._last_cdf_filename = new_filename

        self._data = {}
        self._firstTime = None
        self._lastTime = None

    def makeNewFile(self):
        """Create a new CDF file.

        If there is a CDF file already being processed, close that CDF file.

        Parameters
        ----------
        No parameters defined.
        """

        self.close()

        self._cdf_temp_name = self._outputDirectory + '__tmp' + str(os.getpid()) + '_' + str(random.randint(1, 65535)) + '.cdf'
        self._cdf = pycdf.CDF(self._cdf_temp_name, '')

        # OLD WAY  self._cdf = pycdf.CDF (self._cdf_temp_name, new_filename)
        # but changed since documentation says it would copy the data too and
        # self._last_cdf_filename is set by the close() method

        return

# Close the CDF record and start a new record

    def closeRecord(self):
        """Close the current CDF record and start a new CDF record.

        If the CDF file is to be split at a pre-defined time boundary,
        then the current CDF file is closed and a new CDF file
        is created before a new CDF record commences if the file
        boundary condition is met.

        Parameters
        ----------
        No parameters defined.
        """

        if self._doNotSplit:
            return
        if self._lastTime - self._firstTime >= self._boundary:
            self.makeNewFile()

        return

    def setFileNamingConvention(self, file_naming_convention):
        """Set the file naming convention for the time string on the end.

        Currently, this is "%Y%m%d%H%M00", and only can use the start time.

        Parameters
        ----------
        file_naming_convention : str
            The file naming convention based on the start time.  The default is "%Y%m%d%H%M00".
        """
        if not isinstance(file_naming_convention, str):
            raise TypeError('file_naming_convention parameter must be a str')

        self._file_naming_convention = file_naming_convention

        return

# Set the version number of this CDF
    def setVersionNumber(self, version):
        """Set the version number for the CDF generated.

        The value is initially set to 0.0.0 by the class constructor

        Parameters
        ----------
        version : str
            The version number for the CDF produced in the format
            n.n.n, where n represents a number.

            For example, 4.2.0 is a valid value.

        Raises
        ------
        TypeError
            If the version argument is not of the correct type.
        ValueError
            If the version argument is not in the format n.n.n (e.g. 4.2.0).
        """

        if not isinstance(version, str):
            raise TypeError('version parameter must be a str')

        # Split the version parameter into separate components.

        versionNumbersList = version.split('.')
        numLevels = len(versionNumbersList)
        if numLevels != 3:
            raise ValueError('version should have 3 levels (e.g. 4.2.0)')

        else:
            # Make sure each component represents a digit since we only use
            # numbers for the version.

            for j in range(numLevels):
                vpart = versionNumbersList[j]
                goodVal = vpart.isdigit()
                if not goodVal:
                    # print 'ERROR: ' + vpart + ' is invalid - must be an int.'
                    raise TypeError('each level must consist only of integers')

            self._version = version

        return

# Set the directory to write the CDFs
    def setOutputDirectory(self, outputDirectory):
        """Set the directory into which the CDF files are to be written.

        If this method is not called, the CDF files are written in the directory 
        specified when the class is instantiated.

        Parameters
        ----------
        outputDirectory : str
            The name of the directory where the CDF files are to be placed.

            If the directory does not already exists, it will be created.

        Raises
        ------
        TypeError
            If the outputDirectory argument is not of the correct type.
        """

        if not isinstance(outputDirectory, str):
            raise TypeError('outputDirectory parameter must be a str')

        if not outputDirectory.endswith(('/', '\\')):
            outputDirectory += '/'
        self._outputDirectory = outputDirectory

        # Make sure directory exists or pycdf creates error

        if not os.path.exists(self._outputDirectory):
            os.makedirs(self._outputDirectory)
        return

# Set this to true to never split the file based on six hours
    def setDoNotSplit(self, doNotSplit, boundary=datetime.timedelta(hours=6)):
        """Determines if CDF files are to be split on a pre-defined boundary.

        The default, as set by the class constructor, generates a single CDF file.

        Parameters
        ----------
        doNotSplit : Boolean
            A flag which defines whether or not the CDF file(s) generated are
            to be split on a pre-defined time boundary (default is 6 hours).

            True means never split the file - one single CDF file is generated.
            False means automatically split the CDF file at the pre-defined
            time boundaries.

        boundary : datetime.timedelta, optional
            The time interval at which the CDF file is to be split into
            multiple files (default = 6 hours).

        Raises
        ------
        TypeError
            If one of the arguments is not of the correct type.
        """

        if not isinstance(doNotSplit, bool):
            raise TypeError('doNotSplit parameter must be a bool')
        if not isinstance(boundary, datetime.timedelta):
            raise TypeError('boundary parameter must be a datetime.timedelta value')

        self._doNotSplit = doNotSplit
        self._boundary = boundary
        return

# Will return the name of the last CDF file created
# NOTE: this will return None if no CDF file has been written yet

    def getLastCDFFilename(self):
        """Return the name of the last CDF file produced.

        Parameters
        ----------
        No parameters defined.

        Returns
        -------
        str
            The name of the last CDF file created (keyword None if no CDF)
        """

        return self._last_cdf_filename

# -------------------------------------------------------------------------------
    def addSupportVariableAttributes(self, variable_name, short_description='',
                                     long_description='', units_string=' ', format_string='', validmin=None,
                                     validmax=None, lablaxis=' ',
                                     si_conversion=' > ', scaleType='linear'
                                     ):
        """Define the required attributes for a support variable in the CDF file.

        These required attributes include FIELDNAM, VALIDMIN, VALIDMAX,
                                 LABLAXIS, UNITS, FORMAT, CATDESC,
                                 VAR_TYPE and SI_CONVERSION.

        VAR_TYPE is defaulted to "support_data".

        Parameters
        ----------
        variable_name : str
            The string identifier for the variable.
        short_description : str, optional
            The string which describes the variable (default is empty string).
        long_description : str, optional
            A catalog description of the variable (default is empty string).
        units_string : str, optional
            A string representing the units of the variable,
            e.g., nT for magnetic field (default is ' ').

            Use a blank character, rather than "None" or "unitless",
            for variables that have no units (e.g., a ratio).
        format_string : str, optional
            The output format used when extracting data values (default is empty string).

            The magnitude and the number of significant figures needed
            should be carefully considered, with respect to the values
            of validmin and validmax parameters.
        validmin : pycdf.const, optional
            The minimum value for the variable that are expected over the
            lifetime of a mission (default is None).

            The value must match variable's dataType.
        validmax : pycdf.const, optional
            The maximum value for the variable that are expected over the
            lifetime of a mission (default is None).

            The value must match variable's dataType.
        lablaxis : str, optional
            A short string which can be used to label a y-axis for a plot
            or to provide a heading for a data listing (default is " ").
        si_conversion : str, optional
            A string which defines the conversion factor that the variable
            must be multiplied by in order to turn it to generic SI units
            (default is " > ").

            The string must contain 2 text fields separated by the delimiter >.
        scaleType : str, optional
            A string which indicates whether the variable should have a linear
            or a log scale (default is 'linear').
        """

        self.addVariableAttribute("FIELDNAM", variable_name, short_description)
        self.addVariableAttribute("VALIDMIN", variable_name, validmin)
        self.addVariableAttribute("VALIDMAX", variable_name, validmax)
        if len (units_string) == 0:
           units_string = 'unitless'
        self.addVariableAttribute("UNITS", variable_name, units_string)
        self.addVariableAttribute("FORMAT", variable_name, format_string)
        self.addVariableAttribute("CATDESC", variable_name, long_description)
        self.addVariableAttribute("VAR_TYPE", variable_name, "support_data")
        self.addVariableAttribute("SI_CONVERSION", variable_name, si_conversion)
        self.addVariableAttribute("LABLAXIS", variable_name, lablaxis)
        self.addVariableAttribute("SCALETYP", variable_name, scaleType)

# -----------------------------------------------------------------------------------------
    def addPlotVariableAttributes(self, variable_name, short_description='',
                                  long_description='', display_type='', units_string=' ', format_string='',
                                  lablaxis='', dataType=None, validmin=None, validmax=None,
                                  scaleType='linear', addFill=True):
        """Define the required attributes for a plot variable in the CDF file.

        These required attributes include FIELDNAM, VALIDMIN, VALIDMAX,
                                LABLAXIS, FILLVAL, SCALETYP, UNITS, FORMAT,
                                CATDESC, VAR_TYPE, DISPLAY_TYPE, SI_CONVERSION,
                                DEPEND_0, and COORDINATE_SYSTEM.

        FILLVAL is defaulted based upon the dataType value specified.
        VAR_TYPE is defaulted to "data".
        SI_CONVERSION is defaulted to " > ".
        DEPEND_0 is defaulted to "Epoch".
        COORDINATE_SYSTEM is defaulted to "BCS".

        Parameters
        ----------
        variable_name : str
            The string identifier for the variable.
        short_description : str, optional
            The string which describes the variable (default is empty string).
        long_description : str, optional
            A catalog description of the variable (default is empty string).
        display_type : str, optional
            A string which tells automated software what type of plot to make
            (default is empty string).

            Examples include time_series, spectrogram, stack_plot, image.
        units_string : str, optional
            A string representing the units of the variable,
            e.g., nT for magnetic field (default is ' ').

            Use a blank character, rather than "None" or "unitless", for
            variables that have no units (e.g., a ratio or a direction cosine).
        format_string : str, optional
            The output format used when extracting data values
            (default is empty string).

            The magnitude and the number of significant figures needed should
            be carefully considered, with respect to the values of validmin
            and validmax parameters.
        lablaxis : str, optional
            A short string which can be used to label a y-axis for a plot
            or to provide a heading for a data listing (default is empty string).
        dataType : pycdf.const, optional
            The data type of the variable (default is None).

            If the addFill flag is set to True, then the dataType parameter
            must be specified; otherwise, an abort is issued by the code.
        validmin : pycdf.const, optional
            The minimum value for the variable that are expected over the
            lifetime of a mission (default is None).

            The value must match dataType value specified.
        validmax : pycdf.const, optional
            The maximum value for the variable that are expected over the
            lifetime of a mission (default is None).

            The value must match dataType value specified.
        scaleType : str, optional
            A string which indicates whether the variable should have a linear
            or a log scale (default is 'linear').
        addFill : Boolean, optional
            A flag to indicate if the FILLVAL attribute is to be set
            (default is True).

            FILLVAL is the number inserted in the CDF in place of data values
            that are known to be bad or missing.  The value used is dependent
            upon the dataType value specified and should match the data type
            of the variable.
        """

        self.addVariableAttribute("FIELDNAM", variable_name, short_description)
        self.addVariableAttribute("VALIDMIN", variable_name, validmin)
        self.addVariableAttribute("VALIDMAX", variable_name, validmax)
        self.addVariableAttribute("LABLAXIS", variable_name, lablaxis)
        if addFill:
            if dataType == pycdf.const.CDF_DOUBLE:
                self.addVariableAttribute("FILLVAL", variable_name, 1.0e31)
            elif dataType == pycdf.const.CDF_FLOAT:
                self.addVariableAttribute("FILLVAL", variable_name, 1.0e31)
            elif dataType == pycdf.const.CDF_UINT1:
                self.addVariableAttribute("FILLVAL", variable_name, 255)
            elif dataType == pycdf.const.CDF_UINT2:
                self.addVariableAttribute("FILLVAL", variable_name, 65535)
            elif dataType == pycdf.const.CDF_INT4:
                self.addVariableAttribute("FILLVAL", variable_name, 1)
            elif dataType == pycdf.const.CDF_UINT4:
                self.addVariableAttribute("FILLVAL", variable_name, 4294967294)
            else:
                valid_data_types = ('CDF_DOUBLE', 'CDF_FLOAT', 'CDF_UINT1', 'CDF_UINT2', 'CDF_INT4', 'CDF_UINT4')
                print ('For {0} data_type must be one of {valids}'.format(variable_name, valids=repr(valid_data_types)))
                os.abort()
        self.addVariableAttribute("SCALETYP", variable_name, scaleType)
        self.addVariableAttribute("UNITS", variable_name, units_string)
        self.addVariableAttribute("FORMAT", variable_name, format_string)
        self.addVariableAttribute("CATDESC", variable_name, long_description)
        self.addVariableAttribute("VAR_TYPE", variable_name, "data")
        self.addVariableAttribute("DISPLAY_TYPE", variable_name, display_type)
        self.addVariableAttribute("SI_CONVERSION", variable_name, " > ")
        self.addVariableAttribute("DEPEND_0", variable_name, "Epoch")
        self.addVariableAttribute("COORDINATE_SYSTEM", variable_name, "BCS")
