##Program untuk extract informasi dari eksternal file

##Program didesain agar pengguna dapat mengekstrak informasi terupdate tentang corona virus kata kunci yang diinginkan 
##dalam waktu singkat tanpa harus membaca keseluruhan file untuk memperoleh informasi

*Bahasa Pemograman : Python (versi 3 ke atas)
*Web Framework : HTML,CSS,flask
*Library atau Modul lainnya yang harus diinstall terlebih dahulu : nltk 

##Struktur File
├───doc
├───src
│   ├───static
│   │   └───css
│   ├───templates
│   └───__pycache__
└───test
*Folder doc berisi laporan dan juga file READ.me
*older src mengandung folder static, templates dan file program
*Folder static berisi file css
*Folder templates berisi file html
*File patternMatching.py berisi kode program untuk algoritma string matching antara lain: BM Algorithm, KMP Algorithm, Regex
*File app.py berisi kode program untuk backend applikasi tersebut


##Cara run program
*Pada cmd ketik:
python app.py
kemudian buka browser dengan link
http://127.0.0.1:5000/

##Input: Multiple text file pada folder test,keyword,algoritma yang diiginkan

##Ouput: Output tentang data numeric(kuantitas) serta data waktu(tanggal) serta kalimat dalam text yang mengandung  keyword yang diinput
