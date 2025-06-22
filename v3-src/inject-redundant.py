from database import inject_dataset

def get_file(filepath):
    boolean = False
    try:
        boolean = inject_dataset(filepath)
        if boolean == True and filepath:
            print("[inject] dataset has been successfully injected into the database.")
            boolean = True
            return boolean
        else:
            print("[inject] no file provided. Please try again.")
            boolean = False
            return boolean
    except Exception as e:
            print(f"[get_file] error: {e}")
            boolean = False
            return boolean
    
 