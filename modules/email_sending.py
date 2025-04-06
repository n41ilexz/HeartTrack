import mailjet_rest
from dotenv import load_dotenv
import os



def send_email(anomaly):
    # Setează cheile API
    load_dotenv()
    api_key = os.getenv("MAILJET_API_KEY")
    api_secret = os.getenv("MAILJET_API_SECRET")

    # Creează o instanță a clientului Mailjet
    mj = mailjet_rest.Client(auth=(api_key, api_secret), version='v3.1')

    # Creează mesajul
    data = {
        'Messages': [
            {
                'From': {
                    'Email': 'stamatenarcis20091501@gmail.com',
                    'Name': 'HTK Companion'
                },
                'To': [
                    {
                        'Email': 'frunzamario82@gmail.com',
                        'Name': 'Frunza Mario'
                    }
                ],
                'Subject': 'HTK Companion - Alertă',
                'HTMLPart': f'<h2>{anomaly}</h2>''<h3>HTK Companion - demo</h3>''<h4>Datele sunt doar de referință, acesta este doar un demo!</h4>',
            }
        ]
    }

    # Trimite emailul
    result = mj.send.create(data=data)

    # Verifică dacă trimiterea a fost reușită
    if result.status_code == 200:
        print("Emailul a fost trimis cu succes!")
    else:
        print("A apărut o eroare:", result.status_code, result.text)

if __name__ == "__main__":
    send_email("Test")