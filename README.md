   # Bike Sharing Dashboard

This repository contains a **Bike Sharing Dashboard** project developed using Python and Streamlit. It visualizes key metrics about bike-sharing data, including rentals by season, user types, and weather conditions.

## Setup Environment Using Anaconda

Follow these steps to set up your environment with Anaconda:

1.  Create and activate a new environment:
    ```bash
    conda create --name main-ds python=3.9
    conda activate main-ds
    ```
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Setup Environment Using Shell/Terminal

For those not using Anaconda, follow these steps to set up the environment using pipenv:

1.  Create a new project folder and navigate to it:
    ```bash
    mkdir proyek_analisis_data
    cd proyek_analisis_data
    ```
2.  Install dependencies using `pipenv`:
    ```bash
    pipenv install
    pipenv shell
    pip install -r requirements.txt
    ```

## Run the Streamlit App

Once the environment is set up, you can run the Streamlit app with the following command:

```bash
cd dashboard
streamlit run dashboard.py
```