from pathlib import Path
from sentence_transformers import SentenceTransformer


class MiniLM:

	def __init__(self):

		model_path = Path(__file__).resolve().parent.joinpath( "paraphrase-multilingual")
		self.model = SentenceTransformer(str(model_path)).to("cuda:0")

	def docEmbedding(self, sentences):
		
		vecs = self.model.encode(sentences)
		embed = vecs.mean(axis=0).tolist()

		return embed
