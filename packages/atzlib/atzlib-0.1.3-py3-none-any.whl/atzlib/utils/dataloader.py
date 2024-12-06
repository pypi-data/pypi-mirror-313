"""파일 전처리 모듈. """
import glob
import os
import pandas as pd

from langchain.document_loaders import PyMuPDFLoader, CSVLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_directory(folder_path, chunk_size, chunk_overlap, suffix):
    #TODO: 디렉토리 로딩은 나중에 수정하기
    files = glob.glob(os.path.join(folder_path, f"*.{suffix}"))
    bag_of_texts = []
    for file in files:  # 지정된 파일을 읽어서 Chunk로 분리
        if suffix == 'pdf':
            docs = PyMuPDFLoader(file).load()
        if suffix == 'txt':
            docs = TextLoader(file).load()
        texts = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap).split_documents(docs)
        bag_of_texts.append(texts)
    return bag_of_texts

def load_pdf(file_path, file_name, chunk_size, chunk_overlap):
    combined_path = os.path.join(file_path, file_name)
    docs = PyMuPDFLoader(combined_path).load()
    texts = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap).split_documents(docs)
    return texts

def load_csv(file_path):    
    loader = CSVLoader(file_path=file_path, csv_args={
        'delimiter': ',',
    })
    texts = loader.load()
    
    return texts


if __name__ == "__main__":
    print('Running dataloader.py')
    