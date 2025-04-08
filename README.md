![Screenshot (6)](https://github.com/user-attachments/assets/e1ec0dd7-d682-4aa2-a110-bad0bf94d0b8)
Backend according to all technical constraints suggested in assignment.
1. What was your initial thought process when you first read the problem statement, and how did you break it down?
The main goal was to find nearby properties within 50km of a location, even if the input had spelling errors. I broke it into steps: correct the input, get coordinates, calculate distances to properties, and return the closest ones. Then I built an API around it.
2. What tools, libraries, or resources did you use, and why?
I used Python with FastAPI for speed and simplicity. To handle spelling mistakes, I used RapidFuzz for its fast and accurate fuzzy matching. For geocoding, I used geopy with Nominatim, and calculated distances using the Haversine formula.
3. What was a key challenge you faced, and how did you solve it?
Handling misspelled inputs was tricky. I solved it using RapidFuzz to match user queries with known locations. It handled small typos really well. I also made sure the API responds quickly by keeping the code lightweight and using caching where needed.
4. If you had more time, what improvements or alternatives would you explore?
I’d look into using offline location data to avoid relying on external APIs. Also, using geo-indexing or spatial databases would help if the property list grows. Maybe even add logging or analytics for tele-callers.
