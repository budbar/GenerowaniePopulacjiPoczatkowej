import numpy as np


def compute_amount_of_combinations(lower_limit, upper_limit, accuracy):
    return int((upper_limit - lower_limit) * 10**accuracy + 1)


def compute_binary_string_length(lower_limit, upper_limit, accuracy):
    combinations = compute_amount_of_combinations(lower_limit, upper_limit, accuracy)
    m = 0

    while 2**m <= combinations:
        m += 1

    return m


def generate_population(lower_limit, upper_limit, accuracy, dimensions=1):
    combinations = compute_amount_of_combinations(lower_limit, upper_limit, accuracy)
    population = []

    for _ in range(combinations):
        if dimensions == 1:
            individual = np.random.uniform(lower_limit, upper_limit)
        else:
            individual = np.random.uniform(lower_limit, upper_limit, dimensions)

        individual = np.round(individual, accuracy)
        population.append(individual)

    return population


def convert_population_to_binary(population, binary_string_length):
    binary_values_list = []

    for index, value in enumerate(population):
        binary_index = bin(index)[2:].zfill(binary_string_length)
        binary_values_list.append(binary_index)

    return binary_values_list


def evaluate_specimens(binary_values, lower_limit, upper_limit, binary_string_length):
    shifted_values = []

    for binary_value in binary_values:
        decimal_value = int(binary_value, 2)
        shifted_value = lower_limit + ((upper_limit - lower_limit) * decimal_value) / (2**binary_string_length - 1)
        shifted_values.append(shifted_value)

    return shifted_values


def compute_rastrigin(x, a, omega):
    n = 1
    result = a * n + x**2 - a * np.cos(omega * x)

    return result


def generate_initial_population(a, omega, lower_limit, upper_limit, accuracy):
    population = generate_population(lower_limit, upper_limit, accuracy)

    binary_string_length = compute_binary_string_length(lower_limit, upper_limit, accuracy)
    binary_values = convert_population_to_binary(population, binary_string_length)

    evaluated_specimens = evaluate_specimens(binary_values, lower_limit, upper_limit, binary_string_length)

    result_values = [compute_rastrigin(individual, a, omega) for individual in evaluated_specimens]

    print("Wygenerowana populacja i wartości funkcji Rastrigina:")
    for iteration, (individual, result) in enumerate(zip(evaluated_specimens, result_values), start=1):
        print(f"Osobnik {iteration}: {individual}, Wartość Rastrigina: {result}")


def main():
    a = 10
    omega = 20 * np.pi
    lower_limit = -1
    upper_limit = 1
    accuracy = 1

    generate_initial_population(a, omega, lower_limit, upper_limit, accuracy)


if __name__ == "__main__":
    main()
