import speedtest
# request kaldırıldı, Response GSC doğrulaması için eklendi.
from flask import Flask, render_template, jsonify, Response 

# Flask uygulamasını başlatma
app = Flask(__name__)

# --- GOOGLE SEARCH CONSOLE DOĞRULAMA ROTASI (Önceki doğrulama hatasını çözmek için korundu) ---
# Google, bu rotada '/google23deb7ca2e5a553c.html' dosyasını arıyor.
# Bu rota, o dosyayı sunucu kök dizininde (root directory) taklit eder.
@app.route('/google23deb7ca2e5a553c.html')
def google_verification():
    # Dosya içeriği, genellikle doğrulama dizesinin kendisidir.
    # Google'ın doğrulama dosyasını HTML olarak döndürüyoruz.
    return Response('google-site-verification: google23deb7ca2e5a553c.html', mimetype='text/html')
# -------------------------------------------------

def get_internet_speed():
    """
    Measures download, upload speed, and ping using the speedtest-cli library.
    Returns speeds in Mbps and ping in ms.
    """
    try:
        # Speedtest nesnesi oluşturma
        st = speedtest.Speedtest()
        
        # En yakın ve en iyi sunucuyu bulma (bu, testin doğruluğu için önemlidir)
        st.get_best_server()
        
        # İndirme ve yükleme hızlarını BPS cinsinden ölçme
        download_speed_bps = st.download()
        upload_speed_bps = st.upload()
        
        # Ping süresini milisaniye (ms) cinsinden alma
        ping = st.results.ping

        # Hızları daha okunaklı olan Mbps'ye (Megabits Per Second) dönüştürme ve yuvarlama
        download_speed_mbps = round(download_speed_bps / 1000000, 2)
        upload_speed_mbps = round(upload_speed_bps / 1000000, 2)
        
        # Sonuçları JSON olarak döndürmek üzere bir sözlükte toplama
        results = {
            "download": download_speed_mbps,
            "upload": upload_speed_mbps,
            "ping": round(ping, 2) # Ping'i de yuvarlıyoruz
        }
        
        return results
    
    except Exception as e:
        # Hata durumunda İngilizce hata mesajı döndürme ve loglama
        print(f"Error during speed test: {e}")
        return {"error": f"An error occurred during the speed test. Please check your connection. Details: {e}"}


# Ana sayfa: Sadece HTML şablonunu gösterir
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# Hız Testi API Endpoint'i: JavaScript tarafından POST isteğiyle çağrılır
@app.route('/run_test', methods=['POST'])
def run_test_api():
    """
    Runs the speed test via an AJAX call and returns results in JSON format.
    """
    results = get_internet_speed()
    
    # Hata kontrolü: Eğer sonuçlarda 'error' anahtarı varsa HTTP 500 hatası döndür.
    if 'error' in results:
        return jsonify(results), 500
        
    # Başarılı sonuçları Flask'in `jsonify` fonksiyonu ile JSON formatında gönderir
    return jsonify(results)


# Uygulamayı başlatma
if __name__ == '__main__':
    # Flask will automatically use the correct host/port on Render
    app.run(debug=True)
