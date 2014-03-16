# Notes
* If we want to add actual email, we can use SendGrid:
    * Account: http://sendgrid.com/developers
    * Sample: https://github.com/tbarn/basicEmail
* If we want actual $, we can use:
    * Stripe: https://stripe.com/ca
    * Braintree: https://www.braintreepayments.com/developers
    * PayPal: https://developer.paypal.com/docs/api/
* Need to check for errors and produce messages
* I recommend using bootstrap for front-end and modals to flash error messages

# Clerk
* Add new borrower
    1. Get information
* Checkout items borrowed by someone
    1. Provide card number
    1. Provide call numbers
    1. Check if account is valid
        * which involves...
    1. Check if items are available
    1. Create the borrowing records for each
    1. Print a list of items and due dates
* Process a return
    1. Get catalogue number (call number?)
    1. Determine borrower
    1. Record it is in
        * I feel like this should be the last step in this process...
    1. If overdue
        * Fine the borrower
    1. If a hold request exists
        * Put item on hold
        * Email borrower who requested
* Report: overdue items
    1. Display a list of overdue items and their borrowers
    1. Can email any or all of them

# Borrower
* Search for books
    1. Enter term(s):
        * title(s?)
        * author(s)
        * subject(s)
    1. Return list of books and copies in and out
* Place hold request
    1. Search
    1. If out
        * Click button to hold
* Check account
    1. Display items currently borrowed
    1. Display hold requests placed
    1. Display outstanding fines
* Pay a fine
    1. Enter in $ to pay
    1. Enter in CC #
    1. Pay

# Librarian
* Add new book or copy of book
    1. Get information
    1. If exists
        * Add a copy
        * Should imitate the search feature?
* Report: checked out items
    1. Display a list of items that are checked out, out date, due date
    1. Flag items that are overdue
        * Is this a visual thing or system thing that sets a status?
    1. Order by call number
    1. Filter by subject
* Report: most popular items in a year
    1. Enter year
    1. Enter number n
    1. Display a list of items that were borrowed
        * Ordered by borrowed count
        * Filtered by year
        * Limited by n

# Deliverables
* A cover page with team info
* A brief introduction to the system, a brief user manual, and a list of assumptions made during implementation
* The file with the code for the creation of the tables
* The files with the code for the operations, the transactions, and interface
