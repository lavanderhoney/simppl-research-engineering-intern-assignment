# research-engineering-intern-assignment

The dashboard is hosted on: https://simppl-research-engineering-intern.onrender.com/
**NOTE**:Because of the free tier of Render, the website may take some time to load, while displaying a 502 error.
## Overview

This repository contains the assignment for the Research Engineering Intern position at Simppl. The project demonstrates the application of data analysis and visualization techniques to derive insights from a given dataset.

## Repository Structure

The repository is organized as follows:

- **`notebooks/`**: Jupyter notebooks detailing the data analysis process.
- **`frontend/`**: Python script for the Streamlit dashboard.
    - **`/plots`**: HTML files of the interactive plotly plots
    - **`/pages`**: Python script for storytelling and chatbot pages of the dashboard.
- **`requirements.txt`**: Lists the Python dependencies required to run the project.

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/lavanderhoney/simppl-research-engineering-intern-assignment.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd simppl-research-engineering-intern-assignment
   ```

3. **Create and activate a virtual environment**:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use 'env\Scripts\activate'
   ```

4. **Install the required dependencies**:

   ```bash
   cd frontend
   pip install -r requirements.txt
   ```

## Usage

```bash
cd frontend
streamlit run dashboard.py
```
## Screenshots
![alt text](<Screenshot 2025-03-18 224728.png>)
![alt text](<Screenshot 2025-03-18 224737.png>)
![alt text](<Screenshot 2025-03-18 224809.png>)
![alt text](<Screenshot 2025-03-18 224846.png>)
![alt text](<Screenshot 2025-03-18 224908.png>)
![alt text](<Screenshot 2025-03-18 224927.png>)
![alt text](<Screenshot 2025-03-18 224939.png>)
![alt text](<Screenshot 2025-03-18 224958.png>)
![alt text](<Screenshot 2025-03-18 225012.png>)

## Demo Video
Part-1: https://drive.google.com/file/d/13ocoqQanRAtgbTJ1iP2qsTd_66X8UguW/view?usp=sharing
Part-2: https://drive.google.com/file/d/1Ka9hpGMqJkscEcNp168iC_eYQT7x7mjQ/view?usp=sharing