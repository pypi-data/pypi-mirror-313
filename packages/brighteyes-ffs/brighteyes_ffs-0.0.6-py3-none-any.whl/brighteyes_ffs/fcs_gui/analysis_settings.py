#from functions.appearance import corr_long_label as cll
import numpy as np
import matplotlib.image as mpimg
import copy

#current = os.path.dirname(os.path.realpath('analysis_settings.py'))
#parent = os.path.dirname(current)
#sys.path.append(parent)

from ..fcs.fcs2corr import fcs_av_chunks, fcs_crosscenter_av
from ..fcs.fcs_polar import g2polar

"""
==============================================================================
FFSlib = [FFSexp1, FFSexp2, FFSexp3, etc.] with each element corresponding to 
one FFS experiment, i.e. 1 2d image and multiple FFS measurements
    
    FFSexp1 = [FFSfile1, FFSfile2, FFSfile3, etc.] with each element
    corresponding to one FFS measurement

FFSlib
     -> FFSexp: image
         -> FFSfile: single spot measurement
             -> metadata
             -> analysis
==============================================================================
"""

class FFSlib:
    # FFSlib is the main data object, it contains all images,
    # each of which may contain multiple FFS experiments,
    # each of which may contain multiple analyses.
    # Each image is an FFSexperiment object
    def __init__(self):
        self.lib = []
        self.activeImage = None
        self.version = '1.0'
        self.notes = ''
        self.dateCreated = ''
        self.dateModified = ''
    
    @property
    def nrImages(self):
        return len(self.lib)
    
    def addImage(self, image, fname, mdata=None):
        newImageObj = FFSimage()
        newImageObj.imageName = fname
        newImageObj.image = image
        if mdata is not None:
            newImageObj.imageMetadata = mdata
        newImageObj.imageRaw = image # may be deleted
        self.lib.append(newImageObj)
    
    def addRandomImage(self):
        self.addImage(np.zeros((5,5)), 'no_image_added')
    
    def getImage(self, imageNr='active'):
        # return the imageNr-th image object from the library
        # by default return current image object
        if isinstance(imageNr, str) and imageNr == 'active':
            imageNr = self.activeImage
        if imageNr is None or self.nrImages < 1:
            return None
        if imageNr > -1:
            imageNr = np.min((imageNr, self.nrImages-1))
        image = self.lib[imageNr]
        return image
    
    def removeImage(self, imageNr='active'):
        if imageNr == 'active':
            imageNr = self.activeImage
        if imageNr is not None and imageNr < self.nrImages:
            del self.lib[imageNr]
            if self.nrImages == 0:
                self.activeImage = None
            else:
                self.activeImage = 0
    
    def getImageName(self, imageNr):
        image = self.getImage(imageNr)
        if image is None:
            return "No images added yet."
        return image.imageName
    
    def returnImage(self, imageNr=-1):
        # return the imageNr-th image from the library
        image = self.getImage(imageNr)
        if image is None:
            return mpimg.imread('files/Cells_DEKegfp_75x75um.jpg')
        return image.image
    
    
class FFSimage:
    # FFSimage contains everything related to a single 2D image
    def __init__(self):
        self.imageName = "" # path to image
        self.imageMetadata = FFSmetadata() # image 
        self.image = None
        self.imageRaw = None
        self.ffsList = [] # empty list that will be filled with FFSfile objects
        self.activeFFS = None
    
    @property
    def nrfiles(self):
        # return the number of FFS files for image
        return len(self.ffsList)
    
    def update(self, imageName=None, image=None, ffsList=None):
        if imageName is not None:
            self.imageName = imageName
        if image is not None:
            self.image = image
        if ffsList is not None:
            self.ffsList = ffsList
    
    def addFFSfile(self, FFSfileObj):
        self.ffsList.append(FFSfileObj)
    
    def remove_ffs_file(self, fileNr):
        if fileNr is not None and fileNr < self.nrfiles:
            del self.ffsList[fileNr]
            
    def getFFSfile(self, fileNr='active'):
        if type(fileNr) == str and fileNr == 'active':
            fileNr = self.activeFFS
        if fileNr is not None and fileNr < self.nrfiles:
            return self.ffsList[fileNr]
        return None
    
    def printImageMetadata(self):
        txt = ''
        for prop in ['numberOfPixels', 'numberOfLines', 'rangeX', 'dwellTime', 'pxsize']:
            propvalue = getattr(self.imageMetadata, prop)
            if propvalue is not None:
                if prop == 'numberOfPixels':
                    txt += str(int(propvalue))
                if prop == 'numberOfLines':
                    txt += ' x ' + str(int(propvalue)) + ' pixels\n'
                if prop == 'rangeX':
                    txt += str(int(propvalue)) + ' x ' + str(int(propvalue)) + ' um\n'
                if prop == 'dwellTime':
                    txt += 'Dwelltime: ' + str(int(1e6*propvalue)) + ' us\n'
                if prop == 'pxsize':
                    txt += 'Pixel size: ' + "{:.3f}".format(propvalue) + ' um\n'
                
        return txt
        
        

class FFSfile:
    # each FFS file for each image contains a single FFSfile object
    def __init__(self):
        self.fname = "" # path to file
        self.label = None # file nick name
        self.metadata = FFSmetadata()
        self.analysisList = [] # list of correlations to calculate
        self.timetrace = None
        self.airy = None
        self.activeAnalysis = None # choose which analysis is active by default
    
    @property
    def nrAnalyses(self):
        return len(self.analysisList)
    
    @property
    def coords(self):
        return self.metadata.coords
    
    @property
    def duration(self):
        return self.metadata.duration
    
    @property
    def numberofelements(self):
        if self.timetrace is None:
            return None
        if len(np.shape(self.timetrace)) > 1:
            # 2 dimensions
            return np.shape(self.timetrace)[1]
        else:
            return len(self.timetrace)
    
    def addAnalysis(self, mode, resolution=10, chunksize=10, algorithm='multipletau', chunksOff="allon", activeAnalysis=-1):
        FFScorrObj = FFScorr()
        duration = self.metadata.duration
        if activeAnalysis == -1:
            self.activeAnalysis = self.nrAnalyses
        else:
            self.activeAnalysis = activeAnalysis
        if chunksOff == "allon":
            chunksOff = np.ones(np.clip(int(np.floor(duration / chunksize)), 1, None))
        FFScorrObj.analysis(mode, resolution, chunksize, chunksOff, algorithm)
        self.analysisList.append(FFScorrObj)
    
    def remove_analysis(self, anNr):
        if anNr is not None and anNr < self.nrAnalyses:
            del self.analysisList[anNr]
            if self.nrAnalyses == 0:
                self.activeAnalysis = None
            else:
                self.activeAnalysis = np.min((self.nrAnalyses-1, self.activeAnalysis))
    
    def copy_correlation(self, anNr):
        # get analysis
        an_orig = self.getanalysis(analysisNr=anNr)
        if an_orig is None:
            return
        # copy analysis and fit
        self.analysisList.append(copy.deepcopy(an_orig))
        an = self.getanalysis(analysisNr=self.nrAnalyses-1)
        # remove all fits
        for i in range(an.nrFits):
            an.remove_fit(0)
    
    def use_fit_as_data(self, anNr, fitNr):
        # get analysis and fit object
        an_orig = self.getanalysis(analysisNr=anNr)
        if an_orig is None:
            return
        fits = copy.deepcopy(an_orig.returnFitObj(fitNr=fitNr))
        if fits is None:
            return
        # copy analysis and fit
        self.analysisList.append(copy.deepcopy(an_orig))
        an = self.getanalysis(analysisNr=self.nrAnalyses-1)
        # remove all fits
        for i in range(an.nrFits):
            an.remove_fit(0)
        # fill correlation analysis with fit as correlation data
        elements = an.settings.elements # central, sum3x3, sum5x5
        for element in elements:
            Gsingle = an.getCorr(element)
            fit = fits.fitAllCurves
            if Gsingle is not None and fit[0].fitfunctionLabel not in ['Model-free displacement analysis', 'Mean squared displacement']:
                for j in range(len(fit)):
                    if element == fit[j].data:
                        # fit found, add fitres to all chunks
                        for c in range(int(an.nrchunks(duration=self.metadata.duration))):
                            Gchunk = an.getCorr(element + '_chunk' + str(c))
                            fitres = fit[j].fitresult
                            fitrange = fit[j].fitrange
                            start = fitrange[0]
                            stop = fitrange[1]
                            xout = Gchunk[start:stop, 0]
                            yout = Gchunk[start:stop, 1] - fitres
                            Gout = np.zeros((len(xout), 2))
                            Gout[:,0] = xout
                            Gout[:,1] = yout
                            setattr(an.corrs, element + '_chunk' + str(c), Gout)
                            an.settings.update(chunksOff=an.settings.chunksOff, analysis=an)
                            
                        
    
    def getanalysis(self, analysisNr=-1):
        if analysisNr == -1:
            # return active analysis
            analysisNr = self.activeAnalysis
        if analysisNr is not None and analysisNr < self.nrAnalyses:
            return self.analysisList[analysisNr]
        return None
    
    def update(self, fname=None, label=None, coords=None, timetrace=None, airy=None, activeAnalysis=None):
        if label is not None:
            self.label = label
        if coords is not None:
            self.metadata.coords = coords
        if timetrace is not None:
            self.timetrace = timetrace
        if airy is not None:
            self.airy= airy
        if activeAnalysis is not None:
            if activeAnalysis == 'None':
                activeAnalysis = None
            self.activeAnalysis = activeAnalysis


class FFSmetadata:
    def __init__(self,
                 numberOfPixels = None,
                 numberOfLines = None,
                 numberOfFrames = None,
                 rangeX = None,
                 rangeY = None,
                 rangeZ = None,
                 numberOfDataPoints = None,
                 holdOffx5 = None,
                 holdOff = None,
                 timeResolution = None,
                 dwellTime = None,
                 duration = None,
                 pxsize = None,
                 coords = None
                 ):
        self.numberOfPixels = numberOfPixels
        self.numberOfLines = numberOfLines
        self.numberOfFrames = numberOfFrames
        self.rangeX = rangeX # µm
        self.rangeY = rangeY # µm
        self.rangeZ = rangeZ # µm
        self.numberOfDataPoints = numberOfDataPoints
        self.holdOffx5 = holdOffx5 # ns
        self.holdOff = holdOff # ns
        self.timeResolution = timeResolution # µs
        self.dwellTime = dwellTime # s
        self.duration = duration # s
        self.pxsize = pxsize # µm
        self.coords = coords # row, column number [y, x] of FFS position


class FFScorr:
    # for each file multiple FFScorr analysis objects can be added for different
    # types of analyses, e.g. spot-variation, iMSD, etc.
    def __init__(self):
        self.mode = None
        self.settings = CorrSettings()
        self.corrs = None
        self.fits = [] # list with fit results
        self.activeFit = None # choose which fit to show by default
    
    @property
    def NcurvesMode(self):
        return len(self.settings.elements)
    
    @property
    def nrFits(self):
        return len(self.fits)
    
    def analysis(self, correlationObj, resolution, chunksize, chunksOff, algorithm, activeFit=-1, detType='Genoa Instruments 5x5'):
        self.mode = correlationObj.mode
        
        self.settings.elements = correlationObj.elements
        self.settings.listOfG = correlationObj.listOfG
        self.settings.average = correlationObj.average
        
        self.settings.resolution = resolution
        self.settings.algorithm = algorithm
        self.settings.chunksize = chunksize # s
        self.settings.chunksOff = chunksOff
        if activeFit == -1:
            activeFit = self.nrFits
        self.activeFit = activeFit
    
    def nrchunks(self, duration):
        if duration is not None:
            N = int(np.floor(duration / self.settings.chunksize))
            return N
        return None
    
    def remove_fit(self, fitNr):
        if fitNr is not None and fitNr < self.nrFits:
            del self.fits[fitNr]
            if self.nrFits == 0 or self.activeFit is None:
                self.activeFit = None
            else:
                self.activeFit = np.min((self.nrFits-1, self.activeFit))
    
    def returnFitObj(self, fitNr=-1):
        # by default return active fit object
        f = self.fits
        if fitNr == -1:
            fitNr = self.activeFit
        if fitNr is not None and len(f) > fitNr:
            return f[fitNr]
        return None
    
    def getCorr(self, corrtype="random"):
        # return average correlation central, sum3x3, sum5x5, etc.
        Gall = self.corrs
        if Gall is None:
            return None
    
        keys = list(Gall.__dict__.keys())
    
        if corrtype == "random":
            keys = list(Gall.__dict__.keys())
            keys.remove("dwellTime")
            try:
                keys.remove("crossCenterAv")
            except:
                pass
            try:
                keys.remove("chunksOff")
            except:
                pass
            Gsingle = getattr(Gall, keys[0])
        elif 'crossCenterAv' in corrtype:
            if 'chunk' in corrtype:
                chunk = corrtype[len('crossCenterAv'):]
                Gsingle = fcs_crosscenter_av(Gall, returnField=chunk, returnObj = False)
            else:
                Gsingle = fcs_crosscenter_av(Gall, returnObj = False)
        else:
            try:
                Gsingle = getattr(Gall, corrtype + "_averageX")
            except:
                try:
                    Gsingle = getattr(Gall, corrtype + "_average")
                except:
                    Gsingle = getattr(Gall, corrtype)
        return Gsingle
    
    def analysisSummary(self):
        return self.mode + " " + str(self.settings.resolution) + "/" + str(self.settings.chunksize)
    
    def calcCorr(self):
        # calculate correlation only if not yet calculated before
        if self.corrs is None:
            return True
        return False
    
    def update(self, mode=None, settings=None, corrs=None, fits=None, activeFit=None):
        # mainly used to store calculated correlations in analysis object
        if mode is not None:
            self.mode = mode
        if settings is not None:
            self.settings = settings
        if corrs is not None:
            self.corrs = corrs
        if fits is not None:
            self.fits = fits
        if activeFit is not None:
            # use activeFit = 'None' to set active fit to None
            if activeFit == 'None':
                activeFit = None
            self.activeFit = activeFit
    
    def corrParam(self):
        # return all parameters needed to perform autocorrelation calculation
        return self.mode, self.settings.resolution, self.settings.chunksize
    
    def addFitAnalysis(self, fitfunctionmodel, fitarray, startvalues, fitrange=[1, -1]):
        # fitarray has length 12 (11 parameters + weighted fit)
        mode = self.mode
        modelname = fitfunctionmodel.model
        if any(fitarray) > 0 or modelname in ['Maximum entropy method free diffusion', 'Flow heat map', 'Model-free displacement analysis']:
            corrFitObj = CorrFit()
            corrFitObj.fitAnalysis(mode, fitfunctionmodel, fitarray, startvalues, fitrange, self.settings.elements)
            self.fits.append(corrFitObj)
            self.activeFit = self.nrFits - 1
    
    def update_fit_analysis(self, fitfunctionmodel, fitarray, startvalues, fitrange=[1, -1], fitNr=-1):
        mode = self.mode
        if fitNr == -1:
            fitNr = self.activeFit
        if any(fitarray) > 0 or fitfunctionmodel.model in ['Maximum entropy method free diffusion', 'Flow heat map', 'Model-free displacement analysis']:
            corrFitObj = self.fits[fitNr]
            corrFitObj.fitAllCurves = [] # empty the object and fill it from scratch
            corrFitObj.fitAnalysis(mode, fitfunctionmodel, fitarray, startvalues, fitrange, self.settings.elements)
                    
        
class CorrSettings():
    def __init__(self):
        self.elements = None # fields that are returned by fcs2corr
        self.listOfG = None # what is sent to fcs2corr
        self.resolution = None
        self.algorithm = None
        self.chunksize = None
        self.chunksOff = None
        self.average = None # which cross-correlations should be averaged for flow analysis
    
    def update(self, elements=None, resolution=None, chunksize=None, chunksOff=None, analysis=None, algorithm=None, listOfG=None):
        if elements is not None:
            self.elements = elements
        if listOfG is not None:
            self.listOfG = listOfG
        if algorithm is not None:
            self.algorithm = algorithm
        if resolution is not None:
            self.resolution = resolution
        if chunksize is not None:
            self.chunksize = chunksize
        if chunksOff is not None:
            # if chunksOff is changed, also the average correlation is changed
            self.chunksOff = chunksOff
            G = analysis.corrs
            idx = np.nonzero(chunksOff)
            idx = list(idx[0]) # list of indices of good chunks
            try:
                G = fcs_av_chunks(G, idx)
                try:
                    G = fcs_crosscenter_av(G, returnField='_averageX')
                except:
                    pass
                analysis.update(corrs=G)
            except:
                pass
            

class CorrFit():
    def __init__(self):
        self.fitAllCurves = [] # list with each element consisting of 3 objects with fits for central, sum3, sum5
    
    @property
    def Nfitcurves(self):
        return len(self.fitAllCurves)

    def returnField(self, field):
        if field == "fitAllCurves":
            return self.fitAllCurves
        if field == "w0":
            w0 = []
            Ncurves = len(self.fitAllCurves)
            for i in range(Ncurves):
                w0.append(self.fitAllCurves[i].w0)
            return w0
        if field == "D":
            D = []
            Ncurves = len(self.fitAllCurves)
            for i in range(Ncurves):
                D.append(self.fitAllCurves[i].D)
            return D
        fits = self.fitAllCurves
        if len(fits) == 0:
            return None
        return fits[0].returnField(field)
    
    def returnAll(self, field):
        fits = self.fitAllCurves
        if len(fits) == 0:
            return None
        data = []
        for i in range(len(fits)):
            data.append(getattr(fits[i], field))
        
        return data
    
    def fitrange(self):
        fits = self.fitAllCurves
        if len(fits) == 0:
            return None
        fit = fits[0]
        return fit.fitrange
    
    def fitresults(self, returntype="string"):
        # return 12 fit start values for the (3) fcs curves, either as strings or as 2d array
        Ncurves = len(self.fitAllCurves)
        Nparam = 12
        stv = ["NaN" for j in range(Nparam)]
        bls = [False for j in range(Nparam)]
        fitfunction = None
        fitresArray = np.zeros((Nparam, Ncurves))
        for i in range(Ncurves):
            fit = self.fitAllCurves[i]
            fitfunction = fit.fitfunctionLabel
            power10 = fit.paramFactors10
            for j in range(len(fit.paramidx)):
                fitabsv = fit.startvalues[fit.paramidx[j]] / power10[j]
                fitresArray[j, i] = fitabsv
                if np.abs(fitabsv) < 1e-2 or np.abs(fitabsv) > 999:
                    fitresString = str(fitabsv)[0:10]
                else:
                    fitresString = str(fitabsv)[0:4]
                if i == 0:
                    stv[j] = fitresString
                else:
                    stv[j] += fitresString
                if i < Ncurves - 1:
                    stv[j] += ", "
                bls[j] = bool(fit.fitarray[fit.paramidx[j]])
        bls[-1] = bool(fit.fitarray[-1])
        if returntype == "string":
            return [stv, bls, fitfunction]
        else:
            return fitresArray
    
    def fitresultsMFDA(self):
        # return scatter plot for model-free displacement analysis
        Ncurves = len(self.fitAllCurves)
        N = 5 # pixels per dimension
        difftimesarray = np.zeros((N, N))
        corrvarray = np.ones((N, N))
        Nfound = 0
        for vert in range(N):
            for hor in range(N):
                # find the right fit
                for c in range(Ncurves):
                    if self.fitAllCurves[c].data == 'V'+str(vert-int(np.floor(N/2)))+'_H'+str(hor-int(np.floor(N/2))):
                        fitr = self.fitAllCurves[c].fitresult
                        difftimesarray[vert, hor] = self.fitAllCurves[c].fitresult[0]
                        if len(fitr) > 1:
                            corrvarray[vert, hor] = self.fitAllCurves[c].fitresult[1]
                        Nfound += 1
        if Nfound > 0:
            return difftimesarray, corrvarray
        
        return None
    
    def fitresultsFlowMap(self):
        # return radial distributions for flow heat map
        Ncurves = len(self.fitAllCurves)
        fit = self.fitAllCurves[-1] # color as a function of radius
        
        if fit.fitresult is None:
            return
        
        N = int(len(fit.fitresult))
        columnorder = ['Right', 'Up', 'Left', 'Down']
        allfits = np.zeros((N, len(columnorder)))
        columnNotFound = False
        for i in range(Ncurves):
            try:
                c = columnorder.index(self.fitAllCurves[i].data)
                allfits[:, c] = self.fitAllCurves[i].fitresult
            except:
                columnNotFound = True
        
        if columnNotFound:
            return np.zeros((5,5)), [0,0], columnNotFound
        
        z, flow = g2polar(allfits)
        u = 2*flow[0]
        r = 2*flow[1]
    
        return z, [r, u], columnNotFound
    
    def fitresultsMEM(self, tau, nparam=5):
        # return diffusion times distributions for MEM fit
        Ncurves = len(self.fitAllCurves)
        fit0 = self.fitAllCurves[0]
        
        taumin = np.log10(tau[fit0.fitrange[0]])
        taumax = np.log10(tau[fit0.fitrange[1]-1])
        tauD = np.logspace(taumin, taumax, len(fit0.startvalues[0:-nparam]))
        
        fitresArray = np.zeros((len(tauD), Ncurves))
        for i in range(Ncurves):
            fit = self.fitAllCurves[i]
            fitresArray[:, i] = fit.startvalues[0:-nparam]
        
        fit = self.fitAllCurves[0]
        power10 = fit.paramFactors10
        Nparam = 12
        stv = ["NaN" for j in range(Nparam)]
        bls = [False for j in range(Nparam)]
        for j in range(len(fit.paramidx)):
            fitabsv = fit.startvalues[-1-nparam+fit.paramidx[j]] / power10[j]
            stv[j] = fitabsv
            bls[j] = bool(fit.fitarray[fit.paramidx[j]])
        stv[0] = len(tauD)
        
        return fitresArray, tauD, stv, bls
    
    def fitresultsMSD(self):
        fit0 = self.fitAllCurves[0]
        D = fit0.startvalues[0]
        rho = 1e-3 * fit0.startvalues[3] # µm
        slope = 2 / rho**2 * D
        offset = fit0.startvalues[1]
        tauvar = fit0.fitresult
        tau = tauvar[0]
        var = tauvar[1]
        varfit = tau * slope + offset
        
        return tau, var, varfit
            
    def fitAnalysis(self, mode, fitmodel, fitarray, startvalues, fitrange=[1, -1], data=[]):
        for i in range(len(data)):
            self.fitAllCurves.append(FitSingleObj(data[i], fitmodel, fitarray, startvalues[:,i], fitrange))
    
class FitSingleObj:
    def __init__(self, data, fitmodel, fitarray, startvalues, fitrange):
        # fitmodel is an object of the class fitModels
        
        Nparam = fitmodel.Nparam + 1 # weighted fit
        self.minbound = np.array(fitmodel.paramMinbound)
        self.maxbound = np.array(fitmodel.paramMaxbound)
        self.paramFactors10 = np.array(fitmodel.paramFactors10)
        self.data = data # central, sum3, sum5, etc.
        self.fitfunctionLabel = fitmodel.model # more readable name of the fit function
        self.fitrange = fitrange
        self.fitresult = None # fit residuals
        
        paramind = fitmodel.fitfunctionParamUsed
        
        self.fitfunction = fitmodel.fitfunctionName # fit function used for the calculation (not a string but a function)
        fitarrayTemp = np.array([False for i in range(Nparam)])
        startvTemp = np.array(fitmodel.allparamDefvalues).astype(float)
        if paramind is not None:
            for i in range(len(paramind)):
                fitarrayTemp[paramind[i]] = fitarray[i]
                startvTemp[paramind[i]] = float(startvalues[i]) * fitmodel.paramFactors10[i]
            fitarrayTemp[Nparam-1] = fitarray[-1]
        else:
            fitarrayTemp = None
            startvTemp = None
        
        self.fitarray = fitarrayTemp
        self.startvalues = startvTemp
        self.paramidx = paramind # array indices with the parameters of interest (for startvalues and fitarray)
        self.w0 = None # beam waist (nm)
        self.D = None # diffusion coefficient (µm^2/s)
    
    def update(self, fitresult=None, startvalues=None, w0=None, D=None):
        # start values contains two lists [startv, fitv]
        # with startv containing the start values of both the fitted and unfitted parameters
        # fitv the 
        # start values are [M x 1] vector with M the 12 (or 7 for circFCS) fit parameters
        if fitresult is not None:
            self.fitresult = fitresult
        if startvalues is not None:
            self.startvalues = startvalues
        if w0 is not None:
            self.w0 = w0
        if D is not None:
            self.D = D