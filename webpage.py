import http.server
import socketserver
import requests
import cgi

class TextGeneratorHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Display a form for entering a prompt
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write("""
            <html>
                <head>
                    <style>
                        div {
                        }
                        .container {
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        height: 100%;
                        background: linear-gradient(to right, #9a39a3, #4167a8);
                        background-size: cover;
                        background-position: center;
                        color: #ffffff;
                        font-family: sans-serif;
                        }
                        .buttons {
                        display: flex;
                        flex-direction: row;
                        }
                        button {
                        background-color: #ffffff;
                        color: #9a39a3;
                        border: none;
                        font-size: 16px;
                        font-weight: bold;
                        padding: 06px;
                        cursor: pointer;
                        margin-right: 10px;
                        font-family: sans-serif;
                        }
                        input {
                        border-radius: 10px;
                        border-color: #ffffff;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Try Chat GPT</h1>
                        <form method="POST">
                            <label>Enter a topic:</label>
                            <input type="text" name="prompt">
                            <input type="submit" value="Generate text">
                        </form>
                        <br>
                        <div class="buttons">
                            <a href="https://medium.com/@thakurnitika/subscribe">
                            <button>Subscribe</button>
                            </a>
                            <a href="https://medium.com/@thakurnitika">
                            <button>Click to read more</button>
                            </a>
                        </div>
                    </div>
                </body>
                </html>
                """.encode())

    def do_POST(self):
        # Get the user-entered prompt from the form
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     }
        )
        prompt = form["prompt"].value

        # Set up the API key and endpoint. Enter your API key in below line
        api_key = "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        endpoint = "https://api.openai.com/v1/completions"

        # Set the model
        model = "text-davinci-003"

        # Set the maximum number of tokens (characters=tokens *4 ) to generate at a time
        max_tok = 256
        # Initialize the generated text
        generated_text = ""
        # Set the "continue" flag to "true" to indicate that we want to continue generating text
        continue_flag = "true"
        # Make a request to the GPT-3 API
        while continue_flag == "true":
            # Make a request to the API
            payload = {
                "model": model,
                "prompt": f"{prompt}\n\n{generated_text}",
                "max_tokens": max_tok,
                "stop": continue_flag,
            }
            headers = {"Authorization": f"Bearer {api_key}"}
            r = requests.post(endpoint, json=payload, headers=headers)
            # Append the generated text to the result
            generated_text += r.json()["choices"][0]["text"]

            # Check the "stop" field of the response to see if we should continue generating text
            if r.json()["choices"][0]["finish_reason"] =='stop':
                continue_flag = True

        # Send a response with the generated text
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(f"""
        <html>
            <head>
                <style>
                    div {{
                    }}
                    .container {{
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    height: 100%;
                    background: linear-gradient(to right, #9a39a3, #4167a8);
                    background-size: cover;
                    background-position: center;
                    color: #ffffff;
                    font-family: sans-serif;
                    }}
                    .buttons {{
                    display: flex;
                    flex-direction: row;
                    }}
                    button {{
                    background-color: #ffffff;
                    color: #9a39a3;
                    border: none;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 06px;
                    cursor: pointer;
                    margin-right: 10px;
                    font-family: sans-serif;
                    }}
                    .output-box {{
                        border: 2px solid #9a39a3;
                        border-radius: 10px;
                        width: 50%;
                        height: 30%;
                        overflow: auto;
                        padding: 10px;
                        font-family: sans-serif;
                        color: #000000;
                        background-color: #ffffff;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Try Chat GPT</h1>
                    <div class="output-box">
                    {generated_text}
                    </div>
                    <br>
                    <div class="buttons">
                        <a href="https://medium.com/@thakurnitika/subscribe">
                        <button>Subscribe</button>
                        </a>
                        <a href="https://medium.com/@thakurnitika">
                        <button>Click to read more</button>
                        </a>
                    </div>
                </div>
            </body>
            </html>
            """.encode())
    
# Set up the HTTP server
PORT = 8000
Handler = TextGeneratorHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

print(f"Serving at port {PORT}")
httpd.serve_forever()
