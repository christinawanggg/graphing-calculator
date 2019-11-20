import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
import math

# Main prodedure to draw f(x), first derivative, second derivative, and mark min/max/inflection/removable discontinuity points
# Return: Indicator whether f(x) has any removable discontinuity points
def graph(derivative, x):
    # rounding precision
    rounding_number = 2

    # calculate the y points using different functions: f, first derivative, second derivative
    with np.errstate(divide='ignore', invalid='ignore'):
        y = f(x)
        y1 = my_firstDerivative(x)
        y2 = my_secondDerivative(x)

    # Find out removable discontinuity points

    # Array for removable discontinuity points
    removable_pts_x = []
    removable_pts_y = []

    # Return value to indicate whether there is any non removable discontinuty point.
    # Use to determine whether to calculate integral
    has_non_removable_discontinuity_point = False

    # When f(x[i]) is either invalid (np.nan) or infinite (np.inf) after the calculation,
    # use the trend lines to determine whether the point is removable or nonremoveable discontinuity points.
    # If the trend on the left (i-2, i-1) is reverse comparing to the trend from the cross (i-1, i+1), it is nonremovable, otherwise removable
    # OR
    # If the trend on the right (i+1, i+2) is reverse comparing to the trend from the cross (i-1, i+1), it is nonremovable, otherwise removable
    # For removable discontinuity point, average (i-1, i+1) to get the f(x[i]) since f(x[i]) itself is invalid or infinite.
    # Only store removable discontinuity point when f(x[i]) is a valid number.
    n = len(x)
    for i in range(0, n):
        if (np.isnan(y[i]) or np.isinf(y[i])):
            if (i >= 2 and i <= n - 2):
                #print "First:", (y[i-1] - y[i-2]), " Third:", (y[i+1] - y[i-1])
                if ((y[i-1] - y[i-2]) * (y[i+1] - y[i-1]) < 0.0):
                    #print "Nonremovable discontinuity point:", x[i]
                    s = "Nonremovable discontinuity point:" + str(x[i])
                    has_non_removable_discontinuity_point = True
                else:
                    m = x[i]
                    k = (y[i-1] + y[i+1])/2
                    if (not np.isnan(k)):
                        removable_pts_x.append(m)
                        removable_pts_y.append(k)
                        print "Removable discontinuity point: (", m,",", k, ")"
            elif (i >= 1 and i <= n - 3):
                #print "Second:", (y[i+2] - y[i+1]), " Third:", (y[i+1] - y[i-1])
                if ((y[i+2] - y[i+1]) * (y[i+1] - y[i-1]) < 0.0):
                    #print "Nonremovable discontinuity point:", x[i]
                    s = "Nonremovable discontinuity point:" + str(x[i])
                    has_non_removable_discontinuity_point = True
                else:
                    m = x[i]
                    k = (y[i-1] + y[i+1])/2
                    if (not np.isnan(k)):
                        removable_pts_x.append(m)
                        removable_pts_y.append(k)
                        print "Removable discontinuity point: (", m,",", k, ")"
            else:
                # print "Discontinuity point:", x[i]
                s = "Discontinuity point:" + str(x[i])

    # If no invalid or infinite f(x[i]) found, still need to find out whether f(x) graph has any non removable discontinuity point.
    # Use the similar concept as above by comparing the trend of left, the trend of cross, the trend of right to determine whether
    # this is a non removable discontinuity point: the trend of left should be the same as the trend of right, where both are opposite
    # the trend of cross
    if (not has_non_removable_discontinuity_point):
        for i in range(0, n):
            if (i >= 1 and i < n - 2):
                g1 = y[i] - y[i-1]
                g2 = y[i+1] - y[i]
                g3 = y[i+2] - y[i+1]
                if (g1 * g3 > 0.0 and g1 * g2 < 0.0 and g2 * g3 < 0):
                    has_non_removable_discontinuity_point = True
            elif (i >= 2 and i < n - 1):
                g1 = y[i] - y[i-1]
                g2 = y[i+1] - y[i]
                g3 = y[i-1] - y[i-2]
                if (g1 * g3 > 0.0 and g1 * g2 < 0.0 and g2 * g3 < 0):
                    has_non_removable_discontinuity_point = True

    # Find out min, max, infection points

    min_pts_x = []
    min_pts_y = []
    max_pts_x = []
    max_pts_y = []
    inflection_pts_x = []
    inflection_pts_y = []

    # Initialize the starting point on the y axis
    prev_y = y[0]
    prev_y1 = y1[0]
    prev_y2 = y2[0]

    for i in range(1, len(x) - 1):
        curr_y = round(y[i], rounding_number)
        curr_y1 = round(y1[i], rounding_number)
        curr_y2 = round(y2[i], rounding_number)

        next_y = round(y[i + 1], rounding_number)
        next_y1 = round(y1[i + 1], rounding_number)
        next_y2 = round(y2[i + 1], rounding_number)

        # Use first derivative, if multiplication of prev and next is negative,
        #                          and absolute multiplication is smaller than absolute prev and next
        #                          and absolute curr is smaller than absolute prev and next
        #                          and prev and curr are non zero
        cn = prev_y1 * next_y1
        if (cn < 0 and abs(cn) <= abs(prev_y1) and abs(cn) <= abs(next_y1) and abs(curr_y1) < abs(prev_y1) and abs(curr_y1) < abs(next_y1) and 0.0 != prev_y1 and 0.0 != next_y1):
            # If prev is more than 0, then MAX
            #print "Curr_y1 = ", curr_y1 , "and Next_y1 = ", next_y1
            if (prev_y1 > 0.0 and (not np.isnan(curr_y)) and (not np.isinf(curr_y))):
                print "Max at (", round(x[i], rounding_number), ",", curr_y, ")"
                max_pts_x.append(round(x[i], rounding_number))
                max_pts_y.append(curr_y)
            # If prev is less than 0, then MIN
            elif (prev_y1 < 0.0 and (not np.isnan(curr_y)) and (not np.isinf(curr_y))):
                print "Min at (", round(x[i], rounding_number), ",", curr_y , ")"
                min_pts_x.append(round(x[i], rounding_number))
                min_pts_y.append(curr_y)

        # print "(", x[i], ",", prev_y2, ",", curr_y2, ",", next_y2, ")"

	# Apply the second derivative with the Same condition as first derivative to capture all the inflection points
        poi = prev_y2 * next_y2
        if (poi < 0 and abs(poi) <= abs(prev_y2) and abs(poi) <= abs(next_y2) and abs(curr_y2) < abs(prev_y2) and abs(curr_y2) < abs(next_y2) and 0.0 != prev_y2 and 0.0 != next_y2 and (not np.isnan(curr_y)) and (not np.isinf(curr_y))):
            #print "Curr_y2 = ", curr_y2 , "and Next_y2 = ", next_y2
            print "Point of Inflection at (", round(x[i], rounding_number), ",", curr_y, ")"
            inflection_pts_x.append(round(x[i], rounding_number))
            inflection_pts_y.append(curr_y)

	# Set prev to curr and go to the next point
        prev_y = curr_y
        prev_y1 = curr_y1
        prev_y2 = curr_y2

    # Plot the graph and all the relevant points

    with np.errstate(divide='ignore', invalid='ignore'):
        axes = plt.gca()
        axes.set_xlim([-10,10])
        axes.set_ylim([-10,10])
        plt.title("Graph")
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.plot(x, y, label = 'Function (f(x))')
        plt.plot(x, my_firstDerivative(x), label = 'First Derivative')
        plt.plot(x, my_secondDerivative(x), label = 'Second Derivative')
        plt.plot(removable_pts_x, removable_pts_y,'o', label = 'Hole')
        plt.plot(min_pts_x, min_pts_y,'^', label = 'Minimum Value')
        plt.plot(max_pts_x, max_pts_y, 'v', label = 'Maximum Value')
        plt.plot(inflection_pts_x, inflection_pts_y, 'p', label = 'Point of Inflection')

        fontP = FontProperties()
        fontP.set_size("small")
        plt.legend(prop = fontP)

        plt.show()
        return has_non_removable_discontinuity_point

# Regular function
def f(x):
    global mycode
    mycode_local = mycode.replace("sin(", "np.sin(")
    mycode_local = mycode_local.replace("cos(", "np.cos(")
    mycode_local = mycode_local.replace("tan(", "np.tan(")
    mycode_local = mycode_local.replace("1x", "1*x")
    mycode_local = mycode_local.replace("2x", "2*x")
    mycode_local = mycode_local.replace("3x", "3*x")
    mycode_local = mycode_local.replace("4x", "4*x")
    mycode_local = mycode_local.replace("5x", "5*x")
    mycode_local = mycode_local.replace("6x", "6*x")
    mycode_local = mycode_local.replace("7x", "7*x")
    mycode_local = mycode_local.replace("8x", "8*x")
    mycode_local = mycode_local.replace("9x", "9*x")
    mycode_local = mycode_local.replace("0x", "0*x")
    mycode_local = mycode_local.replace("pix", "pi*x")
    mycode_local = mycode_local.replace("pi", "math.pi")
    mycode_local = mycode_local.replace("e^x", "np.exp(x)")
    mycode_local = mycode_local.replace("e^(", "np.exp(")
    mycode_local = mycode_local.replace("^", "**")
    mycode_local = mycode_local.replace("log(", "np.log10(")
    mycode_local = mycode_local.replace("ln(", "np.log(")
    mycode_local = mycode_local.replace(")(", ")*(")
    # print mycode_local
    return eval(mycode_local)

# Derivative function
def derivative(c, func):
    x = c + 1. / 1000.
    numerator = func(x) - func(c)
    denominator = x - c
    derivative = numerator / denominator
    return derivative

# First derivative function calling to the generic derivative function with regular function
def my_firstDerivative(x):
    return derivative(x, f)

# Second derivative function calling to the generic derivative function with first derivation function
def my_secondDerivative(x):
    return derivative(x, my_firstDerivative)

# Integral function
# Return: If the calculation encounter an exception, return np.nan as invalid integral
def integral(a, b, n):
    change  = (b - a)/(1.0 * n)
    w = change * (0.5)
    ftc = 0
    z = 0
    for i in range(0, n):
        try:
            if (i == 0 or i == n):
                z = w*(derivative(a+i*change, f))
                #print "x = ", a + i*change ," and z = ", z
            else:
                z = 2*(w*derivative(a+i*change, f))
                #print "x = ", a + i*change ," and z = ", z
        #except ZeroDivisionError as err:
           # z = 0.0
        except:
            return np.nan
        # print "i =", i, ", z =", z
        ftc += z
    return ftc


# Enter the function
mycode = raw_input("Enter the function: ")

# Enter the starting point and treat pi specially
input_s = raw_input("Enter starting value for the integral: ")
if (input_s.lower() == 'pi'):
    a = math.pi
else:
    a = float(input_s)

# Enter the ending point and treat pi specially
input_s = raw_input("Enter ending value for the integral: ")
if (input_s.lower() == 'pi'):
    b = math.pi
else:
    b = float(input_s)

# Enter the intervals
n = int(raw_input("Enter number of sub-intervals for the integral: "))

# Build the range of x points from start to end with number intervals based on the input
# -10.0, -9.999, -9.998, ..., 9.998, 9.999, 10.0
xpoints = np.linspace(-10, 10, 1001)

# Draw the original graph
has_non_removable_discontinuity_point = graph(f, xpoints)
print ""

# If the graph has non removable discontinuity point, no FTC
if (has_non_removable_discontinuity_point):
    print "FTC does not apply because the graph is not continuous from x =", a, "to x =", b
else:
    with np.errstate(divide='ignore', invalid='ignore'):
        integral_val = integral(a, b, n)

    # If the integral is valid, perform FTC comparison; otherwise, FTC does not apply
    if (np.isnan(integral_val)):
        print "FTC does not apply"
        #print "Since, f(", b, ") - f(", a, ") and/or Integral of f'(x) from ", a, "to", b,  "does not exist, FTC does not apply"
    else:
        print "Integral of f'(x) from", a, "to", b, "=", format(integral_val, ".3f")

        try:
            val = f(b) - f(a)
            print "f(", b, ") - f(", a, ") = " , format(val, ".3f")
            if (val - integral_val <= 0.35):
                print "Because f(", b, ") - f(", a, ") = Integral of f'(x) from", a, "to", b, ", FTC holds true"
            else:
                print "FTC does not apply"
                #print "Since, f(", b, ") - f(", a, ") does not equal Integral of f'(x) from ", a, "to", b, ",FTC does not apply"
        except:
            print "FTC does not apply"
            #print "Since, f(", b, ") - f(", a, ") does not equal Integral of f'(x) from ", a, "to", b, ",FTC does not apply"
