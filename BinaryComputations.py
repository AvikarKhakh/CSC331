WORD_BITS = 8 # word size = 8 bits
MASK = (~0) ^ (~0 << WORD_BITS) # mask to keep results to 8 bits 

# mask n down to 8 bits and convert to binary string
def to_binary(n: int, bits: int = WORD_BITS) -> str:
    mask = (~0) ^ (~0 << bits)              
    return f"{(n & mask):0{bits}b}"        

# add two integers using bitwise operations 
def add(a: int, b: int) -> int:
    # loop until there is no carry
    while b != 0:
        carry = (a & b) & MASK
        a = (a ^ b) & MASK
        b = (carry << 1) & MASK
    return a

# compute two's complement of an integer
def twos_complement(n: int) -> int:
    return add(~n & MASK, 1)

# subtract two integers by subracting b from a using two's complement
def subtract(a: int, b: int) -> int:
    a = a & MASK
    b = b & MASK
    return add(a, twos_complement(b)) & MASK

# show step-by-step decimal to binary for 5,3,2
def run_task_one(n: int, bits: int = WORD_BITS) -> str:

    mask_bits = (~0) ^ (~0 << bits)
    n_masked = n & mask_bits

    print(f"Decimal n: {n}")
    print(f"Masked n: {to_binary(n, bits)}")

    bit_values = []

    for i in reversed(range(bits)):
        # Extract the i-th bit and shift right by i, then AND 1
        shifted = (n_masked >> i) & mask_bits     
        bit_lsb = shifted & 1
        # Step print to help user understand the process
        print(f"bit {i}: ({to_binary(n_masked, bits)} >> {i}) = " f"{to_binary(shifted, bits)} & 1 = {bit_lsb}")
        bit_values.append('1' if bit_lsb else '0')
    # build final binary string from left to right
    result_bin_string = "".join(bit_values)
    print(f"Final: {n} -> {result_bin_string} \n")
    return result_bin_string

# subtract two 4-bit integers
def subtract_four_bits(a: int, b: int, *, wrap: bool = False) -> int:
    bits = 4
    mask = (~0) ^ (~0 << bits)

    # add two 4-bit integers using bitwise operations within the 4-bit limit
    def add4(x: int, y: int) -> int:
        x = x & mask
        y = y & mask
        
        # loop until there is no carry
        while y != 0:
            # calculate sum and carry within 4 bit width
            sum = (x ^ y) & mask
            # left shift carry and mask to 4 bit width
            carry = ((x & y) << 1) & mask
            # x becomes sum, y becomes carry
            x = sum 
            y = carry
        
        return x
    
    # mask inputs to 4 bit width
    A = a & mask
    B = b & mask
    
    # compute two's complement of B within 4 bits
    negB = add4(~B & mask, 1) & mask
    result = add4(A, negB) & mask
    return result, f"{result:0{bits}b}"

# print results for A - B in decimal and binary
def requirement_four(a: int, b: int):
    print(f"A = {a} ({to_binary(a)})")
    print(f"B = {b} ({to_binary(b)})")
    difference = subtract(a, b)
    print(f"Decimal Result: {difference}")
    print(f"Decimal Result:  {to_binary(difference)}")


# run code by running file
if __name__ == "__main__":
    # test A - B where A < B for 4-bit subtraction
    requirement_four(60, 40)
    
    # test step-by-step binary conversion with different numbers
    print("\n\nBinary steps:\n")
    for num in (5, 3, 2):
        run_task_one(num)

    # change parameters to test different values where A > B
    decimal_4, binary_4 = subtract_four_bits(5, 3)
    print(f"4-bit Subtraction Answer = {decimal_4} ({binary_4})")        