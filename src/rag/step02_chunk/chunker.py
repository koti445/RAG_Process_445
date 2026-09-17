import tiktoken

from src.core.config import get_settings
from src.domain.models import TextChunk

class TextChunker:
    
    def __init__(self) -> None:
        settings = get_settings()
        self.chunk_size = settings.chunk_size
        self.chunk_overlap = settings.chunk_overlap
        self.encoding = tiktoken.get_encoding("cl100k_base")
        
    def count_tokens(self, text: str) -> int:
        return len(self.encoding.encode(text))
        
        
    def chunk(self, text: str, metadata: dict | None = None) -> list[TextChunk]:
        metadata  = metadata  or {}
        tokens =  self.encoding.encode(text)
        chunks: list[TextChunk] = []
        
        start =0
        index=0
        
        while start < len(tokens):
            end=min(start + self.chunk_size, len(tokens))
            chunk_tokens = tokens[start:end]
            chunk_text =  self.encoding.decode(chunk_tokens)
            
            chunks.append(
            TextChunk(
            content = chunk_text,
            chunk_index = index,
            token_count = len(chunk_tokens),
            meta_data = {**metadata, "start_token": start, "end_token":end}
            )
            )
            
            if end >= len(tokens):
                break
                
                
            start = end  -  self.chunk_overlap
            index +=1
            
        return chunks
    
    