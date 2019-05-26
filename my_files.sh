#!/bin/bash
echo on
tdir="ttt`date +%Y%m%d%H%M%S`"
rdir=$tdir".tgz"
mkdir -p ~/$tdir/html ~/$tdir/html/2016FarmersCalendar ~/$tdir/cgi ~/$tdir/usrlocalbin
cp -v /var/www/html/* ~/$tdir/html 2>>/dev/null
#cp -v /var/www/html/storage/* ~/$tdir/html/storage 2>>/dev/null
cp -v /var/www/html/2016FarmersCalendar/* ~/$tdir/html/2016FarmersCalendar 2>>/dev/null
cp -v /usr/lib/cgi-bin/* ~/$tdir/cgi 2>>/dev/null
cp -v /usr/local/bin/* ~/$tdir/usrlocalbin 2>>/dev/null
cp -v ~/.vimrc ~/$tdir
cp -v ~/.profile ~/$tdir
cp -v ~/.bashrc ~/$tdir
tar czvf ~/$rdir ~/$tdir
mv ~/$rdir ~/$tdir
