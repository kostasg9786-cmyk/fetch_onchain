import requests
from datetime import datetime

def get_onchain_data():
    try:
        # 1. Λήψη δεδομένων Hashrate
        hashrate_res = requests.get("https://blockchain.info").json()
        current_hashrate = hashrate_res['values'][-1]['y']
        prev_hashrate = hashrate_res['values'][-7]['y']
        hashrate_change = ((current_hashrate - prev_hashrate) / prev_hashrate) * 100
        
        # 2. Λήψη δεδομένων Τιμής από CoinGecko
        price_res = requests.get("https://coingecko.com").json()
        current_price = price_res['market_data']['current_price']['usd']
        ath_price = price_res['market_data']['ath']['usd']
        drop_from_ath = ((current_price - ath_price) / ath_price) * 100
        
        # Υπολογισμός On-Chain Σκορ
        miner_score = -1 if hashrate_change < -2 else 0
        profit_score = -1 if drop_from_ath > -15 else 0
        total_score = miner_score + profit_score
        status = "Διόρθωση / 🪓 Capitulation" if total_score <= -1 else "Σταθεροποίηση / ⚖️ Ισορροπία"
        
        # Δημιουργία του HTML αρχείου για την ιστοσελίδα
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>📊 BTC On-Chain Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f4f6f9; color: #333; }}
        h1 {{ color: #1a202c; }}
        .status {{ font-size: 1.2em; font-weight: bold; padding: 10px; background: #fff; border-left: 5px solid #e53e3e; margin-bottom: 20px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; background: #fff; border-radius: 4px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
        th {{ background-color: #4a5568; color: white; }}
        tr:hover {{ background-color: #f7fafc; }}
        .score {{ font-weight: bold; color: #e53e3e; }}
    </style>
</head>
<body>
    <h1>📊 Ολιστικός Πίνακας On-Chain Δεδομένων BTC</h1>
    <p><em>Τελευταία ενημέρωση: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</em></p>
    
    <div class="status">🚨 Κατάσταση On-Chain Ψυχολογίας: {status} (Σκορ: {total_score})</div>
    
    <table>
        <tr>
            <th>Δείκτης On-Chain</th>
            <th>Τρέχουσα Τιμή / Κατάσταση</th>
            <th>Κανόνας & Σήμα</th>
            <th>Σκορ</th>
        </tr>
        <tr>
            <td><b>💡 Hashrate (Εβδομαδιαία Μεταβολή)</b></td>
            <td>{hashrate_change:.2f}%</td>
            <td>&lt; -2% = Miner Capitulation</td>
            <td class="score">{miner_score}</td>
        </tr>
        <tr>
            <td><b>📉 Απόσταση από το ATH (Profit Taking Risk)</b></td>
            <td>{drop_from_ath:.2f}%</td>
            <td>&gt; -15% = Υψηλό ρίσκο ρευστοποιήσεων</td>
            <td class="score">{profit_score}</td>
        </tr>
    </table>
</body>
</html>
"""
        # Εγγραφή απευθείας στο index.html
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print("Το index.html ενημερώθηκε επιτυχώς!")
    except Exception as e:
        print(f"Σφάλμα: {e}")

if __name__ == "__main__":
    get_onchain_data()
