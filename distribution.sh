#!/bin/bash

####### COPIA FILES
VERSION=`cat libdidyoureadme.py | grep 'version="2'| cut --delimiter='"'  -f 2`
TIME=`date +%Y%m%d%H%M%S`
CWD=`pwd`
DIR=/tmp/didyoureadme-$VERSION-$TIME
DIRSRCLINUX=$DIR/src.linux/didyoureadme-$VERSION/ # Se instala con un makefile
DIRBINLINUX=$DIR/bin.linux/didyoureadme-$VERSION # Es un directorio con el ejecutable
mkdir -p $DIRSRCLINUX
mkdir -p $DIRBINLINUX

echo "Este script crea el fichero $FILE para ser subido a sourceforge"
echo "En Linux hay que tener instalado cx_freeze"

rm $CWD/dist/*

#GENERA SRC LINUX
make compile
mkdir $DIRSRCLINUX/doc
mkdir $DIRSRCLINUX/i18n
mkdir $DIRSRCLINUX/images
mkdir $DIRSRCLINUX/ui
mkdir $DIRSRCLINUX/sql

cp      Makefile \
	AUTHORS.txt \
        CHANGELOG.txt \
        GPL-3.txt \
        INSTALL.txt \
        RELEASES.txt \
        didyoureadme.py \
        didyoureadme.pro \
        libdidyoureadme.py \
        didyoureadme.desktop \
        didyoureadme-backup \
        $DIRSRCLINUX

cp      i18n/*.ts \
        $DIRSRCLINUX/i18n

cp 	sql/didyoureadme.data \
        sql/didyoureadme.sql \
        $DIRSRCLINUX/sql

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
####### binaries linux
DESTDIR=$DIRBINLINUX make all
sed -i -e 's:so="src.linux":so="bin.linux":' $DIRBINLINUX/bin/didyoureadme
cxfreeze-3.2 $DIRBINLINUX/bin/didyoureadme --include-path=$DIRBINLINUX/lib/didyoureadme/ --target-dir=$DIRBINLINUX/dist/didyoureadme
echo "Execute didyoureadme" > $DIRBINLINUX/dist/README.txt
cp $DIRBINLINUX/share/didyoureadme/*.qm $DIRBINLINUX/dist/didyoureadme
cp $DIRBINLINUX/bin/didyoureadme-backup $DIRBINLINUX/dist/didyoureadme
echo "  * Comprimiendo binario linux..."
cd $DIRBINLINUX/dist
tar cvz  -f $CWD/dist/didyoureadme-bin-linux-$VERSION.tar.gz * -C $DIRBINLINUX/dist > /dev/null
cd $CWD
