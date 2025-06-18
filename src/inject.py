from v2_database import inject_dataset

def ask(filepath):
    if filepath:
        inject_dataset(filepath)
        print("Dataset has been successfully injected into the database.")
        return True
    else:
        print("No file provided. Please try again.")
        return False