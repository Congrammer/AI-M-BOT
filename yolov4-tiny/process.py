import os

# Current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
current_dir += 'data/obj/'
print(current_dir)

# Percentage of images to be used for the test set
percentage_test = 10

# Create and/or truncate train.txt and test.txt
file_train = open('data/train.txt', 'w')
file_test = open('data/test.txt', 'w')

# Enable multiple extension names
types = ('.jpg', '.png', '.JPG', '.jpeg')

# Populate train.txt and test.txt
counter = 1
index_test = round(100 / percentage_test)
for pathAndFilename in os.listdir(current_dir):
    title, ext = os.path.splitext(pathAndFilename)

    if ext in types:
        if counter == index_test:
            counter = 1
            file_test.write(current_dir + title + ext + '\n')
        else:
            counter += 1
            file_train.write(current_dir + title + ext + '\n')

file_train.close()
file_test.close()
