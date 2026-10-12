# RouteNest — Bus Ticket Reservation

A polished multi-page bus reservation website made with Flask, HTML, CSS and JavaScript. The site includes bus search, filters, sorting, booking validation, ticket confirmation, reference lookup, contact page, automated tests, Docker configuration and a GitHub Actions workflow.

> **Demo notice:** The buses/fare values are sample data. Reservations are stored only in memory and disappear when the server restarts. No payment is collected, emails are not sent and messages are not stored permanently. Use a database and payment/security review before real use.

## Pages and interactions
- **Home:** search buses, swap cities, pick a popular destination.
- **Find buses:** filter by city/date/type and sort by fare, departure or rating.
- **Book:** validate passenger details and view a live fare calculation.
- **Confirmation:** see ticket details and copy the booking reference.
- **My bookings:** search for a booking using its reference.
- **About / Contact:** information pages and demo contact form.
- **Health/API:** `/health`, `/api/buses`, `/api/stats`.

## 1. Install Python (Windows)
Install Python 3.12 from https://www.python.org/downloads/ and select **Add python.exe to PATH** during setup. Open PowerShell and verify:

```powershell
py -3.12 --version
```

## 2. Extract the ZIP and open the folder
Extract `routenest_bus_ticket_reservation.zip`. In File Explorer, open the extracted `routenest_bus_ticket_reservation` folder. Click the address bar, type `powershell`, and press Enter. Confirm that `app.py` and `requirements-dev.txt` are in this folder:

```powershell
 dir
```

## 3. Create the virtual environment

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this command in the same terminal, then activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

You should see `(.venv)` near the beginning of the terminal prompt.

## 4. Install packages

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

If `pytest` is missing later, make sure `(.venv)` is visible and run the install command again.

## 5. Run the automated tests

```powershell
python -m pytest -v
```

The suite checks the home page, health endpoint, bus API and filters, successful booking, invalid booking attempts, reference lookup, contact form, statistics API and 404 page. Test output should show all tests as `PASSED`.

## 6. Start the website

```powershell
python app.py
```

Open **http://127.0.0.1:8080** in your browser. Stop the server with `Ctrl+C` in PowerShell.

## 7. Explore every feature
1. On Home, choose a source, destination and date. Try the swap-cities button.
2. On Find buses, change the bus type and sort order.
3. Select a bus, enter passenger information, choose a seat count, and watch the total update.
4. Confirm a booking and use the copy-reference button.
5. Open My bookings and paste the reference to retrieve the reservation.
6. Submit the Contact form and inspect the confirmation message.
7. Open `http://127.0.0.1:8080/health` to see the health JSON.
8. Open `http://127.0.0.1:8080/api/buses` and `http://127.0.0.1:8080/api/stats` to inspect the API responses.

## 8. Optional shortcut for Windows
Double-click `run_windows.bat` to create the environment, install packages, run tests and start the app. The manual steps above are recommended the first time so you can see each stage.

## 9. Run with Docker (optional)
Install and start Docker Desktop. In the project folder:

```powershell
docker build -t routenest:local .
docker run --rm -p 8080:8080 routenest:local
```

Then visit http://127.0.0.1:8080. Stop the container with `Ctrl+C`.

## 10. Upload to GitHub
Create an empty repository on GitHub. In PowerShell in the project directory:

```powershell
git init
git add .
git commit -m "Build RouteNest bus reservation website"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the example remote URL with your own repository URL. Open the repository's **Actions** tab to view the workflow. It installs packages, runs pytest, and builds a Docker image; it does not publish the image or deploy the application by itself.

## 11. Optional Google Cloud Run deployment
This may create billable resources. Check current Google Cloud pricing and billing before proceeding. Install the Google Cloud CLI and authenticate, then run:

```powershell
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud run deploy routenest --source . --region asia-south1 --allow-unauthenticated
```

Replace `YOUR_PROJECT_ID` with your Google Cloud project ID and follow the prompts. Use the service URL printed after deployment. The current in-memory store is not durable or shared between service instances, so this is a demo deployment only.

## Project structure

```text
routenest_bus_ticket_reservation/
├── app.py
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── Dockerfile
├── .dockerignore
├── .gitignore
├── run_windows.bat
├── README.md
├── REPORT.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── buses.html
│   ├── book.html
│   ├── confirmation.html
│   ├── my_bookings.html
│   ├── about.html
│   ├── contact.html
│   └── 404.html
├── static/
│   ├── css/style.css
│   └── js/main.js
├── tests/test_app.py
└── .github/workflows/ci.yml
```
