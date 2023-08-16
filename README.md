# Digital Innovation - IA2
I made an arduino with a temperature and humidity sensor detect data. This was put into a database. API data was collected and also inserted into a database. This all was put onto a webapp.

Some specifications:

## Identification

You are required to build a prototype IoT system that allows users to:

- view Bureau of Meteorology (BOM) data stored in an SQLite database•view Arduino sensor data stored in an SQLite database
- receive alerts (via the user interface)•adjust alert thresholds.

### The IoT system to be developed must:
- be accessible for a wide range of users
- incorporate useability principles.

## Component Specifications
### Data
- System BOM data will include:
  - temperature (°C)
  - apparent temperature (°C)
  - relative humidity (%)
  - date/time (Eastern Standard Time) of recordings
  - data available from http://reg.bom.gov.au/fwo/IDQ60901/IDQ60901.94576.json
- System Arduino data will include:
  - internal temperature (°C)
  - relative humidity (%)
  - date/time (Eastern Standard Time) of recording.
### User Experience
- The system must contain an interface with the following specifications:
  - design choices corresponding to the style of the UAP website - www.uapcompany.com. Of particular importance is a match to the current colour
scheme, font family and element layout style
  - the UAP logo visible on the upper left of each form/page (size: 90 x 90)
  - adherence to useability principles
- In the event of a threshold breach the following output will be visible:
  - large warning message
  - current temperatures and humidity readings (large font size)
  - red interface background
  - appropriate image indicating a breach is occurring.
- While no breach is occurring, the following output will be visible:
  - current status message
  - current temperatures and humidity readings (large font size)
  - green interface background
  - appropriate image indicating no current issues.
  - current threshold levels
### Code
- Algorithms and code tooread records from the Arduino sensor and store them in a database
  - access the BOM API and store required data in a database
  - allow the input of safe threshold temperatures
  - display current temperatures and humidity readings
  - display a warning if the threshold is breached
#
