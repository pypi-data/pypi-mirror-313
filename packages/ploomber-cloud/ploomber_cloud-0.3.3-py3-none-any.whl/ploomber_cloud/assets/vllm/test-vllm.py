import argparse
import http.client
import json
import sys

api_key = "$API_KEY"
app_id = "$APP_ID"
model_name = "$MODEL_NAME"


def completion(prompt):
    conn = http.client.HTTPSConnection(f"{app_id}.ploomberapp.io")

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    data = {
        "model": model_name,
        "prompt": [prompt],
    }

    conn.request("POST", "/v1/completions", body=json.dumps(data), headers=headers)

    res = conn.getresponse()
    data = res.read()

    if res.code in {302, 503}:
        sys.exit("vLLM not running yet, wait for the deployment to finish...")

    response = json.loads(data.decode("utf-8"))
    return response["choices"][0]["text"]


def main(prompt):
    print(f"Prompt: {prompt}")
    response = completion(prompt)
    print(f"vLLM response: {response}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI application")
    parser.add_argument(
        "prompt",
        type=str,
        help="The prompt for the model",
        default="Python is...",
        nargs="?",
    )
    args = parser.parse_args()

    main(args.prompt)
