

def main():
    """Test runtime of the app."""
    from pyICU.connection.Connector import MimicConnector
    from pyICU.connection.key import mimic_demo_engine

    """Test connection to mimic database and concept loading."""
    connector = MimicConnector(mimic_demo_engine)
    print(connector.concepts)
    print(connector.execute_query(
        "SELECT * FROM mimiciv_derived.icustay_detail LIMIT 10;"))


if __name__ == "__main__":
    main()
