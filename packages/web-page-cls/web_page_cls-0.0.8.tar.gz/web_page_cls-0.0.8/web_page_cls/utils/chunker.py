"""
Chunk text to parst for Mistral LLM
"""
from mistral_common.protocol.instruct.messages import UserMessage
from mistral_common.protocol.instruct.request import ChatCompletionRequest
from mistral_common.tokens.tokenizers.mistral import MistralTokenizer


class ChunkerMistral:
    """
    Chunk text to parst for Mistral LLM
    """

    def __init__(self, model_name="mistral-nemo"):
        self.tokenizer = MistralTokenizer.from_model(model_name, strict=True)
        self.model_name = model_name

    def get_mistral_token_count(self, content: str) -> int:
        """
        Get size of tokens for Mistral model
        """

        tokenized = self.tokenizer.encode_chat_completion(
            ChatCompletionRequest(
                messages=[
                    UserMessage(content=content),
                ],
                model=self.model_name,
            )
        )
        tokens, _text = tokenized.tokens, tokenized.text

        return len(tokens)

    def chunk(self, content: str, chunk_max_tokens=4000, delimiter='\n') -> list[str]:
        """
        Chunk text for LLM
        """
        lines = content.split(delimiter)

        result = []
        current_token_size = 0
        current_chunk = ""

        for line in lines:

            line_tokens_size = self.get_mistral_token_count(line)

            if current_token_size + line_tokens_size > chunk_max_tokens:

                result.append(current_chunk)
                current_chunk = ""
                current_token_size = 0

            else:
                current_token_size += line_tokens_size
                current_chunk += line + delimiter
                
        result.append(current_chunk)

        return result


if __name__ == '__main__':

    from web_page_cls.utils.io import read_txt_file

    war_and_piece = read_txt_file('war_and_peace.ru.txt')

    chunker = ChunkerMistral(model_name='mistral-nemo')

    chunks = chunker.chunk(war_and_piece, chunk_max_tokens=1000)

    print(len(chunks))
