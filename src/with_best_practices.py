from parsons import Table, GoogleBigQuery
import pandas as pd
import os
from typing import List
from time import sleep

##########


def aggregate_data(query_results: List[Table]) -> pd.DataFrame:
    """
    Takes a list of Parsons Tables, converts them to DataFrame objects,
    and returns a stacked DataFrame object
    """

    # Running list of DataFrames
    output = []

    # Loop through query results and append DataFrame to list
    for result in query_results:
        output.append(result.to_dataframe())

    return pd.concat(output).sort_values(by="player_name").reset_index(drop=True)


def nba_player_query(
    bq: GoogleBigQuery,
    player_name: str,
    dataset_name: str = "nba_dbt__clean",
    table_name: str = "cln_player__averages",
) -> Table:
    """
    Queries a given `dataset.table` with a given NBA player name
    """

    # NOTE - Even this is not best practice!
    # https://www.w3schools.com/sql/sql_injection.asp
    base_query = f"select player_name, avg_points from {dataset_name}.{table_name} where player_name = '{player_name}'"
    response = bq.query(sql=base_query)
    print(f"Successfully queried {player_name}...")

    return response


def main(bq: GoogleBigQuery, player_names: list):
    """
    Loops through NBA players, gets their stats, and prints to the console
    """

    print("Starting the script...")
    # Running list of NBA player data
    nba_player_data = []

    # Loop through incoming list of players and add their data to the list
    print("Running queries...")
    for player in player_names:
        nba_player_data.append(nba_player_query(bq=bq, player_name=player))

    # Stack the player data and print to the console
    knicks_players = aggregate_data(query_results=nba_player_data)

    # For dramatic effect
    sleep(1)

    print("\nEnd result...\n")
    print(knicks_players.head())


#####

if __name__ == "__main__":
    """
    By instantiating these variables and objects OUTSIDE of the main function,
    we can control what goes into our program at runtime. That means we can easily
    test this code by mocking the `GoogleBigQuery` object
    """

    BIGQUERY = GoogleBigQuery(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
    TESTING = str(os.environ.get("TESTING")) == "true"

    VILLANOVA_PLAYERS = ["Donte DiVincenzo", "Josh Hart", "Jalen Brunson"]
    KENTUCKY_PLAYERS = ["Julius Randle", "Immanuel Quickley", "Jacob Toppin"]

    # We'll toggle between these two lists depending on the environment
    PLAYER_NAMES = KENTUCKY_PLAYERS if TESTING else VILLANOVA_PLAYERS

    main(bq=BIGQUERY, player_names=PLAYER_NAMES)
