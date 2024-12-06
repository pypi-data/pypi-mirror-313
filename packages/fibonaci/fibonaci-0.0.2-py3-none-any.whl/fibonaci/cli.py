def fib(n):
	if n < 3:
    	    return n-1
	fib1 = 0
	fib2 = 1
	for _ in range(n-2):
    	    fibn = fib1 + fib2
    	    fib2, fib1 = fib1, fibn
	return fibn

def main():
	import sys
	n = int(sys.argv[1])
	sys.set_int_max_str_digits(1000000)
	print(f"fib({n}) = {str(fib(n))}")
