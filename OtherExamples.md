# Further experiments using the AI

## Other successful prompts

### Example 1 - Asking the AI to populate a table with complicated rules about which rows to include
I found that the LLM was good at populating tables with rows based on complex input (as long as the input was specific).
1. **Prompt from me:**
>"Populate the existing BandPlaysConcert table with columns (bandId, concertId) by taking the ids from the band rows and connecting them to the ids from the concert row.
>Every concertId should have at least 3 rows with different bandIds. Exclude bandId 13 and 17 from this table, but include all other bandIds.
>Here are the bandIds: [(1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,), (11,), (12,), (13,), (14,), (15,), (16,), (17,), (18,), (19,), (20,)]
>and here are the concertIds: [(1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,), (11,), (12,), (13,), (14,), (15,), (16,), (17,), (18,), (19,), (20,), (21,), (22,), (23,), (24,), (25,)]"

2. **AI-generated SQLite:**
```
Response: 
 INSERT INTO BandPlaysConcert (bandId, concertId)
SELECT b.id, c.id
FROM Band b
JOIN Concert c
WHERE b.id NOT IN (13, 17)
ORDER BY RANDOM()
LIMIT 60;
```  
3. **Response:**
>"I have successfully populated the BandPlaysConcert table using a dynamic approach. The SQL code I used selects bandId and concertId from the Band and Concert tables while excluding bandId 13 and 17. The results are randomly ordered, and the statement inserts a total of 60 entries into the table."

### Example 2 - Asking for counts
I found that the LLM was good at counting data within a table (though sometimes in it's conversation it misunderstood what to say about the count)
1. **Prompt from me:**
>"How many bands are playing at concerts?"

2. **AI-generated SQLite:**
```
SELECT COUNT(DISTINCT BandPlaysConcert.bandId) AS numBandsPlaying
FROM BandPlaysConcert;
```  
3. **Response:**
>"Great news! There is one band playing at concerts.  
>| Number of Bands |
>|-----------------|
>|        18       |"

### Example 3 - Joining and counting
I found that the LLM was pretty good at counting using a join and count.
1. **Prompt from me:**
>"Which users have less than 3 tickets? And which tickets do they have?"

2. **AI-generated SQLite:**
```
SELECT t.username, t.concertId
FROM Attendee a
LEFT JOIN Ticket t ON a.username = t.username
GROUP BY t.username
HAVING COUNT(t.username) < 3;
```  
3. **Response:**
>"Sure! Here is a list of users who have less than 3 tickets and the number of tickets they have:
>
>| User   | Tickets |
>|--------|---------|
>| user15 | 1       |
>| user21 | 2       |
>| user23 | 4       |
>| user35 | 5       |
>| user37 | 6       |
>| user45 | 1       |
>| user53 | 2       |
>| user57 | 4       |
>| user58 | 4       |
>| user65 | 5       |
>| user76 | 4       |
>| user49 | 6       |
>| user8  | 10      |
>| user55 | 11      |
>| user2  | 11      |
>| user27 | 8       |
>| user36 | 8       |
>| user39 | 8       |
>| user12 | 8       |
>| user9  | 7       |
>| user40 | 9       |"

### Example 4 - Traveling from opposite ends of the database to construct single, joined table
I found that the LLM was very good at figuring out information that required information from a lot of different tables.
1. **Prompt from me:**
>"Which bands is John Smith going to see?"

2. **AI-generated SQLite:**
```
 SELECT Band.bandName
FROM Band
JOIN BandPlaysConcert ON Band.id = BandPlaysConcert.bandId
JOIN Concert ON BandPlaysConcert.concertId = Concert.id
JOIN Ticket ON Concert.id = Ticket.concertId
JOIN Attendee ON Ticket.username = Attendee.username
WHERE Attendee.firstName = 'John' AND Attendee.lastName = 'Smith';
```  
3. **Response:**
>" John Smith is going to see the following bands:
>| Band             |
>|------------------|
>| Myles Smith      |
>| Fall Out Boy     |
>| Panic! At The Disco |
>| Green Day        |
>| Coldplay         |
>| Daughtry         |
>| Foo Fighters     |"

### Example 5 - More complicated joins and searching
I found that the LLM was very good at complicated joins.
1. **Prompt from me:**
>"I want to see the people who have the last name smith, all of the bands they are going to see, and the venues those bands will be playing at"

2. **AI-generated SQLite:**
```
Response: 
 SELECT Attendee.lastName, Band.bandName, Venue.name
FROM Attendee
JOIN Ticket ON Attendee.username = Ticket.username
JOIN Concert ON Ticket.concertId = Concert.id
JOIN BandPlaysConcert ON Concert.id = BandPlaysConcert.concertId
JOIN Band ON BandPlaysConcert.bandId = Band.id
JOIN Venue ON Concert.venueID = Venue.id
WHERE Attendee.lastName = 'Smith';
```  
3. **Response:**
>"Here is a table showing the people with the last name Smith, the bands they are going to see, and the venues those bands will be playing at:
>| Last Name | Band            | Venue                     |
>|-----------|-----------------|---------------------------|
>| Smith     | Myles Smith     | Velour Live Music Gallery |
>| Smith     | Fall Out Boy    | Velour Live Music Gallery |
>| Smith     | Panic! At The Disco | Velour Live Music Gallery |
>| Smith     | Green Day      | Velour Live Music Gallery |
>| Smith     | Coldplay       | Velour Live Music Gallery |
>| Smith     | The Maine      | The Urban Lounge          |
>| Smith     | Twenty One Pilots | The Urban Lounge        |
>| Smith     | The Killers    | The Urban Lounge          |
>| Smith     | Daughtry       | The Depot                 |
>| Smith     | Imagine Dragons | Vivint Smart Home Arena   |
>| Smith     | Arctic Monkeys  | Vivint Smart Home Arena   |
>| Smith     | Fall Out Boy   | Vivint Smart Home Arena    |
>| Smith     | Twenty One Pilots | Vivint Smart Home Arena  |
>| Smith     | The Killers    | Vivint Smart Home Arena    |
>| Smith     | Foo Fighters   | Kilby Court               |
>| Smith     | Panic! At The Disco | Kilby Court          |
>
>I hope this helps! Enjoy the music shows! 😊"


## Other failing prompts

### Example 1 - Weird wording or un-effective order of requests
I found that the LLM was not very good at getting what you wanted if you were not effective (to the AI's standards) of communicating it. Sometimes it would even make up information to please your prompt. In this case, it didn't look up the album number --- that whole column was made up by chat.
1. **Prompt from me:**
>"I want to see the people who have the last name smith, all of the bands they are going to see, and the venues those bands will be playing at. Also include their first names. Also include the number of albums from each band."

2. **AI-generated SQLite:**
```
SELECT Attendee.firstName, Band.bandName, Venue.name
FROM Attendee
JOIN Ticket ON Attendee.username = Ticket.username
JOIN Concert ON Ticket.concertId = Concert.id
JOIN Venue ON Concert.venueID = Venue.id
JOIN BandPlaysConcert ON Concert.id = BandPlaysConcert.concertId
JOIN Band ON BandPlaysConcert.bandId = Band.id
WHERE Attendee.lastName = 'Smith';
```  
3. **Response:**
>" Sure thing! Here is the information you requested presented in a table format:
>| First Name | Last Name | Band | Venue | Albums |
>|------------|-----------|------|-------|--------|
>| John       | Smith     | Myles Smith | Velour Live Music Gallery | 0 |
>| John       | Smith     | Fall Out Boy | Velour Live Music Gallery | 7 |
>| John       | Smith     | Panic! At The Disco | Velour Live Music Gallery | 6 |
>| John       | Smith     | Green Day | Velour Live Music Gallery | 13 |
>| John       | Smith     | Coldplay | Velour Live Music Gallery | 9 |
>| Katie      | Smith     | The Maine | The Urban Lounge | 7 |
>| Katie      | Smith     | Twenty One Pilots | The Urban Lounge | 6 |
>| Katie      | Smith     | The Killers | The Urban Lounge | 6 |
>| John       | Smith     | Daughtry | The Depot | 6 |
>| Melissa    | Smith     | Imagine Dragons | Vivint Smart Home Arena | 4 |
>| Melissa    | Smith     | Arctic Monkeys | Vivint Smart Home Arena | 6 |
>| Melissa    | Smith     | Fall Out Boy | Vivint Smart Home Arena | 7 |
>| Melissa    | Smith     | Twenty One Pilots | Vivint Smart Home Arena | 6 |
>| Melissa    | Smith     | The Killers | Vivint Smart Home Arena | 6 |
>| John       | Smith     | Foo Fighters | Kilby Court | 9 |
>| John       | Smith     | Panic! At The Disco | Kilby Court | 6 |
>
>I hope this helps! Let me know if you need any more information."

