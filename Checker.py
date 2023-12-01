import sqlite3


def query1():
     # Query 1
    print("Years chosen : ")
    query = "SELECT Year FROM SummerOlympics" 
    cursor.execute(query)
    years = cursor.fetchall()
    for year in years:
        print(year[0])

def query2():
    # Query 2
    print("\nMost ranked country : ")

    query = """
    SELECT Country, COUNT(*) AS Count
    FROM (
        SELECT Rank_1_nation AS Country FROM SummerOlympics
        UNION ALL
        SELECT Rank_2_nation AS Country FROM SummerOlympics
        UNION ALL
        SELECT Rank_3_nation AS Country FROM SummerOlympics
    )
    WHERE Country IS NOT NULL
    GROUP BY Country
    ORDER BY Count DESC
    LIMIT 1
    """
    cursor.execute(query)
    print(cursor.fetchone()[0])

def query3():
    # Query 3
    print("\nAverage Number of althletes : ")
    query = "SELECT AVG(Athletes) FROM SummerOlympics" 
    cursor.execute(query)
    print(cursor.fetchone()[0])



print('in checker')
# Create a SQLite DB
conn = sqlite3.connect('OlympicsData.db')
cursor = conn.cursor()

# Check if database rows are completely populated
query = "SELECT COUNT(*)  FROM SummerOlympics WHERE DONE_OR_NOT_DONE = 0" 
cursor.execute(query)
count = cursor.fetchone()[0]

if(count==0):
    print("\nDatabase is completely populated\n")
    # Q1 - What are the years chosen?
    query1()
    # Q2 - Which country has been most ranked?
    query2()
    # Q3 - What are the average number of atheletes?
    query3()
else:
    print("\nDatabase is NOT completely populated !!")
    