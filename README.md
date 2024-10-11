# LLMDB

## Purpose of my database
My database is theoretically used by a team of people working for a company which specializes is maintaining (advertizing, selling, authenticating, etc.) concert tickets for several different venues.

## ERD diagram


## What works well and what doesn't

***The AI worked better when I gave it a list of my tables. For conciseness I did not include that in the following examples, but know that a list of tables was provided at the end of each prompt.***

### Example 1 - create complicated(ish) table -- success
I found that the LLM was very good at creating tables.
1. **Prompt from me:**
>"Create a table called BandPlaysConcert. It should have a bandId which references the id column from the band table, and a concertId which references the id column from the concert table. There should also be a separate, unique id that auto increments. The combination of bandId and concertId should be unique"

2. **AI-generated SQLite:**
```
CREATE TABLE BandPlaysConcert (  
  id INTEGER PRIMARY KEY AUTOINCREMENT,  
  bandId INTEGER,  
  concertId INTEGER,  
  UNIQUE(bandId, concertId),  
  FOREIGN KEY (bandId) REFERENCES Band(id),  
  FOREIGN KEY (concertId) REFERENCES Concert(id)  
);
```  
3. **Response:**
>The table BandPlaysConcert has been successfully created. Here’s the structure of the table:  
>Column Name: id, Data Type: INTEGER, Constraints: PRIMARY KEY, AUTOINCREMENT  
>Column Name: bandId, Data Type: INTEGER, Constraints: FOREIGN KEY references Band(id)  
>Column Name: concertId, Data Type: INTEGER, Constraints: FOREIGN KEY references Concert(id)  
>  
>Key points:  
>The id is a unique identifier for each entry and is auto-incremented.  
>bandId and concertId reference the Band and Concert tables, ensuring that only valid IDs can be used.  
>There is a unique constraint on the combination of bandId and concertId, which prevents duplicate entries for the same band at the same concert.  
>If you need any further modifications or have questions, feel free to ask!  
