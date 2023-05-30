# server 配置
SERVER_IP = '127.0.0.1'
SERVER_PORT = '10002'
SERVER_DEBUG = True

# OPENAI
OPENAI_API_KEY = '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'

# mongodb
MONGODB_DSN = "mongodb://127.0.0.1:27017/"
MONGODB_DB = "chat-assistant"
MONGODB_COl = "chat_record"

# embedding
EMBEDDING_SAVE_PATH = "./emb"

# knowledge
DOCUMENT_CALLBACK_COUNT = 2
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 50
DOCUMENT_DATA_PATH = "./data"

# venus
VENUS_SECRET_ID = "gPc7BneV41MivhOwZtPHWSn4"
VENUS_SECRET_KEY = "vEBvF3SJoHn5DdSZNL6fkbIz"

# logging
LOGGING_MODE = 'file' #file
LOGGING_filename = './server.log'

# promptS
PROMPTS = ["datamesh"]


