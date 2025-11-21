from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

def get_video_id(url: str) -> str:
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    else:
        raise ValueError("Invalid YouTube URL")

def fetch_transcript(url: str) -> str:
    video_id = get_video_id(url)
    api = YouTubeTranscriptApi()
    transcript_data = api.fetch(video_id, languages=['en'])
    return " ".join([item.text for item in transcript_data])

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.5
)

parser = StrOutputParser()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

chat_prompt = ChatPromptTemplate([
    ("system", "You are a helpful assistant. Your answer should be tailored to the nature of the question — whether that means summarizing, listing key points, or replying concisely with a single line or word. Choose the format that best fits the situation."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "Context:\n{context}\n\nAnswer the query:\n{query}")
])

def process_request(url : str , query : str , chat_history : list ):
    transcipt = fetch_transcript(url)
    chunks = splitter.create_documents([transcipt])
    vector_store = Chroma.from_documents(chunks,embeddings)
    retriver = vector_store.as_retriever(search_type ='similarity',search_kwargs={'k':4})
    parallel_chain = RunnableParallel({
        'context' : retriver | RunnableLambda(format_docs),
        'query' : RunnablePassthrough()
    })
    inject_history = lambda **x : {**x,'chat_history':chat_history}
    main_chain = parallel_chain | RunnableLambda(inject_history) | chat_prompt | model | parser
    result = main_chain.invoke(query)
    chat_history.extend([HumanMessage(content=query),AIMessage(content=result)])
    
    return result,chat_history



