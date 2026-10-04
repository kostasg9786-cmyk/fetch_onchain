import requests
import json
import os
from datetime import datetime

def get_onchain_data():
    try:
        # 1. Λήψη δεδομένων Hashrate & Δυσκολίας (Miner Capitulation)
        hashrate_res = requests.get("https://blockchain.info").json()
        current_hashrate = hashrate_res['values'][-1]['y']
        prev_hashrate = hashrate_res['values'][-7]['y']
        hashrate_change = ((current_hashrate - prev_hashrate) / prev_hashrate) * 100
        
        # 2. Λήψη δεδομένων Τιμής & Market Cap
        price_res = requests.get("https://coingecko.com").json()
        current_price = price_res['market_data']['current_price']['usd']
        ath_price = price_res['market_data']['ath']['usd']
        drop_from_ath = ((current_price - ath_price) / ath_price) * 100
        
        # Υπολογισμός On-Chain Σκορ
        miner_score = -1 if hashrate_change < -2 else 0
        profit_score = -1 if drop_from_ath > -15 else 0
        
        total_score = miner_score + profit_score
        status = "Διόρθωση / 🪓 Capitulation" if total_score <= -1 else "Σταθεροποίηση / ⚖️ Ισορροπία"
        
        # Δημιουργία του Markdown Πίνακα
        markdown_content = f"""# 📊 Ολιστικός Πίνακας On-Chain Δεδομένων BTC
*Τελευταία ενημέρωση: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*

### 🚨 Κατάσταση On-Chain Ψυχολογίας: `{status}` (Σκορ: {total_score})

| Δείκτης On-Chain | Τρέχουσα Τιμή / Κατάσταση | Κανόνας & Σήμα | Σκορ |
| :--- | :--- | :--- | :--- |
| **💡 Hashrate (Εβδομαδιαία Μεταβολή)** | {hashrate_change:.2f}% | < -2% = Miner Capitulation | **{miner_score}** |
| **📉 Απόσταση από το ATH (Profit Taking Risk)** | {drop_from_ath:.2f}% | > -15% = Υψηλό ρίσκο ρευστοποιήσεων | **{profit_score}** |
| **🐋 Whales Exchange Inflow (Εκτίμηση)** | ⏳ Αναμονή Ροών | 📈 > 85% = Whales πουλάνε στα ανταλλακτήρια | **0** |

### 💡 Συμπέρασμα για την Ανάλυσή σου:
"""
        if total_score <= -1:
            markdown_content += "Οι on-chain δείκτες **τεκμηριώνουν την Bearish άποψή σου**. Υπάρχει είτε κόπωση/συνθηκολόγηση των Miners είτε αυξημένο ρίσκο profit taking επειδή η τιμή είναι ψηλά. Τα ράλι είναι για σορτάρισμα.\n"
        else:
            markdown_content += "Η αγορά βρίσκεται σε ισορροπία. Οι Miners κρατάνε τις θέσεις τους και δεν παρατηρείται ακόμη πανικός ή μαζικό de-risking.\n"
            
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(markdown_content)
            
        print("Το README.md ενημερώθηκε επιτυχώς!")
    except Exception as e:
        print(f"Σφάλμα κατά τη λήψη των δεδομένων: {e}")

if __name__ == "__main__":
    get_onchain_data()
