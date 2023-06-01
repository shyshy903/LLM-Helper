from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import DirectoryLoader
from langchain.vectorstores import Chroma
from langchain.text_splitter import TokenTextSplitter
import config
import os


class Knowledge:

    emb_model = OpenAIEmbeddings(openai_api_key = config.OPENAI_API_KEY)

    def __int__(self) -> None:
        pass


    def save_knowledge(self):
        text_splitter = TokenTextSplitter(chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP)
        doc_loader = DirectoryLoader(config.DOCUMENT_DATA_PATH, glob='**/*.txt')
        docs = doc_loader.load()
        doc_texts = text_splitter.split_documents(docs)
        vectordb = Chroma(persist_directory=config.EMBEDDING_SAVE_PATH, embedding_function=self.emb_model)
        texts = []
        metadatas = []
        doc_idx = 0
        doc_cnt = 0
        doc_size = 100
        for doc in doc_texts:
            texts.append(doc.page_content)
            metadatas.append(doc.metadata)
            doc_idx = doc_idx + 1
            doc_cnt = doc_cnt + 1
            if doc_idx == doc_size:
                vectordb.add_texts(texts, metadatas)
                vectordb.persist()
                doc_idx = 0
                texts = []
                metadatas = []
        vectordb.add_texts(texts, metadatas)
        vectordb.persist()


    def clear_knowlede(self):
        os.rmdir(config.EMBEDDING_SAVE_PATH)
        pass


    def get_knowledeg(self, msg: str) -> str:
        try:
            vectordb = Chroma(persist_directory=config.EMBEDDING_SAVE_PATH, embedding_function=self.emb_model)
            docs = vectordb.similarity_search_with_score(msg, k=config.DOCUMENT_CALLBACK_COUNT)
            print(msg)
            print(docs[0])
            res_str = ""
            for doc,score in docs:
                print(score)
                if score < 0.1:
                    continue
                res_str = res_str + doc.page_content
                res_str += "\n"
        except Exception as e:
            res_str = ""
        print(len(res_str))
        return res_str

    def call_knowledge(self, msg: str):
        return self.get_knowledeg(msg)


knowledge = Knowledge()

if __name__ == "__main__":
    # knowledge.save_knowledge()
    print(knowledge.call_knowledge("怎么在DataMesh创建空间？"))
