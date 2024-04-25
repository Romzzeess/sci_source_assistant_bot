import os

from langchain_community.chat_models import GigaChat
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import CharacterTextSplitter
from langchain.schema import HumanMessage, SystemMessage


# Инициализация модели гигачат про
access_token = os.getenv("access_token")
credentials = os.getenv("credentials")

giga = GigaChat(
	model="GigaChat-Pro",
	max_tokens=7000,
	temperature=0.7,
	credentials=credentials,
	scope="GIGACHAT_API_CORP",
	verify_ssl_certs=False
)


def translate_topic_to_ru(text: str, llm=giga):
	initial_queries_prompt = f"Translate text '{text}' to Russian. Return only translated sentence."

	messages = [
		SystemMessage(content="Answer only in Russian."),
		HumanMessage(content=initial_queries_prompt),
	]
	result = llm(messages)
	return result.content


def summarize_documents(documents: list[str], llm=giga):

	text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
			chunk_size=1000, chunk_overlap=10
		)
	documents = text_splitter.create_documents(texts=documents)

	split_docs = [doc for doc in text_splitter.split_documents(documents)]

	# Map
	map_template = """The following is a set of documents
		{docs}
		Based on this list of docs, please identify the main themes and write summary of them.
		Add the main takeaways from the document.
		Helpful Answer:"""  # Return result text in Russian.

	map_prompt = PromptTemplate.from_template(map_template)
	map_chain = LLMChain(llm=llm, prompt=map_prompt)

	# Reduce
	reduce_template = """The following is set of summaries:
		{docs}
		Take these and distill it into a final, consolidated summary of the main themes.
		Helpful Answer:"""
	reduce_prompt = PromptTemplate.from_template(reduce_template)

	# Run chain
	reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

	# Run chain
	topics = map_chain.run(split_docs)
	summary = reduce_chain.run(topics)

	return translate_topic_to_ru(summary)
