# ParkingPermit
This is a very simple python script that takes the Harvard University Parking Permit PDFs from the HOPPS system and converts it into a Pocket Printer Friendly format, then sends it to a designated telegram chat to print automatically. 

## Usage 
Running the watchdog_parking.py file, drop some parking permit PDFs generated from the Harvard Parking Permit Website. The watchdog will then recognize the pdf and run a script to convert the pdf into a png file, extract the required text and reformat it, as well as cropping and resizing the QR code. It will then generate a image file that will have all of the components above in a nicely formatted, pocketprinter friendly format. Then the file will be sent through a designated telegram channel @ParkingPermit.

The user can configure a few things in this code, which will be later added as a configurable option file.

1. Car Number Plate
2. Telegram Chat ID
3. Telegram API Code 
4. Width of Pocket Printer Paper 
5. DPI of Print
6. Font Size 

User may freely change the following variables withoout interfering with the functionality of the code. 

Run the code using 'python watchdog_parking.py'.