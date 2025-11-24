import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from duckduckgo_search import DDGS
import datetime
import os

# Load configuration
CONFIG_FILE = 'config.json'

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"Error: {CONFIG_FILE} not found.")
        return None
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def search_jobs():
    keywords = [
        "frontend", "backend", "software development", "software engineering",
        "software product", "AI engineering", "data science", "Python", "C++", "hacker"
    ]
    
    results = []
    print("Searching for jobs...")
    
    with DDGS() as ddgs:
        for keyword in keywords:
            query = f"entry level internship startup {keyword}"
            print(f"Searching for: {query}")
            try:
                # Search for recent results (past day/week if possible, but DDGS 'time' param is limited)
                # We'll just get top results for now.
                search_results = ddgs.text(query, max_results=5)
                for r in search_results:
                    # Basic extraction - Title often contains Position and Company
                    title = r.get('title', 'Unknown')
                    link = r.get('href', '#')
                    
                    # specific formatting or extraction logic could go here
                    # For now, we assume Title has "Position at Company" or similar
                    
                    results.append({
                        'keyword': keyword,
                        'title': title,
                        'link': link
                    })
            except Exception as e:
                print(f"Error searching for {keyword}: {e}")
                
    return results

def format_email_body(results):
    html = """
    <html>
    <head>
        <style>
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #f9f9f9; }
        </style>
    </head>
    <body>
        <h2>Daily Job Search Results</h2>
        <table>
            <tr>
                <th>Keyword</th>
                <th>Title (Company & Position)</th>
                <th>Link</th>
            </tr>
    """
    
    for r in results:
        html += f"""
            <tr>
                <td>{r['keyword']}</td>
                <td>{r['title']}</td>
                <td><a href="{r['link']}">Link</a></td>
            </tr>
        """
    
    html += """
        </table>
    </body>
    </html>
    """
    return html

def send_email(config, body):
    sender_email = config.get('sender_email')
    sender_password = config.get('sender_password')
    receiver_email = config.get('receiver_email')

    if not sender_email or not sender_password or not receiver_email:
        print("Error: Missing email credentials in config.")
        return

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"Job Search Results - {datetime.date.today()}"

    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def main():
    config = load_config()
    if not config:
        return

    results = search_jobs()
    if results:
        body = format_email_body(results)
        send_email(config, body)
    else:
        print("No results found.")

if __name__ == "__main__":
    main()
