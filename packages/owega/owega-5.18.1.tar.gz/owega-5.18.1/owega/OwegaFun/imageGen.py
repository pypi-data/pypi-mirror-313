"""Image generation functions."""
import json
from openai import OpenAI, OpenAIError

from .functions import Functions
from ..config import baseConf

ImageGenerators = Functions()


def __gen_image(*args, **kwargs) -> str:
    image_prompt = ""
    if len(args) > 0:
        image_prompt = args[0]
    image_prompt = kwargs.get("image_prompt", image_prompt)
    rdict = {}
    if not image_prompt:
        rdict["function_status"] = "No prompt provided, no image generated"
        return json.dumps(rdict)

    api_key_envvar = True
    try:
        client = OpenAI()
    except OpenAIError:
        api_key_envvar = False
        client = OpenAI(api_key='')

    if baseConf.get("api_key", "").startswith("sk-"):
        client.api_key = baseConf.get("api_key", "")
    else:
        if not api_key_envvar:
            rdict["function_status"] = "OpenAI API key invalid"
            return json.dumps(rdict)

    response = client.images.generate(
        model="dall-e-3",
        prompt=image_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image = response.data[0]
    image_url = image.url
    image_newprompt = image.revised_prompt
    rdict["generated_image"] = image_url
    rdict["revised_prompt"] = image_newprompt

    rdict["function_status"] = "Image successfully generated."
    return json.dumps(rdict)


__gen_image_desc = {
    "name": "gen_image",
    "description":
        "Generates an image from given prompt, and returns the image as an url,"
        " and the prompt after it's been revised."
    ,
    "parameters": {
        "type": "object",
        "properties": {
            "image_prompt": {
                "type": "string",
                "description":
                    "the prompt to generate an image with. will use DALL-E 3"
            }
        },
        "required": ["image_prompt"],
    },
}


ImageGenerators.addFunction(__gen_image, __gen_image_desc)
