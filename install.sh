pip install -r requirements.txt
mkdir $PREFIX/src/pngbanner || true
cp main.py $PREFIX/src/pngbanner/main.py
cp pngbanner-install $PREFIX/bin/pngbanner
chmod +x $PREFIX/bin/pngbanner