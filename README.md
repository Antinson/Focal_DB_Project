
# Goal

The goal of this project was to simplify a process at work where we needed to scan our inventory of cameras and put them into an Excel sheet which we would then need to send to our manager, who would then proceed to combine manually all Excel sheets from different technicians into one document which would then be used to track inventory

Problems
- Camera duplication (scanning so many cameras with similar MAC ids there would sometimes be double-ups)
- No information about the camera (Only the MAC IDs were known, total cameras were known but not what type they were)
- Scans once every 2 months slowed inventory distribution
- Less predictive data collected
- No visibility of current technician stock

Solved
- Duplications handled automatically
- Camera information including type, FOV, status (broken, working) along with scan date
- Scans during shift
- Predictive data collected, including scan time and date, status
- Admin dashboard to view and filter by country, technician


# Preview









# How to Run

### Docker

#### First build the image
docker build -t camera_app .

#### Then run
docker run -p port:port camera_app
