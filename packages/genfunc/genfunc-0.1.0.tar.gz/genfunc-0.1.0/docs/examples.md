# Examples

## Basic Examples

### Mathematical Functions

```python
# Generate a factorial function
result = func.generate(
    "Create a function that calculates the factorial of a number",
    call=True,
    n=5
)
print(result)  # Output: 120

# Generate a Fibonacci sequence function
func.generate("""
Create a function that returns the Fibonacci sequence up to n terms
""")
```

### String Processing

```python
# Generate a string reversal function
result = func.generate(
    "Create a function that reverses a string",
    call=True,
    text="Hello, World!"
)
print(result)  # Output: "!dlroW ,olleH"
```

## Data Processing Examples

### Pandas DataFrame Processing

```python
# Generate a data cleaning function
func.generate("""
Create a function that takes a pandas DataFrame and:
1. Removes duplicate rows
2. Fills missing values with mean
3. Converts dates to datetime
4. Returns the cleaned DataFrame
""")
```

### Data Analysis

```python
# Generate a statistical analysis function
func.generate("""
Create a function that performs statistical analysis on a dataset:
- Calculate mean, median, mode
- Compute standard deviation
- Identify outliers
- Return results as a dictionary
""")
```

## API Integration Examples

### REST API Client

```python
# Generate an API client function
func.generate("""
Create a function that:
1. Makes a GET request to an API endpoint
2. Handles authentication via API key
3. Processes JSON response
4. Returns specific fields
""")
```

## File Processing Examples

### CSV Processing

```python
# Generate a CSV processing function
func.generate("""
Create a function that:
1. Reads a CSV file
2. Processes specific columns
3. Performs calculations
4. Saves results to a new CSV
""")
```

## Algorithm Examples

### Sorting Algorithms

```python
# Generate a QuickSort implementation
func.generate("""
Create a function that implements the QuickSort algorithm
with the following requirements:
1. In-place sorting
2. Handles duplicate values
3. Optimized pivot selection
""")
```

## Error Handling Examples

```python
# Generate a function with robust error handling
func.generate("""
Create a function that processes user input with:
1. Type validation
2. Range checking
3. Error messaging
4. Graceful failure handling
""")
```

Each example includes comments and expected outputs where applicable. Feel free to modify these examples for your specific use case.