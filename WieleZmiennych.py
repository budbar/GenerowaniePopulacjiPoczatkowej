import numpy as np


def compute_amount_of_combinations(variables):
    for variable in variables:
        lower_limit = variable["lower_limit"]
        upper_limit = variable["upper_limit"]
        accuracy = variable["accuracy"]

        combinations = int((upper_limit - lower_limit) * 10**accuracy + 1)
        variable["combinations"] = combinations

    return variables


def compute_binary_string_length(variables):
    for variable in variables:
        combinations = variable["combinations"]

        m = 0
        while 2**m <= combinations:
            m += 1

        variable["m"] = m

    return variables


def generate_population(variables):
    for variable in variables:
        population = []
        lower_limit = variable["lower_limit"]
        upper_limit = variable["upper_limit"]
        accuracy = variable["accuracy"]
        combinations = variable["combinations"]

        for _ in range(combinations):
            individual = np.random.uniform(lower_limit, upper_limit)
            individual = np.round(individual, accuracy)
            population.append(individual)

        variable["population"] = population

    return variables


def convert_population_to_binary(variables):
    for variable in variables:
        binary_values = []
        population = variable["population"]
        binary_string_length = variable["m"]

        for index, value in enumerate(population):
            binary_value = bin(index)[2:].zfill(binary_string_length)
            binary_values.append(binary_value)

        variable["binary_values"] = binary_values

    return variables


def merge_binary_values(variables):
    # Oblicz maksymalną długość, aby wiedzieć, ile wartości musimy połączyć
    max_length = max(len(variable["binary_values"]) for variable in variables)

    # Zainicjalizuj listę z pustymi stringami o długości max_length
    merged_binary_values = [''] * max_length

    # Iteruj po każdym słowniku
    for variable in variables:
        binary_values = variable["binary_values"]

        # Iteruj po indeksach i łącz wartości
        for index in range(len(binary_values)):
            merged_binary_values[index] += binary_values[index]

    return merged_binary_values


def convert_binary_to_decimal(merged_binary_values):
    decimal_values = []

    for binary_value in merged_binary_values:
        decimal_value = int(binary_value, 2)
        decimal_values.append(decimal_value)

    return decimal_values


def evaluate_specimens(variables, decimal_values):
    result = []

    for decimal_value in decimal_values:
        values = []
        for variable in variables:
            lower_limit = variable["lower_limit"]
            upper_limit = variable["upper_limit"]
            binary_string_length = variable["m"]

            shifted_value = lower_limit + ((upper_limit - lower_limit) * decimal_value) / (2**binary_string_length - 1)
            values.append(shifted_value)

        result.append(values)

    return result


def compute_rastrigin(vectorX, a, omega):
    n = len(vectorX)
    result = a * n

    for x in vectorX:
        result += x**2 - a * np.cos(omega * x)

    return result


def generate_initial_population(a, omega, variables):
    variables = compute_amount_of_combinations(variables)               # Obliczamy ilość kombinacji dla zmiennych i zapisujemy wynik w kluczu
    variables = generate_population(variables)                          # Dodajemy populację dla każdej zmiennej i zapisujemy ją w kluczu

    variables = compute_binary_string_length(variables)                 # Obliczamy długość łańcucha binarnego dla każdej zmiennej i zapisujemy w kluczu
    variables = convert_population_to_binary(variables)                 # Konwertujemy populację na łańcuchy binarne i zapisujemy w kluczu

    merged_binary_values = merge_binary_values(variables)               # Łączymy ze sobą wartości binarne populacji zmiennych
    decimal_values = convert_binary_to_decimal(merged_binary_values)    # Konwertujemy wartości binarne na dziesiętne

    evaluated_specimens = evaluate_specimens(variables, decimal_values) # Przesuwamy wartości do przedziału każdej zmiennej

    result_values = [compute_rastrigin(individual, a, omega) for individual in evaluated_specimens]

    print("Wygenerowana populacja i wartości funkcji Rastrigina:")
    for iteration, (individual, result) in enumerate(zip(evaluated_specimens, result_values), start=1):
        print(f"Osobnik {iteration}: {individual}, Wartość Rastrigina: {result}")


def main():
    a = 10
    omega = 20 * np.pi

    variables = [
        {"lower_limit": -1, "upper_limit": 1, "accuracy": 1},
        {"lower_limit": -2, "upper_limit": 2, "accuracy": 1},
        {"lower_limit": -3, "upper_limit": 3, "accuracy": 1},
        {"lower_limit": -5, "upper_limit": 5, "accuracy": 1}
    ]

    generate_initial_population(a, omega, variables)


if __name__ == "__main__":
    main()