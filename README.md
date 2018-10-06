# iTunes-Parser-Python
Comand line application: parse through iTunes playlist .xml files and perform various operations with them

ARGS

--common [file] [file]     Creats a .txt file with a list of comman track titles between the 2 supplied files (looks only at name)
--stats  [file]            Creats a matplotlib chart plotting song rating & duration and shows it to the screen
--dups   [file][file]      Creats a .txt file listing duplicate songs (compares name and duration)
