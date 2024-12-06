from bs4 import BeautifulSoup
import tiktoken, logging, traceback, json
from openai import OpenAI

# __all__ = [
#     name for name, obj in globals().items()
#     if callable(obj) or isinstance(obj, type)  # Include functions and classes
# ]

class AIUtils:

    @staticmethod
    def clean_html(html=None, exclude_attr=None, tags_to_remove=[]):
        soup = BeautifulSoup(html, 'lxml')

        # Remove specified tags
        for tag_name in tags_to_remove:
            for tag in soup.find_all(tag_name):
                tag.decompose()

        # Remove all attributes except the excluded one
        for tag in soup.find_all(True):  # find all tags
            for attr in list(tag.attrs):  # create a list to avoid runtime changes
                if attr != exclude_attr:
                    del tag.attrs[attr]

        # Extract body content
        body = soup.body

        # Return cleaned HTML as a string
        return str(body)

    @staticmethod
    def remove_tags(html):
        soup = BeautifulSoup(html, "html.parser")
        for data in soup(['style', 'script', 'header', 'head', 'footer', 'title', 'meta', 'link', '<ul class="nav">']):
            data.decompose()
        return ' '.join(soup.stripped_strings)

    @staticmethod
    def count_tokens(model: str="gpt-4o-mini", input_string: str = None) -> int:
        tokenizer = tiktoken.encoding_for_model(model)
        tokens = tokenizer.encode(input_string)
        return len(tokens)

    @staticmethod
    def calculate_cost_input(model: str="gpt-4o-mini", input_string: str=None) -> float:
        if input_string:
            num_tokens = AIUtils.count_tokens(model, input_string)
            total_cost = (num_tokens / 1_000_000) * 0.15
            logging.info(f"The total token for input_string: {num_tokens} using {model} is cost: {total_cost:.6f}$")
            return total_cost
        return 0

    @staticmethod
    def calculate_cost_output(model: str="gpt-4o-mini", output_string: str=None) -> float:
        if output_string:
            num_tokens = AIUtils.count_tokens(model, output_string)
            total_cost = (num_tokens / 1_000_000) * 0.6
            logging.info(f"The total token for input_string: {num_tokens} using {model} is cost: {total_cost:.6f}$")
            return total_cost
        return 0

    @staticmethod
    def ai_parse_string(model: str="gpt-4o-mini", api_key: str=None, prompt: str=None) -> dict:
        results = {}
        try:
            client = OpenAI(
                api_key=api_key,
            )

            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )

            results = completion.choices[0].message.content
            results = json.loads(results.replace("```", "").replace("json", "").strip())
        except:
            logging.error(traceback.format_exc())

        return results


# if __name__ == '__main__':
#     ai_model = 'gpt-4o-mini'
#     api_key = "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"
#
#     input_string = 'Viking and Thermador Appliance Repair In San Diego'
#     prompt = 'given this player name : "' + str(input_string) + '" return a concise response that must be in JSON format. The JSON object you return must have a key of `gender`. The value attached to the `gender` key should only either be `Male` or `Female` .'
#     results_ai = AIUtils.ai_parse_string(model=ai_model, api_key=api_key, prompt=prompt)
#     print(f'results_ai: {results_ai}')