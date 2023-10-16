import sqlite3

def main(param_dict):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        List: List of reviews for the given dealership
    """
    
    # Assuming you pass the path to the SQLite database in the parameters
    db_path = param_dict.get("DB_PATH")

    if not db_path:
        return {"error": "DB_PATH is not provided"}

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Execute a query to fetch all reviews
        cursor.execute("SELECT * FROM reviews")
        reviews = cursor.fetchall()

        # Close the connection
        conn.close()
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return {"error": str(e)}

    # Convert the raw reviews data (list of tuples) into a more friendly format
    reviews_list = [{"id": r[0], "review": r[1]} for r in reviews]  # Adjust this based on your table structure

    return {"reviews": reviews_list}
