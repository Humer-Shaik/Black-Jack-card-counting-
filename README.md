🧠 Purpose of the App
A Flask web app that:

Lets users upload or capture a card image

Lets them select the card value manually (e.g., A, 2, 3... K)

Uses OpenCV to detect how many cards are present in the image

Tracks the running count based on the Hi-Lo card counting system (used in blackjack)

Gives a recommendation: BET / NO BET / NEUTRAL

📦 Main Libraries Used
Library	Purpose
Flask	Backend web framework
request	Handle file uploads and form data
render_template_string	Render HTML directly in the script
PIL	Validate image format (via Image)
OpenCV (cv2)	Image processing to detect cards
base64	Convert image to displayable format
numpy	Handle image arrays

🧩 Key Components Explained
1. 🧮 Hi-Lo Card Values
python
Copy
Edit
CARD_VALUES = {
    '2': +1, '3': +1, '4': +1, '5': +1, '6': +1,
    '7':  0, '8':  0, '9':  0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}
These values follow the Hi-Lo card counting strategy used in blackjack to predict whether the deck favors the player or dealer.

2. 🎨 HTML Template (with Bootstrap)
This is written in Jinja2 inside a Python string (template = """...""") and rendered using render_template_string.

Key UI Features:
Displays:

Detected card count

Running count

Recommendation (BET/NO BET/NEUTRAL)

Lets users:

Upload/take a card photo

Manually select which card they uploaded

Shows last uploaded image and card value

3. 🧠 detect_cards_opencv(image_bytes)
This function processes the uploaded image using OpenCV:

python
Copy
Edit
def detect_cards_opencv(image_bytes):
    ...
Steps:
Convert image bytes to a NumPy array

Convert to grayscale

Blur & threshold the image to detect edges

Find contours (possible card shapes)

Filter:

Area too small? Ignore

Not a 4-point contour? Ignore

Aspect ratio not in card shape? Ignore

Count how many card-like objects were found

4. 📥 / Route (Main Logic)
python
Copy
Edit
@app.route("/", methods=("GET", "POST"))
def index():
    ...
If it's a POST request:
Reads the uploaded file

Validates the image using Pillow

Detects number of cards using detect_cards_opencv

Base64 encodes the image to preview it in the browser

Updates the running count based on the user-selected card

Error Handling:
No file uploaded → show error

Invalid image → show error

Any other exception → show error

Recommendation Logic:
python
Copy
Edit
if running_count >= 2:
    rec = "BET: Good deck"
elif running_count <= -1:
    rec = "NO BET: Bad deck"
else:
    rec = "NEUTRAL: Use caution"
5. 🏁 Running the App
python
Copy
Edit
if __name__ == "__main__":
    app.run(debug=True)
Starts the Flask development server.

✅ Final Flow Summary:
User uploads or takes a photo of cards.

Selects the card value (e.g., A, 10, K...).

App:

Detects how many cards are in the image

Updates the running count using Hi-Lo system

Displays the count and betting recommendation

Shows the last uploaded image and card selection

🚀 Suggestions for Improvement (Optional)
Use OCR/AI models to auto-detect card values from the image.

Add reset count button.

Persist history using session or database.

Add authentication for multiple users.
