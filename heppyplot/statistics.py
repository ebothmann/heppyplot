import math

def central_value_member(values, axis=0):
    if axis == 1:
        return values[:,0]
    else:
        return values[0,:]

def standard_error(values, which=68, axis=0):
    lows = []
    highs = []
    other_axis = 1 if axis == 0 else 0
    for other_axis_i in range(0, values.shape[other_axis]):
        cv = values[0, other_axis_i]
        evs = values[1:, other_axis_i]
        x2_estimate = 0.0
        x_estimate = 0.0
        for ev in evs:
            x_estimate += ev
            x2_estimate += ev**2
        x_estimate /= evs.shape[0]
        x2_estimate /= evs.shape[0]
        error = math.sqrt(x2_estimate - x_estimate**2)
        high = cv + error
        low = cv - error
        highs.append(high)
        lows.append(low)
    return (lows, highs)

def asymmetric_hessian_error(values, which=68, axis=0):
    lows = []
    highs = []
    other_axis = 1 if axis == 0 else 0
    for other_axis_i in range(0, values.shape[other_axis]):
        cv = values[0, other_axis_i]
        evs = values[1:, other_axis_i]
        error = [0.0, 0.0]
        for i in range(0, evs.shape[0], 2):
            (ev_p, ev_m) = evs[i:i+2]
            error[0] += max(ev_p - cv, ev_m - cv, 0)**2
            error[1] += max(cv - ev_p, cv - ev_m, 0)**2
        high = cv + math.sqrt(error[0])
        low = cv - math.sqrt(error[1])
        highs.append(high)
        lows.append(low)
    return (lows, highs)