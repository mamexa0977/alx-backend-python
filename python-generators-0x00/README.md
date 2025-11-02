# Python Generators Project

This project demonstrates advanced usage of Python generators for efficient data processing with large datasets.

## Project Structure

- `seed.py` - Database setup and seeding
- `0-stream_users.py` - Single row streaming with generators
- `1-batch_processing.py` - Batch processing with memory efficiency
- `2-lazy_paginate.py` - Lazy loading paginated data
- `4-stream_ages.py` - Memory-efficient aggregation

## Features

1. **Database Setup**: MySQL database creation and population
2. **Generator Streaming**: Efficient row-by-row data access
3. **Batch Processing**: Memory-efficient large dataset handling
4. **Lazy Pagination**: On-demand data loading
5. **Memory-Efficient Aggregation**: Calculating averages without loading all data

## Requirements

- Python 3.x
- MySQL Server
- mysql-connector-python

## Installation

```bash
pip install mysql-connector-python