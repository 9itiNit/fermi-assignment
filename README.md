![Screenshot (6)](https://github.com/user-attachments/assets/e1ec0dd7-d682-4aa2-a110-bad0bf94d0b8)
Backend according to all technical constraints suggested in assignment.
1. What was your initial thought process when you first read the problem statement, and how did you break it down?
I started by understanding the main goal—find nearby properties within 50km of a location, even if the input is slightly misspelled. I broke it down into: correcting the user’s input, getting coordinates for the location, calculating distances to all properties, and returning the closest ones. Finally, I wrapped it all into a simple API.
2. What tools, libraries, or resources did you use, and why?
I used Python and FastAPI for quick development and performance. For handling misspelled queries, I used fuzzywuzzy. To get coordinates, I used geopy with Nominatim, and for distance, I used the Haversine formula. FastAPI was ideal due to its speed and ease of use.
3. What was a key challenge you faced, and how did you solve it?
The biggest challenge was dealing with misspelled location inputs. To solve this, I used fuzzy string matching to map the user’s input to the closest valid location. It worked well even when characters were swapped or missing. Another challenge was keeping the response under 2 seconds, which I managed by caching frequent locations and keeping things lightweight.
4. If you had more time, what improvements or alternatives would you explore?
I’d probably replace fuzzywuzzy with RapidFuzz for better speed. Also, using an offline database for city coordinates could avoid API limits and make it faster. If the property count grows, I’d also look into vector search or geo-indexing for faster distance queries.
