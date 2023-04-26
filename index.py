import csv

from simplechain.stack import VectorDatabaseFactory, TextEmbedderFactory

if __name__ == "__main__":
    index = VectorDatabaseFactory.create("annoy", 768, "index.ann", "metadata.json")
    embedder = TextEmbedderFactory.create("ai21")

    metadata = []
    paragraphs = []

    for row in csv.reader(open('data/AI21.csv', 'r')):
        metadata.append(row)
        paragraphs.append(row[0])

    embeds = embedder.embed_all(paragraphs)
    index.add_all(embeds, metadata)
