from flask import Flask, render_template
from models.recommendation import RecommendationSystem
from models.likemanager import LikeManager

app = Flask(__name__)

like_manager = LikeManager()
recommendation_system = RecommendationSystem(like_manager)

# Data contoh
like_manager.add_like("user1", "Tulus")
like_manager.add_like("user2", "Nadin Amizah")

@app.route("/admin/recommendation")
def admin_recommendation():
    recommendations = {
        "user1": recommendation_system.get_recommendations_for_user("user1"),
        "user2": recommendation_system.get_recommendations_for_user("user2")
    }
    return render_template("recommendation_admin.html", recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)
