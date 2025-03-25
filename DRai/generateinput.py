import pandas as pd

# Sample customer support chat data
data = {
    "message": [
        "Hello, I'm having trouble logging into my account.",
        "Thank you for reaching out! Could you provide more details about the issue?",
        "Whenever I enter my password, I receive an error message.",
        "I see. Have you tried resetting your password?",
        "Yes, I have, but I still can't log in.",
        "I understand. Let me check your account. Please hold on for a moment.",
        "Thanks for your patience. Your account has been fixed. Please try logging in now.",
        "I tried, and it's working now! Thanks a lot!",
        "You're welcome! Let us know if you need further assistance.",
        "Hi, I need help canceling my subscription.",
        "I can assist with that. May I know your subscription ID?",
        "My subscription ID is 12345. I want to cancel before the next billing cycle.",
        "Got it! Your subscription has been canceled. You won’t be charged next month.",
        "Thanks for the quick response!",
        "You're very welcome! Have a great day!",
        "Hey, I received a damaged product in my order. What should I do?",
        "I'm sorry to hear that. Could you share your order number?",
        "Sure! It's #98765. The item is broken.",
        "I understand. We'll send a replacement. Would you like a refund instead?",
        "A replacement works fine for me. Thank you!",
        "You're welcome! Your new item will arrive in 3-5 days.",
        "My internet is running very slow. Can you check?",
        "I apologize for the inconvenience. I’ll run diagnostics on your connection.",
        "It seems like there’s a temporary outage in your area. It should be resolved within 2 hours.",
        "Alright, thanks for the update.",
        "No problem! Let us know if the issue persists.",
        "Hi, I want to update my payment method.",
        "Sure! You can update your payment details in your account settings.",
        "I tried, but I’m getting an error.",
        "I’ll look into that. What error message are you seeing?",
        "It says 'Invalid card details'.",
        "I see. Please ensure your card details are correct and try again.",
        "I double-checked, but it's still not working.",
        "Let me escalate this to our billing team. They will contact you shortly.",
        "Okay, thanks for your help!",
        "You're welcome! Have a great day!",
        "Hello, I need help setting up my new router.",
        "Of course! Are you experiencing any specific issues during setup?",
        "Yes, it’s not connecting to the internet.",
        "I see. Have you tried restarting both the router and modem?",
        "Yes, multiple times, but no luck.",
        "Let’s try resetting the router to factory settings. Hold the reset button for 10 seconds.",
        "That worked! Thank you so much.",
        "Glad to hear that! Let us know if you need any further assistance."
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
input_csv_path = "input.csv"
df.to_csv(input_csv_path, index=False, encoding="utf-8-sig")

print(f"File {input_csv_path} has been created successfully.")
