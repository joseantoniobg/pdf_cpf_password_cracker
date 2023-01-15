def generateCpfValidationDigits(cpf):
    numbers = [int(digit) for digit in cpf if digit.isdigit()]
    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    numbers.append(expected_digit)
    cpf = cpf + str(expected_digit)
    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    return cpf + str(expected_digit)