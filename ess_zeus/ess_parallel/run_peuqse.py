import PEUQSE
import PEUQSE.UserInput

import dill


if __name__ == "__main__":
    import observed_values_00  #Just a simple example. The user can also put the values in directly into the runfile or extract from a csv, for example.
    import simulation_model_00 #Simple example.
        
    #Provide the observed X values and Y values and uncertainties -- all should be arrays or lists with nesting like [[1,2,3]] or [[1,2,3,4],[4,5,6,6]]
    PEUQSE.UserInput.responses['responses_abscissa'] = observed_values_00.observed_data_x_values
    PEUQSE.UserInput.responses['responses_observed'] = observed_values_00.observed_data_y_values
    PEUQSE.UserInput.responses['responses_observed_uncertainties'] = observed_values_00.observed_data_y_values_uncertainties
   
    #Optional: provide labels for the responses axes and parameter names.
    PEUQSE.UserInput.simulated_response_plot_settings['x_label'] = 'distance (m)'
    PEUQSE.UserInput.simulated_response_plot_settings['y_label'] = r'$time (s)$'
    PEUQSE.UserInput.model['parameterNamesAndMathTypeExpressionsDict'] = {'a':'a','b':'b'}
    
    #Provide the prior distribution and uncertainties of the individual parameters.
    PEUQSE.UserInput.model['InputParameterPriorValues'] = [200, 500] #prior expected values for a and b
    PEUQSE.UserInput.model['InputParametersPriorValuesUncertainties'] = [100, 200] #required. #If user wants to use a prior with covariance, then this must be a 2D array/ list. To assume no covariance, a 1D
    #UserInput.model['InputParameterInitialGuess'] = [150,400] #Can optionally change the initial guess to be different from prior means.

    #Provide a function that returns simulated values -- must of the same form as observed values, should be arrays or lists with nesting like [[1,2,3]] or [[1,2,3,4],[4,5,6,6]]
    PEUQSE.UserInput.model['simulateByInputParametersOnlyFunction'] = simulation_model_00.simulation_function_wrapper #This must simulate with *only* the parameters listed above, and no other arguments.

    #mcmc length should typically be on the order of 10,000 per parameter. By default, the burn in will be the first 10% of the mcmc length.
    PEUQSE.UserInput.parameter_estimation_settings['mcmc_length'] = 100 #10000 is the default.

    PEUQSE.UserInput.parameter_estimation_settings['mcmc_parallel_sampling'] = True
    PEUQSE.UserInput.parameter_estimation_settings['mcmc_continueSampling'] = False  # for now we're not picking up from previous runs
    
    # saves all of the post burn in responses for ESS/mcmc. overwrites the old responses if you continue sampling. 
    #PEUQSE.UserInput.parameter_estimation_settings['exportAllSimulatedOutputs'] = True 
    
    #After filinlg the variables of the UserInput, now we make a 'parameter_estimation' object from it.
    

    print(f'main rank={PEUQSE.parallel_processing.currentProcessorNumber}/{PEUQSE.parallel_processing.numProcessors}')
    PE_object = PEUQSE.parameter_estimation(PEUQSE.UserInput)
    
    #Now we can do the mcmc!
    #PE_object.doMetropolisHastings()
    PE_object.doEnsembleSliceSampling()
    
    #Finally, create all plots!
    PE_object.createAllPlots()
    #The createAllPlots function calls each of the below functions so that the user does not have to.    
    #    PE_object.makeHistogramsForEachParameter()    
    #    PE_object.makeSamplingScatterMatrixPlot()
    #    PE_object.createSimulatedResponsesPlots()
    
    PE_object.save_to_dill("PE_object_00a0.dill")

