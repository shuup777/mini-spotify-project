# users/services.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from .models import UserProfile, FreeSubscription, ListeningHistory, UserPreferences, Notification, PlayEvent
from datetime import datetime
import time

class UserAuthenticator:
    def register(self, request, username, password, display_name):
        if User.objects.filter(username=username).exists():
            print(f"Error: Username '{username}' sudah ada.")
            return None, "Username sudah digunakan."

        print(f"\nMendaftarkan user baru: {username}...")

        # Buat user Django
        user = User.objects.create_user(username=username, password=password)
        
        # Buat profil dan data terkait
        profile = UserProfile.objects.create(user=user, display_name=display_name)
        subscription = FreeSubscription.objects.create(user=user)
        history = ListeningHistory.objects.create(user=user)
        preferences = UserPreferences.objects.create(user=user)
        
        print(f"Registrasi berhasil untuk {display_name}!")
        return user, None # Kembalikan user dan pesan error jika ada

    def login(self, request, username, password):
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(f"\nLogin berhasil! Selamat datang, {user.profile.display_name}.")
            return user
        else:
            print("\nError: Username atau password salah.")
            return None

    def logout(self, request):
        logout(request)
        print("Logout berhasil. Sesi telah diakhiri.")

# --- SERVIS UNTUK LOGIKA USER ---

class UserService:
    def play_song(self, user, song_object):
        # Asumsikan song_object adalah instance dari model Song
        print(f"\n{user.profile.display_name} memutar lagu: {song_object.title}")
        
        # Tambahkan ke history
        user.listening_history.add_event(song_object)
        
        # Cek iklan
        if not user.subscription.can_skip_ads():
            print("--- Memutar Iklan (Pengguna Gratis) ---")
            time.sleep(1) # Simulasi waktu iklan
        
        print(f"🎵 Sedang Memutar: {song_object.title}...")
        time.sleep(2) # Simulasi durasi lagu

    def like_song(self, user, song_object):
        # Misalnya, kita tambahkan lagu ke field 'liked_songs' di model User
        # (Anda perlu menambahkan ManyToManyField di model User atau buat model terpisah seperti 'LikedSong')
        # Untuk sementara, kita gunakan logika sederhana
        if song_object not in user.liked_songs.all():
            user.liked_songs.add(song_object)
            print(f"[User] {user.profile.display_name} menyukai {song_object.title}")
        else:
            print(f"[User] {user.profile.display_name} sudah menyukai {song_object.title}")

    def follow_user(self, user, user_to_follow):
        if user_to_follow not in user.following.all():
            user.following.add(user_to_follow)
            print(f"[User] {user.profile.display_name} sekarang mengikuti {user_to_follow.profile.display_name}")
        else:
            print(f"[User] {user.profile.display_name} sudah mengikuti {user_to_follow.profile.display_name}")

    def create_playlist(self, user, name):
        # Anda perlu membuat model Playlist di apps lain atau di sini
        # Misalnya, dari apps 'music' atau 'playlists'
        from music.models import Playlist # Ganti dengan app yang benar
        new_playlist = Playlist.objects.create(name=name, owner=user)
        print(f"[User] Playlist baru dibuat: {new_playlist.name}")
        return new_playlist

    def upgrade_subscription(self, user):
        from .models import PremiumSubscription
        if isinstance(user.subscription, FreeSubscription):
            # Hapus subscription lama
            user.subscription.delete()
            # Buat yang baru
            premium_sub = PremiumSubscription.objects.create(user=user)
            print("[User] Langganan telah di-upgrade ke Premium!")
        else:
            print("[User] Anda sudah menjadi pengguna Premium.")

    def get_unread_notifications(self, user):
        return user.notifications.filter(is_read=False)

    def update_profile(self, user, new_name=None, new_bio=None):
        user.profile.update_profile(new_name=new_name, new_bio=new_bio)

    def update_preferences(self, user, new_theme=None, new_quality=None):
        user.preferences.update_settings(theme=new_theme, audio_quality=new_quality)

