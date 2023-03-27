from helper import helper
from db_operations import db_operations

#create connection path to playlist database, create clean data from songs.csv
db_ops = db_operations("playlist.db")
data = helper.data_cleaner("songs.csv")

#start screen of code
def startScreen():
    print("Welcome to your playlist!")

#returns if songs table has any records
def is_empty():
    query = '''
    SELECT COUNT(*)
    FROM songs;
    '''

    result = db_ops.single_record(query)
    return result == 0

#fills table from songs.csv if it's empty
def pre_process():
    if is_empty():
        attribute_count = len(data[0])
        placeholders = ("?,"*attribute_count)[:-1]
        query = "INSERT INTO songs VALUES("+placeholders+")"
        db_ops.bulk_insert(query, data)
        
# NEW
# ask user if they want to load new songs into the database
def user_pre_process():
    print('''Would you like to load new songs into the database?
    1. Yes
    2. No''')
    return helper.get_choice([1,2])
        
# NEW
# fills table from user's .csv file
def fill_table():
    # ask user for location of the file
    file_path = input('Enter the location of the file containing the new songs: ')
    songs = helper.data_cleaner(file_path)
    
    # fill table with songs from file_path
    attribute_count = len(songs[0])
    placeholders = ("?,"*attribute_count)[:-1]
    query = "INSERT INTO songs VALUES("+placeholders+")"
    db_ops.bulk_insert(query, songs)

#show user menu options
def options():
    print('''Select from the following menu options: 
    1. Find songs by artist
    2. Find songs by genre
    3. Find songs by feature
    4. Update song by name
    5. List all attributes of a song by song name
    6. Remove a song by name
    7. Remove records with null values
    8. Exit''')
    return helper.get_choice([1,2,3,4,5,6,7,8])

#search the songs table by artist
def search_by_artist():
    #get list of all artists in table
    query = '''
    SELECT DISTINCT Artist
    FROM songs;
    '''
    print("Artists in playlist: ")
    artists = db_ops.single_attribute(query)

    #show all artists, create dictionary of options, and let user choose
    choices = {}
    for i in range(len(artists)):
        print(i, artists[i])
        choices[i] = artists[i]
    index = helper.get_choice(choices.keys())

    #user can ask to see 1, 5, or all songs
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    #print results
    query = '''SELECT DISTINCT name
    FROM songs
    WHERE Artist =:artist ORDER BY RANDOM()
    '''
    dictionary = {"artist":choices[index]}
    if num != 0:
        query +="LIMIT:lim"
        dictionary["lim"] = num
    results = db_ops.name_placeholder_query(query, dictionary)
    helper.pretty_print(results)

#search songs by genre
def search_by_genre():
    #get list of genres
    query = '''
    SELECT DISTINCT Genre
    FROM songs;
    '''
    print("Genres in playlist:")
    genres = db_ops.single_attribute(query)

    #show genres in table and create dictionary
    choices = {}
    for i in range(len(genres)):
        print(i, genres[i])
        choices[i] = genres[i]
    index = helper.get_choice(choices.keys())

    #user can ask to see 1, 5, or all songs
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    #print results
    query = '''SELECT DISTINCT name
    FROM songs
    WHERE Genre =:genre ORDER BY RANDOM()
    '''
    dictionary = {"genre":choices[index]}
    if num != 0:
        query +="LIMIT:lim"
        dictionary["lim"] = num
    results = db_ops.name_placeholder_query(query, dictionary)
    helper.pretty_print(results)

#search songs table by features
def search_by_feature():
    #features we want to search by
    features = ['Danceability', 'Liveness', 'Loudness']
    choices = {}

    #show features in table and create dictionary
    choices = {}
    for i in range(len(features)):
        print(i, features[i])
        choices[i] = features[i]
    index = helper.get_choice(choices.keys())

    #user can ask to see 1, 5, or all songs
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    #what order does the user want this returned in?
    print("Do you want results sorted in asc or desc order?")
    order = input("ASC or DESC: ")

    #print results
    query = "SELECT DISTINCT name FROM songs ORDER BY "+choices[index]+" "+order
    dictionary = {}
    if num != 0:
        query +=" LIMIT:lim"
        dictionary["lim"] = num
    results = db_ops.name_placeholder_query(query, dictionary)
    helper.pretty_print(results)

# NEW
# updates information for a song
def update_song():
    song = input("Enter song name you would like to update: ")
    # print all attributes of that song
    db_ops.song_attributes(song)
    
    # get songID from song name
    songID = db_ops.find_songID(song)
    
    # ask user which attribute they would like to modify
    print('''Which information would you like to modify?
    1. Song name
    2. Album name
    3. Artist name
    4. Release date
    5. Explicit attribute''')
    choice = helper.get_choice([1,2,3,4,5])

    if choice == 1:
        # update song name
        new_song_name = input("Enter the new song name: ")
        db_ops.update_song_name(new_song_name, songID)
    if choice == 2:
        # update album name
        new_album_name = input("Enter the new album name: ")
        db_ops.update_album_name(new_album_name, songID)
    if choice == 3:
        # update artist name
        new_artist_name = input("Enter the new artist name: ")
        db_ops.update_artist_name(new_artist_name, songID)
    if choice == 4:
        # update release date
        new_release_date = input("Enter the new release date in yyyy-mm-dd format: ")
        db_ops.update_release_date(new_release_date, songID)
    if choice == 5:
        # update explicit value (can only be yes or no)
        print('''Select what you would like to change the explict value to:
        1. True
        2. False''')
        explict_value = helper.get_choice([1,2])
        db_ops.update_explicit_attribute(explict_value, songID)
"""
# NEW
# function to update records in bulk
def update_bulk():
    print('''What would you like to bulk update by?
    1. Album
    2. Artist
    3. Genre''')
    choice = helper.get_choice([1,2,3])
    
    if choice == 1:
        album = input("Which album would you like to bulk update?")
    if choice == 2:
        artist = input("Which artist would you like to bulk update?")
    if choice == 3:
        genre = input("Which genre would you like to bulk update?")
    
    # ask user which attribute they would like to modify
    print('''Which information would you like to modify?
    1. Song name
    2. Album name
    3. Artist name
    4. Release date
    5. Explicit attribute''')
    modify = helper.get_choice([1,2,3,4,5])
    
    if choice == 1:
        # bulk update by album
        if modify == 1:
            # update song
            new_song_name = input("Enter the new song name: ")
            db_ops.bulk_update_song(album, 'Album', new_song_name)
"""
# NEW
# function to help delete song from table
def delete_song():
    song = input("Enter song name you would like to delete: ")
    # get songID from song name
    songID = db_ops.find_songID(song)
    db_ops.remove_song(songID)
    
# NEW
# function to help delete any records with NULL values for any attributes
def delete_null():
    query = '''
    DELETE FROM songs
    WHERE Name IS NULL
    OR Artist IS NULL
    OR Album IS NULL
    OR releaseDate IS NULL
    OR Genre IS NULL
    OR Explicit IS NULL
    OR Duration IS NULL
    OR Energy IS NULL
    OR Danceability IS NULL
    OR Acousticness IS NULL
    OR Liveness IS NULL
    OR Loudness IS NULL;
    '''
    db_ops.delete_null(query)

#main program
startScreen()
pre_process()
user_pre_choice = user_pre_process()
if user_pre_choice == 1:
    fill_table()

#main program loop
while True:
    user_choice = options()
    if user_choice == 1:
        search_by_artist()
    if user_choice == 2:
        search_by_genre()
    if user_choice == 3:
        search_by_feature()
    if user_choice == 4:
        """print("Would you like to bulk update records? Yes (1) or No (2)")
        bulk = helper.get_choice([1,2])
        if bulk == 1:
            update_bulk()
        if bulk == 2:"""
        update_song()
    if user_choice == 5:
        song = input("Enter the song name: ")
        db_ops.song_attributes(song)
    if user_choice == 6:
        delete_song()
    if user_choice == 7:
        delete_null()
    if user_choice == 8:
        print("Goodbye!")
        break

db_ops.destructor()