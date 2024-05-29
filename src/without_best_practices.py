from parsons import GoogleBigQuery
import pandas as pd
import os

##########


def my_function(data):
    output = []

    for x in data:
        output.append(x.to_dataframe())

    return pd.concat(output).sort_values(by="player_name").reset_index(drop=True)


def main():
    print("Starting the script...")
    # Object instantiated in main function
    bq = GoogleBigQuery(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])

    print("Running queries...")
    # Repetitive code
    jalen_brunson = bq.query(
        "select player_name, avg_points from nba_dbt__clean.cln_player__averages where player_name = 'Jalen Brunson'"
    )
    print("Successfully queried Jalen Brunson...")

    josh_hart = bq.query(
        "select player_name, avg_points from nba_dbt__clean.cln_player__averages where player_name = 'Josh Hart'"
    )
    print("Successfully queried Josh Hart...")

    dante_divencenzo = bq.query(
        "select player_name, avg_points from nba_dbt__clean.cln_player__averages where player_name = 'Donte DiVincenzo'"
    )
    print("Successfully queried Donte DiVincenzo...")

    # Invoke ambiguous function
    data = my_function([jalen_brunson, josh_hart, dante_divencenzo])

    print("\nEnd result...\n")
    print(data.head())


if __name__ == "__main__":
    main()
