import csv
import os
import time
import logging
from collections import Counter

import ai21
from simplechain.stack import TextEmbedderFactory, VectorDatabaseFactory
import shutil


class Indexer:
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()
        ai21.api_key = os.environ['AI21_API_KEY']
        self.embedder = TextEmbedderFactory.create("ai21")
        self.index = VectorDatabaseFactory.create("annoy", 768, "data/index.ann", "data/metadata.json")

    def setup_index(self):
        raw_data = {}

        for row in csv.reader(open('data/AI21.csv', 'r', encoding='iso-8859-1')):
            if row[0] in raw_data:
                raw_data[row[0]].append(row[1])
            else:
                raw_data[row[0]] = [row[1]]

        # Convert the dictionary to a list of tuples
        data = [(k, v) for k, v in raw_data.items()]

        # Breaks the strings with 2000+ characters into smaller strings
        for i, tupl in enumerate(data):
            if len(tupl[0]) > 2000:
                data.pop(i)
                for j in range(0, len(tupl[0]), 2000):
                    s = tupl[0]
                    new_tuple = (s[j:j + 2000], tupl[1])
                    data.insert(i + j, new_tuple)

        embeds = self.embedder.embed_all([tupl[0] for tupl in data])
        self.index.add_all(embeds, data)
        self.index.save()

        return len(data)

    def get_context(self, request, n=10):
        context_str, links_str = "", ""
        try:
            results_dict = self.index.get_nearest_neighbors(self.embedder.embed(request), n, include_distances=True)
            indexes = set()
            for i in results_dict['ids']:
                if i < 3:
                    if i >= 2:
                        indexes.add(i-2)
                    if i >= 1:
                        indexes.add(i-1)
                    indexes.add(i)
                else:
                    if results_dict['distances'][i] > 0.8:
                        break

            indexes = list(indexes)
            indexes.sort()
            context = []
            links_counter = Counter()
            if len(indexes) > 0:
                metadata = self.index.get_item_given_index(indexes[0]['metadata'])
                for link in metadata['link']:
                    links_counter[link] += 1
                context.append("- " + str(metadata['paragraph']))
                for i in range(1, len(indexes)):
                    if indexes[i] - 1 != indexes[i-1]: # new paragraph
                        context.append("\n - ")
                    else:
                        context.append(" ")
                    metadata = self.index.get_item_given_index(indexes[i]['metadata'])
                    for link in metadata['link']:
                        links_counter[link] += 1
                    context.append("- " + str(metadata['paragraph']))
            context_str = "".join(context)

            if links_counter:
                links_str = ":link: **The following links may be useful:**\n- " + "\n- ".join(
                    [link[0] for link in links_counter.most_common(3)])
        except Exception as e:
            # Keep going if the index fails
            links_str = ""
            context_str = ""
        return context_str, links_str


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


def setup():
    logging.basicConfig(filename='logs/indexer.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')
    logging.info("Setting up AI21 Index...")
    start_time = time.time()

    try:
        indexer = Indexer()
        num_items = indexer.setup_index()
        logging.info(f"AI21 Index created with {num_items} items in {time.time() - start_time} seconds.")
    except Exception as e:
        # Move the data folder back to its original location
        delete_contents_in_folder("data/")
        copy_files_from_source_to_dest("temp_data/", "data/")

        logging.error(e)
        logging.info(f"AI21 Index creation failed after {time.time() - start_time} seconds.")


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    ai21.api_key = os.environ['AI21_API_KEY']
    setup()
