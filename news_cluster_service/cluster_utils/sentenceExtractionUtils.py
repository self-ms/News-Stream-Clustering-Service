from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.text_rank import TextRankSummarizer


class textRankExtractor:

	def __init__(self,num_of_sent):
		
		self.num_of_sent = num_of_sent
		self.summarizer = TextRankSummarizer()

	def getSummarySententces(self, doc):
		
		parser = PlaintextParser.from_string(doc,Tokenizer("english"))
		summary =self.summarizer(parser.document,self.num_of_sent)

		return [sent._text for sent in summary]
