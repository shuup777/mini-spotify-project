class LikeManager:
    def __init__(self):
        # Format: { user_id: [list artis yang disukai] }
        self.likes = {}

    def add_like(self, user_id, artist_name):
        """
        Tambahkan 'like' baru ke user.
        """
        if user_id not in self.likes:
            self.likes[user_id] = []
        if artist_name not in self.likes[user_id]:
            self.likes[user_id].append(artist_name)

    def get_liked_artists(self, user_id):
        """
        Ambil semua artis yang disukai oleh user tertentu.
        """
        return self.likes.get(user_id, [])
