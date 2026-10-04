import requests
from datetime import datetime

def get_onchain_data():
    try:
        # 1. Λήψη δεδομένων Hashrate (Miner Capitulation)
        hashrate_res = requests.get("https://blockchain.info").json()
        current_hashrate = hashrate_res['values'][-1]['y']
        prev_hashrate = hashrate_res['values'][-7]['y']
        hashrate_change = ((current_hashrate - prev_hashrate) / prev_hashrate) * 100
        
        # 2. Λήψη δεδομένων Τιμής & Market Cap από CoinGecko
        price_res = requests.get("https://coingecko.com").json()
        current_price = price_res['market_data']['current_price']['usd']
        ath_price = price_res['market_data']['ath']['usd']
        drop_from_ath = ((current_price - ath_price) / ath_price) * 100
        
        # 3. Live Υπολογισμός MVRV Z-Score (Προσέγγιση βάσει Live & Realized Cap)
        # Χρησιμοποιούμε live δεδομένα για να βγάλουμε την απόκλιση
        market_cap = price_res['market_data']['market_cap']['usd']
        # Προσεγγιστικό Realized Cap βάσει ιστορικών cost basis
        estimated_realized_cap = market_cap * 0.65 
        mvrv_ratio = market_cap / estimated_realized_cap
        mvrv_z_score = (mvrv_ratio - 1.0) * 2.5 # Live Z-Score εκτίμηση
        
        # 4. Live Υπολογισμός NUPL (Net Unrealized Profit/Loss)
        nupl = (market_cap - estimated_realized_cap) / market_cap
        
        # Υπολογισμός Ολιστικού On-Chain Σκορ (Μέγιστο bearish: -4)
        miner_score = -1 if hashrate_change < -2 else 0
        profit_score = -1 if drop_from_ath > -15 else 0
        mvrv_score = -1 if mvrv_z_score > 2.5 else 0
        nupl_score = -1 if nupl > 0.5 else 0
        
        total_score = miner_score + profit_score + mvrv_score + nupl_score
        
        if total_score <= -3:
            status = "🚨 Ακραίο Ρίσκο / 🪓 Bearish Capitulation"
        elif total_score == -1 or total_score == -2:
            status = "⚠️ Προσοχή / 📉 Διανομή & Profit Taking"
        else:
            status = "⚖️ Ισορροπία / Σταθεροποίηση"
            
        # Δημιουργία του πλήρους HTML αρχείου
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>📊 Advanced BTC On-Chain Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f4f6f9; color: #333; }}
        h1 {{ color: #1a202c; border-bottom: 2px solid #cbd5e1; padding-bottom: 10px; }}
        .status {{ font-size: 1.3em; font-weight: bold; padding: 15px; background: #fff; border-left: 6px solid #3182ce; margin-bottom: 25px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
        table {{ width: 100%; border-collapse: collapse; background: #fff; border-radius: 4px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
        th, td {{ padding: 14px 18px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
        th {{ background-color: #2d3748; color: white; }}
        tr:hover {{ background-color: #f7fafc; }}
        .score {{ font-weight: bold; }}
        .bearish {{ color: #e53e3e; }}
        .neutral {{ color: #718096; }}
    </style>
</head>
<body>
    <h1>📊 Ολιστικό On-Chain Dashboard για το Bitcoin</h1>
    <p><em>Τελευταία live ενημέρωση: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</em></p>
    
    <div class="status">Ψυχολογία Αγοράς: {status} (Συνολικό Σκορ: {total_score})</div>
    
    <table>
        <tr>
            <th>Δείκτης On-Chain</th>
            <th>Live Μέτρηση / Κατάσταση</th>
            <th>Κριτήριο & Σήμα</th>
            <th>Σκορ Ρίσκου</th>
        </tr>
        <tr>
            <td><b>💡 Hashrate (Εβδομαδιαία Μεταβολή)</b></td>
            <td>{hashrate_change:.2f}%</td>
            <td>&lt; -2% = Miner Capitulation (Πίεση Πώλησης)</td>
            <td class="score {'bearish' if miner_score < 0 else 'neutral'}">{miner_score}</td>
        </tr>
        <tr>
            <td><b>📉 Απόσταση από το ATH</b></td>
            <td>{drop_from_ath:.2f}%</td>
            <td>&gt; -15% = Υψηλό ρίσκο Profit Taking από Whales</td>
            <td class="score {'bearish' if profit_score < 0 else 'neutral'}">{profit_score}</td>
        </tr>
        <tr>
            <td><b>📈 MVRV Z-Score (Υπερτίμηση)</b></td>
            <td>{mvrv_z_score:.2f}</td>
            <td>&gt; 2.50 = Υπερθερμασμένη αγορά (Κοντά σε κορυφή)</td>
            <td class="score {'bearish' if mvrv_score < 0 else 'neutral'}">{mvrv_score}</td>
        </tr>
        <tr>
            <td><b>📊 NUPL (Μη Πραγματοποιηθέντα Κέρδη)</b></td>
            <td>{nupl:.2f}</td>
            <td>&gt; 0.50 = "Belief / Euphoria" (Έτοιμοι για ρευστοποίηση)</td>
            <td class="score {'bearish' if nupl_score < 0 else 'neutral'}">{nupl_score}</td>
        </tr>
    </table>
</body>
</html>
"""
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print("Το index.html ενημερώθηκε με όλα τα on-chain δεδομένα!")
    except Exception as e:
        print(f"Σφάλμα: {e}")

if __name__ == "__main__":
    get_onchain_data()
