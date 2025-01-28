# Crime Analysis Project

## Overview
This project aims to analyze crime data to identify patterns, trends, and insights that can aid law enforcement agencies, policymakers, and researchers. The dataset includes detailed metadata about reported crimes, including their type, location, time, and associated attributes.

## Dataset Fields
The dataset contains the following key fields:

- **ID**: A unique identifier for each crime record.
- **Case Number**: A unique identifier for the crime case.
- **Date**: The timestamp when the crime was reported.
- **Block**: The address block where the crime occurred (e.g., street name and number).
- **IUCR**: The Illinois Uniform Crime Reporting code, categorizing the crime type.
- **Primary Type**: The broad category of the crime (e.g., theft, assault).
- **Description**: A more detailed description of the crime.
- **Location Description**: The place where the crime occurred (e.g., residence, street).
- **Arrest**: Indicates if an arrest was made (True/False).
- **Domestic**: Whether the crime involved domestic issues (True/False).
- **Beat**: The police beat where the crime occurred (a geographic area patrolled by police).
- **District**: The police district where the crime was reported.
- **Ward**: The city ward (political divisions) of the crime location.
- **Community Area**: A neighborhood or community area in the city.
- **FBI Code**: The FBI classification code for the crime.
- **X Coordinate, Y Coordinate, Latitude, Longitude**: Geographical coordinates of the crime location.
- **Location**: The specific location, which could be a set of coordinates or a general address.
- **Year**: The year the crime occurred.
- **Updated On**: The timestamp when the data was last updated.

## Goals
1. **Trend Analysis**: Identify temporal trends in crime rates (e.g., year-over-year changes).
2. **Spatial Analysis**: Map crime hotspots and analyze geographic patterns.
3. **Crime Classification**: Categorize crimes using IUCR and FBI codes.
4. **Arrest Patterns**: Evaluate the relationship between arrests and crime types or locations.
5. **Domestic Crimes**: Study domestic crimes and their prevalence in specific areas.

## Tools and Technologies
- **Programming Languages**: Python
- **Data Analysis Libraries**: Pandas, Pyspark
- **Visualization Libraries**: JavaScript
- **Big Data Tools**: Apache Spark, Hadoop

## Key Features
- **Data Cleaning**: Handle missing values, remove duplicates, and standardize formats.
- **Exploratory Data Analysis (EDA)**: Generate descriptive statistics and visualizations.
- **Predictive Modeling**: Use machine learning algorithms to predict crime trends.
- **Interactive Dashboards**: Create dashboards for real-time crime monitoring.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/amoeed786/Big-Data-Project.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Big_Data_Project
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
For Dataset you can use below link to download it first.
[Kaggle Dataset Link](https://www.kaggle.com/datasets/adelanseur/crimes-2001-to-present-chicago)
1. Load the dataset into the project directory.
2. Run Pyspark_scripty script:
   ```bash
   python Pyspark_scripty.py
   ```
3. Make sure to config Hadoop Setup as well.
4. Perform analysis using the provided Jupyter notebooks.
5. Generate visualizations and reports.


## Contact
For questions or collaboration opportunities, please contact:
- **Name**: [Abdul Moeed]
- **Email**: [moeedrajpoot59@gmail.com]
- **GitHub**: [amoeed786]

---

Happy analyzing! 🎉