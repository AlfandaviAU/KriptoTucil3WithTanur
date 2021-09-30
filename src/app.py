from flask import Flask, render_template, request, redirect, url_for
from forms import Todo
from steganography import *
from modified_rc4 import *
import sys, os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'

# Output steganography
try:
    os.mkdir("output")
except:
    pass

@app.route('/', methods=['GET', 'POST'])
def main():
    request_method = request.method
    return render_template('index.html',request_method=request_method)


@app.route('/rc4', methods=['GET', 'POST'])
def page_rc4():
    request_method = request.method
    if len(request.form) == 0:
        result = ""
    else:
        if len(request.files.get("srcfile").filename) != 0:
            srctext = request.files.get("srcfile").read()
        else:
            srctext = request.form.get("message")

        rckey   = request.form.get("key")
        if len(rckey) > 0:
            result  = mod_rc4(srctext, rckey)

    return render_template('rc4.html',request_method=request_method, result=result)


@app.route('/stegano', methods=['GET', 'POST'])
def page_stegano():
    request_method = request.method

    return render_template('stegano.html',request_method=request_method)



@app.route('/enc_stegano', methods=['GET', 'POST'])
def encode_stegano():
    srcfilename = request.files.get("cover-file").filename

    filestream  = request.files.get("cover-file")
    outputfile  = "output/steg-" + srcfilename
    if request.form.get("key") == "":
        stegoKey = None
    else:
        stegoKey = request.form.get("key")

    stegoEnc = request.form.get("metode-steg")
    print(stegoEnc)
    # TODO : Enkripsi RC4

    if srcfilename.split(".")[1] == "png":
        stegEncoder = StegPNG(filestream, outputfile)
    elif srcfilename.split(".")[1] == "wav":
        stegEncoder = StegWAV(filestream, outputfile)

    embedfilestream = request.files.get("embed-file")
    stegEncoder.encode(embedfilestream.read(), stegoKey)

    return redirect('/stegano')

@app.route('/dec_stegano', methods=['GET', 'POST'])
def decode_stegano():
    srcfilename = request.files.get("file").filename.split(".")

    filestream  = request.files.get("file")
    outputfile  = "output/dec-" + srcfilename[0] + ".txt"
    if request.form.get("key") == "":
        stegoKey = None
    else:
        stegoKey = request.form.get("key")

    if srcfilename[1] == "png":
        stegDecoder = StegPNG(filestream, outputfile)
    elif srcfilename[1] == "wav":
        stegDecoder = StegWAV(filestream, outputfile)

    try:
        stegDecoder.decode()
    except:
        # Objek bukan stego object yang valid / lcg header salah
        # TODO : Handler ?
        pass

    return redirect('/stegano')


if __name__ == '__main__':
    app.run(debug=True)
