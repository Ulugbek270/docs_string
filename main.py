import paramiko
import time
from pdf_string import PDFTextExtractor
hostname = '10.20.10.115' 
username = 'ulugbek'
password = 'xu3W37CEeZj8'

client = paramiko.SSHClient()

client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname, username=username, password=password)


extractor = PDFTextExtractor()
text = extractor.extract_text("./doc1.pdf")

# print(text)
prompt = f"""
Can you analyse this Uzbek/Cyrillic document.

You need to analyse and give me basic info about it:
- author
- company
- date
- summary

If you did not get any text, say so.

TEXT:
{text}
"""

try:

    stdin, stdout, stderr = client.exec_command(
        'OLLAMA_NO_STREAM=1 ollama run qwen2.5:7b '
        f'{prompt}' ,

        get_pty=True
    )

    output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()

    print("OUTPUT:")
    print(output)

    if error:
        print("ERROR:")
        print(error)

except paramiko.AuthenticationException:
    print("Authentication failed, please check your credentials.")
except paramiko.SSHException as e:
    print(f"SSH error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client.close()
    print("Connection closed.")
