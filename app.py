from flask import Flask, request, render_template_string
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import base64
import numpy as np
import cv2

app = Flask(__name__)

# Hi‑Lo card values
CARD_VALUES = {
    '2': +1, '3': +1, '4': +1, '5': +1, '6': +1,
    '7':  0, '8':  0, '9':  0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

running_count = 0

template = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Smart Card Counter</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background: linear-gradient(to right, #dbeafe, #f0f9ff);
      font-family: 'Segoe UI', sans-serif;
    }
    .card-counter {
      max-width: 950px;
      margin: 2rem auto;
      padding: 2rem;
      border-radius: 1rem;
      background-color: white;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    .preview-img {
      max-width: 100%;
      max-height: 300px;
      object-fit: contain;
    }
    .title {
      font-weight: bold;
      font-size: 2.2rem;
    }
    .form-label {
      font-weight: 500;
    }
  </style>
</head>
<body>
  <div class="card card-counter">
    <div class="card-body">
      <h2 class="title text-center mb-4">Smart Card Counter</h2>

      {% if error %}
        <div class="alert alert-danger text-center">
          <strong>Error:</strong> {{ error }}
        </div>
      {% endif %}

      <div class="row mb-4">
        <div class="col-md-4 text-center">
          <h6>Detected Cards</h6>
          <h2 class="text-primary">{{ detected }}</h2>
        </div>
        <div class="col-md-4 text-center">
          <h6>Running Count</h6>
          <h2 class="text-dark">{{ count }}</h2>
        </div>
        <div class="col-md-4 text-center">
          <h6>Recommendation</h6>
          <h4 class="{{ 'text-success' if count>=2 else 'text-danger' if count<=-1 else 'text-muted' }}">
            {{ rec }}
          </h4>
        </div>
      </div>

      <form method="post" enctype="multipart/form-data" class="row g-3">
        <div class="col-md-8">
          <label class="form-label">Take or Upload Card Image</label>
          <input class="form-control" type="file" name="card_image" accept="image/*" capture="environment">
        </div>
        <div class="col-md-4">
          <label class="form-label">Recognized Card</label>
          <select class="form-select" name="card">
            {% for c in cards %}
              <option value="{{c}}">{{c}}</option>
            {% endfor %}
          </select>
        </div>
        <div class="col-12 d-grid">
          <button class="btn btn-outline-primary btn-lg" type="submit">Analyze</button>
        </div>
      </form>

      {% if image_data %}
        <hr class="my-4">
        <h5 class="text-center">Last Upload Preview</h5>
        <div class="text-center">
          <img src="data:image/png;base64,{{ image_data }}" class="preview-img border rounded mb-2">
          <p class="mt-2">You selected: <strong>{{ last_card }}</strong></p>
        </div>
      {% endif %}
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

def detect_cards_opencv(image_bytes):
    arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    cnts, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    card_cnt = 0
    for c in cnts:
        area = cv2.contourArea(c)
        if area < 2000:
            continue

        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) != 4:
            continue

        x, y, w, h = cv2.boundingRect(approx)
        ar = w / float(h)
        if 0.5 < ar < 0.8 or 1.2 < ar < 1.8:
            card_cnt += 1

    return card_cnt

@app.route("/", methods=("GET", "POST"))
def index():
    global running_count
    image_data = None
    last_card = None
    error = None
    detected = 0

    if request.method == "POST":
        f = request.files.get("card_image")
        if not f:
            error = "No file part in the request."
        else:
            data = f.read()
            try:
                detected = detect_cards_opencv(data)

                buf = BytesIO(data)
                img = Image.open(buf)
                img.verify()
                buf.seek(0)
                img = Image.open(buf)

                out = BytesIO()
                img.save(out, format="PNG")
                image_data = base64.b64encode(out.getvalue()).decode("ascii")

                last_card = request.form.get("card")
                running_count += CARD_VALUES.get(last_card, 0)

            except UnidentifiedImageError:
                error = "Uploaded file is not a valid image."
            except Exception as e:
                error = f"Error processing image: {e}"

    if running_count >= 2:
        rec = "BET: Good deck"
    elif running_count <= -1:
        rec = "NO BET: Bad deck"
    else:
        rec = "NEUTRAL: Use caution"

    return render_template_string(
        template,
        detected=detected,
        count=running_count,
        rec=rec,
        cards=list(CARD_VALUES.keys()),
        image_data=image_data,
        last_card=last_card,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)