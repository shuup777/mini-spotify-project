class RecommendationSystem:
    def __init__(self, like_manager):
        self.like_manager = like_manager

    def get_recommendations_for_user(self, user_id):
        """
        Menghasilkan daftar artis yang direkomendasikan untuk user.
        (simulasi sederhana berdasarkan data 'like')
        """
        liked_artists = self.like_manager.get_liked_artists(user_id)

        # Jika user belum pernah like, tampilkan rekomendasi umum
        if not liked_artists:
            return ["Artis Populer 1", "Artis Populer 2", "Artis Populer 3"]

        # Simulasi: rekomendasi artis mirip (nama beda dikit aja)
        recommendations = [f"{artist} (Rekomendasi Serupa)" for artist in liked_artists]
        return recommendations
