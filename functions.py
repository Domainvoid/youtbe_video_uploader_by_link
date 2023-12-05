import re
import os
import json
def yt_title():
    dir = "shorts"
    video_path = None
    for x, y, z in os.walk(dir):
        if z:
            video_path = os.path.join(dir, z[0])
            video_title = os.path.splitext(z[0])[0]
        else:
            pass
            #print("No files found in directory:", dir)


    # Remove hashtags and truncate to 100 characters
    new_title = video_title.replace('#', '') + "|thanks for watching do subscribe!😊"
    if len(new_title) > 100:
        new_title = new_title[:100]
    if not new_title.strip():
        new_title = "respect+++"

    new_video_file = video_path
    file_path = 'metadata.json'

    with open(file_path, 'r') as file:
        data = json.load(file)
    data['title'] = new_title
    data['video_file'] = new_video_file

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def path():
    root=''
    filename=''
    mp4_path=[]
    txt_path=[]
    for x,y,z in os.walk("reels"):
       root=x
       filename=z
    for name in filename:
        if '.mp4' in name:
            mp4_path.append(os.path.join(root,name))
        if'.txt' in name:
            txt_path.append(os.path.join(root, name))
    return mp4_path , txt_path
def remove_emojis(text):
    # Regex pattern to match emojis
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def insta_title():
    try:
        var = ''
        # Assuming path() returns two lists: one for .mp4 files and one for .txt files
        mp4_path, txt_path = path()
        print(txt_path, mp4_path)
        if txt_path and mp4_path:
            with open(txt_path[0], "r", encoding='utf-8') as file:
                input_string = file.readline()

            # Remove emojis and hashtags from the string
            input_string = remove_emojis(input_string)
            hash_index = input_string.find('#')
            if hash_index != -1:
                var = input_string[:hash_index].strip()
            else:
                var = input_string.strip()

            # Trim title to 100 characters
            if len(var) > 100:
                var = var[:100].rstrip()
            file_path = 'metadata.json'

            new_title = var + " | thanks for watching do subscribe! 😊"
            new_video_file = mp4_path[0]
            print(new_video_file)
            with open(file_path, 'r') as file:
                data = json.load(file)
            data['title'] = new_title
            data['video_file'] = new_video_file
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
            print("done!")
            return True
        else:
            print("No .mp4 or .txt files found in the directory.")
            return False
    except Exception as e:
        print(f"An exception occurred: {e}")
        return False


def insta_tags():
    with open(path()[1], "r", encoding='utf-8') as file:
        input_string = file.readlines()
    # Remove emojis from the string
    #input_string = remove_emojis(input_string)
    tags=''
    for x in input_string :
        if '#' in x  :
            tags=x
            tags=tags.replace(' ',',')
            break
    return tags


def delete_files_in_folder():
    folder_path = ['reels', 'shorts']
    file_path="metadata.json"
    with open(file_path, 'r') as file:
        data = json.load(file)
    data['title'] = 'respect'
    data['video_file'] = ''
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    for x in folder_path:
        for filename in os.listdir(x):
            file_path = os.path.join(x, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    #print(f"Deleted file: {file_path}")
                else:
                    pass
                    #print(f"Skipped non-file: {file_path}")
            except Exception as e:
                pass
                #print(f"Failed to delete {file_path}. Reason: {e}")