import numpy as np

# generate Additive White Noise
def generateAWN(pdf, sample_rate, duration=1, mean=0, std=1):
    if pdf == "gaussian":
        noise = np.random.normal(mean, std, sample_rate * duration)
    elif pdf == "uniform":
        # uniform law supported on (a,b), then:
        # mean = (a+b)/2
        # var  = (b-a)^2/12         ie: std  = (b-a)/(2*sqrt(3))
        # that is, from mean and var:
        # a = mean - std*sqrt(3)
        # b = mean + std*sqrt(3)
        noise = np.random.uniform(low=mean - std * np.sqrt(3), high=mean + std * np.sqrt(3), size=None)
        ###FIXME: equivalently ?
        # noise = mu+std*np.random.uniform(low=0, high=1, size=None)
    else:
        print("Not implemeted yet!")

    return noise