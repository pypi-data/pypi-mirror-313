import random
import time
from datetime import datetime

def number(*args):
    # If one argument is passed, use it as the range max (0 to max)
    if len(args) == 1:
        return random.randint(0, args[0])

    # If two arguments are passed, use them as the range (min to max)
    elif len(args) == 2:
        return random.randint(args[0], args[1])

    # If the third argument is 'd' for decimals, handle floating point precision
    elif len(args) == 3 and isinstance(args[2], str) and args[2].startswith('d'):
        # Extract the number of decimal places
        decimal_places = int(args[2][1:])
        lower = args[0]
        upper = args[1]
        return round(random.uniform(lower, upper), decimal_places)

    # Handle the case where the first argument is a datetime or derived value
    elif len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], str):
        lower = int(args[0])
        upper = int(args[1])
        return random.randint(lower, upper)
    
    # Default case: generate a random number based on current time + nanoseconds
    else:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')  # Current time + microseconds
        seed = int(timestamp) % (args[0] if args else 100000000)
        random.seed(seed)
        return random.randint(0, 100000000)
