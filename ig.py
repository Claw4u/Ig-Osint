import instaloader
from instastories import instaloader as stories_loader

def download_posts(username):
    L = instaloader.Instaloader()
    
    # Login jika perlu
    # L.login("your_username", "your_password")  # Uncomment jika ingin login

    # Mengunduh semua postingan
    profile = instaloader.Profile.from_username(L.context, username)
    print(f"Downloading posts from {username}...")
    for post in profile.get_posts():
        L.download_post(post, target=profile.username)
    print("Posts downloaded successfully.")

def download_stories(username):
    downloader = stories_loader.Instaloader()
    print(f"Downloading stories from {username}...")
    downloader.download_stories(usernames=[username])
    print("Stories downloaded successfully.")

def download_highlights(username):
    L = instaloader.Instaloader()
    
    # Login jika perlu
    # L.login("your_username", "your_password")  # Uncomment jika ingin login

    # Mengunduh sorotan
    profile = instaloader.Profile.from_username(L.context, username)
    print(f"Downloading highlights from {username}...")
    for highlight in profile.get_highlights():
        L.download_highlight(highlight, target=profile.username)
    print("Highlights downloaded successfully.")

if __name__ == "__main__":
    target_username = input("Enter the Instagram username to download from: ")
    
    download_posts(target_username)
    download_stories(target_username)
    download_highlights(target_username)