
import cv2
import pandas as pd
import numpy as np
import os
import sys

# Constants
HEADSHOT_DIR = "posts/stuperlatives/data/headshots"
LABEL_PATH = "posts/stuperlatives/data/appearance_labels.csv"
CASCADE_PATH = "posts/stuperlatives/data/haarcascade_frontalface_default.xml"

def detect_attributes(image_path, face_cascade):
    img = cv2.imread(image_path)
    if img is None:
        return False, False, False
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    has_beard = False
    has_mustache = False
    is_redhead = False
    
    if len(faces) == 0:
        return False, False, False
        
    # Take the largest face
    faces = sorted(faces, key=lambda x: x[2]*x[3], reverse=True)
    (x, y, w, h) = faces[0]
    
    # --- REDHEAD DETECTION ---
    # Look at a region slightly above the face and the top of the face for hair
    # Or just the whole image if headshot is tight? 
    # Let's take the top half of the face rect and expand it upwards
    hair_region_y = max(0, y - int(h*0.3))
    hair_region_h = int(h * 0.5)
    hair_roi = img[hair_region_y:hair_region_y+hair_region_h, x:x+w]
    
    if hair_roi.size > 0:
        hsv = cv2.cvtColor(hair_roi, cv2.COLOR_BGR2HSV)
        
        # Red is at both ends of the hue spectrum (0-10 and 170-180 approx)
        # Saturation needs to be somewhat high to be "red" hair not just brown/skin
        lower_red1 = np.array([0, 50, 50])
        upper_red1 = np.array([15, 255, 255])
        lower_red2 = np.array([165, 50, 50])
        upper_red2 = np.array([180, 255, 255])
        
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = mask1 + mask2
        
        red_ratio = np.sum(mask > 0) / mask.size
        # Threshold: purely empirical. 10% red pixels in hair region?
        if red_ratio > 0.15: 
            is_redhead = True
            
    # --- FACIAL HAIR DETECTION (Heuristic) ---
    # Skin sample: Cheeks (sides of face, middle height)
    # Beard region: Bottom 1/3 of face
    # Mustache region: Between nose and mouth (approx 2/3 down, center)
    
    # Approximate regions
    cheek_y = y + int(h * 0.4)
    cheek_h = int(h * 0.15)
    cheek_roi = gray[cheek_y:cheek_y+cheek_h, x+int(w*0.1):x+int(w*0.3)] # Right cheek (viewer's left)
    
    beard_roi_y = y + int(h * 0.65)
    beard_roi = gray[beard_roi_y:y+h, x:x+w]
    
    mustache_roi_y = y + int(h * 0.55)
    mustache_roi_h = int(h * 0.15)
    mustache_roi = gray[mustache_roi_y:mustache_roi_y+mustache_roi_h, x+int(w*0.25):x+int(w*0.75)]
    
    if cheek_roi.size > 0 and beard_roi.size > 0:
        skin_brightness = np.mean(cheek_roi)
        beard_brightness = np.mean(beard_roi)
        
        # If beard region is significantly darker than skin
        # This fails for dark skin tones. 
        # Better: use edge detection (Canny) or texture entropy. Hair is textured.
        
        beard_edges = cv2.Canny(beard_roi, 100, 200)
        edge_density = np.sum(beard_edges) / beard_roi.size
        
        # Thresholds are magic numbers here.
        if edge_density > 20: # High texture usually means hair
             has_beard = True
             
    if cheek_roi.size > 0 and mustache_roi.size > 0:
         mustache_edges = cv2.Canny(mustache_roi, 100, 200)
         mus_edge_density = np.sum(mustache_edges) / mustache_roi.size
         
         if mus_edge_density > 15:
             has_mustache = True
             
    # If beard is true, mustache is likely true (full beard). 
    # If only mustache region has high texture, it's a mustache.
    
    return has_beard, has_mustache, is_redhead

def auto_label():
    if not os.path.exists(LABEL_PATH):
        print("Label file not found.")
        return
        
    if not os.path.exists(CASCADE_PATH):
        print("Haar cascade not found.")
        return

    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
    df = pd.read_csv(LABEL_PATH)
    
    print("Starting automated labeling...")
    
    for idx, row in df.iterrows():
        img_path = os.path.join(HEADSHOT_DIR, f"{row['player_id']}.png")
        if os.path.exists(img_path):
            beard, mustache, redhead = detect_attributes(img_path, face_cascade)
            
            # Update dataframe
            df.at[idx, 'has_beard'] = beard
            df.at[idx, 'has_mustache'] = mustache
            df.at[idx, 'is_redhead'] = redhead
            
            p_name = row['player_name'] if 'player_name' in row else row['player_id']
            if beard or mustache or redhead:
                print(f"[{p_name}] Beard: {beard}, Stache: {mustache}, Red: {redhead}")
            
    df.to_csv(LABEL_PATH, index=False)
    print("Labeling complete.")

if __name__ == "__main__":
    auto_label()
