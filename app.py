import os

from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-only-change-me')

# ---------- Master games catalog ----------
# TODO: replace with a real query against your games table. This is the single
# source of truth for every game card across Top games / Slots / Crash games.
# NOTE: these are real industry game titles used here purely as display names for
# our own decorative demo pages — no actual provider integration is wired up.
# 'image' points to static/img/games/<file> — original illustrated placeholder art
# (not real provider assets). Templates fall back to the colored 'initials' box
# via onerror if the file is missing.
GAMES = [
    {'slug': 'aviator', 'name': 'Aviator', 'provider': 'Spribe', 'initials': 'AV', 'color': '#1F3D2E', 'category': 'crash', 'hot': True, 'image': 'aviator.png'},
    {'slug': 'jetx', 'name': 'JetX', 'provider': 'SmartSoft Gaming', 'initials': 'JX', 'color': '#14211B', 'category': 'crash', 'hot': True, 'image': 'jetx.png'},
    {'slug': 'plinko', 'name': 'Plinko', 'provider': 'Spribe', 'initials': 'PL', 'color': '#1B1306', 'category': 'crash', 'hot': False, 'image': 'plinko.png'},
    {'slug': 'mines', 'name': 'Mines', 'provider': 'Spribe', 'initials': 'MN', 'color': '#0F2A28', 'category': 'crash', 'hot': False, 'image': 'mines.png'},
    {'slug': 'chicken-road', 'name': 'Chicken Road', 'provider': 'InOut Games', 'initials': 'CR', 'color': '#1F3D2E', 'category': 'crash', 'hot': False, 'image': 'chicken-road.png'},
    {'slug': 'dragon-tower', 'name': 'Dragon Tower', 'provider': 'Gamzix', 'initials': 'DT', 'color': '#1B1306', 'category': 'crash', 'hot': True, 'image': 'dragon-tower.png'},
    {'slug': 'sweet-bonanza', 'name': 'Sweet Bonanza', 'provider': 'Pragmatic Play', 'initials': 'SB', 'color': '#1B1306', 'category': 'slot', 'hot': True, 'image': 'sweet-bonanza.png'},
    {'slug': 'wolf-gold', 'name': 'Wolf Gold', 'provider': 'Pragmatic Play', 'initials': 'WG', 'color': '#0F2A28', 'category': 'slot', 'hot': False, 'image': 'wolf-gold.png'},
    {'slug': 'sugar-rush', 'name': 'Sugar Rush', 'provider': 'Pragmatic Play', 'initials': 'SR', 'color': '#1F3D2E', 'category': 'slot', 'hot': False, 'image': 'sugar-rush.png'},
    {'slug': 'big-bass-bonanza', 'name': 'Big Bass Bonanza', 'provider': 'Pragmatic Play', 'initials': 'BB', 'color': '#14211B', 'category': 'slot', 'hot': True, 'image': 'big-bass-bonanza.png'},
    {'slug': 'gates-of-olympus', 'name': 'Gates of Olympus', 'provider': 'Pragmatic Play', 'initials': 'GO', 'color': '#1B1306', 'category': 'slot', 'hot': True, 'image': 'gates-of-olympus.png'},
    {'slug': 'fortune-tiger', 'name': 'Fortune Tiger', 'provider': 'PG Soft', 'initials': 'FT', 'color': '#0F2A28', 'category': 'slot', 'hot': False, 'image': 'fortune-tiger.png'},
    {'slug': 'book-of-dead', 'name': 'Book of Dead', 'provider': "Play'n GO", 'initials': 'BD', 'color': '#1F3D2E', 'category': 'slot', 'hot': False, 'image': 'book-of-dead.png'},
    {'slug': 'money-train-3', 'name': 'Money Train 3', 'provider': 'Relax Gaming', 'initials': 'MT', 'color': '#14211B', 'category': 'slot', 'hot': False, 'image': 'money-train-3.png'},

    # ---- newer additions ----
    {'slug': 'aero', 'name': 'Aero', 'provider': 'Onlyplay', 'initials': 'AE', 'color': '#3a1414', 'category': 'crash', 'hot': False, 'image': 'aero.png'},
    {'slug': 'avrika', 'name': 'Avrika', 'provider': 'Onlyplay', 'initials': 'AV', 'color': '#160505', 'category': 'crash', 'hot': False, 'image': 'avrika.png'},
    {'slug': 'chicken-panic', 'name': 'Chicken Panic', 'provider': 'InOut Games', 'initials': 'CP', 'color': '#2a1c0a', 'category': 'crash', 'hot': False, 'image': 'chicken-panic.png'},
    {'slug': 'aviabet', 'name': 'AviaBet', 'provider': 'BGaming', 'initials': 'AB', 'color': '#3a0d24', 'category': 'crash', 'hot': False, 'image': 'aviabet.png'},
    {'slug': 'crossfire-chicken', 'name': 'Crossfire Chicken', 'provider': 'InOut Games', 'initials': 'CF', 'color': '#2a0a0a', 'category': 'crash', 'hot': True, 'image': 'crossfire-chicken.png'},
    {'slug': 'aviatrix', 'name': 'Aviatrix', 'provider': 'Aviatrix Gaming', 'initials': 'AX', 'color': '#0a1830', 'category': 'crash', 'hot': True, 'image': 'aviatrix.png'},
    {'slug': 'crashx', 'name': 'CrashX', 'provider': 'BGaming', 'initials': 'CX', 'color': '#1c0505', 'category': 'crash', 'hot': False, 'image': 'crashx.png'},
    {'slug': 'goalx', 'name': 'GoalX', 'provider': 'Onlyplay', 'initials': 'GX', 'color': '#0a2a12', 'category': 'crash', 'hot': False, 'image': 'goalx.png'},
    {'slug': 'tajiri-fruits', 'name': 'Tajiri Fruits', 'provider': 'Summit Originals', 'initials': 'TF', 'color': '#3a1a06', 'category': 'slot', 'hot': False, 'image': 'tajiri-fruits.png'},
    {'slug': 'fruit-mania', 'name': 'Fruit Mania', 'provider': 'Booongo', 'initials': 'FM', 'color': '#141033', 'category': 'slot', 'hot': False, 'image': 'fruit-mania.png'},
    {'slug': 'regal-fruits', 'name': 'Regal Fruits 1000', 'provider': 'Booongo', 'initials': 'RF', 'color': '#2a1040', 'category': 'slot', 'hot': False, 'image': 'regal-fruits.png'},
    {'slug': 'hot-hot-fruit', 'name': 'Hot Hot Fruit', 'provider': "Play'n GO", 'initials': 'HF', 'color': '#3a0a0a', 'category': 'slot', 'hot': True, 'image': 'hot-hot-fruit.png'},
    {'slug': 'aztec-gems', 'name': 'Aztec Gems', 'provider': 'Pragmatic Play', 'initials': 'AG', 'color': '#062a2a', 'category': 'slot', 'hot': False, 'image': 'aztec-gems.png'},
    {'slug': 'mayan-gold', 'name': 'Mayan Gold', 'provider': 'BGaming', 'initials': 'MG', 'color': '#241804', 'category': 'slot', 'hot': True, 'image': 'mayan-gold.png'},
    {'slug': 'gold-888', 'name': '888 Gold', 'provider': "Play'n GO", 'initials': '888', 'color': '#2a0505', 'category': 'slot', 'hot': False, 'image': 'gold-888.png'},
    {'slug': 'fire-strike', 'name': 'Fire Strike', 'provider': 'Pragmatic Play', 'initials': 'FS', 'color': '#2a0808', 'category': 'slot', 'hot': False, 'image': 'fire-strike.png'},
]


# ---------- Discover ----------

@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', active_nav='promotions', user=session.get('user'))


@app.route('/top-games')
def top_games():
    return render_template('top_games.html', active_nav='top_games', games=GAMES, user=session.get('user'))


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
    games = [g for g in GAMES if g['category'] == 'crash']
    return render_template('crash_games.html', active_nav='crash_games', games=games, user=session.get('user'))


@app.route('/slots')
def slots():
    games = [g for g in GAMES if g['category'] == 'slot']
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


@app.route('/game/<slug>')
def game_detail(slug):
    game = next((g for g in GAMES if g['slug'] == slug), None)
    if not game:
        return render_template('404.html', active_nav=None, user=session.get('user')), 404
    return render_template('game_detail.html', active_nav=game['category'] + '_games' if game['category'] == 'crash' else 'slots',
                            game=game, user=session.get('user'))


@app.route('/wallet/deposit', methods=['POST'])
def wallet_deposit():
    # PLACEHOLDER ONLY — no payment gateway is wired up yet.
    # A real implementation needs, at minimum:
    #   - M-Pesa: Safaricom Daraja STK Push API call, then a callback endpoint
    #     that verifies the payment and credits the wallet server-side
    #   - USDT: a per-user deposit address + blockchain confirmation listener
    #   - Bank: reconciliation against your bank's transaction feed
    # None of that exists here. This just confirms the form submitted correctly.
    method = request.form.get('method', 'mpesa')
    flash(f'Deposit request received via {method.upper()}. Payment processing is not yet connected.', 'success')
    return redirect(url_for('wallet'))


@app.route('/wallet/withdraw', methods=['POST'])
def wallet_withdraw():
    # PLACEHOLDER ONLY — same caveat as wallet_deposit(). A real withdrawal flow
    # needs server-side balance verification, fraud/AML checks, and an actual
    # payout call (Daraja B2C for M-Pesa, a signed on-chain transfer for USDT)
    # before the wallet balance is ever decremented.
    method = request.form.get('method', 'mpesa')
    flash(f'Withdrawal request received via {method.upper()}. Payout processing is not yet connected.', 'success')
    return redirect(url_for('wallet'))


# Add near the top of app.py, alongside other imports:
#
#   from games_provider import launch_game, ProviderNotConfigured, ProviderError
#
# Add this route anywhere alongside game_detail():

@app.route('/game/<slug>/play')
def game_play(slug):
    game = next((g for g in GAMES if g['slug'] == slug), None)
    if not game:
        return render_template('404.html', active_nav=None, user=session.get('user')), 404

    if not session.get('user'):
        flash('Please log in to play.', 'error')
        return redirect(url_for('login'))

    player_id = session['user']['username']  # TODO: swap for your real internal player id once auth is real

    try:
        result = launch_game(
            slug=slug,
            player_id=player_id,
            player_currency='KES',
            return_url=url_for('wallet', _external=True),
        )
    except ProviderNotConfigured:
        # Not wired up yet — fall back to the existing decorative demo page
        # instead of a broken/blank screen.
        flash('Live game session isn\'t connected yet — showing the demo version.', 'success')
        return redirect(url_for('game_detail', slug=slug))
    except ProviderError as e:
        flash(f'Could not start the game right now ({e}). Please try again shortly.', 'error')
        return redirect(url_for('game_detail', slug=slug))

    return render_template(
        'game_play.html',
        active_nav=game['category'] + '_games' if game['category'] == 'crash' else 'slots',
        game=game,
        game_url=result['game_url'],
        user=session.get('user'),
    )


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html', active_nav=None, user=session.get('user')), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html', active_nav=None, user=session.get('user')), 500


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # PLACEHOLDER ONLY — replace with a real check against an admin users table
        # (hashed passwords, role column, ideally 2FA given this exposes financial data).
        # This currently accepts ANY non-empty username/password. Do not deploy as-is.
        if username and password:
            session['admin_user'] = username
            return redirect(url_for('admin_dashboard'))

        return render_template('admin_login.html', error='Enter a username and password.')

    return render_template('admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_user', None)
    return redirect(url_for('admin_login'))


@app.route('/admin')
def admin_dashboard():
    if not session.get('admin_user'):
        return redirect(url_for('admin_login'))

    # TODO: replace all of the below with real aggregate queries against your
    # users/transactions/bets tables (scoped to admin/staff roles only).
    kpis = {
        'active_users': '3,204',
        'active_users_delta': 4.2,
        'deposits_today': 482110,
        'deposits_delta': 8.6,
        'withdrawals_today': 310450,
        'withdrawals_delta': 2.1,
        'net_ggr': 171660,
        'ggr_delta': 12.4,
    }
    deposits_chart = [
        {'label': 'Mon', 'pct': 55}, {'label': 'Tue', 'pct': 68}, {'label': 'Wed', 'pct': 42},
        {'label': 'Thu', 'pct': 74}, {'label': 'Fri', 'pct': 88}, {'label': 'Sat', 'pct': 95},
        {'label': 'Sun', 'pct': 100},
    ]
    recent_transactions = [
        {'user': '254***925', 'type': 'Deposit', 'method': 'M-Pesa', 'amount': 2000, 'status': 'complete', 'time': '09:14'},
        {'user': '254***441', 'type': 'Withdrawal', 'method': 'USDT', 'amount': 5000, 'status': 'pending', 'time': '08:52'},
        {'user': '254***769', 'type': 'Deposit', 'method': 'M-Pesa', 'amount': 500, 'status': 'complete', 'time': '08:40'},
        {'user': '254***908', 'type': 'Withdrawal', 'method': 'M-Pesa', 'amount': 1200, 'status': 'failed', 'time': '08:15'},
        {'user': '254***317', 'type': 'Deposit', 'method': 'Bank', 'amount': 10000, 'status': 'pending', 'time': '07:58'},
    ]

    return render_template(
        'admin_dashboard.html',
        active_nav='overview',
        admin_user=session.get('admin_user'),
        kpis=kpis,
        deposits_chart=deposits_chart,
        recent_transactions=recent_transactions,
    )


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
