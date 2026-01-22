try:
    use_dill = True
    if use_dill:  # Use this if you get the `TypeError: cannot pickle 'module' object` error
        import dill
        global MPI
        
        from mpi4py import MPI as _MPI

        _MPI.pickle.__init__(dill.dumps, dill.loads, dill.HIGHEST_PROTOCOL)
        MPI = _MPI
    else:
        from mpi4py import MPI
    rank = MPI.COMM_WORLD.Get_rank()
    numProcessors = MPI.COMM_WORLD.Get_size()
    numSimulations = numProcessors - 1 #Normally, we will use rank 0 for controlling.
    currentProcessorNumber = rank
    #now this number can be accessed from elsewhere using parallel_processing.CurrentProcessorNumber
    if numProcessors > 1:
        using_mpi = True
    else:
        using_mpi = True
except ModuleNotFoundError:
    currentProcessorNumber=0
    numProcessors=1
    using_mpi = False



