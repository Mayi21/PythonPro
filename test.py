import os

video_file_path = '/Users/xaohii/Downloads/3&4&5&11'
dirs = os.listdir(video_file_path)
for s in dirs:
    if s.endswith(".mp4"):
        old_file_path = os.path.join(video_file_path, s)
        new_file_name = s[s.index("【"):s.index("(")] + ".mp4"
        new_file_path = os.path.join(video_file_path, new_file_name)
        os.rename(old_file_path, new_file_path)
