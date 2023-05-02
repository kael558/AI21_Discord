import csv
import os
import time
import logging

import ai21
from simplechain.stack import TextEmbedderFactory, VectorDatabaseFactory
import shutil


def setup_index():
    embedder = TextEmbedderFactory.create("ai21")
    index = VectorDatabaseFactory.create("annoy", 768, "data/index.ann", "data/metadata.json")

    metadata = []
    paragraphs = []

    for row in csv.reader(open('data/AI21.csv', 'r', encoding='iso-8859-1')):
        metadata.append(row)
        paragraphs.append(row[0])

    # Breaks the strings with 2000+ characters into smaller strings
    for i, s in enumerate(paragraphs):
        if len(s) > 2000:
            paragraphs.pop(i)
            for j in range(0, len(s), 2000):
                paragraphs.insert(i + j, s[j:j + 2000])

    embeds = embedder.embed_all(paragraphs)
    index.add_all(embeds, metadata)
    index.save()

    return len(paragraphs)


def delete_contents_in_folder(directory):
    files = os.listdir(directory)

    # Loop through each file and delete it
    for file in files:
        file_path = os.path.join(directory, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path} with error: {e}")


def copy_files_from_source_to_dest(source_dir, destination_dir):
    # Create the destination directory if it does not exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # List all files in the source directory
    files = os.listdir(source_dir)

    # Loop through each file in the source directory and copy it to the destination directory
    for file in files:
        src_file = os.path.join(source_dir, file)
        dst_file = os.path.join(destination_dir, file)
        shutil.copy(src_file, dst_file)


if __name__ == "__main__":
    ai21.api_key = os.environ['AI21_API_KEY']

    from dotenv import load_dotenv

    load_dotenv()

    logging.basicConfig(filename='logs/indexer.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')
    logging.info("Setting up AI21 Index...")
    start_time = time.time()

    try:
        num_items = setup_index()
        logging.info(f"AI21 Index created with {num_items} items in {time.time() - start_time} seconds.")
    except Exception as e:
        # Move the data folder back to its original location
        delete_contents_in_folder("/data")
        copy_files_from_source_to_dest("/temp_data", "/data")

        logging.error(e)
        logging.info(f"AI21 Index creation failed after {time.time() - start_time} seconds.")
