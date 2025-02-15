from tkinter import messagebox
import customtkinter as ctk
import random
import json

"""
    Bu program, İngilizce kelimeleri öğrenmek ve anlamlarını kontrol etmek için tasarlanmıştır.
    Yeni kelimeler ekleyebilir, rastgele sorular sorarak öğrendiklerinizi test edebilirsiniz.
    
    Eklediğiniz kelimenin diğer anlamlarını ve doğru okunuşunu öğrenmek için Tureng gibi web tabanlı bir sözlükten faydalanabilirsiniz.
    
    Alternatif olarak, yapay zeka desteği ile kelimenin doğru okunuşunu öğrenebilir ve ekleyebilirsiniz.
"""

# Kelime veritabanı dosyası
KELIME_DOSYASI = "kelimeler.txt"  # dosyanın adını değiştirebilirsiniz.

# Kelimeleri yükleme fonksiyonu
def kelimeleri_yukle():
    """
    Kelime veritabanını dosyadan yükler.
    Eğer dosya yoksa veya bozuksa kullanıcıya bilgi verir ve boş bir veritabanı döner
    """
    try:
        with open(KELIME_DOSYASI, "r", encoding="utf-8") as dosya:
            return json.load(dosya)
    except FileNotFoundError:
        messagebox.showwarning("Uyarı", "Kelime veritabanı bulunamadı, yeni bir veritabanı oluşturulacak.")
        return {}
    except json.JSONDecodeError:
        messagebox.showerror("Hata", "Veritabanı bozuk. Yeni bir veritabanı oluşturulacak")
        return {}

# Kelimeleri kaydetme fonksiyonu
def kelimeleri_kaydet():
    """
    Kelime veritabanını dosyaya yazar.
    """
    with open(KELIME_DOSYASI, "w", encoding="utf-8") as dosya:
        json.dump(kelimeler, dosya, ensure_ascii=False, indent=4)

# Kelime veritabanını yükle
kelimeler = kelimeleri_yukle()

# Yeni kelime ekleme kısmını göster/gizle
def toggle_kelime_ekle():
    """
    Kelime ekleme çerçevesini açar/kapatır.
    """
    if ekleme_cercevesi.winfo_ismapped():
        ekleme_cercevesi.pack_forget()
    else:
        ekleme_cercevesi.pack(after = kelime_ekle_butonu, pady=20)

# Yeni kelime ekleme fonksiyonu
def kelime_ekle():
    """
    Kullanıcıdan alınan yeni kelimeyi veritabanına ekler ve dosyaya kaydeder.
    Tüm alanlar doldurulmamışsa hata mesajı gösterir.
    """
    ingilizce = ing_kutusu.get().strip()
    turkce = tur_kutusu.get().strip()
    okunus = ok_kutusu.get().strip()

    if ingilizce and turkce and okunus:
        kelimeler[ingilizce] = {"turkce": turkce, "okunus": okunus}
        kelimeleri_kaydet()
        messagebox.showinfo("Başarılı", "Kelime başarıyla eklendi!")
        ing_kutusu.delete(0, ctk.END)
        tur_kutusu.delete(0, ctk.END)
        ok_kutusu.delete(0, ctk.END)
    else:
        messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")

def toggle_kelime_sil():
    """
    Kelime sil çerçevesini açar/kapatır.
    """
    if sil_cercevesi.winfo_ismapped():
        sil_cercevesi.pack_forget()
    else:
        sil_cercevesi.pack(pady=20)

def kelime_sil():
    """
    Kullanıcıdan alınan ingilizce kelimeyi siler ve veritabanını günceller.
    """

    kelime = sil_kutusu.get().strip()
    if kelime in kelimeler:
        del kelimeler[kelime]
        kelimeleri_kaydet()
        messagebox.showinfo("Başarılı", f"'{kelime}' kelimesi başarıyla silindi!")
        sil_kutusu.delete(0, ctk.END)
        kelime_listesi_goster()
    else:
        messagebox.showerror("Hata", f"'{kelime}' kelimesi Bulunamadı!")

def all_destroy():
    """
    txt dosyasındaki tüm kelimeleri siler.
    """
    if not kelimeler:
        messagebox.showinfo("Bilgi", "Kelime veritabanı zaten boş")
        return
    
    cevap = messagebox.askyesno("Onay", "Tüm kelimeleri silmek istediğinize emin misiniz?")
    if cevap:
        kelimeler.clear() #Tüm kelimeleri siler
        kelimeleri_kaydet()
        messagebox.showinfo("Başarılı", "Tüm kelimeler başarıyla silindi!")
        


def kelime_listesi_goster():
    """
    Mevcut kelimeleri bir liste olarak kullanıcıya gösterir.
    """

    if not kelimeler:
        messagebox.showinfo("Bilgi", "Kelime listesi boş!")
        return

    liste_penceresi = ctk.CTkToplevel()
    liste_penceresi.title("Kelime Listesi")
    liste_penceresi.geometry("600x650")

    # Pencereyi ön plana çıkarır
    liste_penceresi.attributes("-topmost", True)

    liste_penceresi.configure(fg_color="gray20")

    # Arama çerçevesi
    arama_frame = ctk.CTkFrame(liste_penceresi, fg_color="gray25")
    arama_frame.pack(fill="x", padx=10, pady=5)

    arama_entry = ctk.CTkEntry(arama_frame, placeholder_text="Kelimeyi ara...")
    arama_entry.pack(fill="x", padx=5, pady=5)

    canvas = ctk.CTkCanvas(liste_penceresi, bg="gray20", highlightthickness=0)
    scrollbar = ctk.CTkScrollbar(liste_penceresi, command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    scrollable_frame = ctk.CTkFrame(canvas, fg_color="gray20")

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)

    kelime_label_list = []

    def listeyi_guncelle():
        """Aramaya bağlı olarak listeyi günceller"""
        for label in kelime_label_list:
            label.destroy()
        kelime_label_list.clear()

        arama_metini = arama_entry.get().lower()

        for i, (ingilizce, veri) in enumerate(kelimeler.items(), start=1):
            turkce = veri["turkce"]
            okunus = veri["okunus"]
            kelime_metni = f"{i}) {ingilizce} ({okunus}) = {turkce}"

            # Girilmiş olan değere göre filtreler
            if arama_metini in ingilizce.lower() or arama_metini in turkce.lower() or arama_metini in okunus.lower():
                label = ctk.CTkLabel(scrollable_frame,
                        text=kelime_metni, 
                        font=("Arial", 14),
                        text_color="white",
                        fg_color="gray20",
                        wraplength=500)
                label.pack(anchor="w", padx=10, pady=5)
                kelime_label_list.append(label)

        update_scrollregion()

    # Arama kutusuna yazıldıkça filtreler
    arama_entry.bind("<KeyRelease>", lambda event: listeyi_guncelle())

    # Scroll bölgesini güncelleyen fonksiyon
    def update_scrollregion():
        liste_penceresi.update_idletasks()
        bbox = canvas.bbox("all")
        if bbox:
            canvas.config(scrollregion=bbox)

            # Eğer içerik yeterli değilse kaydırma çubuğunu gizle
            if bbox[3] > liste_penceresi.winfo_height():
                scrollbar.pack(side="right", fill="y")
            else:
                scrollbar.pack_forget()

    def mouse_wheel(event):
        if canvas.bbox("all")[3] > liste_penceresi.winfo_height():
            canvas.yview_scroll(-1 * (event.delta // 60), "units")

    # Fare tekerleği olayını bağla
    canvas.bind_all("<MouseWheel>", mouse_wheel)

    # İlk açılışta listeyi doldurur
    listeyi_guncelle()

    liste_penceresi.after(100, lambda: liste_penceresi.attributes("-topmost", True))

    

# Widget oluşturmayı basitleştiren fonksiyonlar
# Bir metin girişi(Entry) widget'ı oluşturur.
def create_entry(parent, font=("Arial", 15), placeholder_text="", width=250, height=40):
    entry = ctk.CTkEntry(parent, font=font, placeholder_text=placeholder_text, width=width, height=height)
    entry.pack(pady=5)
    return entry

# Bir Button widget'ı oluşturur.
def create_button(parent, text, font=("Arial", 14), fg_color="0078D4", text_color="white", command=None):
    button = ctk.CTkButton(parent, text=text, font=font, fg_color=fg_color, text_color=text_color, command=command)
    button.pack(pady=8)
    return button

# Bir Label widget'ı oluşturur.
def create_label(parent, text, font=("Arial", 12), bg="#f9f9f9"):
    label = ctk.CTkLabel(parent, text=text, font=font, text_color=bg)
    label.pack()
    return label


# Rastgele soru sorma fonksiyonu
def soru_sor():
    """
    Veritabanından rastgele bir kelime seçer ve kullanıcıya sorar.
    Kullanıcı doğru cevap verirse bir sonraki soruya geçilir.
    Yanlış cevap verirse doğru cevap gösterilir.
    """
    if not kelimeler:
        messagebox.showerror("Hata", "Kelime havuzu boş! Önce kelime ekleyin.")
        return

    ingilizce, veri = random.choice(list(kelimeler.items()))
    turkce = veri["turkce"]
    okunus = veri["okunus"]

    def cevabi_kontrol_et(event=None):
        """
        Kullanıcının cevabını kontrol eder ve doğru/yanlış durumunu bildirir.
        """
        cevap = cevap_kutusu.get().strip()
        if cevap.lower() == turkce.lower():
            messagebox.showinfo("Doğru!", "Cevabınız doğru!")
            cevap_kutusu.delete(0, ctk.END)
            soru_sor() # Yeni soruaya geçer
        else:
            messagebox.showerror("Yanlış!", f"Yanlış cevap. Doğru cevap: {turkce}")
            cevap_kutusu.delete(0, ctk.END)

    # Soru ekranını temizle ve yeniden oluştur
    for widget in soru_cercevesi.winfo_children():
        widget.destroy()

    create_label(soru_cercevesi, f" '{ingilizce} ({okunus})' kelimesinin Türkçesi nedir? ", font=("Arial", 20)).pack(pady=10)

    global cevap_kutusu
    cevap_kutusu = create_entry(soru_cercevesi)

    # Cevabı kontrol etme butonu
    create_button(soru_cercevesi, "Cevabı Kontrol Et", fg_color="#0078D4", text_color="black", command=cevabi_kontrol_et)

    # Enter tuşuna bastığımızda cevabı kontrol eder.
    cevap_kutusu.bind("<Return>", cevabi_kontrol_et)

# Ana pencere
def main():
    """
    Uygulamanın ana ekranını oluşturur ve çalıştırır.
    """
    global kelimeler, ekleme_cercevesi, soru_cercevesi, ing_kutusu, tur_kutusu, ok_kutusu
    global sil_cercevesi, sil_kutusu, kelime_ekle_butonu
    ctk.set_appearance_mode("black")
    root = ctk.CTk()
    root.title("İngilizce Kelime Çalışma")
    root.geometry("800x800")

    left_frame = ctk.CTkFrame(root, width=400)
    left_frame.pack(side="left", fill="both", expand=True)

    right_frame = ctk.CTkFrame(root, width=400)
    right_frame.pack(side="right", fill="both", expand=True)
    
    # Soru sorma kısmı
    soru_cercevesi = ctk.CTkFrame(left_frame)
    soru_cercevesi.pack(pady=20)

    # Soru sorma butonu
    create_button(left_frame, "Soru Sor", fg_color="#ffc107", text_color="black", command=soru_sor)

    # Kelime Listesini gösterme butonu
    create_button(right_frame, "Kelime Listesini Göster", fg_color="#17a2b8", text_color="black", command=kelime_listesi_goster)

    # Yeni kelime ekleme butonu
    kelime_ekle_butonu = create_button(right_frame, "Yeni Kelime Ekle", fg_color="#28a745", text_color="black", command=toggle_kelime_ekle)

    # Kelime ekleme çerçevesi
    ekleme_cercevesi = ctk.CTkFrame(right_frame)

    create_label(ekleme_cercevesi, "\nYeni Kelime Ekle\n", font=("Arial", 20), bg="#28a745")

    create_label(ekleme_cercevesi, "İngilizce:")
    ing_kutusu = create_entry(ekleme_cercevesi, placeholder_text="İngilizce kelimeyi giriniz")

    create_label(ekleme_cercevesi, "Türkçe:")
    tur_kutusu = create_entry(ekleme_cercevesi, placeholder_text="Türkçe okunuşunu giriniz")

    create_label(ekleme_cercevesi, "Okunuşu:")
    ok_kutusu = create_entry(ekleme_cercevesi, placeholder_text="Okunuşunu giriniz")

    # Kelimeyi ekleme Butonu
    create_button(ekleme_cercevesi, "Kelimeyi Ekle", fg_color="#0078D4", text_color="black", command=kelime_ekle)

    create_button(right_frame, "Kelime Sil", fg_color="#dc3545", text_color="black", command=toggle_kelime_sil)

    # Kelime silme kısmı
    sil_cercevesi = ctk.CTkFrame(right_frame)

    create_label(sil_cercevesi, "\nKelime Sil\n", font=("Arial", 20), bg="#dc3545")
    sil_kutusu = create_entry(sil_cercevesi, placeholder_text="İngilizce kelime giriniz")

    create_button(sil_cercevesi, "Kelimeyi Sil", fg_color="#dc3545", text_color="black", command=kelime_sil) 

    create_button(sil_cercevesi, "Tüm Kelimeleri Sil", fg_color="black", text_color="red", command=all_destroy)

    root.mainloop()

if __name__ == "__main__":
    main()