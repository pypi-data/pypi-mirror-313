##########################################################################################################################################################################
#                                             This is package for simple machine learning                                                                                #
##########################################################################################################################################################################
# Example 1:                                                                                                                                                             #
# import catnet                                                                                                                                                          #
# import numpy as np                                                                                                                                                     #
# model=catnet.Model()                                                                                                                                                   #
# model.add(catnet.layers.MRELU(16))                                                                                                                                     #
# x = np.array([[1],[2]])  # Inputs (all in [])                                                                                                                          #
# y = np.array([[2],[3]])  # Outputs (all in [])                                                                                                                         #
# model.train(np.array([[1],[2]]),np.array([[2],[3]]),True,optim=catnet.optimize.Adam(0.01), loss=losses.MSE(),epochs=500,logging=True) # Disable logging for Python IDLE#
# answer=0                                                                                                                                                               #
# for pred in model(np.array([[1]])):                                                                                                                                    #
# 	 answer=pred[0]                                                                                                                                                      #
# print(answer)                                                                                                                                                          #
##########################################################################################################################################################################
