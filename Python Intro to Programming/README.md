# Airline Booking Management System

A desktop airline and flight booking application developed in **Python** with **Tkinter** for the IY499 Introduction to Programming practical assignment.

The system simulates a multi-airline booking platform with separate **Passenger** and **Administrator** dashboards. Passengers can create accounts, search daily flights across all supported routes, sort results, select seats, review dynamically calculated fares, confirm bookings, change or cancel bookings, check in, and generate boarding passes. Administrators can view all flights, review all bookings, and inspect booking statistics through a simple bar chart.

The project demonstrates variables, arithmetic operations, selection, iteration, functions, lists, dictionaries, JSON file handling, linear search, recursive binary search, bubble sort, validation, error recovery, data visualisation, and graphical user-interface design.

---

## Features

### Passenger features

- Passenger registration and secure login
- Flight search by origin, destination, and date
- Pop-up calendar for date selection
- Daily flights for every valid origin and destination combination
- Automatic generation of flights for future dates
- Flight sorting by price, departure time, airline, or date
- Seat selection and fare calculation
- Booking review and confirmation
- Unique booking-reference generation
- View and search saved bookings
- Change flights and seats
- Cancel eligible bookings
- Online check-in
- Boarding-pass display and text export
- Contact Us email link

### Administrator features

- Separate administrator dashboard
- View all generated flights
- View all passenger bookings
- View flight, booking, active-booking, and check-in totals
- Bar chart of active bookings by airline

---

## Demonstration Login Details

The following accounts are created automatically when the program runs for the first time.

### Passenger account

| Field | Details |
|---|---|
| Email | `passenger@airline.local` |
| Password | `Passenger123` |
| Dashboard | Passenger Dashboard |

### Administrator account

| Field | Details |
|---|---|
| Email | `admin@airline.local` |
| Password | `Admin123` |
| Dashboard | Administrator Dashboard |

> These credentials are included for assessment demonstration only and should not be reused in a real production system.

---

## Requirements

- Python 3.10 or later recommended
- Tkinter support
- No third-party Python packages are required

The application uses only Python standard-library modules, including:

- `tkinter`
- `json`
- `pathlib`
- `datetime`
- `calendar`
- `hashlib`
- `hmac`
- `secrets`
- `uuid`
- `copy`
- `webbrowser`
- `collections`

On some Linux systems, Tkinter may need to be installed separately:

```bash
sudo apt install python3-tk
```

---

## Installation

1. Clone this repository:

```bash
git clone https://github.com/walid-alhsn/-IY4101-and-IY499-OOP-and-Python-Final-Projects-Abdullahi.git
```

2. Open the project folder:

```bash
cd Python Intro to Programming
```

3. Run the application:

```bash
python main.py
```

Alternative commands:

```bash
py main.py
```

or:

```bash
python3 main.py
```

No `pip install` command is required.

---

## How to Use the Program

### Passenger workflow

1. Log in using the demonstration passenger account or create a new passenger account.
2. Open **Search & Book**.
3. Select an origin and a different destination.
4. Choose a present or future date using the calendar.
5. Search for available flights.
6. Sort the results if required.
7. Select a flight and choose an available seat.
8. Review the complete fare.
9. Confirm the booking and record the booking reference.
10. Open **My Bookings** to view, change, cancel, or check in.
11. After check-in, display or save the boarding pass.

### Administrator workflow

1. Log out of the passenger account.
2. Log in using the administrator credentials.
3. Use **View Flights** to inspect the generated timetable.
4. Use **View All Bookings** to inspect passenger bookings.
5. Use **Statistics** to view booking totals and the airline bar chart.

---

## Project Structure

```text
Airline-Booking-Management-System/
│
├── main.py
├── README.docx
├── Airline_Booking_System_Design_and_Testing.docx
│
├── data/                    # Created automatically
│   ├── users.json
│   ├── flights.json
│   └── bookings.json
│
└── boarding_passes/         # Created automatically
    └── boarding_pass_<reference>.txt
```

The `data` and `boarding_passes` folders are generated automatically when the application starts.

---

## Algorithms and Programming Techniques

### Linear search

Linear search is used to locate user accounts, match flights against a route and date, and find selected records.

### Recursive binary search

Bookings are sorted by booking reference before a recursive binary search is used to locate a specific booking.

### Bubble sort

The program includes its own bubble-sort implementation for ordering flight results by price, time, airline, or date.

### Dynamic fare calculation

The total fare combines:

- base price;
- airport tax;
- demand adjustment;
- seat charge.

Window seats in columns **A** and **D** have a higher seat charge than standard seats in columns **B** and **C**.

### File handling and recovery

The program stores data in JSON files and writes changes to a temporary file before replacing the original file. Booking, cancellation, and flight-change operations also preserve backup copies so related files can be restored if a save fails.

---

## Data Storage

| File | Purpose |
|---|---|
| `data/users.json` | Passenger and administrator account records |
| `data/flights.json` | Generated flights and current seat availability |
| `data/bookings.json` | Booking, fare, status, and change-history records |
| `boarding_passes/` | Exported text boarding passes |

Passwords are not stored as plain text. Each password is stored as a salted PBKDF2-HMAC-SHA256 hash.

---

## Supported Cities

The generated timetable supports flights between all valid ordered combinations of:

- Abuja
- Dubai
- Kano
- Lagos
- London
- Manchester
- New York
- Paris

An origin cannot be the same as its destination.

---

## Testing

The project was tested across the following areas:

- passenger and administrator login;
- registration validation;
- flight-search validation;
- future timetable generation;
- flight sorting;
- seat selection;
- fare calculation;
- booking creation;
- duplicate-seat prevention;
- booking search;
- flight changes;
- cancellations;
- check-in;
- boarding-pass generation;
- file persistence;
- administrator tables and statistics.

Detailed test cases, results, screenshots, and flowcharts are provided in:

```text
Airline_Booking_System_Design_and_Testing.docx
```

---

## Known Limitations

- Airline names, routes, schedules, and prices are demonstration data.
- The system does not connect to live airline databases.
- The system does not process real payments.
- The system does not send real tickets or emails.
- All prices are displayed in pounds sterling.
- Demonstration login credentials are stored in the source code to make tutor access straightforward.
- The application is intended for educational use rather than production deployment.

---

## Security and Technical References

The following resources were consulted for features beyond the basic module content:

- [Python `hashlib` documentation](https://docs.python.org/3/library/hashlib.html)
- [Python `hmac` documentation](https://docs.python.org/3/library/hmac.html)
- [Python `secrets` documentation](https://docs.python.org/3/library/secrets.html)
- [Python `uuid` documentation](https://docs.python.org/3/library/uuid.html)
- [Python `pathlib` documentation](https://docs.python.org/3/library/pathlib.html)
- [Python `tkinter.ttk` documentation](https://docs.python.org/3/library/tkinter.ttk.html)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

Any code closely adapted from an external source should also be identified in a nearby code comment with the relevant source link.

---

## Declaration of Own Work

I confirm that this assignment is my own work.  
Where I have referred to online sources, I have provided comments detailing the reference and included a link to the source.

---

## Author

**Abdullahi Alhassan**  
**Module:** IY499 – Introduction to Programming  
**Student ID:** 303069863  
**Contact:** `qkf526@york.ac.uk`
