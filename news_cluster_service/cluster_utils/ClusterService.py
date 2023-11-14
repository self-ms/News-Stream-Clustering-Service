import numpy as np
from joblib import load
from pathlib import Path
from cluster_utils.embeddingModels import MiniLM
from cluster_utils.sentenceExtractionUtils import textRankExtractor


class newsCluster:

	def __init__(self):

		self.summary_extractor = textRankExtractor(2)
		self.embedding = MiniLM()

		model_path = Path(__file__).resolve().parent.joinpath( "KnnModel.joblib")

		self.Knn_Model = load(str(model_path))

	def getDocumentsClass(self,data_frame):

		data_frame['sent'] = data_frame.apply(lambda row: self.summary_extractor.getSummarySententces(row['text']), axis=1)
		data_frame['embd'] = data_frame.apply(lambda row: self.embedding.docEmbedding(row['sent']), axis=1)
		data_frame = self.__dropNois(data_frame)
		X = np.matrix(data_frame['embd'].to_list())
		data_frame['pred'] = self.Knn_Model.predict(X)
		data_frame['important'] = data_frame.apply(lambda row: self.__idx2class(int(row['pred'])), axis=1)
		
		return data_frame.drop(['pred','sent'], axis=1)

	def __dropNois(self, df):

		nois = []
		for ind in df.index:
			try:
				if len(df['embd'][ind]) !=384:
					nois.append(ind)
			except:
				nois.append(ind)
		df = df.drop(nois)

		return df

	def __idx2class(self,num):
		
		idx2class = {1:'cls'}
		try:
			return [idx2class[num]]
		except:
			return []
