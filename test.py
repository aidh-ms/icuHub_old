

def main():
    """Test runtime of the app."""
    import db.mimic as mimic

    print(mimic.get_vitalsign(34422196))


if __name__ == "__main__":
    main()
