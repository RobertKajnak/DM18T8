def benchmarkMSE(Y):
    if Y.ndim == 2:
        Y = Y.T[0]
    MSE = 0
    for i in range(1,len(Y)):
        MSE = MSE + (Y[i]-Y[i-1])**2
    MSE = MSE/len(Y)
    return MSE