# -----------------------------------------------------------------------------
# generate_sample_database.py
# -----------------------------------------------------------------------------
# This script serves as an example of how to use the `create_database` function
# from the `precomputed_ai_weights` module. It generates a sample precomputed
# weights database based on specified parameters and saves this database to a
# JSON file named `sample_database.json`.
#
# The generated JSON file can then be used by other scripts (e.g., for testing
# or simulation purposes) to load the precomputed weights.
# -----------------------------------------------------------------------------

import json
from precomputed_ai_weights import create_database

def main():
    # --- Parameters for Sample Database Generation ---
    # num_inputs: Defines how many separate input values the simulated neuron will take.
    #             For example, 2 means the neuron takes two inputs, say x and y.
    num_inputs = 2

    # input_bit_depth: Determines the range of each input value.
    #                  The maximum value for an input is `2**input_bit_depth - 1`.
    #                  For input_bit_depth = 2, inputs can range from 0 to (2^2 - 1) = 3.
    #                  So, for num_inputs=2 and input_bit_depth=2, combinations like
    #                  (0,0), (0,1)...(3,3) will be generated.
    input_bit_depth = 2

    # operation: The mathematical operation to precompute. Currently, "multiply" is supported.
    #            The database will store the result of this operation for each input combination.
    operation = "multiply"

    print(f"Generating database with: num_inputs={num_inputs}, input_bit_depth={input_bit_depth}, operation='{operation}'")

    # Generate the database using the function from precomputed_ai_weights.py
    # The `create_database` function returns a dictionary with tuple keys.
    try:
        # Note: create_database returns a dictionary with tuple keys, e.g., {(0,0): 0, (0,1): 0, ...}
        database_tuple_keys = create_database(num_inputs=num_inputs, input_bit_depth=input_bit_depth, operation=operation)
        print("Database with tuple keys generated successfully.")
    except ValueError as e:
        print(f"Error generating database: {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred during database generation: {e}")
        return

    # Define the output file name
    output_filename = "sample_database.json"

    # --- Save the Database to a JSON File ---
    # JSON format requires keys to be strings. The `database_tuple_keys` dictionary
    # currently has tuples as keys (e.g., (0,0)).
    # We need to convert these tuple keys into their string representations (e.g., "(0,0)")
    # before serializing to JSON. The `query_database` function in the other module is
    # designed to handle these stringified tuple keys when loading from JSON.
    database_string_keys = {str(key): value for key, value in database_tuple_keys.items()}
    print(f"Converted {len(database_string_keys)} tuple keys to string keys for JSON serialization.")

    try:
        with open(output_filename, 'w') as f:
            json.dump(database_string_keys, f, indent=4)
        print(f"Database saved to {output_filename}")
    except IOError as e:
        print(f"Error saving database to file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during file saving: {e}")

if __name__ == "__main__":
    main()
