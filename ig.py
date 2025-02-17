import os
import requests
import json
import time
import getpass
from datetime import datetime
import instaloader
from collections import Counter

class InstagramOSINT:
    def __init__(self):
        # Configure reasonable download options
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
        except instaloader.exceptions.BadCredentialsException:
            print(f"[-] Login failed: Incorrect username or password")
            return False
        except instaloader.exceptions.ConnectionException as e:
            print(f"[-] Login failed: Connection error - {e}")
            return False
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
        except instaloader.exceptions.ProfileNotExistsException:
            print(f"[-] Profile '{target_username}' does not exist")
            return None, None
        except instaloader.exceptions.ConnectionException as e:
            print(f"[-] Connection error while fetching profile: {e}")
            return None, None
        except Exception as e:
            print(f"[-] Failed to fetch profile information: {e}")
            return None, None
    
    def download_public_posts(self, profile, limit=10):
        """Download recent public posts (images and videos)"""
        if profile is None:
            print("[-] Invalid profile object")
            return False
            
        try:
            target_username = profile.username
            
            if profile.is_private:
                print("[-] Cannot download posts from private profile")
                return False
            
            print(f"\n[+] Downloading up to {limit} most recent posts...")
            
            # Create directory for downloads
            save_path = f"downloads/{target_username}/posts"
            os.makedirs(save_path, exist_ok=True)
            
            count = 0
            for index, post in enumerate(profile.get_posts()):
                if index >= limit:
                    break
                
                try:
                    # Download post
                    self.loader.download_post(post, target=save_path)
                    print(f"  Downloaded post from {post.date}")
                    count += 1
                except Exception as e:
                    print(f"  Failed to download post: {e}")
                
                # Respect rate limits
                time.sleep(2)
            
            if count > 0:
                print(f"[+] {count} posts saved to {save_path}")
            else:
                print(f"[-] No posts downloaded")
            return True
        
        except instaloader.exceptions.ConnectionException as e:
            print(f"[-] Connection error while downloading posts: {e}")
            return False
        except Exception as e:
            print(f"[-] Failed to download posts: {e}")
            return False
    
    def download_profile_picture(self, profile):
        """Download profile picture"""
        if profile is None:
            print("[-] Invalid profile object")
            return None
            
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
                print(f"[-] Failed to download profile picture (status code: {response.status_code})")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"[-] Network error downloading profile picture: {e}")
            return None
        except Exception as e:
            print(f"[-] Failed to download profile picture: {e}")
            return None
    
    def download_stories(self, profile):
        """Download public stories"""
        if profile is None:
            print("[-] Invalid profile object")
            return False
            
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
                # Check if any stories were downloaded
                if len(os.listdir(save_path)) > 0:
                    print(f"[+] Stories saved to {save_path}")
                    return True
                else:
                    print("[-] No stories found or available")
                    return False
            except instaloader.exceptions.LoginRequiredException:
                print("[-] Login required to download stories")
                return False
            except instaloader.exceptions.ConnectionException as e:
                print(f"[-] Connection error while downloading stories: {e}")
                return False
            except Exception as e:
                print(f"[-] Failed to download stories: {e}")
                return False
                
        except Exception as e:
            print(f"[-] Failed to download stories: {e}")
            return False
    
    def download_highlights(self, profile):
        """Download highlights"""
        if profile is None:
            print("[-] Invalid profile object")
            return False
            
        try:
            target_username = profile.username
            
            if profile.is_private and not profile.followed_by_viewer:
                print("[-] Cannot download highlights from private profile (not following)")
                return False
            
            print(f"\n[+] Attempting to download highlights for {target_username}...")
            
            # Create directory for downloads
            save_path = f"downloads/{target_username}/highlights"
            os.makedirs(save_path, exist_ok=True)
            
            count = 0
            
            try:
                # Get highlights
                highlights = self.loader.get_highlights(profile)
                
                if not highlights:
                    print("[-] No highlights found or not accessible")
                    return False
                
                for highlight in highlights:
                    highlight_dir = os.path.join(save_path, highlight.title.replace('/', '_'))
                    os.makedirs(highlight_dir, exist_ok=True)
                    
                    try:
                        print(f"  Downloading highlight: {highlight.title}")
                        items_count = 0
                        
                        # Download items in the highlight
                        for item in highlight.get_items():
                            # For each item (story) in the highlight reel
                            self.loader.download_storyitem(item, highlight_dir)
                            print(f"    Downloaded item from {item.date}")
                            count += 1
                            items_count += 1
                            # Respect rate limits
                            time.sleep(1)
                            
                        if items_count == 0:
                            print(f"    No items found in highlight '{highlight.title}'")
                            
                    except instaloader.exceptions.ConnectionException as e:
                        print(f"  Connection error downloading highlight '{highlight.title}': {e}")
                    except Exception as e:
                        print(f"  Failed to download items from highlight '{highlight.title}': {e}")
                    
                    # Respect rate limits between highlights
                    time.sleep(2)
                
                if count > 0:
                    print(f"[+] Downloaded {count} items from highlights to {save_path}")
                    return True
                else:
                    print("[-] No highlight items were downloaded")
                    return False
            
            except instaloader.exceptions.LoginRequiredException:
                print("[-] Login required to download highlights")
                return False
            except instaloader.exceptions.ConnectionException as e:
                print(f"[-] Connection error while accessing highlights: {e}")
                return False
            except Exception as e:
                print(f"[-] Error with highlights retrieval: {e}")
                return False
                
        except Exception as e:
            print(f"[-] Failed to download highlights: {e}")
            return False
    
    def analyze_user_activity(self, profile, post_limit=10):
        """Analyze posting patterns and activity"""
        if profile is None:
            print("[-] Invalid profile object")
            return None
            
        try:
            target_username = profile.username
            
            if profile.is_private:
                print("[-] Cannot analyze private profile")
                return None
            
            print("\n[+] Analyzing user activity and posting patterns...")
            
            posts_dates = []
            hashtags = Counter()
            mentioned_users = Counter()
            locations = Counter()
            
            post_count = 0
            
            for index, post in enumerate(profile.get_posts()):
                if index >= post_limit:
                    break
                
                post_count += 1
                
                # Store post date
                posts_dates.append(post.date)
                
                # Analyze hashtags - safely handle potentially None values
                try:
                    if post.caption_hashtags:
                        for hashtag in post.caption_hashtags:
                            if hashtag:  # Check if not None or empty
                                hashtags[hashtag] += 1
                except (AttributeError, TypeError):
                    print("  Warning: Could not process hashtags for a post")
                
                # Analyze mentioned users - safely handle potentially None values
                try:
                    if post.caption_mentions:
                        for user in post.caption_mentions:
                            if user:  # Check if not None or empty
                                mentioned_users[user] += 1
                except (AttributeError, TypeError):
                    print("  Warning: Could not process mentions for a post")
                
                # Analyze locations - safely handle potentially None values
                try:
                    if post.location:
                        loc_name = post.location.name if post.location and post.location.name else "Unknown"
                        locations[loc_name] += 1
                except (AttributeError, TypeError):
                    print("  Warning: Could not process location for a post")
                
                # Respect rate limits
                time.sleep(1)
                
            # Check if we found any posts
            if post_count == 0:
                print("[-] No posts found to analyze")
                return None
                
            print(f"[+] Analyzed {post_count} posts")
            
            # Analyze posting times
            day_counts = Counter()
            hour_counts = Counter()
            
            for date in posts_dates:
                if date:  # Check if date is not None
                    day_counts[date.weekday()] += 1
                    hour_counts[date.hour] += 1
            
            # Results - with safety checks
            analysis = {
                "most_active_day": max(day_counts.items(), key=lambda x: x[1])[0] if day_counts else None,
                "most_active_hour": max(hour_counts.items(), key=lambda x: x[1])[0] if hour_counts else None,
                "top_hashtags": hashtags.most_common(5),
                "top_mentioned_users": mentioned_users.most_common(5),
                "top_locations": locations.most_common(3)
            }
            
            # Convert day number to name
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            if analysis["most_active_day"] is not None:
                analysis["most_active_day"] = days[analysis["most_active_day"]]
            
            print("\n[+] Activity Analysis:")
            if analysis["most_active_day"]:
                print(f"  Most active day: {analysis['most_active_day']}")
            else:
                print("  Most active day: Not enough data")
                
            if analysis["most_active_hour"] is not None:
                print(f"  Most active hour: {analysis['most_active_hour']}:00")
            else:
                print("  Most active hour: Not enough data")
            
            if analysis['top_hashtags']:
                print("  Top hashtags:")
                for tag, count in analysis['top_hashtags']:
                    print(f"    #{tag}: {count} posts")
            else:
                print("  No hashtags found in analyzed posts")
            
            if analysis['top_mentioned_users']:
                print("  Top mentioned users:")
                for user, count in analysis['top_mentioned_users']:
                    print(f"    @{user}: {count} mentions")
            else:
                print("  No user mentions found in analyzed posts")
            
            if analysis['top_locations']:
                print("  Top locations:")
                for loc, count in analysis['top_locations']:
                    print(f"    {loc}: {count} posts")
            else:
                print("  No location data found in analyzed posts")
            
            return analysis
            
        except instaloader.exceptions.ConnectionException as e:
            print(f"[-] Connection error while analyzing user activity: {e}")
            return None
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
    
    # Create downloads directory if it doesn't exist
    os.makedirs("downloads", exist_ok=True)
    
    print("[+] Please enter your login credentials")
    
    # Get login information
    username = input("[?] Your Instagram username: ")
    password = getpass.getpass("[?] Your Instagram password: ")
    
    tool = InstagramOSINT()
    
    # Login
    login_attempts = 0
    max_attempts = 3
    
    while login_attempts < max_attempts:
        if tool.login(username, password):
            break
        login_attempts += 1
        if login_attempts < max_attempts:
            print(f"[!] Attempt {login_attempts} of {max_attempts}")
            username = input("[?] Your Instagram username: ")
            password = getpass.getpass("[?] Your Instagram password: ")
        else:
            print("[-] Maximum login attempts reached. Exiting...")
            exit(1)
    
    # Get target username
    target_username = input("\n[?] Enter the target Instagram username to analyze: ")
    
    # Get profile info with retry mechanism
    profile_info = profile = None
    attempts = 0
    max_profile_attempts = 3
    
    while attempts < max_profile_attempts and profile_info is None:
        profile_info, profile = tool.get_public_profile_info(target_username)
        if profile_info is None:
            attempts += 1
            if attempts < max_profile_attempts:
                print(f"[!] Attempt {attempts} of {max_profile_attempts}")
                target_username = input("\n[?] Enter the target Instagram username to analyze (or press Enter to exit): ")
                if not target_username:
                    print("[-] Exiting...")
                    exit(0)
            else:
                print("[-] Failed to get profile information after multiple attempts. Exiting...")
                exit(1)
    
    while True:
        choice = show_menu()
        
        if choice == '1':
            tool.download_profile_picture(profile)
        
        elif choice == '2':
            try:
                post_limit = input("[?] How many posts do you want to download? (default: 10): ")
                post_limit = int(post_limit) if post_limit else 10
                if post_limit <= 0:
                    print("[-] Number of posts must be positive. Using default of 10.")
                    post_limit = 10
                tool.download_public_posts(profile, post_limit)
            except ValueError:
                print("[-] Invalid input. Using default of 10 posts.")
                tool.download_public_posts(profile, 10)
        
        elif choice == '3':
            tool.download_stori
