import httpx
import base64
from rich import print
from pathlib import Path


class SEATALK:
    def __init__(self,
            group_id: str,
            message: str = None,
            mention_lst: list = None,
            image_path: str | Path = None,
            file_path: Path = None,
    ):
        # config
        self.headers = {'Content-Type': 'application/json'}
        self.group_id = group_id
        self.mention_lst = mention_lst

        # text
        self.message = message

        # image
        self.image_path = image_path

        # file
        self.file_path = file_path

    def create_text_message(self) -> dict:
        return {
            'tag': 'text',
            'text': {
                'content': self.message,
                'mentioned_email_list': self.mention_lst,
                'at_all': False,
                'format': 1  # 1: markdown | 2: text
            }
        }

    def create_file(self) -> dict:
        file_path = str(self.file_path) if isinstance(self.file_path, Path) else self.file_path
        raw = open(file_path, 'rb').read()
        base64_encoded = base64.b64encode(raw).decode('latin-1')
        return {
            'tag': 'file',
            'file': {
                'filename': self.file_path.name,
                'content': base64_encoded
            }
        }

    def create_image_message(self) -> dict:
        image_path = str(self.image_path) if isinstance(self.image_path, Path) else self.image_path
        raw = open(image_path, 'rb').read()
        base64_encoded = base64.b64encode(raw).decode('latin-1')
        return {
            'tag': 'image',
            'image_base64': {
                'content': base64_encoded
            }
        }

    def send(self):
        # config
        config = {'url': self.group_id, 'headers': self.headers}

        # text
        if self.message:
            config.update({'json': self.create_text_message()})
            response = httpx.post(**config)

        # image
        if self.image_path:
            config.update({'json': self.create_image_message()})
            response = httpx.post(**config)

        # file
        if self.file_path:
            config.update({'json': self.create_file()})
            response = httpx.post(**config)

        if response.status_code != 200:
            print(f'Request returned an error {response.status_code}, the response is:\n{response.text}')


# group_id = 'https://openapi.seatalk.io/webhook/group/_3ek_iqGTvu_-jnOuZ7yjA'  # Survey
# text = '**Chameleon ne**'
# SEATALK(
#     group_id,
#     message=text,
#     mention_lst=['xuankhang.do@shopee.com'],
#     image_path='/home/kevin/Downloads/MainBefore.jpg'
# ).send()

# SEATALK(
#     group_id,
#     file_path=Path('/home/kevin/Downloads/classify_cat_miniLM_l2.ipynb')
# ).send()
