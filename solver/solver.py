from docplex.mp.model import Model as MipModel
from itertools import combinations

def primes(lower, upper):
    primes = []
    for num in range(lower,upper + 1):
        if num > 1:
            for i in range(2,num):
                if (num % i) == 0:
                    break
            else:
                primes.append(num)
    return primes

def main():
    prime_numbers = primes(0,100) # Consider all prime numbers between 0 and 100
    square_size = 3 # Consider squares with size 3x3

    model = MipModel("ponder-april")
    variables = {(i,j,pi): model.binary_var() for i in range(square_size) for j in range(square_size) for pi,pnum in enumerate(prime_numbers)}

    # Select a unique prime number for each field in the square
    for pi,pnum in enumerate(prime_numbers):
        model.add(model.sum(variables[(i,j,pi)] for i in range(square_size) for j in range(square_size)) <= 1)

    # Every cell of the square needs to contain a prime number
    for i in range(square_size):
        for j in range(square_size):
            model.add(model.sum(variables[(i,j,pi)] for pi,pnum in enumerate(prime_numbers)) == 1)

    # The average of all rows and columns need to be prime numbers too
    for i in range(square_size):
        for comb in combinations(prime_numbers, square_size):
            if sum(comb)/square_size != int(sum(comb)/square_size) or int(sum(comb)/square_size) not in prime_numbers:
                model.add(model.sum(variables[(i,j,pi)] for j in range(square_size) for pi,pnum in enumerate(prime_numbers) if pnum in comb) <= square_size - 1)
                model.add(model.sum(variables[(j,i,pi)] for j in range(square_size) for pi,pnum in enumerate(prime_numbers) if pnum in comb) <= square_size - 1)

    # The average of every diagonal should be a prime number too
    edge_fields_a = [(i,j) for i in range(square_size) for j in range(square_size) if i == 0 or j == 0]
    edge_fields_b = [(i,j) for i in range(square_size) for j in range(square_size) if i == 2 or j == 0]
    diagonals_a = [[(i+a,j+a) for a in range(square_size) if i+a < square_size and j+a < square_size] for i,j in edge_fields_a]
    diagonals_b = [[(i-a,j+a) for a in range(square_size) if i-a >= 0 and j+a < square_size] for i,j in edge_fields_b]
    for diagonal in diagonals_a + diagonals_b:
        if len(diagonal) > 1:
            for comb in combinations(prime_numbers, len(diagonal)):
                if sum(comb)/len(diagonal) != int(sum(comb)/len(diagonal)) or int(sum(comb)/len(diagonal)) not in prime_numbers:
                    model.add(model.sum(variables[(i,j,pi)] for i,j in diagonal for pi,pnum in enumerate(prime_numbers) if pnum in comb) <= len(diagonal) - 1)
    
    # Solve the model
    #model.minimize(model.sum(variables[(i,j,pi)]*pnum for i in range(square_size) for j in range(square_size) for pi,pnum in enumerate(prime_numbers)))
    solution = model.solve(log_output = True)

    # Print the solution
    sol = {}
    if solution:
        for i in range(square_size):
            row_string = ""
            for j in range(square_size):
                for pi,pnum in enumerate(prime_numbers):
                    if variables[(i,j,pi)].solution_value >= 0.5:
                        sol[(i,j)] = pnum
                        row_string += "%3.0f"%pnum
            print(row_string)
        return sol
    else:
        return {}
        print("A solution doesn't exist")

if __name__ == "__main__":
    main()