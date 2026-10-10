"""CampusFlow command-line application."""

from campusflow.tickets import create_ticket, find_ticket
from campusflow.workflow import (
    assign_ticket,
    change_status,
    get_work_queue,
)
from campusflow.storage import load_tickets, save_tickets
from campusflow.reports import (
    generate_report,
    list_tickets,
)


def display_ticket(ticket):
    """Print the details of one ticket."""
    print("\n------------------------------")
    print(f"ID:              {ticket['id']}")
    print(f"Title:           {ticket['title']}")
    print(f"Category:        {ticket['category']}")
    print(f"Urgency:         {ticket['urgency']}")
    print(f"Affected users:  {ticket['affected_users']}")
    print(f"Priority:        {ticket['priority']}")
    print(f"Status:          {ticket['status']}")
    print(f"Assigned to:     {ticket['assigned_to'] or 'Unassigned'}")
    print("------------------------------")


def display_tickets(tickets):
    """Display every ticket or a message when none exist."""
    if not tickets:
        print("\nNo tickets found.")
        return

    for ticket in tickets:
        display_ticket(ticket)


def create_ticket_from_input(tickets):
    """Collect user input and create a ticket."""
    title = input("Ticket title: ")
    category = input("Category (Network/Hardware/Software/Other): ")
    urgency = input("Urgency (low/medium/high): ")
    affected_users_text = input("Number of affected users: ").strip()

    # Reject decimals, text, zero, and negative values.
    if not affected_users_text.isdigit():
        raise ValueError(
            "Affected users must be a positive whole number."
        )

    affected_users = int(affected_users_text)

    ticket = create_ticket(
        tickets,
        title,
        category,
        urgency,
        affected_users,
    )

    save_tickets(tickets)
    print(f"\nTicket {ticket['id']} created successfully.")
    display_ticket(ticket)


def view_one_ticket(tickets):
    """Find and display one ticket."""
    ticket_id = input("Enter ticket ID (for example T001): ")
    ticket = find_ticket(tickets, ticket_id)
    display_ticket(ticket)


def assign_ticket_from_input(tickets):
    """Collect assignment information."""
    ticket_id = input("Enter ticket ID: ")
    staff_name = input("Staff member name: ")

    ticket = assign_ticket(tickets, ticket_id, staff_name)
    save_tickets(tickets)

    print(f"\nTicket {ticket['id']} assigned to {ticket['assigned_to']}.")


def change_status_from_input(tickets):
    """Collect and apply a status change."""
    ticket_id = input("Enter ticket ID: ")
    print("Available statuses: open, in_progress, resolved")
    print("To reopen a resolved ticket, select open.")

    new_status = input("Enter new status: ")

    ticket = change_status(tickets, ticket_id, new_status)
    save_tickets(tickets)

    print(f"\nTicket {ticket['id']} status is now {ticket['status']}.")


def display_queue(tickets):
    """Display the priority-ordered work queue."""
    queue = get_work_queue(tickets)

    if not queue:
        print("\nThe work queue is empty.")
        return

    print("\n=== WORK QUEUE ===")

    for ticket in queue:
        print(
            f"{ticket['id']} | {ticket['priority'].upper()} | "
            f"{ticket['status']} | {ticket['title']}"
        )


def display_report(tickets):
    """Display the report, including empty reports."""
    report = generate_report(tickets)

    print("\n=== CAMPUSFLOW REPORT ===")
    print(f"Total tickets: {report['total_tickets']}")

    print("\nTickets by status:")
    for status, count in report["by_status"].items():
        print(f"{status}: {count}")

    print("\nTickets by priority:")
    for priority, count in report["by_priority"].items():
        print(f"{priority}: {count}")


def display_menu():
    """Print the main menu."""
    print("\n========== CAMPUSFLOW ==========")
    print("1. Create ticket")
    print("2. List all tickets")
    print("3. View one ticket")
    print("4. Assign ticket")
    print("5. Change ticket status / reopen")
    print("6. View work queue")
    print("7. View reports")
    print("8. Save tickets")
    print("0. Exit")
    print("================================")


def main():
    """Run the CampusFlow application."""
    try:
        tickets = load_tickets()
    except (ValueError, RuntimeError) as error:
        print(f"ERROR: {error}")
        print("Fix the saved data before restarting. No data was reset.")
        return

    print("Welcome to CampusFlow!")
    print(f"Loaded {len(tickets)} saved ticket(s).")

    while True:
        display_menu()
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                create_ticket_from_input(tickets)

            elif choice == "2":
                display_tickets(list_tickets(tickets))

            elif choice == "3":
                view_one_ticket(tickets)

            elif choice == "4":
                assign_ticket_from_input(tickets)

            elif choice == "5":
                change_status_from_input(tickets)

            elif choice == "6":
                display_queue(tickets)

            elif choice == "7":
                display_report(tickets)

            elif choice == "8":
                save_tickets(tickets)
                print("Tickets saved successfully.")

            elif choice == "0":
                save_tickets(tickets)
                print("Tickets saved. Goodbye!")
                break

            else:
                print("Invalid menu option. Please choose again.")

        except (ValueError, RuntimeError) as error:
            print(f"ERROR: {error}")

        except (EOFError, KeyboardInterrupt):
            print("\nSaving and exiting...")
            try:
                save_tickets(tickets)
            except RuntimeError as error:
                print(f"ERROR: {error}")
            break


if __name__ == "__main__":
    main()