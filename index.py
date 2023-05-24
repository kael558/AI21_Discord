import csv
import logging
import os
import shutil
import time

import ai21
from simplechain.stack import TextEmbedderFactory, VectorDatabaseFactory

logging.basicConfig(filename='logs/indexer.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')


class Indexer:
    def __init__(self, data_file: str = "data/index.ann", metadata_file: str = "data/metadata.json"):
        from dotenv import load_dotenv
        load_dotenv()
        ai21.api_key = os.environ['AI21_API_KEY']
        self.embedder = TextEmbedderFactory.create("ai21")
        self.index = VectorDatabaseFactory.create("annoy", 768, data_file, metadata_file)

    def setup_index(self):
        data = []
        for i, row in enumerate(csv.reader(open('data/AI21.csv', 'r', encoding='UTF-8'))):
            if i == 0:  # Skip the header
                continue
            data.append(row)

        embeds = self.embedder.embed_all([d[0] for d in data])  # embed the titles
        data = [{"title": d[0], "text": d[1], "link": d[2]} for d in data]
        self.index.add_all(embeds, data)
        self.index.save()

        return len(data)

    def get_context(self, request, n=5):
        context, links = [], []
        try:
            # If 'AI21' is in string, it maps it to generic pages too often. So we remove it.
            request = request.replace('AI21', '')

            results_dict = self.index.get_nearest_neighbors(self.embedder.embed(request), n, include_distances=True)

            for i, item_idx in enumerate(results_dict['ids']):
                if results_dict['distances'][i] > 1:
                    break
                links.append(results_dict['metadata'][i]['link'])
                context.append(results_dict['metadata'][i]['text'])
        except Exception as e:
            logging.error(e)
            return None, None

        if len(context) == 0:
            return None, None

        length = 49999//len(context)
        context = [c[:length] for c in context]
        context_str = "".join(context)  # Contextual Answers API has 50k character limit
        links_str = ":link: **The following links may be useful:**\n- " + "\n- ".join(links)

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
    """ 
    Sets up index and data files in data/ folder.
    """
    from dotenv import load_dotenv

    load_dotenv()
    ai21.api_key = os.environ['AI21_API_KEY']
    setup()
