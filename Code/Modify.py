import numpy as np
import sys
from sklearn.neighbors import KernelDensity
from statsmodels.nonparametric.bandwidths import bw_silverman


def applyKDE (start_range, end_range, sample_size, array):
    x = np.linspace(start_range, end_range, sample_size, endpoint=True)[:, np.newaxis]
    data = np.array(array)
    data = data.reshape((-1, 1))
    bandwidth = float(0.05)
    counter = 0
    Finish = False

    while (bandwidth != float(0)):
        if counter == 200: 
            Finish = True
            ### Alternative way if cannot find bandwidth to achieve well-behave probabilities
            try: bandwidth = bw_silverman(data) 
            except ValueError: bandwidth = 20
        
        ### Perfroming KDE
        kd = KernelDensity(kernel='gaussian', bandwidth=bandwidth).fit(data)
        kd_vals = np.exp(kd.score_samples(x))
        prob_list = []
        step = (end_range - start_range) / (sample_size - 1)  # Step size
        x = np.linspace(start_range, end_range, sample_size)[:, np.newaxis]  # Generate values in the range
        np.set_printoptions(threshold=sys.maxsize)
        kd_vals = np.exp(kd.score_samples(x))  # Get PDF values for each x
        prob_list = np.array(kd_vals).tolist()
        pST = np.sum(kd_vals * step)  # Approximate the integral of the PDF
        
        ### Adding 0.05 if the sum of probabilities not closed to 1
        if (float(pST) < float(0.95) or float(pST) > float(1.00)) and Finish == False: 
            counter += 1
            bandwidth += float(0.05)
            continue
        elif Finish == True: break
        else: break
    return prob_list


