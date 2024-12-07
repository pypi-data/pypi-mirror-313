# ETL Pipeline Library

## Description

This library is designed for building **ETL pipelines** (Extract, Transform, Load). It provides a set of processors to perform various data operations, such as extracting, transforming, and loading data into the desired format. Each processor in the library is a standalone unit that can be linked together in a chain to perform complex operations.

Processors support working with various data formats (CSV, JSON, ZIP, and others), allow flexible data processing configurations, handle exceptions, and interact with file systems to read and write data.

## Key Features

- **Clean architecture with processor chains**: Each processor performs a specific task and can pass data to the next processor in the chain.
- **Support for various data formats**: The library includes processors for working with CSV, JSON, ZIP, and other formats.
- **Flexibility and configuration**: Support for various configuration options, such as custom converters for numbers, error handling methods, and working with large files.
- **Automation**: Option to automatically delete the source files after processing.
- **Error handling mechanisms**: The library provides support for ignoring or handling different exceptions at various stages of data processing.

## Main Components

### 1. **BaseProcessor**
The base class for all processors. It supports the chain of responsibility, allows configuring subprocessors for parallel or sequential processing, and manages exceptions.

### 2. **ChainAnyProcessor**
A processor that attempts to process data through a series of sub-processors in sequence. 

- **Behavior**:
  - Each sub-processor tries to handle the data.
  - The first successful sub-processor is moved to the front of the chain for prioritization in future attempts.
  - If all sub-processors fail, an error is logged.
- **Use Case**: Useful when there are multiple processors capable of handling the same type of data, but with varying likelihoods of success.

### 3. **ChainAllProcessor**
A processor that runs multiple sub-processors in parallel, either using threads or processes.

- **Behavior**:
  - Executes all sub-processors simultaneously.
  - Yields results from sub-processors as soon as they become available.
  - Logs any exceptions that occur during processing.
- **Use Case**: Ideal for parallelizing independent operations, such as processing different parts of a dataset.

### 4. **HttpDataExtractProcessor**
A processor for extracting data via HTTP GET requests, with the option to save the retrieved data to a file.

### 5. **HttpxStreamDownloadProcessor**
A processor for streaming large file downloads via HTTP, with the ability to process data in parallel.

### 6. **CsvParser**
A processor for parsing CSV files using the `pandas` library. It supports numerous options, including handling delimiters, skipping empty lines, and processing data in chunks.

### 7. **JsonParser**
A processor for parsing JSON data from strings or files into Python dictionaries. It supports configuring how numbers, constants (e.g., NaN), and JSON objects are handled with custom functions.

### 8. **UnzipProcessor**
A processor for extracting files from `.zip` archives. It supports extracting data into files, managing chunk sizes, and deleting the original archive after processing.


### 9. **TarExtractProcessor**
A processor for extracting files from `".tar", ".gz", ".bz2", ".xz", ".tgz", ".tbz2"` archives. It supports extracting data into files, managing chunk sizes, and deleting the original archive after processing.

### 10. **RetryProcessor**

A processor designed to handle transient errors by retrying operations based on a customizable retry policy.

- **Key Features**:
  - **Configurable Retry Logic**: Supports setting a maximum number of retries and delays between attempts (fixed or exponential backoff).
  - **White-listed Exceptions**: Retries only specific exceptions defined by the user.
  - **Logging and Metrics**: Logs every retry attempt and provides details about failures.
  - **Fallback Handling**: Allows defining a fallback action if all retry attempts fail.
- **Use Case**: Ideal for handling temporary issues like network timeouts, database connection errors, or transient API failures.

## Example Usage


### Example ETL Pipeline(Flow 1: Using Operator Overloads)

```python
from pipelet.processors.http import HttpDataExtractProcessor
from pipelet.processors.csv_parser import CsvParser
from pipelet.processors.json_parser import JsonParser
from pipelet.processors.unzip import UnzipProcessor
from pipelet.processors.file_system import AbstractFileSystemManager

# Create file system manager
file_system_manager = AbstractFileSystemManager()

# Create processors
http_processor = HttpDataExtractProcessor(file_system_manager)
csv_parser = CsvParser(file_system_manager)
json_parser = JsonParser(file_system_manager)
unzip_processor = UnzipProcessor(file_system_manager)

# Create processor chain using `>>`
pipeline = http_processor >> csv_parser >> json_parser >> unzip_processor

# Run the pipeline
input_data = "https://example.com/data.zip"
for output in pipeline.process(input_data):
    print(output)
```

### Example ETL Pipeline(Flow 2: Combining Parallel and Sequential Processing)

```python
from pipelet.operations import Op, OpAll, OpAny, PipelineConverter
from pipelet.processors.file_system import FileModeEnum

def main():
    # Define the pipeline with parallel processing for parsing and unzipping

    pipeline = [
        Op(
            BaseOpEnum.downloading, 
            kwargs={
                "file_system_manager": {
                    "path": ..., # Here can be your custom file system manager (as an example S3)
                    "kwargs": {...},
                },
                "retry_args": {
                    "retry_processor": ..., # Here can be your custom retry processor
                    "max_retries": 3,
                    "delay": 1,
                    "delay_step": 1,
                    "retry_with_white_exc": True,
                },
                "logging_args": {
                    "logger": ..., # Here can be your custom logger
                    "logging": True, # Logging intup data
                },
            }
        ),
        Op(
            BaseOpEnum.upzip,
            kwargs={
                "file_system_manager": {
                    "path": ..., # Here can be your custom file system manager (as an example S3)
                    "kwargs": {...},
                },
            }
        ),
        OpAny(
            operations = [
                Op(
                    BaseOpEnum.json_parsing, 
                    kwargs={
                        "file_system_manager": {
                            "path": ..., # Here can be your custom file system manager (as an example S3)
                            "kwargs": {...},
                        },
                    }
                ),
                Op(
                    BaseOpEnum.csv_parsing, 
                    kwargs={
                        "file_system_manager": {
                            "path": ..., # Here can be your custom file system manager (as an example S3)
                            "kwargs": {...},
                        },,
                        "white_exceptions": [
                            TypeError,
                            BaseExceptionsEnum.csv_parsing_error,
                            BaseExceptionsEnum.file_system_exception,
                        ],
                    }
                ),
            ],
            kwargs = {...}
        ),
        OpAll(
            operations=[
                Op(
                    "app.processor.CustomProcessor",
                    kwargs = {...}
                ),
                Op(
                    "app.processor.CustomProcessor",
                    kwargs = {...}
                ),
            ],
            kwargs={"use_threads": True} # You can use both threads and processes.
        )
    ]

    # Convert the high-level pipeline definition into a processor chain
    processor = PipelineConverter(pipeline=pipeline).convert()

    # Execute the pipeline
    input_data = "https://example.com/data.zip"
    for output in processor.process(input_data):
        print(output)

if __name__ == "__main__":
    main()
```

## Extensibility
The library is developer-friendly, making it easy to extend and integrate custom processors. Adding a new processor involves subclassing BaseProcessor and implementing its process method. This design ensures seamless integration with existing pipelines.

## Example Usage

```python
from pipelet.processors.base import BaseProcessor
from pipelet.decorators import logging_decorator

class CustomProcessor(BaseProcessor):
    @logging_decorator(custom_logger=...) # If you need this you can use either a custom logger or a default logger
    def process(self, input_data):
        # Custom data processing logic
        yield transformed_data
```

This library is designed to handle a wide range of ETL requirements, making it a reliable choice for both simple and complex workflows. Whether you’re dealing with small-scale data extraction or managing high-throughput pipelines, the library’s flexibility, extensibility, and robust error handling provide a solid foundation for your ETL needs.