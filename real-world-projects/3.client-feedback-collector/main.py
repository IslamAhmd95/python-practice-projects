
import helpers

while True:

    name = input("\nEnter Your Name: ").strip()
    phone = input("Enter Your Phone: ").strip()
    email = input("Enter Your Email: ").strip()
    feedback_message = input("Enter Your Feedback: ").strip()

    feedback = {
        "name": name,
        "phone": phone,
        "email": email,
        "feedback_message": feedback_message,
    }

    try:
        helpers.validate_feedback(feedback)
    except ValueError as e:
        print(f"Error: {e}\n")
        continue

    print(feedback)

    another_feedback = input("Do you want to enter another feedback ? (y/n): ")
    if another_feedback.lower() == 'y':
        continue
    else:
        print("Thank you for your feedback.\n")
        break
