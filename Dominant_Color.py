import cv2
import numpy as np
from sklearn.cluster import KMeans

def find_dominant_color(image, k=5):
    # Check if the image is empty
    if image.size == 0:
        return None

    # 1. Reshape the image to be a list of pixels
    # The image is reshaped from (height, width, 3) to (height * width, 3)
    pixels = image.reshape((-1, 3))

    # 2. Convert to float32, as required by KMeans
    pixels = np.float32(pixels)

    # 3. Apply K-Means clustering
    # n_init='auto' suppresses a future warning in scikit-learn
    kmeans = KMeans(n_clusters=k, n_init='auto', random_state=42).fit(pixels)

    # 4. Find the most frequent cluster
    # np.unique returns the unique labels and their counts
    labels, counts = np.unique(kmeans.labels_, return_counts=True)
    dominant_cluster_index = np.argmax(counts)

    # 5. Get the BGR color of the dominant cluster center
    dominant_color = kmeans.cluster_centers_[dominant_cluster_index]

    # 6. Convert color from float to integer and return as a tuple
    return tuple(int(c) for c in dominant_color)


# --- Main script execution ---

# Initialize video capture from the primary webcam (index 0)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

print("Starting video stream. Press 'q' to quit.")

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Get the frame dimensions
    h, w, _ = frame.shape

    # Define the central rectangle (Region of Interest - ROI)
    # This creates a rectangle covering the central 50% of the screen
    start_x = w // 4
    start_y = h // 4
    end_x = w * 3 // 4
    end_y = h * 3 // 4

    # Extract the ROI from the frame
    roi = frame[start_y:end_y, start_x:end_x]

    # Find the dominant color in the ROI
    dominant_color_bgr = find_dominant_color(roi, k=5)

    # Draw the rectangle on the main frame for visualization
    cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

    # Create a color swatch to display the dominant color
    swatch = np.zeros((70, frame.shape[1], 3), dtype=np.uint8)
    if dominant_color_bgr:
        swatch[:] = dominant_color_bgr
        color_text = f"Dominant Color (BGR): {dominant_color_bgr}"
        
        # Determine a contrasting text color (white or black)
        # Using a simple brightness formula
        brightness = dominant_color_bgr[0] * 0.114 + dominant_color_bgr[1] * 0.587 + dominant_color_bgr[2] * 0.299
        text_color = (0, 0, 0) if brightness > 127 else (255, 255, 255)
        
        cv2.putText(swatch, color_text, (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)

    # Combine the main frame and the color swatch vertically
    combined_display = np.vstack((frame, swatch))

    # Display the resulting frame
    cv2.imshow("Dominant Color Detector", combined_display)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and destroy all windows
cap.release()
cv2.destroyAllWindows()
print("Video stream stopped.")