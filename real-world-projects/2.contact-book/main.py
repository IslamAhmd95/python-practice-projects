import json
import helpers

while True:

    action = input("Enter action (view, add, update, delete, search) or (exit to quit): ").strip().lower()

    if action == "exit":
        print("Exiting the program, Goodbye!")
        break

            
    if action == 'view':

        contacts = helpers.get_contacts()

        print(json.dumps(contacts, indent=4))


    if action == "add":

        name = input("Enter name: ").strip()

        phone = input("Enter phone number: ").replace(" ", "").strip()
        
        email = input("Enter email: ").strip()

        last_contact = helpers.get_last_contact()

        new_id = last_contact["id"] + 1 if last_contact else 1

        contact = {
            "id": new_id,
            "name": name,
            "phone": phone,
            "email": email
        }

        try:
            helpers.validate_contact(contact)
        except ValueError as e:
            print(f"Error: {e}\n")
            continue
        
        contacts = helpers.get_contacts()

        contacts.append(contact)

        try:
            with open("contacts.json", "w") as wf:
                json.dump(contacts, wf, indent=4)
                print(f"Contact {name} has been added successfully.\n")
        except Exception as e:
            print(f"Error: {e}\n")
        

    if action == 'search':

        query = input("Please enter the name/email/phone to search: ").strip().lower()
        contacts = helpers.get_contacts()
        if not contacts:
            print("You don't have any contacts yet.")
            continue

        results = helpers.search_contacts(contacts, query)

        if results:
            print(json.dumps(results, indent=4))
        else:
            print("No matching contacts found.")


    if action == 'update':

        contact_id = helpers.get_contact_id("update")
        if contact_id is None or contact_id is False:
            continue

        contacts = helpers.get_contacts()
        if not contacts:
            print("You don't have any contacts yet.")
            continue

        matching_contact = helpers.get_contact_by_id(contacts, contact_id)
        if not matching_contact:
            print("No matching contact found.")
            continue

        name = input(f"Enter name or press (Enter) to skip: ").strip()

        phone = input(f"Enter phone number or press (Enter) to skip: ").replace(" ", "").strip()
        
        email = input(f"Enter email or press (Enter) to skip: ").strip()

        updated_contact = {
            "id": contact_id,
            "name": name if name else matching_contact['name'],
            "phone": phone if phone else matching_contact['phone'],
            "email": email if email else matching_contact['email']
        }
        
        try:
            helpers.validate_contact(updated_contact)
        except ValueError as e:
            print(f"Error: {e}\n")
            continue
        
        # update in-place
        # matching_contact is a reference to the original contact inside the contacts list, so modifying it directly updates the list, because they both point to the same memory location.
        matching_contact['name'] = updated_contact['name']
        matching_contact['phone'] = updated_contact['phone']
        matching_contact['email'] = updated_contact['email']

        try:
            with open("contacts.json", "w") as wf:
                json.dump(contacts, wf, indent=4)
                print(f"Contact {matching_contact['name']} has been updated successfully.\n")
        except Exception as e:
            print(f"Error: {e}\n")

    
    if action == 'delete':

        contact_id = helpers.get_contact_id("delete")
        if contact_id is None or contact_id is False:
            continue


        contacts = helpers.get_contacts()
        if not contacts:
            print("You don't have any contacts yet.")
            continue

        matching_contact = helpers.get_contact_by_id(contacts, contact_id)
        if not matching_contact:
            print("No matching contact found.")
            continue

        while True:

            confirm_deletion = input(f"Are you sure you want to delete '{matching_contact['name']}' contact [y/n]: ").strip().lower()

            if confirm_deletion == 'y':

                contacts.remove(matching_contact)

                try:
                    with open("contacts.json", "w") as wf:
                        json.dump(contacts, wf, indent=4)
                        print(f"Contact {matching_contact['name']} has been deleted successfully.\n")
                except Exception as e:
                    print(f"Error: {e}\n")

                break

            elif confirm_deletion == 'n':
                
                print("Deletion cancelled.\n")

                break

            else:

                print("Invalid choice. Please enter 'y' or 'n'.\n")


        