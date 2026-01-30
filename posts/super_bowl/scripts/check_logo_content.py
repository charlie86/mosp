
import matplotlib.pyplot as plt
import numpy as np
import os

LOGO_DIR = "/Users/charliethompson/Documents/mosp/posts/stuperlatives/super_bowl/logos"

def get_content_dim(team):
    path = os.path.join(LOGO_DIR, f"{team}.png")
    img = plt.imread(path)
    if img.shape[2] == 4:
        alpha = img[:,:,3]
    else:
        return img.shape[:2]
        
    rows = np.any(alpha > 0.05, axis=1)
    cols = np.any(alpha > 0.05, axis=0)
    r = np.where(rows)[0]
    c = np.where(cols)[0]
    if len(r) > 0 and len(c) > 0:
        return (r[-1] - r[0], c[-1] - c[0])
    return img.shape[:2]

print("NYJ Content Dim:", get_content_dim("NYJ"))
print("NYG Content Dim:", get_content_dim("NYG"))
