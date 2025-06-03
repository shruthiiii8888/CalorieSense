'''import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import csv
# Load EfficientNet model
base_model = EfficientNetB0(weights='imagenet', include_top=False, pooling='avg')

# Suppress TensorFlow progress bar
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

def extract_features(image_path):
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = tf.keras.applications.efficientnet.preprocess_input(image)

    # Run model without displaying progress bar
    features = base_model.predict(image, verbose=0)
    return features.flatten()

def find_best_match(image_path):
    # Load features_db.pkl
    with open('features_db.pkl', 'rb') as f:
        features_db = pickle.load(f)

    # Extract features from the new image
    new_image_features = extract_features(image_path)

    best_match = None
    best_score = -1
    best_category = None

    # Compare with database
    for category, data in features_db.items():
        for image_data in data['images']:
            features = image_data['features']
            similarity = cosine_similarity([new_image_features], [features])[0][0]
            if similarity > best_score:
                best_score = similarity
                best_match = image_data
                best_category = category


    # Print the output only (no progress bar)
    print(f"{best_category},{float(best_score):.2f}")

# Test the function
if __name__ == "__main__":
    import sys
    image_path = sys.argv[1]
    find_best_match(image_path)'''






'''
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import csv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random

# ✅ Load EfficientNet model
base_model = EfficientNetB0(weights='imagenet', include_top=False, pooling='avg')

# ✅ Suppress TensorFlow progress bar
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

# ✅ Function to extract features from image
def extract_features(image_path):
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = tf.keras.applications.efficientnet.preprocess_input(image)

    # ✅ Run model without displaying progress bar
    features = base_model.predict(image, verbose=0)
    return features.flatten()

# ✅ Function to check if the category exists in the CSV
def check_category_in_csv(predicted_category, csv_file_path):
    with open(csv_file_path, 'r', encoding='latin-1') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Food Item'] == predicted_category:
                return True
    return False

# ✅ Function to get metadata from CSV
def get_metadata_from_csv(predicted_category, csv_file_path):
    with open(csv_file_path, 'r', encoding='latin-1') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Food Item'] == predicted_category:
                return {
                    'Calories': row['Calories (kcal)'],
                    'Serving Size': row['Serving Size (g/ml)'],
                    'Quality Rating': row['Quality Rating'],
                    'Ingredients': row['Ingredients'],
                    'Cuisine': row['Cuisuine'],
                    'Preparation': row[' Preparation']
                }
    return None

# ✅ Function to find the best match
def find_best_match(image_path):
    # ✅ Load features_db.pkl
    with open('features_db.pkl', 'rb') as f:
        features_db = pickle.load(f)

    # ✅ Extract features from the new image
    new_image_features = extract_features(image_path)

    best_match = None
    best_score = -1
    best_category = None

    # ✅ Compare with database
    for category, data in features_db.items():
        for image_data in data['images']:
            features = image_data['features']
            similarity = cosine_similarity([new_image_features], [features])[0][0]
            if similarity > best_score:
                best_score = similarity
                best_match = image_data
                best_category = category

    # ✅ Show result if matched
    if best_category:
        if check_category_in_csv(best_category, 'food_data_detailed_updated.csv'):
            metadata = get_metadata_from_csv(best_category, 'food_data_detailed_updated.csv')

            print(f"Predicted Category: {best_category}")
            print(f"Calories: {metadata['Calories']}")
            print(f"Serving Size: {metadata['Serving Size']}")
            print(f"Quality Rating: {metadata['Quality Rating']}")
            print(f"Ingredients: {metadata['Ingredients']}")
            print(f"Cuisine: {metadata['Cuisine']}")
            print(f"Preparation: {metadata['Preparation']}")

            # ✅ Display images
            plt.figure(figsize=(15, 5))

            # ✅ Original image
            plt.subplot(1, 3, 1)
            plt.imshow(mpimg.imread(image_path))
            plt.title("Original Image")

            # ✅ Randomly select 2 images from the category folder
            category_folder = os.path.join(os.getcwd(), 'food', best_category)

            if os.path.exists(category_folder):
                image_files = os.listdir(category_folder)

                # ✅ If less than 2 images exist, show whatever is available
                if len(image_files) >= 2:
                    selected_images = random.sample(image_files, 2)
                elif len(image_files) == 1:
                    selected_images = [image_files[0]]
                else:
                    print(f"No images found in folder: {category_folder}")
                    return

                # ✅ Show 1st matched image
                matched_image_path_1 = os.path.join(category_folder, selected_images[0])
                plt.subplot(1, 3, 2)
                plt.imshow(mpimg.imread(matched_image_path_1))
                plt.title("Matched Image 1")

                # ✅ Show 2nd matched image (if available)
                if len(selected_images) == 2:
                    matched_image_path_2 = os.path.join(category_folder, selected_images[1])
                    plt.subplot(1, 3, 3)
                    plt.imshow(mpimg.imread(matched_image_path_2))
                    plt.title("Matched Image 2")

                # ✅ Show both images
                plt.show()

            else:
                print(f"Folder not found: {category_folder}")

        else:
            print(f"Predicted category '{best_category}' not found in CSV file.")

# ✅ Test the function
if __name__ == "__main__":
    import sys
    image_path = sys.argv[1]
    find_best_match(image_path)
'''

'''

import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import csv
import random
import json
import sys

# ✅ Load EfficientNet model
base_model = EfficientNetB0(weights='imagenet', include_top=False, pooling='avg')

# ✅ Function to extract features from image
def extract_features(image_path):
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = tf.keras.applications.efficientnet.preprocess_input(image)
    features = base_model.predict(image, verbose=0)
    return features.flatten()

# ✅ Function to get metadata from CSV
def get_metadata_from_csv(predicted_category, csv_file_path):
    with open(csv_file_path, 'r', encoding='latin-1') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Food Item'].strip().lower() == predicted_category.strip().lower():
                return {
                    'Calories': row['Calories (kcal)'],
                    'Serving Size': row['Serving Size (g/ml)'],
                    'Quality Rating': row['Quality Rating'],
                    'Ingredients': row['Ingredients'],
                    'Cuisine': row['Cuisuine'],
                    'Preparation': row[' Preparation']
                }
    return None

# ✅ Function to find the best match
def find_best_match(image_path):
    # ✅ Load features_db.pkl
    with open('features_db.pkl', 'rb') as f:
        features_db = pickle.load(f)

    # ✅ Extract features from uploaded image
    new_image_features = extract_features(image_path)

    best_match = None
    best_score = -1
    best_category = None

    # ✅ Compare with database
    for category, data in features_db.items():
        for image_data in data['images']:
            features = image_data['features']
            similarity = cosine_similarity([new_image_features], [features])[0][0]
            if similarity > best_score:
                best_score = similarity
                best_match = image_data
                best_category = category

    # ✅ Fetch metadata from CSV
    metadata = get_metadata_from_csv(best_category, 'food_data_detailed_updated.csv')

    # ✅ Get matched images
    category_folder = os.path.join('food', best_category)
    images = os.listdir(category_folder)

    # ✅ Randomly select 2 images
    matched_images = random.sample(images, 2) if len(images) >= 2 else images

    # ✅ Final JSON Response
    response = {
        'food_item': best_category,
        'calories': metadata['Calories'],
        'serving_size': metadata['Serving Size'],
        'quality_rating': metadata['Quality Rating'],
        'ingredients': metadata['Ingredients'],
        'cuisine': metadata['Cuisine'],
        'preparation': metadata['Preparation'],
        'uploaded_image': image_path,
        'matched_image_1': os.path.join(category_folder, matched_images[0]),
        'matched_image_2': os.path.join(category_folder, matched_images[1]) if len(matched_images) == 2 else None
    }

    # ✅ Output JSON response
    print(json.dumps(response))

if __name__ == "__main__":
    image_path = sys.argv[1]
    find_best_match(image_path)
'''


'''

import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import csv
import random
import json
import sys
from PIL import Image  # ✅ To get image dimensions

# ✅ Load EfficientNet model
base_model = EfficientNetB0(weights='imagenet', include_top=False, pooling='avg')

# ✅ Function to extract features from image
def extract_features(image_path):
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = tf.keras.applications.efficientnet.preprocess_input(image)
    features = base_model.predict(image, verbose=0)
    return features.flatten()

# ✅ Function to get image dimensions
def get_image_dimensions(image_path):
    with Image.open(image_path) as img:
        return img.size  # (width, height)

# ✅ Function to get metadata from CSV
def get_metadata_from_csv(predicted_category, csv_file_path):
    with open(csv_file_path, 'r', encoding='latin-1') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Food Item'].strip().lower() == predicted_category.strip().lower():
                return {
                    'Calories': row['Calories (kcal)'],
                    'Serving Size': row['Serving Size (g/ml)'],
                    'Quality Rating': row['Quality Rating'],
                    'Ingredients': row['Ingredients'],
                    'Cuisine': row['Cuisuine'],
                    'Preparation': row[' Preparation']
                }
    return None

# ✅ Function to find the best match
def find_best_match(image_path):
    # ✅ Load features_db.pkl
    with open('features_db.pkl', 'rb') as f:
        features_db = pickle.load(f)

    # ✅ Extract features from uploaded image
    new_image_features = extract_features(image_path)

    best_match = None
    best_score = -1
    best_category = None

    # ✅ Compare with database
    for category, data in features_db.items():
        for image_data in data['images']:
            features = image_data['features']
            similarity = cosine_similarity([new_image_features], [features])[0][0]
            if similarity > best_score:
                best_score = similarity
                best_match = image_data
                best_category = category

    # ✅ Fetch metadata from CSV
    metadata = get_metadata_from_csv(best_category, 'food_data_detailed_updated.csv')

    # ✅ Get matched images
    category_folder = os.path.join('food', best_category)
    images = os.listdir(category_folder)
    matched_images = random.sample(images, 2) if len(images) >= 2 else images

    # ✅ Get uploaded image dimensions
    width, height = get_image_dimensions(image_path)

    # ✅ Adjust calories based on dimensions
    try:
        original_calories = float(metadata['Calories'])
    except (ValueError, TypeError):
        original_calories = 0

    if width > 224 or height > 224:
        adjusted_calories = original_calories + 100
    else:
        adjusted_calories = max(0, original_calories - 100)  # prevent negative calories

    # ✅ Final JSON Response
    response = {
        'food_item': best_category,
        'calories': round(adjusted_calories, 2),
        'original_calories': metadata['Calories'],
        'image_dimensions': {'width': width, 'height': height},
        'serving_size': metadata['Serving Size'],
        'quality_rating': metadata['Quality Rating'],
        'ingredients': metadata['Ingredients'],
        'cuisine': metadata['Cuisine'],
        'preparation': metadata['Preparation'],
        'uploaded_image': image_path,
        'matched_image_1': os.path.join(category_folder, matched_images[0]),
        'matched_image_2': os.path.join(category_folder, matched_images[1]) if len(matched_images) == 2 else None
    }

    # ✅ Output JSON response
    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    image_path = sys.argv[1]
    find_best_match(image_path)'''





import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import csv
import random
import json
import sys
from PIL import Image

# ✅ Load EfficientNet model
base_model = EfficientNetB0(weights='imagenet', include_top=False, pooling='avg')

# ✅ Function to extract features
def extract_features(image_path):
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = tf.keras.applications.efficientnet.preprocess_input(image)
    features = base_model.predict(image, verbose=0)
    return features.flatten()

# ✅ Function to get image dimensions
def get_image_dimensions(image_path):
    with Image.open(image_path) as img:
        return img.size  # (width, height)

# ✅ Function to get metadata from CSV
def get_metadata_from_csv(predicted_category, csv_file_path):
    try:
        with open(csv_file_path, 'r', encoding='latin-1') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Food Item'].strip().lower() == predicted_category.strip().lower():
                    return {
                        'Calories': row.get('Calories (kcal)', '0'),
                        'Serving Size': row.get('Serving Size (g/ml)', 'Unknown'),
                        'Quality Rating': row.get('Quality Rating', 'Unknown'),
                        'Ingredients': row.get('Ingredients', 'Unknown'),
                        'Cuisine': row.get('Cuisuine', 'Unknown'),
                        'Preparation': row.get(' Preparation', 'Unknown')
                    }
    except Exception as e:
        print(json.dumps({"error": f"Failed to read CSV: {str(e)}"}))
        sys.exit(1)
    return None

# ✅ Main function
def find_best_match(image_path):
    try:
        # ✅ Load features database
        with open('features_db.pkl', 'rb') as f:
            features_db = pickle.load(f)

        # ✅ Extract features from uploaded image
        new_image_features = extract_features(image_path)

        best_score = -1
        best_category = None

        # ✅ Compare uploaded image with stored images
        for category, data in features_db.items():
            for image_data in data['images']:
                features = image_data['features']
                similarity = cosine_similarity([new_image_features], [features])[0][0]
                if similarity > best_score:
                    best_score = similarity
                    best_category = category

        # ✅ Ensure a match was found
        if best_category is None:
            print(json.dumps({"error": "No matching food found"}))
            sys.exit(1)

        # ✅ Fetch metadata
        metadata = get_metadata_from_csv(best_category, 'food_data_detailed_updated.csv')
        if metadata is None:
            print(json.dumps({"error": "Metadata not found"}))
            sys.exit(1)

        # ✅ Ensure category folder exists
        category_folder = os.path.join('food', best_category)
        images = os.listdir(category_folder) if os.path.exists(category_folder) else []
        matched_images = random.sample(images, 2) if len(images) >= 2 else images

        # ✅ Get uploaded image dimensions
        width, height = get_image_dimensions(image_path)

        # ✅ Adjust calories based on image size
        try:
            original_calories = float(metadata['Calories'])
        except (ValueError, TypeError):
            original_calories = 0

        adjusted_calories = original_calories + 10 if width > 224 or height > 224 else max(0, original_calories - 100)

        # ✅ Health note logic (THIS IS THE IMPORTANT FIX)
        if adjusted_calories > 400:
            health_note = " Not Healthy: Calories exceed ."
        else:
            health_note = "Healthy: Within a safe calorie range."

        # ✅ Construct response JSON
        response = {
            'food_item': best_category,
            'calories': round(adjusted_calories, 2),
            'original_calories': metadata['Calories'],
            'image_dimensions': {'width': width, 'height': height},
            'health_note': health_note,  # ✅ THIS WILL ALWAYS SHOW NOW
            'serving_size': metadata['Serving Size'],
            'quality_rating': metadata['Quality Rating'],
            'ingredients': metadata['Ingredients'],
            'cuisine': metadata['Cuisine'],
            'preparation': metadata['Preparation'],
            'uploaded_image': image_path,
            'matched_images': [os.path.join(category_folder, img) for img in matched_images]
        }

        # ✅ Print the JSON response (Only valid JSON is printed)
        print(json.dumps(response))

    except Exception as e:
        print(json.dumps({"error": f"Unexpected error: {str(e)}"}))
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No image path provided"}))
        sys.exit(1)

    image_path = sys.argv[1]

    if not os.path.exists(image_path):
        print(json.dumps({"error": "Image file not found"}))
        sys.exit(1)

    find_best_match(image_path)
