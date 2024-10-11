import DBHelper as db
import AIHelper as ai

def createVenue():
    db.dropTable("Venue")
    response = ai.askAI("Create a table called Venue that has the Venue name (string), address (string), and capacity (int). It should also have a separate, unique id that auto increments.")
    db.runPostQuery(response)
    response = ai.askAI("Populate an existing Venue table with columns (name, address, capacity) with 10 concert venues around salt lake city and provo, utah. If you can't find 10, make some up please! Also, include the full address in the address column, please")
    db.runPostQuery(response)

def createBand():
    db.dropTable("Band")
    response = ai.askAI("Create a table called Band that has the bandName (string), genre (string), numAlbums (int), and numSongs (int). It should also have a separate, unique id that auto increments.")
    db.runPostQuery(response)
    response = ai.askAI("Populate an existing Band table with columns (bandName, genre, numAlbums, numSongs) with 20 different bands. Please include Breaking Benjamin, Myles Smith, and The Maine, but the rest you can choose. If you can't find the genre, number of albums, or number of songs, you can make them up.")
    db.runPostQuery(response)

def createAttendee():
    db.dropTable("Attendee")
    response = ai.askAI("Create a table called Attendee that has a unique username (string), a firstName (string), a lastName (int). username is the primary key.")
    db.runPostQuery(response)
    response = ai.askAI("Populate an existing Attendee table with columns (username, firstName, lastName) with 80 different attendees. Please include some duplicate first names, some duplicate last names, and some duplicate combinations, but not a ton of each. You can make all of these up.")
    db.runPostQuery(response)

def createConcert():
    db.dropTable("Concert")
    response = ai.askAI("Create a table called Concert that has a date (string), a time (string), and a venueID, which is a foreign key referencing the 'id' column in the 'Venue' table. It should also have a separate, unique id that auto increments. The combination of date and venueId should be unique.")
    db.runPostQuery(response)
    venueRows = db.runGetQuery("SELECT * FROM Venue")
    response = ai.askAI("Populate an existing Concert table with columns [date or time in ISO 8601 FORMAT] (date, time, venueID) with 25 different concerts. You can make all of these up, but the venueId must reference an existing id from the Venue table. Also, times should be on the hour or on the half-hour. Here are the venue rows: " + str(venueRows))
    db.runPostQuery(response)

def createTicket():
    db.dropTable("Ticket")
    response = ai.askAI("Create a table called Ticket that has an associated username that references the username from the Attendee table and an associated concertId that references id from the Concert table. It should also have a separate, unique id that auto increments.")
    db.runPostQuery(response)
    attendeeRows = db.runGetQuery("SELECT username FROM Attendee")
    concertRows = db.runGetQuery("SELECT id FROM Concert")
    response = ai.askAI("Populate the existing Ticket table with columns (username, concertId) by creating between 1-5 rows for each username and connecting them to an existing concertId (same concertId for the username. for example, user1 might have 3 rows connected to concert id=5, and user2 might have 4 rows with concert id=14) Please do this for all 80 usernames, but vary the number of rows for each username between 1 and 5. Here are Attendees: " + str(attendeeRows) + ", and here are the concerts: " + str(concertRows))
    db.runPostQuery(response)

def createBandPlaysConcert():
    db.dropTable("BandPlaysConcert")
    response = ai.askAI("Create a table called BandPlaysConcert. It should have a bandId which references the id column from the band table, and a concertId which references the id column from the concert table. There should also be a separate, unique id that auto increments. The combination of bandId and concertId should be unique")
    db.runPostQuery(response)
    bandRows = db.runGetQuery("SELECT id FROM Band")
    concertRows = db.runGetQuery("SELECT id FROM Concert")
    response = ai.askAI("Populate the existing BandPlaysConcert table with columns (bandId, concertId) by taking the ids from the band rows and connecting them to the ids from the concert row. Every concertId should have at least 3 rows with different bandIds. Exclude bandId 13 and 17 from this table, but include all other bandIds. Here are the bandIds: " + str(bandRows) + " and here are the concertIds: " + str(concertRows))
    db.runPostQuery(response)