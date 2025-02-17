import os
import requests
import json
import time
import getpass
from datetime import datetime
import instaloader

class InstagramOSINT:
    def __init__(self):
        self.loader = instaloader.Instaloader()
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
            
            return info
        except Exception as e:
            print(f"[-] Failed to fetch profile information: {e}")
            return None
    
    def download_public_posts(self, target_username, limit=10):
        """Download recent public posts (images and videos)"""
        try:
            profile = instaloader.Profile.from_username(self.loader.context, target_username)
            
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
                    self.loader.download_post(post, save_path)
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
    
    def download_profile_picture(self, target_username):
        """Download profile picture"""
        try:
            profile = instaloader.Profile.from_username(self.loader.context, target_username)
            
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
    
    def analyze_user_activity(self, target_username, post_limit=10):
        """Analyze posting patterns and activity"""
        try:
            profile = instaloader.Profile.from_username(self.loader.context, target_username)
            
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
                "most_active_day": max(day_counts.items(), key=lambda x: x[1])[0],
                "most_active_hour": max(hour_counts.items(), key=lambda x: x[1])[0],
                "top_hashtags": sorted(hashtags.items(), key=lambda x: x[1], reverse=True)[:5],
                "top_mentioned_users": sorted(mentioned_users.items(), key=lambda x: x[1], reverse=True)[:5],
                "top_locations": sorted(locations.items(), key=lambda x: x[1], reverse=True)[:3]
            }
            
            # Convert day number to name
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            analysis["most_active_day"] = days[analysis["most_active_day"]]
            
            print("\n[+] Activity Analysis:")
            print(f"  Most active day: {analysis['most_active_day']}")
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
    profile_info = tool.get_public_profile_info(target_username)
    if not profile_info:
        print("[-] Failed to get profile information. Exiting...")
        exit(1)
    
    # Download profile picture
    tool.download_profile_picture(target_username)
    
    # Ask about downloading posts
    download_posts = input("\n[?] Do you want to download public posts? (y/n): ").lower() == 'y'
    if download_posts:
        post_limit = int(input("[?] How many posts do you want to download? (default: 10): ") or "10")
        tool.download_public_posts(target_username, post_limit)
    
    # Ask about analyzing activity
    analyze_activity = input("\n[?] Do you want to analyze user activity? (y/n): ").lower() == 'y'
    if analyze_activity:
        post_limit = int(input("[?] How many posts do you want to analyze? (default: 10): ") or "10")
        tool.analyze_user_activity(target_username, post_limit)
    
    print("\n[+] OSINT operation completed")
    print("=" * 60)

if __name__ == "__main__":
    main()
