"""
Fitmodels fields:
    model                   str                 name of the model
    paramNames              list of str         names of the parameters
    paramDefvalues          list of numbers     default values for the parameters
    allparamDefvalues       list of numbers     default values for all parameters that the function requires
    fitfunctionParamUsed    list of numbers     indices of the parameters of the fit function that are actually used
    paramFactors10          list of numbers     powers of 10 with which the parameters have to be multiplied
    paramMinbound           list of numbers     minimum values for all parameters (must already include factors of 10)
    paramMaxbound           list of numbers     maximum values for all parameters (must already include factors of 10)
    fitfunctionName         function            name of the fit function
    
    Example: a fit function f(a, b, c, d) has 4 input parameters but parameter c must always be set to 3.14 in a given model
    Then:   paramNames  = ['a', 'b', 'd']
            paramDefvalues = [3, 9.2, -4] # default values for parameters a, b, d
            allparamDefvalues = [-1, -1, 3.14, -1] # set c to 3.14 and all other parameters to -1
            fitfunctionParamUsed = [0, 1, 3] # only parameters 0, 1, and 3 are used for the fit model
"""

class FitModel:
    def __init__(self):
        self.model = None
        self.shortlabel = None
        self.paramNames = None
        self.paramFittable = None
        self.paramDefvalues = None
        self.allparamDefvalues = None
        self.paramFactors10 = None
        self.paramMinbound = None
        self.paramMaxbound = None
        self.fitfunctionName = None
        self.fitfunctionParamUsed = None
    
    def set_params(self, params):
        self.model                  = params.get("model")
        self.shortlabel             = params.get("shortlabel")
        self.paramNames             = params.get("paramNames")
        self.paramFittable          = params.get("paramFittable")
        self.paramDefvalues         = params.get("paramDefvalues")
        self.allparamDefvalues      = params.get("allparamDefvalues")
        self.paramFactors10         = params.get("paramFactors10")
        self.paramMinbound          = params.get("paramMinbound")
        self.paramMaxbound          = params.get("paramMaxbound")
        self.fitfunctionName        = params.get("fitfunctionName")
        self.fitfunctionParamUsed   = params.get("fitfunctionParamUsed")
            
    
    def returnfitparam(self):
        return self.model, self.paramNames, self.paramDefvalues, self.fitfunctionName, self.fitfunctionParamUsed, self.paramFactors10, self.paramMinbound, self.paramMaxbound

    @property
    def Nparam(self):
        if self.fitfunctionName is None and self.allparamDefvalues is None:
            return 1
        if self.model == 'Free diffusion pair-correlation (global fit)':
            return 26
        return(len(self.paramMinbound))
