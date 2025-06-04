# Weather Data Filtering Project

This project provides tools for filtering and analyzing snow depth measurements from weather stations.

## Prerequisites

- Python 3.10 (recommended for data science work)
- Git
- VS Code with Python and Jupyter extensions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/WeatherDataFiltering.git
cd WeatherDataFiltering
```

2. Set up Python 3.10 on your Mac:
```bash
brew install python@3.10
```

3. Create and activate a virtual environment:
```bash
python3.10 -m venv venv
source venv/bin/activate
```

4. Install required packages:
```bash
pip install pandas matplotlib jupyter sqlalchemy
```

## VS Code Setup

1. Open VS Code
2. Install recommended extensions:
   - Python
   - Jupyter
3. Select Python Interpreter:
   - Press `Cmd + Shift + P`
   - Type "Python: Select Interpreter"
   - Choose the interpreter from your virtual environment

## Running the Analysis

1. Open the project in VS Code:
```bash
code .
```

2. Navigate to `src/notebooks/jesses_may2025_filtering.ipynb`
3. Click "Run All" to execute all cells

## Project Structure

```
WeatherDataFiltering/
├── src/
│   ├── notebooks/
│   │   └── jesses_may2025_filtering.ipynb
│   └── utils/
│       ├── snow_depth_utils.py
│       └── filtered_observation.py
├── venv/
└── README.md
```

## Troubleshooting

- If you see "Module not found" errors, ensure your virtual environment is activated
- For database connection issues, verify your credentials in the notebook
- For plotting issues, make sure matplotlib is installed

## Configuration

The filtering parameters can be adjusted in `src/utils/snow_depth_utils.py`:
- `SNOW_DEPTH_CONFIG`: Settings for total snow depth
- `SNOW_DEPTH_24H_CONFIG`: Settings for 24-hour snow measurements

## Support

For questions or issues, please open a GitHub issue or contact [your contact info]