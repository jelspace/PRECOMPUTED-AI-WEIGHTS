' precomputed_neuron.bas
' Author: AI Agent (Bard)
' Date: 2025-06-07 ' Current date during generation
'
' Description:
' This program demonstrates the core concept of precomputed AI weights
' as might be referenced in a project like "PRECOMPUTED-AI-WEIGHTS".
' It simulates a single, simple neuron where the multiplication results
' (input * weight) for all possible discrete input values are precomputed
' and stored in a lookup table.
'
' The primary goal is to show how, by precomputing these results, one can
' avoid repeated multiplications during an "inference" step. This is
' particularly relevant for scenarios with quantized inputs (represented
' here by integer inputs) and can lead to significant power and time
' savings in hardware implementations or performance-critical software.
'
' Key concepts demonstrated:
' 1. Neuron Parameter Definition: Setting up the basic characteristics of our simulated neuron.
' 2. Precomputation: Calculating all possible 'input * weight' products beforehand.
'    This step is done once, typically at a "design" or "compile" time.
' 3. Lookup Table: Storing these precomputed values in an array. This array
'    simulates the "database" of precomputed weights. In a real system, this
'    could be ROM, a dedicated memory block, or part of a larger database.
' 4. Optimized "Inference": Retrieving results directly from the lookup table
'    using the input value as an index, instead of performing a multiplication.
'    This simulates a faster, more efficient inference process.

' Define Neuron Parameters
' These constants define the basic properties of our simplified neuron.
Const INPUT_BITS As Integer = 4          ' Number of bits for the input. This determines the range of possible input values.
                                         ' For example, 4 bits mean 2^4 = 16 possible discrete input values (0-15).
Const NUM_INPUT_VALUES As Integer = 2 ^ INPUT_BITS ' Total number of unique input values possible.
Const NEURON_WEIGHT As Single = 0.75     ' The weight of our neuron. In a real neural network, this would be a learned parameter.
                                         ' We use a Single here for floating-point multiplication.

Print "Neuron Parameters:"
Print "Input Bits: ", INPUT_BITS
Print "Number of Possible Input Values: ", NUM_INPUT_VALUES
Print "Neuron Weight: ", NEURON_WEIGHT
Print

' Precomputation Logic
' This section calculates all possible output values for the neuron and stores them.
' The lookupTable acts as our database of precomputed results.
' 'Shared' makes this table accessible by functions outside the main program block.
Dim Shared lookupTable(0 To NUM_INPUT_VALUES - 1) As Single

Print "Populating Lookup Table..."
' Loop through every possible discrete input value.
For i As Integer = 0 To NUM_INPUT_VALUES - 1
    ' Perform the multiplication once and store it.
    ' This is the core of the "precomputation" step.
    lookupTable(i) = i * NEURON_WEIGHT
Next i
Print "Lookup Table Populated."
Print

' Display a few entries from the lookup table for verification.
' This helps to confirm that the precomputation logic worked as expected.
Print "Sample Lookup Table Entries:"
' Using IIf for a compact way to avoid going out of bounds if NUM_INPUT_VALUES is small.
For i As Integer = 0 To IIf(NUM_INPUT_VALUES - 1 < 4, NUM_INPUT_VALUES - 1, 4) ' Display up to the first 5 entries
    Print "Input "; i; " -> Precomputed Output: "; lookupTable(i)
Next i
Print

' Lookup Function
' This function simulates the "inference" step in our precomputed neuron.
' Instead of calculating 'inputValue * NEURON_WEIGHT', it fetches the result
' directly from the 'lookupTable'.
Function getPrecomputedOutput(inputValue As Integer) As Single
    ' Input validation: Ensure the input is within the range of our precomputed values.
    If inputValue < 0 Or inputValue >= NUM_INPUT_VALUES Then
        Print "Error: Input value "; inputValue; " is out of range."
        Return 0 ' Return a default/error value. In a real system, error handling might be more complex.
    End If
    ' Retrieve the precomputed result from the table. This is much faster than multiplication.
    Return lookupTable(inputValue)
End Function

Print "Lookup Function Defined."
Print

' Main Demonstration Section
' This section shows the lookup function in action with various inputs.
Print "Demonstrating Lookup Function:"

' Test with some valid inputs to show normal operation.
Dim testInputs(0 To 2) As Integer
testInputs(0) = 3
testInputs(1) = 0                        ' Test with zero input.
testInputs(2) = NUM_INPUT_VALUES - 1     ' Test boundary condition (maximum valid input).

For i As Integer = 0 To UBound(testInputs)
    Dim currentInput As Integer = testInputs(i)
    Dim outputVal As Single = getPrecomputedOutput(currentInput)
    Print "Input: "; currentInput; ", Precomputed Output: "; outputVal
Next i

' Test with an invalid input (out of range) to demonstrate error handling.
Print
Print "Demonstrating Lookup Function with invalid input:"
Dim invalidInput As Integer = NUM_INPUT_VALUES ' This value is one greater than the max index.
Dim outputInvalid As Single = getPrecomputedOutput(invalidInput)
Print "Input: "; invalidInput; ", Precomputed Output: "; outputInvalid

invalidInput = -1 ' Test with a negative input, also out of range.
outputInvalid = getPrecomputedOutput(invalidInput)
Print "Input: "; invalidInput; ", Precomputed Output: "; outputInvalid

Print
Print "Demonstration Complete."

' End of program - standard practice in FreeBASIC to explicitly end the program.
End
