import subprocess

class BitNet:
    def generate(self, prompt):
        process = subprocess.Popen(
            [
                "./build/bin/llama-cli",
                "-m", "models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf",
                "-p", prompt,
                "-n", "256",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        response = ""

        while True:
            chunk = process.stdout.read(1)
            if not chunk and process.poll() is not None:
                break

            if chunk:
                response += chunk
                yield chunk

        self.last_response = response

llm = BitNet()

print("\nStreaming Response:")
for token in llm.generate("Hello"):
    print(token, end="", flush=True)

print("\n\nFinal Response:")
print(llm.last_response)