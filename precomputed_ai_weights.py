"""
Proof-of-concept module for simulating a neuron's behavior using precomputed weights.

This module allows for the creation of a "database" (a Python dictionary) that
stores the results of a specific operation (e.g., multiplication) for all possible
combinations of discrete input values. These input values are determined by the
number of inputs and their bit depth.

The primary functions are:
- create_database: Generates this precomputed database.
- query_database: Retrieves a result from the database for a given set of inputs.
- simulate_neuron: Uses query_database to simulate the neuron's output.

This approach is being explored as an alternative to traditional computations in
certain AI scenarios, particularly where input value ranges are constrained and
operations can be exhaustively precalculated.
"""
import itertools

def create_database(num_inputs, input_bit_depth, operation):
  """
  Creates a precomputed weights database by generating all possible input combinations
  and computing the result of the specified operation.

  The maximum value for each input is determined by `2**input_bit_depth - 1`.
  For example, an `input_bit_depth` of 2 means each input can range from 0 to 3.

  Args:
    num_inputs (int): The number of separate input streams to the neuron.
                      Must be a positive integer.
    input_bit_depth (int): The bit depth for each input stream. This determines the
                           range of possible values for each input (0 to 2**input_bit_depth - 1).
                           Must be a positive integer.
    operation (str): A string specifying the operation to perform on the input values.
                     Currently, only "multiply" is implemented.

  Returns:
    dict: A dictionary representing the precomputed database.
          Keys are tuples of input values (e.g., (0, 1), (1, 0)).
          Values are the computed results of the operation for those inputs.
          Example for multiply, num_inputs=2, input_bit_depth=1:
          {(0,0): 0, (0,1): 0, (1,0): 0, (1,1): 1}

  Raises:
    ValueError: If num_inputs or input_bit_depth are not positive integers,
                or if an unsupported operation is specified.

  Current Limitations:
    - Only the "multiply" operation is implemented.
    - The `output_bit_depth` (to potentially truncate or map results) is not yet handled.
    - For databases intended for JSON serialization, the tuple keys will need to be
      converted to strings by the calling code (as done in `generate_sample_database.py`).
      This function returns a dictionary with actual tuple keys.
  """
  if not isinstance(num_inputs, int) or num_inputs <= 0:
    raise ValueError("num_inputs must be a positive integer.")
  if not isinstance(input_bit_depth, int) or input_bit_depth <= 0:
    raise ValueError("input_bit_depth must be a positive integer.")

  database = {}
  max_input_value = 2**input_bit_depth

  # Generate all possible values for a single input
  possible_single_input_values = range(max_input_value)

  # Generate all combinations of input values for num_inputs
  # For example, if num_inputs=2 and possible_single_input_values=[0,1],
  # input_combinations will be [(0,0), (0,1), (1,0), (1,1)]
  input_combinations = itertools.product(possible_single_input_values, repeat=num_inputs)

  for inputs in input_combinations:
    if operation == "multiply":
      result = 1
      for val in inputs:
        result *= val
      database[inputs] = result
    # Add other operations here in the future
    # elif operation == "add":
    #   result = sum(inputs)
    #   database[inputs] = result
    else:
      raise ValueError(f"Unsupported operation: {operation}")

  return database

def query_database(database, input_values):
  """
  Queries the database for a given set of input values.

  This function assumes the database keys are string representations of tuples,
  as would be the case if the database was loaded from a JSON file where tuple keys
  were converted to strings (e.g., "(0, 1)").

  Args:
    database (dict): The precomputed weights database. Keys are expected to be
                     string representations of tuples of input values. Values are
                     the precomputed results.
    input_values (tuple): A tuple of integer input values (e.g., (0, 1)) for which
                          to query the database.

  Returns:
    The precomputed result (typically int or float) from the database for the
    given `input_values`.

  Raises:
    KeyError: If the string representation of `input_values` (e.g., "(0, 1)")
              is not found as a key in the database.
    TypeError: If `input_values` is not a tuple.
  """
  if not isinstance(input_values, tuple):
    raise TypeError("input_values must be a tuple.")

  # Convert the tuple of input values to its string representation
  # This is how keys are stored in the JSON-loaded database
  input_key = str(input_values)

  if input_key in database:
    return database[input_key]
  else:
    # Attempt to find the key with spaces, as Python's str((0, 1)) is '(0, 1)'
    # and json.dump might store it differently if not handled carefully during creation.
    # However, our current save script `generate_sample_database.py` uses `str(key)`,
    # so str((0,1)) becomes "(0, 1)".
    # Let's also check for a common variation without space if the direct match fails.
    # This makes the query slightly more robust to variations in key stringification.
    input_key_no_space = repr(input_values).replace(" ", "") # e.g., "(0,1)"
    if input_key_no_space in database:
      return database[input_key_no_space]
    else:
      raise KeyError(f"Input combination {input_values} (searched as '{input_key}' and '{input_key_no_space}') not found in the database.")

def simulate_neuron(database, input_values):
  """
  Simulates a neuron's output by looking up the result in the precomputed weights database.

  In this version, this function is a direct wrapper around `query_database`.
  Future enhancements might include additional logic, such as applying an activation
  function or handling output bit depth adjustments.

  Args:
    database (dict): The precomputed weights database, where keys are string
                     representations of input tuples (e.g., "(0,1)") and values
                     are the precomputed results.
    input_values (tuple): A tuple of integer input values (e.g., (0, 1)) for which
                          the neuron's output is to be simulated.

  Returns:
    The precomputed result (typically int or float) from the database, representing
    the neuron's output for the given `input_values`.

  Raises:
    KeyError: If the `input_values` combination is not found in the database
              (propagated from `query_database`).
    TypeError: If `input_values` is not a tuple (propagated from `query_database`).
  """
  return query_database(database, input_values)
