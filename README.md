# ML4T (CS7646) Environment Setup

## Required Files

This project requires stock data CSV files in the `data/` directory:
- `data/AAPL.csv` - Apple stock data
- `data/IBM.csv` - IBM stock data

## Setup Instructions

### For Enrolled ML4T Students
Follow the ML4T Development Environment course setup instructions found in Canvas for your term.

### For Non-Enrolled Visitors
1. Download the required data files from the historical course webpage:
   - Navigate to: Current Semester -> Software Setup and Local Environment
   - Download the data folder contents

2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Place the CSV files in the `data/` directory:
   ```
   CS7646/
   ├── data/
   │   ├── AAPL.csv
   │   └── IBM.csv
   ├── PY3.py
   ├── requirements.txt
   └── README.md
   ```

## Running the Code

The `PY3.py` file contains multiple examples. Currently, only the last example will run when executing:
```bash
python PY3.py
```

To run specific examples, you may need to comment out other `if __name__ == "__main__"` blocks.

## Data Format

The CSV files should contain columns:
- Date
- Open
- High
- Low
- Close
- Volume
- Adj Close
