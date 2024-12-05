"""
this Module creates the different Mathis objects for further assembly in the input *.data file
"""

import os, re, copy, platform
from subprocess import check_call
import pymathis.pymathis as pm
import time

# =========================
# Class for MATHIS OBJECTS
# =========================

class Misc():
    """
    Simulation parameters are given in the MISC class
    """

    def __init__(self,**kwargs):
        """
        Misc Object initialization, all default values are loaded and the one given in kwargs are changed
        :param kwargs:
        """
        #initialization is made with the given attributes to be changed
        for key, value in kwargs.items():
            setattr(self, key, value)

    def getModifiedValues(self):
        """
        This function returns a dictionary off all modified attributes compared to default values
        """
        list = self.__dict__.keys()
        list2write = [(key, getattr(self,key)) for key in list if getattr(self,key) != DefaultMathisInputDict['MISC'][key]]
        return dict(list2write)

class Loc():
    """
    LOC object in MATHIS
    """

    def __init__(self, **kwargs):
        # initialization is made with the given attributes to be changed
        for key, value in kwargs.items():
            setattr(self, key, value)

    def getModifiedValues(self):
        """
            function to get only the modified attribute compared to the default values
        """
        list = self.__dict__.keys()
        list2write = [(key,getattr(self,key)) for key in list if getattr(self,key) != DefaultMathisInputDict['LOC'][key]]
        return dict(list2write)

class Branch():
    """
    Create a BRANCH object for MATHIS
    """

    def __init__(self, **kwargs):
        """
        initialization is made with the given attributes to be changed
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def getModifiedValues(self):
        """
        function to get only the modified attribute compared to the default values
        """
        list = self.__dict__.keys()
        list2write = [(key,getattr(self,key)) for key in list if getattr(self,key) != DefaultMathisInputDict['BRANCH'][key]]
        return dict(list2write)

class HSRC():
    """
    Create a HSRC object for MATHIS
    """

    def __init__(self, **kwargs):
        """
        initialization is made with the given attributes to be changed
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def getModifiedValues(self):
        """
        function to get only the modified attribute compared to the default values
        """
        list = self.__dict__.keys()
        list2write = [(key,getattr(self,key)) for key in list if getattr(self,key) != DefaultMathisInputDict['HSRC'][key]]
        return dict(list2write)

class Person():
    """
    Create a Person (occupant) object for MATHIS
    """

    def __init__(self, **kwargs):
        """
        initialization is made with the given attributes to be changed
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def getModifiedValues(self):
        """
        function to get only the modified attribute compared to the default values
        """
        list = self.__dict__.keys()
        list2write = [(key,getattr(self,key)) for key in list if getattr(self,key) != DefaultMathisInputDict['PERSON'][key]]
        return dict(list2write)

class Species():
    """
    Create a SPEC object for MATHIS
    """

    def __init__(self, **kwargs):
        """
        initialization is made with the given attributes to be changed"""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def getModifiedValues(self):
        """function to get only the modified attribute compared to the default values
        """
        list = self.__dict__.keys()
        list2write = [(key,getattr(self,key)) for key in list if getattr(self,key) != DefaultMathisInputDict['SPEC'][key]]
        return dict(list2write)

class Material():
    """
    Create a MAT object for MATHIS
    """

    def __init__(self, **kwargs):
        """
        initialization is made with the given attributes to be changed
        :param kwargs: attributes to be changed

        """

        for key, value in kwargs.items():
            setattr(self, key, value)

    def getModifiedValues(self):
        """
        function to get only the modified attribute compared to the default values
        """
        list = self.__dict__.keys()
        list2write = [(key,getattr(self,key)) for key in list if getattr(self,key) != DefaultMathisInputDict['MAT'][key]]
        return dict(list2write)

class Surf():
    """
    Create a SURF object for MATHIS
    """

    def __init__(self, **kwargs):
        """
        initialization is made with the given attributes to be changed
        :param kwargs: attributes to be changed
        """

        for key, value in kwargs.items():
            setattr(self, key, value)

    def getModifiedValues(self):
        """
        function to get only the modified attribute compared to the default values
        """
        list = self.__dict__.keys()
        list2write = [(key,getattr(self,key)) for key in list if getattr(self,key) !=DefaultMathisInputDict['SURF'][key]]
        return dict(list2write)

class Wall():
    """"
    Create a WALL object for MATHIS
    """

    def __init__(self, **kwargs):
        """initialization is made with the given attributes to be changed"""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def getModifiedValues(self):
        """function to get only the modified attribute compared to the default values"""
        list = self.__dict__.keys()
        list2write = [(key,getattr(self,key)) for key in list if getattr(self,key) != DefaultMathisInputDict['WALL'][key]]
        return dict(list2write)

class Ext():
    """Create a EXT object for MATHIS"""

    def __init__(self,**kwargs):
        """initialization is made with the given attributes to be changed"""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def getModifiedValues(self):
        """function to get only the modified attribute compared to the default values"""
        list = self.__dict__.keys()
        list2write = [(key,getattr(self,key)) for key in list if getattr(self,key) != DefaultMathisInputDict['EXT'][key]]
        return dict(list2write)

class Bound():
    """Create a BOUND object for MATHIS"""

    def __init__(self,**kwargs):
        """initialization is made with the given attributes to be changed"""
        for key, value in kwargs.items():
            if key != 'Default': setattr(self, key, value)

    def getModifiedValues(self):
        """function to get only the modified attribute compared to the default values"""
        list = self.__dict__.keys()
        list2write = [(key,getattr(self,key)) for key in list if getattr(self,key) != DefaultMathisInputDict['BOUND'][key]]
        return dict(list2write)

class Ctrl():
    """Create a CTRL object for MATHIS"""

    def __init__(self, **kwargs):
        """initialization is made with the given attributes to be changed"""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def getModifiedValues(self):
        """function to get only the modified attribute compared to the default values"""
        list = self.__dict__.keys()
        list2write = [(key,getattr(self,key)) for key in list if getattr(self,key) != DefaultMathisInputDict['CTRL'][key]]
        return dict(list2write)

class Mod():
    """Create a Mod object for MATHIS"""

    def __init__(self, **kwargs):
        """initialization is made with the given attributes to be changed"""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def getModifiedValues(self):
        """function to get only the modified attribute compared to the default values"""
        list = self.__dict__.keys()
        # MOD can get multiple arguments depending on the dll being used,
        # thus the list2write has to handle non attribute values in the default dict of the class
        list2write = []
        for key in list:
            if key in DefaultMathisInputDict.keys():
                if getattr(self,key) != DefaultMathisInputDict['MOD'][key]: list2write.append((key,getattr(self,key)))
            else:
                list2write.append((key, getattr(self, key)))
        return dict(list2write)

class Building():
    """Creates the building class object that deals with all other Mathis' Objects"""
    def __init__(self,Name):
        """
        Building Object initialization, if the file Name exists it will be loaded otherwise a new object
        with default values will be created
        :param Name: Building Oject Name, it will be the Name.data file created as Mathis input
        """
        if not Name.endswith('.data'):
            Name = Name+'.data'
        if not os.path.isfile(Name):
            #print('[INFO] --> Empty project created')
            self.Path2Case = os.getcwd()
            self.Path2Mathis = 'null'
            a = Misc(**DefaultMathisInputDict['MISC'])
            a.JOBNAME = Name
            self.Misc = a
            self.Ext = Ext(**DefaultMathisInputDict['EXT'])
            self.Loc = {}
            self.Branch = {}
            self.HSRC = {}
            self.Person = {}
            self.Bound = {}
            self.Species = {}
            self.Material = {}
            self.Surf = {}
            self.Wall = {}
            self.Ctrl = {}
            self.Mod = {}
        else:
            CaseDict = loadExistingFile(Name)
            InputDict = copy.deepcopy(DefaultMathisInputDict)
            self.Path2Case = os.path.dirname(Name)
            self.Path2Mathis = 'null'
            if 'MISC' in CaseDict.keys():
                for key, value in  CaseDict['MISC'].items():
                    InputDict['MISC'][key] = value
                self.Misc = Misc(**InputDict['MISC'])
            else:
                self.Misc = Misc(**InputDict['MISC'])
            self.Misc.JOBNAME = os.path.basename(Name)
            if 'EXT' in CaseDict.keys():
                for key, value in  CaseDict['EXT'].items():
                    InputDict['EXT'][key] = value
                self.Ext = Ext(**InputDict['EXT'])
            self.Loc = {}
            self.Branch = {}
            self.HSRC = {}
            self.Person = {}
            self.Bound = {}
            self.Species = {}
            self.Material = {}
            self.Surf = {}
            self.Wall = {}
            self.Ctrl = {}
            self.Mod = {}
            if 'LOC' in CaseDict.keys():
                if type(CaseDict['LOC']) == list:
                    for a in CaseDict['LOC']:
                        TempDict = copy.deepcopy(InputDict['LOC'])
                        for key, value in a.items():
                            TempDict[key] = value
                        self.addLoc(**TempDict)
                else:
                    TempDict = copy.deepcopy(InputDict['LOC'])
                    for key, value in CaseDict['LOC'].items():
                        TempDict[key] = value
                    self.addLoc(**TempDict)
            if 'BRANCH' in CaseDict.keys():
                if type(CaseDict['BRANCH'])==list:
                    for a in CaseDict['BRANCH']:
                        TempDict = copy.deepcopy(InputDict['BRANCH'])
                        for key, value in a.items():
                            TempDict[key] = value
                        self.addBranch(**TempDict)
                else:
                    TempDict = copy.deepcopy(InputDict['BRANCH'])
                    for key, value in CaseDict['BRANCH'].items():
                        TempDict[key] = value
                    self.addBranch(**TempDict)

            if 'HSRC' in CaseDict.keys():
                if type(CaseDict['HSRC'])==list:
                    for a in CaseDict['HSRC']:
                        TempDict = copy.deepcopy(InputDict['HSRC'])
                        for key, value in a.items():
                            TempDict[key] = value
                        self.addHSRC(**TempDict)
                else:
                    TempDict = copy.deepcopy(InputDict['HSRC'])
                    for key, value in CaseDict['HSRC'].items():
                        TempDict[key] = value
                    self.addHSRC(**TempDict)

            if 'PERSON' in CaseDict.keys():
                if type(CaseDict['PERSON'])==list:
                    for a in CaseDict['PERSON']:
                        TempDict = copy.deepcopy(InputDict['PERSON'])
                        for key, value in a.items():
                            TempDict[key] = value
                        self.addPerson(**TempDict)
                else:
                    TempDict = copy.deepcopy(InputDict['PERSON'])
                    for key, value in CaseDict['PERSON'].items():
                        TempDict[key] = value
                    self.addPerson(**TempDict)

            if 'BOUND' in CaseDict.keys():
                if type(CaseDict['BOUND'])==list:
                    for a in CaseDict['BOUND']:
                        TempDict = copy.deepcopy(InputDict['BOUND'])
                        for key, value in a.items():
                            TempDict[key] = value
                        self.addBound(**TempDict)
                else:
                    TempDict = copy.deepcopy(InputDict['BOUND'])
                    for key, value in CaseDict['BOUND'].items():
                        TempDict[key] = value
                    self.addBound(**TempDict)

            if 'SPEC' in CaseDict.keys():
                if type(CaseDict['SPEC'])==list:
                    for a in CaseDict['SPEC']:
                        TempDict = copy.deepcopy(InputDict['SPEC'])
                        for key, value in a.items():
                            TempDict[key] = value
                        self.addSpecies(**TempDict)
                else:
                    TempDict = copy.deepcopy(InputDict['SPEC'])
                    for key, value in CaseDict['SPEC'].items():
                        TempDict[key] = value
                    self.addSpecies(**TempDict)

            if 'MAT' in CaseDict.keys():
                if type(CaseDict['MAT'])==list:
                    for a in CaseDict['MAT']:
                        TempDict = copy.deepcopy(InputDict['MAT'])
                        for key, value in a.items():
                            TempDict[key] = value
                        self.addMaterial(**TempDict)
                else:
                    TempDict = copy.deepcopy(InputDict['MAT'])
                    for key, value in CaseDict['MAT'].items():
                        TempDict[key] = value
                    self.addMaterial(**TempDict)

            if 'SURF' in CaseDict.keys():
                if type(CaseDict['SURF'])==list:
                    for a in CaseDict['SURF']:
                        TempDict = copy.deepcopy(InputDict['SURF'])
                        for key, value in a.items():
                            TempDict[key] = value
                        self.addSurf(**TempDict)
                else:
                    TempDict = copy.deepcopy(InputDict['SURF'])
                    for key, value in CaseDict['SURF'].items():
                        TempDict[key] = value
                    self.addSurf(**TempDict)

            if 'WALL' in CaseDict.keys():
                if type(CaseDict['WALL'])==list:
                    for a in CaseDict['WALL']:
                        TempDict = copy.deepcopy(InputDict['WALL'])
                        for key, value in a.items():
                            TempDict[key] = value
                        self.addWall(**TempDict)
                else:
                    TempDict = copy.deepcopy(InputDict['WALL'])
                    for key, value in CaseDict['WALL'].items():
                        TempDict[key] = value
                    self.addWall(**TempDict)

            if 'CTRL' in CaseDict.keys():
                if type(CaseDict['CTRL'])==list:
                    for a in CaseDict['CTRL']:
                        TempDict = copy.deepcopy(InputDict['CTRL'])
                        for key, value in a.items():
                            TempDict[key] = value
                        self.addCtrl(**TempDict)
                else:
                    TempDict = copy.deepcopy(InputDict['CTRL'])
                    for key, value in CaseDict['CTRL'].items():
                        TempDict[key] = value
                    self.addCtrl(**TempDict)

            if 'MOD' in CaseDict.keys():
                if type(CaseDict['MOD'])==list:
                    for a in CaseDict['MOD']:
                        TempDict = copy.deepcopy(InputDict['MOD'])
                        for key, value in a.items():
                            TempDict[key] = value
                        self.addMod(**TempDict)
                else:
                    TempDict = copy.deepcopy(InputDict['MOD'])
                    for key, value in CaseDict['MOD'].items():
                        TempDict[key] = value
                    self.addMod(**TempDict)

    def setMisc(self,**kwargs):
        """
        This function enable to change the Misc Object attributes value
        :param kwargs: any possible attribute of Misc Object
        :return: the new Misc Object with new values
        """
        for key, value in kwargs.items():
            setattr(self.Misc, key, value)

    def setExt(self,**kwargs):
        """
        This function enable to change the Ext Object attributes value
        :param kwargs: any possible attribute of Misc Object
        :return: the new Misc Object with new values
        """
        for key, value in kwargs.items():
            setattr(self.Ext, key, value)

    def addLoc(self,**kwargs):
        """
        This function enables to add a Loc Object with any attributes allocated related to Loc Object
        :param kwargs: any possible attribute of Loc Object
        :return: a now Loc Object, a message is raised if the Loc ID already exist, it wont be created
        """
        TempDict = copy.deepcopy(DefaultMathisInputDict['LOC'])
        for key, value in kwargs.items():
            TempDict[key] = value
        a = Loc(**TempDict)
        if a.ID in self.Loc.keys():
            return print('[INFO] - It seems that this LOC ID already exists : '+a.ID)
        self.Loc[a.ID] = a

    def addBranch(self,**kwargs):
        """
        This function enables to add a Branch Object with any attributes allocated related to Branch Object
        :param kwargs: any possible attribute of Branch Object
        :return: a now Branch Object, a message is raised if the Branch ID already exist, it wont be created
        """
        TempDict = copy.deepcopy(DefaultMathisInputDict['BRANCH'])
        for key, value in kwargs.items():
            TempDict[key] = value
        a = Branch(**TempDict)
        if a.ID in self.Branch.keys():
            return print('[INFO] - It seems that this BRANCH ID already exists : '+a.ID)
        self.Branch[a.ID] = a

    def addHSRC(self, **kwargs):
        """
        This function enables to add a HSRC Object with any attributes allocated related to HSRC Object
        :param kwargs: any possible attribute of HSRC Object
        :return: a now HSRC Object, a message is raised if the HSRC ID already exist, it wont be created
        """
        TempDict = copy.deepcopy(DefaultMathisInputDict['HSRC'])
        for key, value in kwargs.items():
            TempDict[key] = value
        a = HSRC(**TempDict)
        if a.ID in self.HSRC.keys():
            return print('[INFO] - It seems that this HSRC ID already exists : '+a.ID)
        self.HSRC[a.ID] = a

    def addPerson(self, **kwargs):
        """
        This function enables to add a Person Object with any attributes allocated related to Person Object
        :param kwargs: any possible attribute of Person Object
        :return: a now Person Object, a message is raised if the Person ID already exist, it wont be created
        """
        TempDict = copy.deepcopy(DefaultMathisInputDict['PERSON'])
        for key, value in kwargs.items():
            TempDict[key] = value
        a = Person(**TempDict)
        if a.ID in self.Person.keys():
            return print('[INFO] - It seems that this PERSON ID already exists : '+a.ID)
        self.Person[a.ID] = a

    def addSpecies(self, **kwargs):
        """
        This function enables to add a Species Object with any attributes allocated related to Species Object
        :param kwargs: any possible attribute of Species Object
        :return: a now Species Object, a message is raised if the Species ID already exist, it wont be created
        """
        TempDict = copy.deepcopy(DefaultMathisInputDict['SPEC'])
        for key, value in kwargs.items():
            TempDict[key] = value
        a = Species(**TempDict)
        if a.ID in self.Species.keys():
            return print('[INFO] - It seems that this SPECIES ID already exists : '+a.ID)
        self.Species[a.ID] = a

    def addMaterial(self, **kwargs):
        TempDict = copy.deepcopy(DefaultMathisInputDict['MAT'])
        for key, value in kwargs.items():
            TempDict[key] = value
        a = Material(**TempDict)
        if a.ID in self.Material.keys():
            return print('[INFO] - It seems that this MATERIAL ID already exists : '+a.ID)
        self.Material[a.ID] = a

    def addSurf(self, **kwargs):
        TempDict = copy.deepcopy(DefaultMathisInputDict['SURF'])
        for key, value in kwargs.items():
            TempDict[key] = value
        a = Surf(**TempDict)
        if a.ID in self.Surf.keys():
            return print('[INFO] - It seems that this SURF ID already exists : '+a.ID)
        self.Surf[a.ID] = a

    def addWall(self, **kwargs):
        TempDict = copy.deepcopy(DefaultMathisInputDict['WALL'])
        for key, value in kwargs.items():
            TempDict[key] = value
        a = Wall(**TempDict)
        if a.ID in self.Wall.keys():
            return print('[INFO] - It seems that this WALL ID already exists : '+a.ID)
        self.Wall[a.ID] = a

    def addCtrl(self, **kwargs):
        TempDict = copy.deepcopy(DefaultMathisInputDict['CTRL'])
        for key, value in kwargs.items():
            TempDict[key] = value
        a = Ctrl(**TempDict)
        if a.ID in self.Ctrl.keys():
            return print('[INFO] - It seems that this CTRL ID already exists : '+a.ID)
        self.Ctrl[a.ID] = a
    def addBound(self, **kwargs):
        TempDict = copy.deepcopy(DefaultMathisInputDict['BOUND'])
        for key, value in kwargs.items():
            TempDict[key] = value
        a = Bound(**TempDict)
        if a.ID in self.Bound.keys():
            return print('[INFO] - It seems that this BOUND ID already exists : '+a.ID)
        self.Bound[a.ID] = a

    def addMod(self, **kwargs):
        TempDict = copy.deepcopy(DefaultMathisInputDict['MOD'])
        for key, value in kwargs.items():
            TempDict[key] = value
        a = Mod(**TempDict)
        if a.ID in self.Mod.keys():
            return print('[INFO] - It seems that this MOD ID already exists : '+a.ID)
        self.Mod[a.ID] = a

    def MakeInputFile(self):
        """
        This function enables to build the .data file required to launch MATHIS either using the dll or using the standalone .exe application

        """
        if not self.Misc.JOBNAME.endswith('.data'): self.Misc.JOBNAME = self.Misc.JOBNAME+'.data'
        if self.Path2Case.endswith('.data'): self.Path2Case = self.Path2Case[:-5]
        file = CreateFile(self.Path2Case,self.Misc.JOBNAME)
        # Write the MISC
        Misc = self.Misc.getModifiedValues()
        CreateObj(file, 'MISC', **Misc)
        # Write the EXT
        try:
            Ext = self.Ext.getModifiedValues()
            CreateObj(file,'EXT', **Ext)
        except:
            CreateObj(file,'EXT')
        # Write the LOC
        WriteObject(file,'LOC', self.Loc)
        # Write the Bound
        WriteObject(file, 'BOUND', self.Bound)
        # Write the Branch
        WriteObject(file,'BRANCH', self.Branch)
        # Write the HSRC
        WriteObject(file,'HSRC', self.HSRC)
        # Write the Person
        WriteObject(file,'PERSON', self.Person)
        # Write the Species
        WriteObject(file,'SPEC', self.Species)
        # Write the Materials
        WriteObject(file,'MAT', self.Material)
        # Write the Surfaces
        WriteObject(file,'SURF', self.Surf)
        # Write the Walls
        WriteObject(file,'WALL', self.Wall)
        # Write the Ctrl
        WriteObject(file,'CTRL', self.Ctrl)
        # Write the Ctrl
        WriteObject(file,'MOD', self.Mod)

        #end of writing
        file.close()

    def run(self, ExternalProcess = False, Verbose = True):
        """
        This function enables to run the mathis case either using the dll of in an external process the external
        process option is used mainly for parallell computing when laucnhing a bunch of case but it requires the path
        to mathis.exe
        :param ExternalProcess : bool to use a check call cmd instead of the dll
        :param Verbose : computation progression given in consol or not

        """
        if ExternalProcess:
            os.chdir(self.Path2Case)
            print('Starting Case : ' + self.Misc.JOBNAME)
            try:
                # if mathis path is given
                if platform.system() == "Windows":
                    if not self.Path2Mathis.endswith('.exe'): self.Path2Mathis += '/Mathis.exe'
                else:
                    if not self.Path2Mathis.endswith('athis'): self.Path2Mathis += '/mathis'
                cmd = [self.Path2Mathis, os.path.join(self.Path2Case, self.Misc.JOBNAME), '-l']
                if Verbose:
                    if os.path.isfile(self.Path2Mathis): print('Simulation is using : '+ self.Path2Mathis)
                    check_call(cmd[:-1])
                else:
                    check_call(cmd, stdout=open(os.devnull, "w"), stderr=open(os.devnull, "w"))
                return 1
            except:
                try:
                    # if mathis is a global variable
                    cmd = ['mathis', os.path.join(self.Path2Case, self.Misc.JOBNAME), '-l']
                    if Verbose:
                        print('Simulation is using the executable set as global Variable')
                        check_call(cmd)
                    else:
                        check_call(cmd, stdout=open(os.devnull, "w"), stderr=open(os.devnull, "w"))
                    return 1
                except:
                    print(
                        'Humm, seems there is an issue with this case : '+self.Misc.JOBNAME+'.\n'
                        'Please check that your Case.Path2Mathis is given or that mathis.exe (or mathis in linux) is set as a global/system variable in your system.\n'
                        'If the problem persists, it means the mathis case has itself a singular error (see case.out file). \n')
                    return 0
        else:
            C_FILE_Path = self.Path2Case
            C_FILE = self.Misc.JOBNAME
            cpt = '--------------------'
            cpt1 = '                    '
            print('\nData file launched : ' + C_FILE)
            time.sleep(0.01)
            # lets go in the right folder and initialise connection with MATHIS
            os.chdir(C_FILE_Path)
            SmartMathis = pm.LoadDll(pm.__file__, C_FILE)
            time.sleep(0.01)
            TimeunitConverter = {'S': 1, 'M': 60, 'H': 3600, 'J': 86400, 'D': 86400}
            TimeUnit = self.Misc.TIMEUNIT[0]
            t = self.Misc.TETA0*TimeunitConverter[TimeUnit]
            dt = self.Misc.DTETA*TimeunitConverter[TimeUnit]
            t_final = self.Misc.TETAEND*TimeunitConverter[TimeUnit]
            start = time.time()
            while t < t_final:
                # Ask MATHIS to compute the current time step
                pm.solve_timestep(SmartMathis, t, dt)
                t = t + dt
                if Verbose:
                    done = t / t_final
                    print('\r', end='')
                    ptcplt = '.' if t % 2 else ' '
                    msg = cpt[:int(20 * done)] + ptcplt + cpt1[int(20 * done):] + str(round(100 * done, 1))
                    print('Computation completed by ' + msg + ' %', end='', flush=True)
            if Verbose:
                print('\n')
                print('CPUTime (sec) : '+str(round(time.time()-start,1)))
            pm.CloseDll(SmartMathis)
            time.sleep(0.01)

    def ReadResults(self, GiveDict = False, Vars = [], Steps = 1, StartTime = 0):
        """
        Function that fetch the results from reading the *.res and *.head files
        :param GiveDict: bool = True, results will be given in a dictionary format, = False results will be given as object with all possible variable as attributes
        :param Vars: List of variable that would be read only
        :param Steps: index growth to fetch data (every Steps withtin the data .res files), useful to get hours values for smaller time step's simulation
        :param StartTime : Start Time at which the results are to be kept
        :return: Results object or dictionary format
        """
        #check if results are available
        if not os.path.isfile(os.path.join(self.Path2Case,self.Misc.JOBNAME)):
            return print('[ERROR] - Hmmm, it seems that there are no result files in the case path. Use the Case.run() function to launch your case')
        FileList = os.listdir(self.Path2Case)
        Data = {}
        Headers = {}
        for file in FileList:
            if self.Misc.JOBNAME in file[:len(self.Misc.JOBNAME)]:
                if '.out' in file:
                    Warnings, CPUTime = readDotOutFile(self.Path2Case,file)
                    continue
                if '.head' in file :
                    header = readDataFile(self.Path2Case,file,'headers')
                    if header: Headers[file[len(self.Misc.JOBNAME) + 1:-5]] = header
                    continue
                if Vars:
                    if not [var for var in Vars if var in file]:
                        continue
                if '.res' in file[-4:]:
                    if file.endswith('ATEC.res'):
                        Data['ATEC'] = readDataFile(self.Path2Case,file,'ATEC')
                        continue
                    data,unit = readDataFile(self.Path2Case,file,'Data',IdxG = Steps, StartTime=StartTime)
                    Data[file[len(self.Misc.JOBNAME) + 1:-4]] = {'Data':data,'Unit':unit}
                if '.mesh' in file[-5:]:
                    Headers[file[len(self.Misc.JOBNAME)+1:-5]+'Mesh'] = ['x (m)']
                    data,unit =  readDataFile(self.Path2Case, file, 'Data')
                    Data[file[len(self.Misc.JOBNAME) + 1:-5]+'Mesh'] = {'Data':data,'Unit':unit}

        # Dict with all single variable as e key
        globalDict = {}
        for key in Data.keys():
            if 'Data' not in Data[key].keys(): continue
            if not Data[key]['Data'] : continue
            for subkey in Headers.keys():
                if subkey in key:
                    if len(key)>len(subkey):
                        if key[len(subkey)] == '_' :
                            for idx,name in enumerate(Headers[subkey]):
                                globalDict[key+'_'+name] = {'Data': Data[key]['Data'][idx+1], 'Time':Data[key]['Data'][0], 'Unit' : Data[key]['Unit']}
                    elif len(key) == len(subkey):
                        for idx, name in enumerate(Headers[subkey]):
                            if subkey=='ext':
                                unit = Data[key]['Unit'][:Data[key]['Unit'].find('value')] + name.replace('_',' ').replace('(','').replace(')','')
                                keyname = key + '_' + name.split('_')[0]
                            else:
                                unit = Data[key]['Unit']
                                keyname = key + '_' + name
                            try : globalDict[keyname] =  {'Data': Data[key]['Data'][idx+1], 'Time':Data[key]['Data'][0], 'Unit' : unit}
                            except : globalDict[keyname] = {'Data': Data[key]['Data'][idx], 'Unit' : unit} # for the mesh file, there is no time column
        try :
            globalDict['Warnings'] = Warnings
            globalDict['CPUTime'] = CPUTime
        except: pass
        try : globalDict['ATEC'] = Data['ATEC']
        except: pass
        # Dict with variable type dict with keys of variable
        globDict = {}
        for key in Data.keys():
            if 'Data' not in Data[key].keys(): continue
            if not Data[key]['Data']: continue
            header_key = []
            for head in Headers.keys():
                if head in key and len(Headers[head])>0:
                    if len(key)>len(head):
                        if key[len(head)] == '_':
                            header_key = head
                    elif len(key)==len(head): header_key = head
            if not header_key : continue
            globDict[key] = {}
            if len(Data[key]) <= 1:
                globDict[key] = Data[key]['Data'][0]
                continue
            if 'Mesh' in key: globDict[key]['Data'] = Data[key]['Data'][0]
            else: globDict[key]['Time'] = Data[key]['Data'][0]
            globDict[key]['Unit'] = Data[key]['Unit']
            for idx,var in enumerate(Data[key]['Data'][1:]):
                globDict[key][Headers[header_key][idx]]=var
        try:
            globDict['Warnings'] = Warnings
            globDict['CPUTime'] = CPUTime
        except: pass
        try: globDict['ATEC'] = globalDict['ATEC'] = Data['ATEC']
        except: pass
        if GiveDict:
            return globDict
        else:
            return Results(**globalDict)

def readDotOutFile(Path,file):
    """
    Function that fecth the warning messages in the .out file
    :param Path: path to results folder
    :param file: file name
    :return: dictionary of warnings messages
    """
    Warnings = {'Time':[],'ITER':[], 'MAXLOC':[], 'MAXRES':[], 'Msg':[]}
    CPUTime = 0
    with open(os.path.join(Path, file), 'r') as f:
        lines = f.read()
    NBWarn = lines.split('WARNING')
    if len(NBWarn)>1: Warnings = fetchInfos(NBWarn, Warnings)
    NBWarn = lines.split('Flow Solver')
    if len(NBWarn)>1: Warnings = fetchInfos(NBWarn, Warnings, FlowCase=1)
    # lets fetch the total computation time
    for line in reversed(lines.split('\n')):
        if line.startswith('Calculation end'):
            try: CPUTime = float(line.split()[-2])
            except: CPUTime = -999
            break
        if line.startswith('Convergence problem'):
            CPUTime = -999
            break
    return Warnings, CPUTime

def fetchInfos(NbWarn,Warnings, FlowCase = 0):
    for idx,warn in enumerate(NbWarn[1:]):
        warnlines = warn.split('\n')
        if FlowCase:
            Warnings['Msg'].append('Flow Solver Issue')
            startingIndex = 0
        else:
            Warnings['Msg'].append(warnlines[0][2:])
            startingIndex = 1
        for warnline in warnlines[startingIndex:]:
            if len(warnline)==0:continue
            if warnline.startswith('Convergence problem'): break
            if warnline.startswith('t='):
                Warnings['Time'].append(warnline)
                break
            else:
                pattern = r'([^=]+)\s*=\s*([^\s]+)'
                matches = re.findall(pattern, warnline)
                matches = [(key.strip(), value) for key, value in matches]
                for ele in matches:
                    #ets remove the substring in bracket if present
                    try : SubKey = ele[0][:ele[0].index('(')]
                    except : SubKey = ele[0]
                    if SubKey in Warnings.keys():
                        Warnings[SubKey].append(ele[1])
                    else:
                        Warnings[SubKey] = [ele[1]]
    return Warnings

def getDefaultMathisValues():
    """
    fetch the defaults variables and values of mathis
    :return: dictionary of defaults attributes and values
    """
    loadDefault = True
    DefaultFileDir = os.path.dirname(pm.__file__)
    DefaultFilePath = os.path.join(DefaultFileDir, 'default.out')
    if platform.system() == "Windows": smartmathisName = "smartmathis.dll"
    else: smartmathisName = "smartmathis.so"
    if os.path.isfile(DefaultFilePath):
        # if time.ctime(os.path.getmtime('default.out'), "%Y-%m-%d %H:%M:%S") < time.ctime(os.path.getmtime(os.path.join(os.path.dirname(pm.__file__),'smartmathis.dll'))):
        if os.path.getmtime(DefaultFilePath) > os.path.getmtime(os.path.join(DefaultFileDir, smartmathisName)):
            loadDefault = False
    if loadDefault:
        if platform.system() == "Windows":
            cmd = ['python.exe', os.path.join(DefaultFileDir, 'getDefaultMathisVal.py')]
        else:
            cmd = ['python', os.path.join(DefaultFileDir, 'getDefaultMathisVal.py')]
        check_call(cmd, stdout=open(os.devnull, "w"), stderr=open(os.devnull, "w"),cwd=DefaultFileDir)
    outputDict = {}
    with open(DefaultFilePath, 'r') as f:
        lines = f.read()
    nbObj = lines.split('&')
    nbObj = nbObj[1:]
    for obj in nbObj:
        obj = obj.split('\n')
        key = obj[0].replace(' ','')
        outputDict[key] = {}
        finished = 0
        idx = 1
        while not finished:
            if key == 'PERSON' and idx == 6:
                att = obj[idx].replace(' ','').replace("'",'').replace('*','')+obj[idx+1].replace(' ','').replace("'",'').replace('*','')
                idx +=1
            elif key == 'PERSON' and idx == 9:
                att = obj[idx].replace(' ', '').replace("'", '') .replace('*','')+ obj[idx + 1].replace(' ', '').replace("'", '').replace('*','')+ \
                      obj[idx+2].replace(' ', '').replace("'", '').replace('*','')
                idx += 2
            else:
                att = obj[idx].replace(' ','').replace("'",'').replace('*','')
            if '/' in att :
                finished = 1
                break
            if not att or len(att)==1:
                idx +=1
                continue
            subkey = att.split('=')[0]
            value = att.split('=')[1]
            if value[-1] ==',': value = value[:-1]
            outputDict[key][subkey] = convert(subkey,value)
            idx += 1
    return outputDict

def readDataFile(path,file,Datatype,IdxG = 1,StartTime = 0):
    """
    function the reads the .res and .head file in the result folder.
    used in ReadResults()
    :param path: path to the result folder
    :param file: file name
    :param Datatype: if it's a head format or a data format
    :param IdxG: index steps to fetch values
    :param StartTime : starting time at which the results are to be kept
    :return:
    """
    with open(os.path.join(path, file), 'r') as f:
        lines = f.read()
    if 'headers' == Datatype:
        return [name for name in lines.split('\n') if name][1:]  # time is always in the first column
    elif 'Data' == Datatype:
        data = []
        Unit = ''
        for idx, line in enumerate(lines.split('\n')):
            if idx==0:
                Unit = line
            if idx>0 and line:
                if (idx-1) % IdxG != 0: continue #because time 0 correspond to line 1 !
                # lets skip the first line
                try:
                    values = [float(val) for val in line.split('  ') if val] # 2 spaces seems to be the separator
                except:
                    values = [float(val) for val in line.split('\t') if val]
                if values[0]>=StartTime:
                    data.append(values)
        return [list(i) for i in zip(*data)], Unit
    else:
        lines = lines.split('\n')
        ATEC = {lines[0].replace(':','') : float(lines[1])}
        for idx, line in enumerate(lines):
            if idx>1 and len(line)>2:
                test = line.split('\t')
                if len(test)==1:
                    key = line.replace(':','')
                    ATEC[key] = {}
                else:
                    if checkDataType(test[0])==str:
                        subkeys = test
                        ATEC[key] = {subkey:0 for subkey in subkeys}
                    else:
                        for ii,val in enumerate(test):
                            ATEC[key][subkeys[ii]] = val
        return ATEC

def checkDataType(data):
    output = str
    try:
        val = float(data)
        output = float
    except: pass
    return output



class Results():
    """
    Class object to store de results and make them easy to plot
    """

    def __init__(self, **data):
        for key, value in data.items():
            setattr(self, key, value)


#----------------------------------------------------------
## External functions to handle the building object methods
#----------------------------------------------------------

def loadExistingFile_old(file):
    """
    NO MORE USED, replaced by loadExistingFile(). its kept here for potential debug mode
    function that enables to load a previous case, it can still present issues as all format of handwritten older datacase cannot be considered
    :param file : fail name to load
    :return : dictionary of all object found to further convert those in mathis objects
    """
    outputDict = {}
    with open(file, 'r',encoding='utf-8-sig') as f:
        lines = f.read()
    nbObj = lines.split('&')
    for obj in nbObj:
        obj = obj.replace('\n',' ').replace('\t',' ')
        key = obj.split(' ')[0]
        if key =='MAT':
            a=1
        output = {}
        att = [tx for tx in obj[len(key)+1:obj.find('/')].replace('=',' = ').split(' ') if tx !='']
        finished = 0
        idx = 0
        while not finished:
            try:
                idxeq = att[idx:].index('=')+idx
                key1 = att[idxeq-1]
                try:
                    nidxeq = att[idxeq+1:].index('=')+idxeq+1
                    val = att[idxeq+1:nidxeq-1]
                except ValueError:
                    val = att[idxeq+1:]
                    finished = 1
                if len(val)==1:
                    val = val[0].replace("'",'')
                else:
                    val = ' '.join(val).replace(' ','')
                value = convert(key1,val)
                # additionnal checks for list with empty value
                if type(value)==list:
                    if [val for val in value if type(val)==str]:
                        valfiltered = [value[idx].replace("'",'') for idx in range(len(value)) if value[idx]] #this is for comma before nothing
                    else:
                        valfiltered = value # [val for val in value if val] because, the above filter fail only if float or int type
                    output[key1] = valfiltered[0] if len(valfiltered) == 1 else valfiltered
                else:
                    output[key1] = value
                idx = nidxeq-1
            except: finished = 1
        if key in outputDict.keys():
            if type(outputDict[key])==list: outputDict[key].append(output)
            else: outputDict[key] = [outputDict[key],output]
        else:
            outputDict[key] = output
    #before returning the full dict, some checks are to be done mostly for tables
    key2remove = []
    for key in outputDict.keys():
        if not outputDict[key]: key2remove.append(key)
    for key in key2remove: del outputDict[key]
    outputDict = check4Tables(outputDict)
    return outputDict


def loadExistingFile(file):
    """
    function that enables to load a previous case, it can still present issues as all format of handwritten older datacase cannot be considered
    :param file : fail name to load
    :return : dictionary of all object found to further convert those in mathis objects
    """
    outputDict = {}
    with open(file, 'r') as f:
        lines = [line.strip() for line in f if not line.startswith('*')]
    for line in lines:
        if line:
            if line[0]=='/':
                if key: outputDict = fillInOutputDict(outputDict,key,keyAtt)
                key = ''
                continue
            if line[0]=='&':
                key = line.split(' ')[0][1:]
                keyAtt = []
                line = line[len(key)+2:]
            att = [tx for tx in line.replace('=',' = ').replace('\t',' ').split(' ') if tx !='']
            for atti in att:
                if atti.endswith('/'):
                    keyAtt.append(atti[:atti.find('/')])
                    if key: outputDict = fillInOutputDict(outputDict, key, keyAtt)
                    key =''
                    break
                keyAtt.append(atti)
    # before returning the full dict, some checks are to be done mostly for tables
    key2remove = []
    for key in outputDict.keys():
        if not outputDict[key]: key2remove.append(key)
    for key in key2remove: del outputDict[key]
    outputDict = check4Tables(outputDict)

    return outputDict

def fillInOutputDict(outputDict,key,att):
    """
    fetch futur attributes for futur objects
    :param outputDict: output
    :param key: future object name
    :param att: attributes
    :return: outputdict updated
    """
    finished = 0
    idx = 0
    output = {}
    while not finished:
            try:
                idxeq = att[idx:].index('=')+idx
                key1 = att[idxeq-1]
                try:
                    nidxeq = att[idxeq+1:].index('=')+idxeq+1
                    val = att[idxeq+1:nidxeq-1]
                except ValueError:
                    val = att[idxeq+1:]
                    finished = 1
                if len(val)==1:
                    val = val[0].replace("'",'')
                else:
                    val = ' '.join(val).replace(' ','').replace("'",'')
                value = convert(key1,val)
                # additionnal checks for list with empty value
                if type(value)==list:
                    if [val for val in value if type(val)==str]:
                        valfiltered = [value[idx].replace("'",'') for idx in range(len(value)) if value[idx]] #this is for comma before nothing
                    else:
                        valfiltered = value # [val for val in value if val] because, the above filter fail only if float or int type
                    output[key1] = valfiltered[0] if len(valfiltered) == 1 else valfiltered
                else:
                    output[key1] = value
                idx = nidxeq-1
            except: finished = 1
    if key in outputDict.keys():
        if type(outputDict[key])==list: outputDict[key].append(output)
        else: outputDict[key] = [outputDict[key],output]
    else:
        outputDict[key] = output
    return outputDict

def convert(att,string):
    """String conversation function, used for previous .data files"""
    possible = [str, int, float]
    nonBoolAttribut = ['QUANTITY']
    for idx,func in enumerate(possible):
        try:
            result = func(string)
            ch = ['TRUE', '.TRUE.','T','T.']
            if string.upper() in ch and att not in nonBoolAttribut:
                return True
            ch = ['FALSE', '.FALSE.','F','F.']
            if string.upper() in ch and att not in nonBoolAttribut:
                return False
        except ValueError:
            continue
        if type(result) is not str and str(result) == string:
            return result
    #its means that we got a string (or several number seperated by a comma
    try:
        int(string[0]) # if pass, means that it's numbers with a comma in between
        idx = string.find(',')
        res = []
        idx0 = 0
        while idx != -1:
            res.append(float(string[idx0:idx+idx0].replace('D','E')))
            idx0 += idx + 1
            idx = string[idx0:].find(',')
        if res:
            #if idx0==len(string): return res[0]
            res.append(float(string[idx0:].replace('D','E')))
            return res
        else:
            return float(string.replace('D','E')) # it means that the string is a num with a simple '.' ending the string
    except:
        idx = string.find('(')
        if idx == -1:
            idx0 = string.find(',')
            if idx0 == -1: return string
            else: return string.split(',')

        else:
            return string[1:-1]


def check4Tables(dicti):
    """function that deals with tables, used for previous .data file"""
    for key in dicti.keys():
        if type(dicti[key])==list:
            for idx in range(len(dicti[key])):
                if [k for k in dicti[key][idx].keys() if k.find('(') != -1]:
                    dicti[key][idx] = developCoord(dicti[key][idx])
                    dicti[key][idx] = getCoord4Table(dicti[key][idx])
        else:
            if [k for k in dicti[key].keys() if k.find('(') != -1]:
                dicti[key] = developCoord(dicti[key])
                dicti[key] = getCoord4Table(dicti[key])
    return dicti

def developCoord(dct):
    a = [re.findall('\(([^)]*:.*[^)]*)\)', s) if ':' in s else [] for s in dct.keys()]
    MainKeys = list(dct.keys())
    for idx,coord in enumerate(a):
        if coord:
            mainKey = MainKeys[idx]
            key = mainKey[:MainKeys[idx].find('(')]
            startidx = int(coord[0][0:coord[0].find(':')])
            endidx = int(coord[0][coord[0].find(':')+1:coord[0].find(',')])
            yidx = int(coord[0][coord[0].find(',')+1:])
            for cpt in range(endidx-startidx+1):
                dct[key+'('+str(startidx+cpt)+','+str(yidx)+')'] = dct[mainKey][cpt]
            del dct[mainKey]
    return dct

def getCoord4Table(dct):
    """filling a matrix using brackets values inside a previous .data file, used for previous .data files"""
    a = [re.findall('\((.*?)\)', s) for s in dct.keys()]
    coord = []
    name = []
    for idx,sc in enumerate(a):
        if sc:
            key = list(dct.keys())[idx]
            if sc[0].find(',') !=-1 :
                coord.append((int(sc[0][:sc[0].find(',')]),int(sc[0][sc[0].find(',')+1:])))
            else :
                coord.append([int(sc[0])])
            name.append(key[:key.find('(')])
    uniqueName = list(set(name))
    import numpy as np
    for nm in uniqueName:
        rows = max([coord[idxn][0] for idxn, val in enumerate(name) if val == nm])
        if rows == 1: dct[nm] = 0
        else:
            try:
                cols = max([coord[idxn][1] for idxn, val in enumerate(name) if val == nm])
                dct[nm] = np.zeros((rows, cols))
            except:
                dct[nm] = [0]*rows
    for idx, cr in enumerate(coord):
        if rows == 1:
            dct[name[idx]] = dct[name[idx]+'('+str(cr[0])+')']
            del dct[name[idx] + '(' + str(cr[0]) + ')']
        else:
            try:
                dct[name[idx]][cr[0]-1,cr[1]-1] = dct[name[idx]+'('+str(cr[0])+','+str(cr[1])+')']
                del dct[name[idx]+'('+str(cr[0])+','+str(cr[1])+')']
            except:
                dct[name[idx]][cr[0]-1] = dct[name[idx]+'('+str(cr[0])+')']
                del dct[name[idx] + '(' + str(cr[0]) + ')']
    for nm in uniqueName:
        if type(dct[nm]) == np.ndarray: dct[nm] = list(map(tuple, dct[nm]))
    return dct

def WriteObject(file,type,OBJ):
    """function linked to the MakeInputFile function"""
    for a in OBJ.keys():
        b = OBJ[a].getModifiedValues()
        CreateObj(file, type, **b)

def write2file(file,header,kwargs):
    """
    This function is made to write the input data file needed for mathis. It's an internal function used in CreateObj()
    :param file: the opened object file
    :param header: the type of object concerned
    :param kwargs: list of attribute
    :return: none
    """
    line2write = '&'+header+' '
    for key, value in kwargs.items():
        if type(value) == str:
            line2write += " " + key + "='" + value +"'"
        elif type(value) == list:
            if type(value[0]) == str:
                line2write += " " + key + "='" + value[0] +"'"
                for val in value[1:]:
                    line2write += ",'"+val+"'"
            elif type(value[0]) == tuple:
                line2write = dealWithTuple(line2write,key,value)
            else:
                line2write += " " + key + "=" + str(value[0])
                for val in value[1:]:
                    line2write += ","+str(val)

        elif type(value) == tuple:
            line2write += " " + key + "=" + str(value[0]) + ',' + str(value[1])
        else:
            line2write += " " + key + "=" + str(value)
        line2write += ' \n'
    line2write += '  /\n'
    file.write(line2write)
    return file

def dealWithTuple(line2write, key, value):
    line2write += ' \n'
    for idx,cpl in enumerate(value):
        for idxy,val in enumerate(cpl):
            line2write += key +'('+str(idx+1)+','+str(idxy+1)+') = '+str(val)+'  '
        line2write += ' \n'
    return line2write


def CreateFile(Path2Case,filename):
    """
    This function create and open the file for the *.data
    :param filename: name of the *.data file
    :return: none
    """
    if not os.path.isdir(Path2Case):
        os.mkdir(Path2Case)
    else:
        for fname in os.listdir(Path2Case):
            if fname.startswith(filename):
                os.remove(os.path.join(Path2Case, fname))
    file = open(os.path.join(Path2Case,filename), 'w')
    return file

def CreateObj(file,Type,**kwargs):
    """
    This function is used to create the corresponding object in the *.data
    :param file: opened file
    :param Type: the type of object to create
    :param kwargs: list of attribute for the object to be created
    :return: the .*data file is appended by the created object with its attributes
    """
    file = write2file(file, Type, kwargs)
    return file

DefaultMathisInputDict = getDefaultMathisValues()


if __name__ == '__main__':
    '''This module creates object handled by mathis'''