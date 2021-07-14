pyinstaller StartGame.py --noconsole --noconfirm --clean --name "Puyo Puyo Tetris" --icon "data/puyologo32x32.ico" --add-data  "data;data/" --add-data "PuyoPuyo;PuyoPuyo/" --add-data "Tetris;Tetris/" --add-data "options.txt;."
del /S /Q "build"
rmdir "build/Puyo Puyo Tetris"
rmdir build
