<img width="1677" alt="Screenshot 2025-07-07 at 2 21 54 PM" src="https://github.com/user-attachments/assets/e4af7bf7-158f-490a-b13b-deb034a085a0" /># Smart Card Counter – Flask + OpenCV

This is a Flask web application that detects the number of playing cards in an uploaded image and updates a running count using the Hi-Lo card counting system used in Blackjack.

## Purpose

- Upload or capture an image of playing cards
- Manually select the card value (e.g., A, 2, 3... K)
- Detect number of visible cards using OpenCV
- Track running count using Hi-Lo logic
- Display betting recommendation based on the count

## Technologies Used

| Library     | Purpose                              |
|-------------|--------------------------------------|
| Flask       | Backend web framework                |
| request     | Handle file uploads and form data    |
| PIL         | Validate and load images             |
| OpenCV      | Image processing and shape detection |
| NumPy       | Image array operations               |
| base64      | Convert image to display format      |

## Card Value Mapping (Hi-Lo System)

python
CARD_VALUES = {
    '2': +1, '3': +1, '4': +1, '5': +1, '6': +1,
    '7':  0, '8':  0, '9':  0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}
Application Flow
User uploads or takes a photo of cards.

User selects the card value manually.

App:

Detects card-like contours using OpenCV

Updates the running count using Hi-Lo logic

Displays recommendation: BET, NO BET, or NEUTRAL

Recommendation Logic
python
Copy
Edit
if running_count >= 2:
    rec = "BET: Good deck"
elif running_count <= -1:
    rec = "NO BET: Bad deck"
else:
    rec = "NEUTRAL: Use caution"
Running the App
To start the server locally:

bash
Copy
Edit
python app.py
Access it in your browser at: http://127.0.0.1:5000/

Future Improvements
Auto-detect card value using OCR or AI

Add reset button for the running count

Store history using sessions or database

Add authentication for multi-user access


<img width="1677" alt="Screenshot 2025-07-07 at 2 22 26 PM" src="https://github.com/user-attachments/assets/b0ed2ded-96f1-44fc-96d2-a7cf377cca5c" />


