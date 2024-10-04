from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to allow React frontend to communicate with Flask backend

# Dummy user data for login
users = {
    'admin': 'password123',
}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if the user exists and the password matches
    if username in users and users[username] == password:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/news', methods=['GET'])
def news():
    news_data = [
        {
            "news_id": "N55528",
            "category": "lifestyle",
            "subcategory": "lifestyleroyals",
            "title": "The Brands Queen Elizabeth, Prince Charles, and Prince Philip Swear By",
            "abstract": "Shop the notebooks, jackets, and more that the royals can't live without.",
            "url": "https://assets.msn.com/labs/mind/AAGH0ET.html"
        },
        {
            "news_id": "N61837",
            "category": "news",
            "subcategory": "newsworld",
            "title": "The Cost of Trump's Aid Freeze in the Trenches of Ukraine's War",
            "abstract": "Lt. Ivan Molchanets peeked over a parapet of sand bags at the front line of the war in Ukraine. Next to him was an empty helmet propped up to trick snipers, already perforated with multiple holes.",
            "url": "https://assets.msn.com/labs/mind/AAJgNsz.html"
        },
        {
            "news_id": "N53526",
            "category": "health",
            "subcategory": "voices",
            "title": "I Was An NBA Wife. Here's How It Affected My Mental Health.",
            "abstract": "I felt like I was a fraud, and being an NBA wife didn't help that. In fact, it nearly destroyed me.",
            "url": "https://assets.msn.com/labs/mind/AACk2N6.html"
        },
        {
            "news_id": "N2073",
            "category": "sports",
            "subcategory": "football_nfl",
            "title": "Should NFL be able to fine players for criticizing officiating?",
            "abstract": "Several fines came down against NFL players for criticizing officiating this week. It's a very bad look for the league.",
            "url": "https://assets.msn.com/labs/mind/AAJ4lap.html"
        },
        {
            "news_id": "N9721",
            "category": "health",
            "subcategory": "nutrition",
            "title": "50 Foods You Should Never Eat, According to Health Experts",
            "abstract": "This is so depressing.",
            "url": "https://assets.msn.com/labs/mind/AABDHTv.html"
        },
        {
            "news_id": "N18680",
            "category": "health",
            "subcategory": "health-news",
            "title": "Michigan apple recall: Nearly 2,300 crates could be contaminated with listeria",
            "abstract": "A Michigan produce company has recalled nearly 2,300 cases of fresh apples that could be contaminated with listeria.",
            "url": "https://assets.msn.com/labs/mind/AAJwfO8.html"
        },
        {
            "news_id": "N58173",
            "category": "autos",
            "subcategory": "autossuvs",
            "title": "Is This The 2021 GMC Yukon Denali?",
            "abstract": "A Motor1.com reader sent this to us, and it sure looks legit.",
            "url": "https://assets.msn.com/labs/mind/AAGZhlc.html"
        },
        {
            "news_id": "N29120",
            "category": "sports",
            "subcategory": "football_nfl",
            "title": "John Dorsey admits talks with Washington, but it 'takes two to tango'",
            "abstract": "Team officials in Washington 'emphatically' denied a rumor of a Trent Williams trade to Cleveland, according to a report Tuesday. A day later, Browns General Manager John Dorsey admitted publicly he has talked to Washington president Bruce Allen. 'We've had a few conversations,' Dorsey said, via Mary Kay Cabot of the Cleveland Plain Dealer. 'It [more]'",
            "url": "https://assets.msn.com/labs/mind/AAISxPW.html"
        },
        {
            "news_id": "N9786",
            "category": "news",
            "subcategory": "newspolitics",
            "title": "Elijah Cummings to lie in state at US Capitol Thursday",
            "abstract": "Cummings, a Democrat whose district included sections of Baltimore, died last week at age 68 from complications related to longstanding health issues.",
            "url": "https://assets.msn.com/labs/mind/AAJgNxm.html"
        }
    ]
    return jsonify(news_data), 200


if __name__ == '__main__':
    app.run(debug=True)