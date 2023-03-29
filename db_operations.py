import sqlite3
import datetime

class db_operations():

    #constructor with connection path to DB
    def __init__(self, conn_path):
        self.connection = sqlite3.connect(conn_path)
        self.cursor = self.connection.cursor()
        print("connection made..")

    #creates table songs in our database
    def create_songs_table(self):
        query = '''
        CREATE TABLE songs(
            songID VARCHAR(22) NOT NULL PRIMARY KEY,
            Name VARCHAR(20),
            Artist VARCHAR(20),
            Album VARCHAR(20),
            releaseDate DATETIME,
            Genre VARCHAR(20),
            Explicit BOOLEAN,
            Duration DOUBLE,
            Energy DOUBLE,
            Danceability DOUBLE,
            Acousticness DOUBLE,
            Liveness DOUBLE,
            Loudness DOUBLE
        );
        '''
        self.cursor.execute(query)
        print('Table Created')

    # function to return a single value from table
    def single_record(self,query):
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    
    # function for bulk inserting records
    def bulk_insert(self,query,records):
        self.cursor.executemany(query,records)
        #self.connection.commit()
        print("query executed..")

    # function to return a single attribute values from table
    def single_attribute(self,query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        #results.remove(None)
        return results
    
    def check_song_name(self):
        choice = input("Enter name of the song: ")
        self.cursor.execute("SELECT * FROM songs WHERE Name = ?", (choice,))
        results = self.cursor.fetchall()
        while len(results) <= 0:
            # song is not in the table
            print("Song is not in the table. Try again.")
            choice = input("Enter name of the song: ")
            self.cursor.execute("SELECT * FROM songs WHERE Name = ?", (choice,))
            results = self.cursor.fetchall()
        return choice
    
    # function to return all attributes given song name
    def song_attributes(self, song_name):
        query = "SELECT * FROM songs WHERE Name = ?"
        self.cursor.execute(query, (song_name,))
        results = self.cursor.fetchone()
        
        # prints attributes with attribute name
        print("Attributes for " + song_name + ": ")
        for attribute in range(len(results)):
            name = self.cursor.description[attribute][0]
            value = results[attribute]
            print(str(name) + ": " + str(value))
            
    # function to update song name
    def update_song_name(self, new_song, songID):
        query = '''
        UPDATE songs
        SET Name = ?
        WHERE songID = ?
        '''
        self.cursor.execute(query, (new_song, songID))
        print("Song name update completed!")
        
    # function to update album name
    def update_album_name(self, new_album, songID):
        query = '''
        UPDATE songs
        SET Album = ?
        WHERE songID = ?
        '''
        self.cursor.execute(query, (new_album, songID))
        print("Album name update completed!")
        
    # function to update artist name
    def update_artist_name(self, new_artist, songID):
        query = '''
        UPDATE songs
        SET Artist = ?
        WHERE songID = ?
        '''
        self.cursor.execute(query, (new_artist, songID))
        print("Artist name update completed!")
        
    # function to check if user entered correct format for releaseDate
    def check_date_format(self):
        date = input("Enter a date in yyyy-mm-dd format: ")
        while True:
            try:
                date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date. Try again.")
                date = input("Enter a date in yyyy-mm-dd format: ")
        return date
                
    # function to update release date
    def update_release_date(self, new_date, songID):
        query = '''
        UPDATE songs
        SET releaseDate = ?
        WHERE songID = ?
        '''
        self.cursor.execute(query, (new_date, songID))
        print("Release date update completed!")
        
    # function to update explicit attribute
    def update_explicit_attribute(self, value, songID):
        if value == 1:
            query = '''
            UPDATE songs
            SET Explicit = "True"
            WHERE songID = ?
            '''
        if value == 2:
            query = '''
            UPDATE songs
            SET Explicit = "False"
            WHERE songID = ?
            '''
        self.cursor.execute(query, (songID,))
        print("Explicit value update completed!")
    
    # function to delete a song given the songID
    def remove_song(self, songID):
        query = '''
        DELETE FROM songs
        WHERE songID = ?
        '''
        self.cursor.execute(query, (songID,))
        print("Song deletion completed!")
            
    # function to return the songID given the song name
    def find_songID(self, song_name):
        query = "SELECT songID FROM songs WHERE Name = ?"
        self.cursor.execute(query, (song_name,))
        results = self.cursor.fetchone()
        return results[0]
    
    # function to remove all records that have a NULL attribute
    def delete_null(self, query):
        self.cursor.execute(query)
        print("Deletion of null records completed!")

    # SELECT with named placeholders
    def name_placeholder_query(self,query,dictionary):
        self.cursor.execute(query,dictionary)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        return results

    #destructor that closes connection with DB
    def destructor(self):
        self.connection.close()