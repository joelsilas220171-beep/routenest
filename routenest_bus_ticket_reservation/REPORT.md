# RouteNest — Bus Ticket Reservation Website

## Overview
RouteNest is a multi-page bus reservation demo built with Python, Flask, HTML, CSS and JavaScript. Users can search sample routes, compare bus options, enter passenger details, receive a booking reference, and look up a reservation.

## Pages and features
- Home page with route search, city swap and popular destinations.
- Bus search/results with source, destination, date and bus-type filters.
- Sort results by fare, departure time or rating.
- Booking form with passenger validation and live fare total.
- Booking confirmation page with copy-reference interaction.
- My Bookings lookup page.
- About and Contact pages.
- Health endpoint and JSON API endpoints.
- Pytest suite, Dockerfile and GitHub Actions workflow.

## Technology stack
Python 3.12, Flask, HTML5, CSS3, JavaScript, pytest, Docker, GitHub Actions, and optional Google Cloud Run deployment.

## Application flow
1. Search by origin and destination.
2. Filter and compare sample buses.
3. Choose a bus and provide passenger details.
4. The app validates the form and available seat count.
5. A booking reference and fare summary are created.
6. Use the reference on My Bookings to view the reservation.

## Testing
Automated tests cover page rendering, health status, API results, route filtering, booking success, seat-capacity checks, invalid email, past dates, reservation lookup, contact form validation, stats and 404 handling.

## Limitations
Routes and fares are sample data. Bookings are stored in memory and reset when the app restarts. The website does not process payments, send email, log users in, or store data in a permanent database. This version is a learning/demo application, not a live ticket sales system.

## Future work
Add persistent database storage, secure authentication, cancellation flows, seat-map selection, payment integration, email/SMS notifications, admin route management, and production monitoring/security controls.
