import os
import requests
import json
import time
import getpass
from datetime import datetime
import instaloader

class InstagramOSINT:
    def __init__(self):
        self.loader = instaloader.Instaloader(
            download_pictures=True,
            download_videos=True,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=True,
            compress_json=False
        )
        self.session = requests.Session()
        
    def login(self, username, password):
        """Log in to Instagram"""
        try:
            self.loader.login(username, password)
            print(f"[+] Successfully logged in as {username}")
            return True
        except Exception as e:
            print(f"[-] Login failed: {e}")
            return False
    
    def get_public_profile_info(self, target_username):
        """Get basic public profile information"""
        try:
            profile = instaloader.Profile.from_username(self.loader.context, target_username)
            
            info = {
                "username": profile.username,
                "full_name": profile.full_name,
                "biography": profile.biography,
                "followers": profile.followers,
                "following": profile.followees,
                "is_private": profile.is_private,
                "is_verified": profile.is_verified,
                "post_count": profile.mediacount,
                "profile_pic_url": profile.profile_pic_url,
                "external_url": profile.external_url
            }
            
            print("\n[+] Public Profile Information:")
            for key, value in info.items():
                print(f"  {key}: {value}")
            
            return info, profile
        except Exception as e:
            print(f"[-] Failed to fetch profile information: {e}")
            return None, None
    
    def download_public_posts(self, profile, limit=10):
        """Download recent public posts (images and videos)"""
        try:
            target_username = profile.username
            
            if profile.is_private:
                print("[-] Cannot download posts from private profile")
                return False
            
            print(f"\n[+] Downloading up to {limit} most recent posts...")
            
            # Create directory for downloads
            save_path = f"downloads/{target_username}/posts"
            os.makedirs(save_path, exist_ok=True)
            
            for index, post in enumerate(profile.get_posts()):
                if index >= limit:
                    break
                
                try:
                    # Download post
                    self.loader.download_post(post, target=save_path)
                    print(f"  Downloaded post from {post.date}")
                except Exception as e:
                    print(f"  Failed to download post: {e}")
                
                # Respect rate limits
                time.sleep(2)
            
            print(f"[+] Posts saved to {save_path}")
            return True
        
        except Exception as e:
            print(f"[-] Failed to download posts: {e}")
            return False
    
    def download_profile_picture(self, profile):
        """Download profile picture"""
        try:
            target_username = profile.username
            
            # Create directory for downloads
            save_path = f"downloads/{target_username}"
            os.makedirs(save_path, exist_ok=True)
            
            # Download profile pic
            filename = f"{save_path}/profile_pic.jpg"
            response = requests.get(profile.profile_pic_url, stream=True)
            
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(f"\n[+] Profile picture saved to {filename}")
                return filename
            else:
                print("[-] Failed to download profile picture")
                return None
                
        except Exception as e:
            print(f"[-] Failed to download profile picture: {e}")
            return None
    
    def download_stories(self, profile):
        """Download public stories"""
        try:
            target_username = profile.username
            
            if profile.is_private and not profile.followed_by_viewer:
                print("[-] Cannot download stories from private profile (not following)")
                return False
            
            print(f"\n[+] Attempting to download stories for {target_username}...")
            
            # Create directory for downloads
            save_path = f"downloads/{target_username}/stories"
            os.makedirs(save_path, exist_ok=True)
            
            # Get user ID for story download
            user_id = profile.userid
            
            try:
                # Download stories
                self.loader.download_stories(userids=[user_id], filename_target=save_path)
                print(f"[+] Stories saved to {save_path}")
                return True
            except instaloader.exceptions.LoginRequiredException:
                print("[-] Login required to download stories")
                return False
            except Exception as e:
                print(f"[-] Failed to download stories: {e}")
                return False
                
        except Exception as e:
            print(f"[-] Failed to download stories: {e}")
            return False
    
    def download_highlights(self, profile):
        """Download highlights"""
        try:
            target_username = profile.username
            
            if profile.is_private and not profile.followed_by_viewer:
                print("[-] Cannot download highlights from private profile (not following)")
                return False
            
            print(f"\n[+] Attempting to download highlights for {target_username}...")
            
            # Create directory for downloads
            save_path = f"downloads/{target_username}/highlights"
            os.makedirs(save_path, exist_ok=True)
            
            # Get highlights
            highlights = self.loader.get_highlights(profile)
            if not highlights:
                print("[-] No highlights found or not accessible")
                return False
            
            for highlight in highlights:
                try:
                    print(f"  Downloading highlight: {highlight.title}")
                    self.loader.download_highlight(highlight, save_path)
                except Exception as e:
                    print(f"  Failed to download highlight '{highlight.title}': {e}")
                
                # Respect rate limits
                time.sleep(2)
            
            print(f"[+] Highlights saved to {save_path}")
            return True
                
        except Exception as e:
            print(f"[-] Failed to download highlights: {e}")
            return False
    
    def analyze_user_activity(self, profile, post_limit=10):
        """Analyze posting patterns and activity"""
        try:
            target_username = profile.username
            
            if profile.is_private:
                print("[-] Cannot analyze private profile")
                return None
            
            print("\n[+] Analyzing user activity and posting patterns...")
            
            posts_dates = []
            hashtags = {}
            mentioned_users = {}
            locations = {}
            
            for index, post in enumerate(profile.get_posts()):
                if index >= post_limit:
                    break
                
                # Store post date
                posts_dates.append(post.date)
                
                # Analyze hashtags
                for hashtag in post.caption_hashtags:
                    hashtags[hashtag] = hashtags.get(hashtag, 0) + 1
                
                # Analyze mentioned users
                for user in post.caption_mentions:
                    mentioned_users[user] = mentioned_users.get(user, 0) + 1
                
                # Analyze locations
                if post.location:
                    loc_name = post.location.name if post.location.name else "Unknown"
                    locations[loc_name] = locations.get(loc_name, 0) + 1
                
                # Respect rate limits
                time.sleep(1)
            
            # Analyze posting times
            day_counts = {i: 0 for i in range(7)}  # 0=Monday, 6=Sunday
            hour_counts = {i: 0 for i in range(24)}
            
            for date in posts_dates:
                day_counts[date.weekday()] += 1
                hour_counts[date.hour] += 1
            
            # Results
            analysis = {
                "most_active_day": max(day_counts.items(), key=lambda x: x[1])[0] if day_counts else None,
                "most_active_hour": max(hour_counts.items(), key=lambda x: x[1])[0] if hour_counts else None,
                "top_hashtags": sorted(hashtags.items(), key=lambda x: x[1], reverse=True)[:5],
                "top_mentioned_users": sorted(mentioned_users.items(), key=lambda x: x[1], reverse=True)[:5],
                "top_locations": sorted(locations.items(), key=lambda x: x[1], reverse=True)[:3]
            }
            
            # Convert day number to name
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            if analysis["most_active_day"] is not None:
                analysis["most_active_day"] = days[analysis["most_active_day"]]
            
            print("\n[+] Activity Analysis:")
            if analysis["most_active_day"]:
                print(f"  Most active day: {analysis['most_active_day']}")
            if analysis["most_active_hour"] is not None:
                print(f"  Most active hour: {analysis['most_active_hour']}:00")
            
            if analysis['top_hashtags']:
                print("  Top hashtags:")
                for tag, count in analysis['top_hashtags']:
                    print(f"    #{tag}: {count} posts")
            
            if analysis['top_mentioned_users']:
                print("  Top mentioned users:")
                for user, count in analysis['top_mentioned_users']:
                    print(f"    @{user}: {count} mentions")
            
            if analysis['top_locations']:
                print("  Top locations:")
                for loc, count in analysis['top_locations']:
                    print(f"    {loc}: {count} posts")
            
            return analysis
            
        except Exception as e:
            print(f"[-] Failed to analyze user activity: {e}")
            return None

def show_menu():
    print("\n" + "=" * 60)
    print("              Instagram OSINT Menu                 ")
    print("=" * 60)
    print("1. Download Profile Picture")
    print("2. Download Posts")
    print("3. Download Stories")
    print("4. Download Highlights")
    print("5. Analyze User Activity")
    print("6. Exit")
    print("=" * 60)
    choice = input("Enter your choice (1-6): ")
    return choice

def main():
    print("=" * 60)
    print("              Instagram OSINT Tool                 ")
    print("=" * 60)
    print("\n[+] Welcome to the Instagram OSINT Tool")
    print("[+] Please enter your login credentials")
    
    # Get login information
    username = input("[?] Your Instagram username: ")
    password = getpass.getpass("[?] Your Instagram password: ")
    
    tool = InstagramOSINT()
    
    # Login
    if not tool.login(username, password):
        print("[-] Login failed. Exiting...")
        exit(1)
    
    # Get target username
    target_username = input("\n[?] Enter the target Instagram username to analyze: ")
    
    # Get profile info
    profile_info, profile = tool.get_public_profile_info(target_username)
    if not profile_info:
        print("[-] Failed to get profile information. Exiting...")
        exit(1)
    
    while True:
        choice = show_menu()
        
        if choice == '1':
            tool.download_profile_picture(profile)
        
        elif choice == '2':
            post_limit = int(input("[?] How many posts do you want to download? (default: 10): ") or "10")
            tool.download_public_posts(profile, post_limit)
        
        elif choice == '3':
            tool.download_stories(profile)
        
        elif choice == '4':
            tool.download_highlights(profile)
        
        elif choice == '5':
            post_limit = int(input("[?] How many posts do you want to analyze? (default: 10): ") or "10")
            tool.analyze_user_activity(profile, post_limit)
        
        elif choice == '6':
            print("\n[+] Exiting Instagram OSINT Tool.")
            break
        
        else:
            print("\n[-] Invalid choice. Please try again.")
    
    print("\n[+] OSINT operation completed")
    print("=" * 60)

if __name__ == "__main__":
    main()
