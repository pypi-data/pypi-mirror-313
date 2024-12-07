import requests
import os
import time
from typing import List, Optional
from string import punctuation
from random import choice
from requests.exceptions import RequestException
import json
from html.parser import HTMLParser
import re
import html.entities

from webscout.AIutel import Optimizers
from webscout.AIutel import Conversation
from webscout.AIutel import AwesomePrompts
from webscout.AIbase import Provider
from webscout import exceptions

class TerminalFormatter(HTMLParser):
    """
    A custom HTML parser that converts HTML content to terminal-friendly formatted text
    using ANSI escape codes.
    """

    def __init__(self):
        super().__init__()
        self.output = []
        self.list_stack = []
        self.ol_counters = []
        self.bold = False
        self.italic = False

    def handle_starttag(self, tag, attrs):
        if tag in ["strong", "b"]:
            self.output.append("\033[1m")  # Bold
            self.bold = True
        elif tag in ["em", "i"]:
            self.output.append("\033[3m")  # Italic
            self.italic = True
        elif tag == "br":
            self.output.append("\n")
        elif tag in ["p", "div", "h1", "h2", "h3", "h4", "h5", "h6"]:
            self.output.append("\n")
        elif tag == "ul":
            self.list_stack.append("ul")
            self.output.append("\n")
        elif tag == "ol":
            self.list_stack.append("ol")
            self.ol_counters.append(1)
            self.output.append("\n")
        elif tag == "li":
            if self.list_stack:
                if self.list_stack[-1] == "ul":
                    self.output.append("• ")  # Bullet point
                elif self.list_stack[-1] == "ol":
                    number = self.ol_counters[-1]
                    self.output.append(f"{number}. ")
                    self.ol_counters[-1] += 1

    def handle_endtag(self, tag):
        if tag in ["strong", "b"]:
            self.output.append("\033[0m")  # Reset
            self.bold = False
        elif tag in ["em", "i"]:
            self.output.append("\033[0m")  # Reset
            self.italic = False
        elif tag in ["p", "div", "h1", "h2", "h3", "h4", "h5", "h6"]:
            self.output.append("\n")
        elif tag == "ul":
            if self.list_stack and self.list_stack[-1] == "ul":
                self.list_stack.pop()
                self.output.append("\n")
        elif tag == "ol":
            if self.list_stack and self.list_stack[-1] == "ol":
                self.list_stack.pop()
                self.ol_counters.pop()
                self.output.append("\n")
        elif tag == "li":
            self.output.append("\n")

    def handle_data(self, data):
        # Remove ANSI escape codes from the data
        data = re.sub(r'\033\[[0-9;]*m', '', data)  
        data = re.sub(r"\s+", " ", data)
        self.output.append(data)

    def handle_entityref(self, name):
        entity = f"&{name};"
        char = html.entities.name2codepoint.get(name, entity)
        self.output.append(chr(char))

    def handle_charref(self, name):
        try:
            if name.startswith("x") or name.startswith("X"):
                char = chr(int(name[1:], 16))
            else:
                char = chr(int(name))
            self.output.append(char)
        except ValueError:
            self.output.append(f"&#{name};")

    def get_text(self):
        return "".join(self.output).strip()


def html_to_terminal(html_content):
    parser = TerminalFormatter()
    parser.feed(html_content)
    return parser.get_text()


class TutorAI(Provider):
    """
    A class to interact with the TutorAI.me API.
    """

    def __init__(
        self,
        is_conversation: bool = True,
        max_tokens: int = 600,
        timeout: int = 30,
        intro: str = None,
        filepath: str = None,
        update_file: bool = True,
        proxies: dict = {},
        history_offset: int = 10250,
        act: str = None,
        system_prompt: str = "You are a helpful AI assistant.",
    ):
        """
        Initializes the TutorAI.me API with given parameters.

        Args:
            is_conversation (bool, optional): Flag for chatting conversationally. Defaults to True.
            max_tokens (int, optional): Maximum number of tokens to be generated upon completion. Defaults to 600.
            timeout (int, optional): Http request timeout. Defaults to 30.
            intro (str, optional): Conversation introductory prompt. Defaults to None.
            filepath (str, optional): Path to file containing conversation history. Defaults to None.
            update_file (bool, optional): Add new prompts and responses to the file. Defaults to True.
            proxies (dict, optional): Http request proxies. Defaults to {}.
            history_offset (int, optional): Limit conversation history to this number of last texts. Defaults to 10250.
            act (str|int, optional): Awesome prompt key or index. (Used as intro). Defaults to None.
            system_prompt (str, optional): System prompt for TutorAI.
                                   Defaults to "You are a helpful AI assistant.".
        """
        self.session = requests.Session()
        self.is_conversation = is_conversation
        self.max_tokens_to_sample = max_tokens
        self.api_endpoint = "https://tutorai.me/api/generate-homeworkify-response"
        self.stream_chunk_size = 1024
        self.timeout = timeout
        self.last_response = {}
        self.system_prompt = system_prompt
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9,en-IN;q=0.8",
            "Cookie": (
                "ARRAffinity=5ef5a1afbc0178c19fc7bc85047a2309cb69de3271923483302c69744e2b1d24; "
                "ARRAffinitySameSite=5ef5a1afbc0178c19fc7bc85047a2309cb69de3271923483302c69744e2b1d24; "
                "_ga=GA1.1.412867530.1726937399; "
                "_clck=1kwy10j%7C2%7Cfpd%7C0%7C1725; "
                "_clsk=1cqd2q1%7C1726937402133%7C1%7C1%7Cm.clarity.ms%2Fcollect; "
                "_ga_0WF5W33HD7=GS1.1.1726937399.1.1.1726937459.0.0.0"
            ),
            "DNT": "1",
            "Origin": "https://tutorai.me",
            "Priority": "u=1, i",
            "Referer": "https://tutorai.me/homeworkify?ref=taaft&utm_source=taaft&utm_medium=referral",
            "Sec-Ch-Ua": '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/129.0.0.0 Safari/537.36 Edg/128.0.0.0"
            ),
        }

        self.__available_optimizers = (
            method
            for method in dir(Optimizers)
            if callable(getattr(Optimizers, method)) and not method.startswith("__")
        )
        self.session.headers.update(self.headers)
        Conversation.intro = (
            AwesomePrompts().get_act(
                act, raise_not_found=True, default=None, case_insensitive=True
            )
            if act
            else intro or Conversation.intro
        )
        self.conversation = Conversation(
            is_conversation, self.max_tokens_to_sample, filepath, update_file
        )
        self.conversation.history_offset = history_offset
        self.session.proxies = proxies

    def ask(
        self,
        prompt: str,
        stream: bool = False,
        raw: bool = False,
        optimizer: str = None,
        conversationally: bool = False,
        attachment_path: Optional[str] = None
    ) -> dict:
        """Chat with TutorAI

        Args:
            prompt (str): Prompt to be send.
            stream (bool, optional): Flag for streaming response. Defaults to False.
            raw (bool, optional): Stream back raw response as received. Defaults to False.
            optimizer (str, optional): Prompt optimizer name - `[code, shell_command]`. Defaults to None.
            conversationally (bool, optional): Chat conversationally when using optimizer. Defaults to False.
            attachment_path (str, optional): Path to attachment file. Defaults to None.

        Returns:
           dict : {}
        ```json
        {
           "text" : "How may I assist you today?"
        }
        ```
        """
        conversation_prompt = self.conversation.gen_complete_prompt(prompt)
        if optimizer:
            if optimizer in self.__available_optimizers:
                conversation_prompt = getattr(Optimizers, optimizer)(
                    conversation_prompt if conversationally else prompt
                )
            else:
                raise Exception(
                    f"Optimizer is not one of {self.__available_optimizers}"
                )

        form_data = {
            "inputMessage": conversation_prompt,
            "attachmentsCount": "1" if attachment_path else "0"
        }
        files = {}
        if attachment_path:
            if not os.path.isfile(attachment_path):
                raise FileNotFoundError(f"Error: The file '{attachment_path}' does not exist.")
            try:
                files["attachment0"] = (os.path.basename(attachment_path), open(attachment_path, 'rb'), 'image/png')
            except Exception as e:
                raise exceptions.FailedToGenerateResponseError(f"Error opening the file: {e}")

        def for_stream():
            try:
                with requests.post(self.api_endpoint, headers=self.headers, data=form_data, files=files, stream=True, timeout=self.timeout) as response:
                    response.raise_for_status()
                    response_chunks = []
                    json_str = ''
                    for chunk in response.iter_content(chunk_size=self.stream_chunk_size, decode_unicode=True):
                        if chunk:
                            response_chunks.append(chunk)
                            yield chunk if raw else dict(text=chunk)
                    json_str = ''.join(response_chunks)
                    try:
                        response_data = json.loads(json_str)
                    except json.JSONDecodeError as json_err:
                        raise exceptions.FailedToGenerateResponseError(f"\nError decoding JSON: {json_err}")
                    homeworkify_html = response_data.get("homeworkifyResponse", "")
                    if not homeworkify_html:
                        raise exceptions.FailedToGenerateResponseError("\nNo 'homeworkifyResponse' found in the response.")
                    clean_text = html_to_terminal(homeworkify_html)
                    self.last_response.update(dict(text=clean_text))
                    self.conversation.update_chat_history(
                        prompt, self.get_message(self.last_response)
                    )
            except requests.exceptions.RequestException as e:
                raise exceptions.FailedToGenerateResponseError(f"An error occurred: {e}")
        
        def for_non_stream():
            response = self.session.post(self.api_endpoint, headers=self.headers, data=form_data, files=files, timeout=self.timeout)
            if not response.ok:
                raise Exception(
                    f"Failed to generate response - ({response.status_code}, {response.reason}) - {response.text}"
                )

            # Parse the entire JSON response
            response_data = response.json()
            homeworkify_html = response_data.get("homeworkifyResponse", "")
            if not homeworkify_html:
                return {"text": "No content found in the response"}  # Default in case content not found
            clean_text = html_to_terminal(homeworkify_html)

            # Simulate streaming by yielding chunks of the content
            chunk_size = self.stream_chunk_size
            for i in range(0, len(clean_text), chunk_size):
                chunk = clean_text[i:i + chunk_size]
                self.last_response.update(dict(text=chunk))
                yield chunk if raw else dict(text=chunk)
            return self.last_response

        return for_stream() if stream else for_non_stream()

    def chat(
        self,
        prompt: str,
        stream: bool = False,
        optimizer: str = None,
        conversationally: bool = False,
        attachment_path: Optional[str] = None,
    ) -> str:
        """Generate response `str`
        Args:
            prompt (str): Prompt to be send.
            stream (bool, optional): Flag for streaming response. Defaults to False.
            optimizer (str, optional): Prompt optimizer name - `[code, shell_command]`. Defaults to None.
            conversationally (bool, optional): Chat conversationally when using optimizer. Defaults to False.
            attachment_path (str, optional): Path to attachment file. Defaults to None.
        Returns:
            str: Response generated
        """

        def for_stream():
            for response in self.ask(
                prompt, True, optimizer=optimizer, conversationally=conversationally, attachment_path=attachment_path,
            ):
                yield self.get_message(response)

        def for_non_stream():
            for response in self.ask(
                prompt, False, optimizer=optimizer, conversationally=conversationally, attachment_path=attachment_path,
            ):
                yield self.get_message(response)

        return for_stream() if stream else for_non_stream()

    def get_message(self, response: dict) -> str:
        """Retrieves message only from response

        Args:
            response (dict): Response generated by `self.ask`

        Returns:
            str: Message extracted
        """
        assert isinstance(response, dict), "Response should be of dict data-type only"
        return response["text"]

if __name__ == "__main__":
    from rich import print

    ai = TutorAI()
    response = ai.chat(input(">>> "), attachment_path=None)
    for chunk in response:
        print(chunk, end="", flush=True)