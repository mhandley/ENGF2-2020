import random

def estimate_pi(precision):
    # we're going to generate several independent estimates, and
    # compare them to decide when we've got an accurate enough answer
    no_of_estimates = 4  
    in_counts = []
    estimates = []
    for i in range(0, no_of_estimates):
        in_counts.append(0)
        estimates.append(0)
    total_count = 0

    while True:
        for i in range(0, no_of_estimates):
            x = random.uniform(-1,1)
            y = random.uniform(-1,1)
            r_squared = x*x + y*y
            if r_squared < 1:
                in_counts[i] += 1
        total_count += 1

        # How do we know if we've reached the required precision?  We
        # calculate several different estimates (no_of_estimates
        # determines how many).
        #
        # We calculate the mean of these independent estimates.  If
        # all of our independent estimates are within the required
        # distance from the mean, we conclude that with reasonable
        # probability, we're done
        
        if total_count % 1000 == 0: # only check every so often

            #calculate our estimates and their mean
            mean_estimate = 0
            for i in range(0, no_of_estimates):
                estimates[i] = 4 * in_counts[i]/total_count
                mean_estimate += estimates[i]
            mean_estimate /= no_of_estimates

            done = True
            for i in range(0, no_of_estimates):
                if abs(mean_estimate - estimates[i]) > precision:
                    done = False
            if done:
                return mean_estimate

# generate pi to the nearest 0.001
print(estimate_pi(0.001))
