import os

from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-only-change-me')


# ---------- Discover ----------

@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', active_nav='promotions', user=session.get('user'))


@app.route('/top-games')
def top_games():
    # TODO: replace with a real query against your games table
    games = [
        {'name': 'Aviator', 'provider': 'Spribe', 'initials': 'AV', 'color': '#1F3D2E', 'hot': True},
        {'name': 'JetX', 'provider': 'SmartSoft', 'initials': 'JX', 'color': '#14211B', 'hot': True},
        {'name': 'Spin Peak', 'provider': 'Summit Originals', 'initials': 'SP', 'color': '#1B1306', 'hot': False},
        {'name': 'Crash X', 'provider': 'BGaming', 'initials': 'CX', 'color': '#0F2A28', 'hot': False},
        {'name': 'Base Camp', 'provider': 'Summit Originals', 'initials': 'BC', 'color': '#1F3D2E', 'hot': False},
        {'name': 'Gold Rush', 'provider': 'Pragmatic Play', 'initials': 'GR', 'color': '#14211B', 'hot': False},
        {'name': 'Ice Peak', 'provider': 'Spribe', 'initials': 'IP', 'color': '#1B1306', 'hot': True},
        {'name': 'Wolf Gold', 'provider': 'Pragmatic Play', 'initials': 'WG', 'color': '#0F2A28', 'hot': False},
    ]
    return render_template('top_games.html', active_nav='top_games', games=games, user=session.get('user'))


@app.route('/leaderboard')
def leaderboard():
    # TODO: replace with a real query ranking players by net winnings this week
    leaders = [
        {'masked_id': '254***925', 'initials': 'JK', 'tier': 'Summit', 'amount': 184200},
        {'masked_id': '254***441', 'initials': 'MW', 'tier': 'Summit', 'amount': 152900},
        {'masked_id': '254***769', 'initials': 'AO', 'tier': 'Ridge', 'amount': 118400},
        {'masked_id': '254***908', 'initials': 'SN', 'tier': 'Ridge', 'amount': 97650},
        {'masked_id': '254***317', 'initials': 'RK', 'tier': 'Base Camp', 'amount': 74300},
        {'masked_id': '254***602', 'initials': 'PM', 'tier': 'Base Camp', 'amount': 61150},
        {'masked_id': '254***184', 'initials': 'DC', 'tier': 'Base Camp', 'amount': 48900},
    ]
    return render_template('leaderboard.html', active_nav='leaderboard', leaders=leaders, user=session.get('user'))


# ---------- Play ----------

@app.route('/crash-games')
def crash_games():
    # TODO: replace with a real query against your games table filtered to category='crash'
    games = [
        {'name': 'JetX', 'provider': 'SmartSoft', 'initials': 'JX', 'color': '#14211B', 'hot': True},
        {'name': 'Spin Peak', 'provider': 'Summit Originals', 'initials': 'SP', 'color': '#1B1306', 'hot': False},
        {'name': 'Crash X', 'provider': 'BGaming', 'initials': 'CX', 'color': '#0F2A28', 'hot': False},
        {'name': 'Base Camp', 'provider': 'Summit Originals', 'initials': 'BC', 'color': '#1F3D2E', 'hot': False},
    ]
    return render_template('crash_games.html', active_nav='crash_games', games=games, user=session.get('user'))


@app.route('/slots')
def slots():
    # TODO: replace with a real query against your games table filtered to category='slots'
    games = [
        {'name': 'Gold Rush', 'provider': 'Pragmatic Play', 'initials': 'GR', 'color': '#14211B', 'hot': True},
        {'name': 'Wolf Gold', 'provider': 'Pragmatic Play', 'initials': 'WG', 'color': '#0F2A28', 'hot': False},
        {'name': 'Sweet Bonanza', 'provider': 'Pragmatic Play', 'initials': 'SB', 'color': '#1B1306', 'hot': True},
        {'name': 'Fire Peak', 'provider': 'Summit Originals', 'initials': 'FP', 'color': '#1F3D2E', 'hot': False},
        {'name': 'Diamond Rift', 'provider': 'BGaming', 'initials': 'DR', 'color': '#14211B', 'hot': False},
        {'name': 'Book of Ridge', 'provider': 'BGaming', 'initials': 'BR', 'color': '#0F2A28', 'hot': False},
        {'name': 'Lucky Slopes', 'provider': 'Summit Originals', 'initials': 'LS', 'color': '#1B1306', 'hot': False},
        {'name': 'Sugar Rush', 'provider': 'Pragmatic Play', 'initials': 'SR', 'color': '#1F3D2E', 'hot': False},
    ]
    return render_template('slots.html', active_nav='slots', games=games, user=session.get('user'))


@app.route('/live-tables')
def live_tables():
    # TODO: replace with a real query against your live tables/dealer schedule
    tables = [
        {'name': 'Summit Blackjack', 'game_type': 'Blackjack', 'dealer': 'Naomi', 'initials': 'BJ', 'color': '#1F3D2E', 'seats_open': 3},
        {'name': 'Ridge Roulette', 'game_type': 'Roulette', 'dealer': 'Kevin', 'initials': 'RL', 'color': '#14211B', 'seats_open': 0},
        {'name': 'Base Camp Baccarat', 'game_type': 'Baccarat', 'dealer': 'Amara', 'initials': 'BC', 'color': '#1B1306', 'seats_open': 5},
        {'name': 'Peak Poker', 'game_type': 'Texas Hold\'em', 'dealer': 'Dennis', 'initials': 'PK', 'color': '#0F2A28', 'seats_open': 2},
        {'name': 'VIP Blackjack', 'game_type': 'Blackjack', 'dealer': 'Naomi', 'initials': 'VB', 'color': '#1F3D2E', 'seats_open': 1},
        {'name': 'Speed Roulette', 'game_type': 'Roulette', 'dealer': 'Kevin', 'initials': 'SR', 'color': '#14211B', 'seats_open': 6},
    ]
    return render_template('live_tables.html', active_nav='live_tables', tables=tables, user=session.get('user'))


@app.route('/sportsbook')
def sportsbook():
    # TODO: replace with a real query against your fixtures/odds provider feed
    leagues = [
        {
            'name': 'English Premier League',
            'fixtures': [
                {'home': 'Arsenal', 'away': 'Chelsea', 'kickoff': '18:30', 'live': False,
                 'odds_home': '1.85', 'odds_draw': '3.40', 'odds_away': '4.20'},
                {'home': 'Man City', 'away': 'Liverpool', 'kickoff': '21:00', 'live': False,
                 'odds_home': '2.10', 'odds_draw': '3.30', 'odds_away': '3.25'},
                {'home': 'Newcastle', 'away': 'Everton', 'kickoff': None, 'live': True, 'minute': 63,
                 'odds_home': '1.55', 'odds_draw': '4.10', 'odds_away': '5.80'},
            ],
        },
        {
            'name': 'Kenyan Premier League',
            'fixtures': [
                {'home': 'Gor Mahia', 'away': 'AFC Leopards', 'kickoff': '15:00', 'live': False,
                 'odds_home': '2.05', 'odds_draw': '3.10', 'odds_away': '3.60'},
                {'home': 'Tusker FC', 'away': 'KCB', 'kickoff': '17:00', 'live': False,
                 'odds_home': '1.70', 'odds_draw': '3.50', 'odds_away': '4.80'},
            ],
        },
    ]
    return render_template('sportsbook.html', active_nav='sportsbook', leagues=leagues, user=session.get('user'))


@app.route('/instant-win')
def instant_win():
    # TODO: replace with a real query against your instant-win games table
    cards = [
        {'name': 'Peak Scratch', 'cost': 20, 'top_prize': 50000, 'initials': 'PS', 'color': '#1F3D2E'},
        {'name': 'Gold Dust', 'cost': 50, 'top_prize': 120000, 'initials': 'GD', 'color': '#1B1306'},
        {'name': 'Ice Reveal', 'cost': 30, 'top_prize': 75000, 'initials': 'IR', 'color': '#0F2A28'},
        {'name': 'Base Camp Cash', 'cost': 10, 'top_prize': 25000, 'initials': 'BC', 'color': '#14211B'},
        {'name': 'Summit Jackpot', 'cost': 200, 'top_prize': 500000, 'initials': 'SJ', 'color': '#1F3D2E'},
        {'name': 'Quick Peak', 'cost': 15, 'top_prize': 35000, 'initials': 'QP', 'color': '#1B1306'},
    ]
    return render_template('instant_win.html', active_nav='instant_win', cards=cards, user=session.get('user'))


# ---------- Account ----------

@app.route('/wallet')
def wallet():
    # TODO: replace with a real balance lookup and transaction history query
    balance = 12480.00
    transactions = [
        {'label': 'M-Pesa deposit', 'date': 'Today, 09:14', 'method': 'M-Pesa', 'direction': 'in', 'amount': 2000},
        {'label': 'Aviator round', 'date': 'Today, 08:52', 'method': 'Wallet', 'direction': 'out', 'amount': 300},
        {'label': 'Cashback credit', 'date': 'Yesterday, 22:10', 'method': 'Wallet', 'direction': 'in', 'amount': 156},
        {'label': 'USDT withdrawal', 'date': 'Yesterday, 18:05', 'method': 'USDT (TRC20)', 'direction': 'out', 'amount': 5000},
        {'label': 'M-Pesa deposit', 'date': '2 days ago, 14:30', 'method': 'M-Pesa', 'direction': 'in', 'amount': 1000},
    ]
    return render_template('wallet.html', active_nav='wallet', balance=balance, transactions=transactions, user=session.get('user'))


@app.route('/history')
def history():
    # TODO: replace with a real query against your bets/rounds table for the logged-in user
    plays = [
        {'game': 'Aviator', 'date': 'Today, 09:41', 'stake': 300, 'result': 'win', 'amount': 840, 'initials': 'AV', 'color': '#1F3D2E'},
        {'game': 'Sweet Bonanza', 'date': 'Today, 09:20', 'stake': 50, 'result': 'loss', 'amount': 50, 'initials': 'SB', 'color': '#1B1306'},
        {'game': 'JetX', 'date': 'Yesterday, 21:12', 'stake': 200, 'result': 'loss', 'amount': 200, 'initials': 'JX', 'color': '#14211B'},
        {'game': 'Summit Blackjack', 'date': 'Yesterday, 20:04', 'stake': 500, 'result': 'win', 'amount': 950, 'initials': 'BJ', 'color': '#0F2A28'},
        {'game': 'Peak Scratch', 'date': '2 days ago, 12:15', 'stake': 20, 'result': 'win', 'amount': 100, 'initials': 'PS', 'color': '#1F3D2E'},
        {'game': 'Wolf Gold', 'date': '2 days ago, 11:50', 'stake': 100, 'result': 'loss', 'amount': 100, 'initials': 'WG', 'color': '#1B1306'},
    ]
    return render_template('history.html', active_nav='history', plays=plays, user=session.get('user'))


# ---------- Auth ----------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form.get('phone')
        password = request.form.get('password')

        # TODO: replace with a real lookup against your users table (psycopg2)
        if phone and password:
            session['user'] = {'username': phone}
            return redirect(url_for('dashboard'))

        return render_template('login.html', error='Invalid phone number or password')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        terms = request.form.get('terms')

        if not terms:
            return render_template('register.html', error='You must confirm you are 18+ and accept the terms.')
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match.')

        # TODO: replace with a real INSERT into your users table (hash the password, check for
        # existing phone number, etc.) via psycopg2
        if full_name and phone and password:
            session['user'] = {'username': phone}
            return redirect(url_for('dashboard'))

        return render_template('register.html', error='Please fill in all fields.')

    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
