def calculate_otsu_threshold(values, frequencies):
    """
    Otsu's method aims to find a threshold that minimizes the intra-class variance (variance within each class) or equivalently maximizes the inter-class variance (variance between classes).

        Here’s a detailed step-by-step method:
        1. Calculate Total Weight and Mean:

    @param values:
    @param frequencies:
    @return:
    """
    # Total number of pixels
    total_pixels = sum(frequencies)

    # Calculate total mean
    total_mean = sum(val * freq for val, freq in zip(values, frequencies)) / total_pixels

    # Initialize Variables:
    max_variance = 0
    optimal_threshold = 0
    weight1 = 0
    sum1 = 0

    # Iterate Through All Possible Thresholds  t:

    for i in range(len(values)):
        # Update weight and mean for the first class (background)
        weight1 += frequencies[i]
        sum1 += values[i] * frequencies[i]

        # Skip if weight1 is 0
        if weight1 == 0:
            continue

        # Calculate weight and mean for the second class (foreground)
        weight2 = total_pixels - weight1
        if weight2 == 0:
            break

        mean1 = sum1 / weight1
        mean2 = (total_mean * total_pixels - sum1) / weight2

        # Calculate between-class variance
        variance_between = weight1 * weight2 * (mean1 - mean2) ** 2

        # Find the  optimal threshold that maximum variance
        if variance_between > max_variance:
            max_variance = variance_between
            optimal_threshold = values[i]

    return optimal_threshold
