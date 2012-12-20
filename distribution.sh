#!/bin/bash

####### COPIA FILES
VERSION=`cat libdidyoureadme.py | grep 'version="2'| cut --delimiter='"'  -f 2`
TIME=`date +%Y%m%d%H%M%S`
CWD=`pwd`
DIR=/tmp/didyoureadme-$VERSION-$TIME
DIRSRCLINUX=$DIR/src.linux/didyoureadme-$VERSION/ # Se instala con un makefile
DIRSRCWINDOWS=$DIR/src.windows/didyoureadme-$VERSION/ # Se necesita la instalción de pyqt, python, opengl, se ejecuta con bat. Habra un bat para compilar con pyinstaller y generar con innosetup el exe
DIRBINLINUX=$DIR/bin.linux/didyoureadme-$VERSION # Es un directorio con el ejecutable
DIRBINWINDOWS=$DIR/bin.windows #Es un instalador windows, generado con wine, para generarlo con windows en srcwindows habrá un bat
mkdir -p $DIRSRCLINUX
mkdir -p $DIRSRCWINDOWS
mkdir -p $DIRBINLINUX
mkdir -p $DIRBINWINDOWS

echo "Este script crea el fichero $FILE para ser subido a sourceforge"
echo "En Linux hay que tener instalado cx_freeze"
echo "Debe tener instalado una versión de wine y sobre el haber instalado"
echo "  - Python 3.3"
echo "  - PyQt4 (ultima version)"
echo "  - pywin32 (ultima version)"
echo "  - cx_freeze (última version)"
echo "  - Inno Setup (ultima version)"

rm $CWD/dist/*

#GENERA SRC LINUX
make compile
mkdir $DIRSRCLINUX/doc
mkdir $DIRSRCLINUX/i18n
mkdir $DIRSRCLINUX/images
mkdir $DIRSRCLINUX/ui

cp      Makefile \
	AUTHORS-ES.txt \
	AUTHORS-EN.txt \
        CHANGELOG-EN.txt \
        CHANGELOG-ES.txt \
        GPL-3.txt \
        INSTALL-EN.txt \
        INSTALL-ES.txt \
        RELEASES.txt \
        didyoureadme.py \
        didyoureadme.pro \
        libdidyoureadme.py \
        didyoureadme.desktop \
        $DIRSRCLINUX

cp      i18n/*.ts \
        $DIRSRCLINUX/i18n

cp 	ui/frm* \
	$DIRSRCLINUX/ui

cp	images/*.png \
	images/*.qrc \
	images/*.ico \
	$DIRSRCLINUX/images


echo "  * Comprimiendo codigo fuente linux..."
cd $DIR/src.linux
tar cvz  -f $CWD/dist/didyoureadme-src-linux-$VERSION.tar.gz * -C $DIR/src.linux > /dev/null
cd $CWD
######## 
DESTDIR=$DIRSRCWINDOWS make all
mv $DIRSRCWINDOWS/bin/didyoureadme $DIRSRCWINDOWS/bin/didyoureadme.py
sed -i -e 's:so="src.linux":so="src.windows":' $DIRSRCWINDOWS/bin/didyoureadme.py
cp $DIRSRCWINDOWS/bin/didyoureadme.py $DIRSRCWINDOWS/bin/didyoureadme.py.src
cp $DIRSRCWINDOWS/bin/didyoureadme.py $DIRSRCWINDOWS/bin/didyoureadme.py.bin
sed -i -e 's:so="src.windows":so="bin.windows":' $DIRSRCWINDOWS/bin/didyoureadme.py.bin

echo "
@echo off
copy /Y bin\\didyoureadme.py.src bin\\didyoureadme.py

cd bin
c:/Python32/python.exe didyoureadme.py
pause" > $DIRSRCWINDOWS/didyoureadme.bat

echo "
rem Solo con x86 no hay opengl 64
rem Instalar pyinstaller directorio en c:\ solo una vez
rem Se necesita pywin32 para pyinstaller 
rem Meter didyoureadme.ico
rem Cambiar ruta de pyinstaller 

cd ..
cd ..
copy /Y bin\\didyoureadme.py.bin bin\\didyoureadme.py
cd share/didyoureadme
rm didyoureadme.spec
rm logdict2.7.3.final.0-1.log
rmdir /s /q build
rmdir /s /q dist
c:\Python27\python.exe c:\pyinstaller\pyinstaller.py -i ficharoja.ico -w -p ..\..\lib\didyoureadme ..\..\bin\didyoureadme.py
copy /Y sounds\\*.wav dist\\didyoureadme\\
pause" > $DIRSRCWINDOWS/share/didyoureadme/generateexe_inno.bat

echo "  * Comprimiendo codigo fuente windows..."
cd $DIR/src.windows
zip -r $CWD/dist/didyoureadme-src-windows-$VERSION.zip ./ >/dev/null
cd $CWD

####### binaries linux
DESTDIR=$DIRBINLINUX make all
sed -i -e 's:so="src.linux":so="bin.linux":' $DIRBINLINUX/bin/didyoureadme
cxfreeze-3.2 $DIRBINLINUX/bin/didyoureadme --include-path=$DIRBINLINUX/lib/didyoureadme/ --target-dir=$DIRBINLINUX/dist/didyoureadme
echo "Execute didyoureadme and play" > $DIRBINLINUX/dist/README.txt
cp $DIRBINLINUX/share/didyoureadme/*.qm $DIRBINLINUX/dist/didyoureadme
echo "  * Comprimiendo binario linux..."
cd $DIRBINLINUX/dist
tar cvz  -f $CWD/dist/didyoureadme-bin-linux-$VERSION.tar.gz * -C $DIRBINLINUX/dist > /dev/null
cd $CWD

###### binaries windows
DESTDIR=$DIRBINWINDOWS make all
sed -i -e 's:so="src.linux":so="bin.windows":' $DIRBINWINDOWS/bin/didyoureadme
wine /root/.wine/drive_c/Python32/python.exe /root/.wine/drive_c/Python32/Scripts/cxfreeze $DIRBINWINDOWS/bin/didyoureadme --include-path=$DIRBINWINDOWS/lib/didyoureadme/ --target-dir=$DIRBINWINDOWS/dist/didyoureadme
cp $DIRBINWINDOWS/share/didyoureadme/*.qm $DIRBINWINDOWS/dist/didyoureadme
cp $CWD/didyoureadme.iss $DIRBINWINDOWS
sed -i -e "s:XXXXXXXX:$VERSION:" $DIRBINWINDOWS/didyoureadme.iss
cd $DIRBINWINDOWS
wine $HOME/.wine/drive_c/Program\ Files\ \(x86\)/Inno\ Setup\ 5/ISCC.exe /o$CWD/dist didyoureadme.iss
cd $CWD

