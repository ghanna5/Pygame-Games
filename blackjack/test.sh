
MOSSDEST=/tmp/bj-mossdest
mkdir -p $MOSSDEST


echo "\"Repo\",\"Lint\",\"Exe\",\"LineCount\",\"MossCopy\""

for i in *-cpsc-386-*; do
    cd $i
    PWD=`pwd`
    BN=`basename $PWD`

    FILES=`find . -type d -name env -prune -false  -o -type d -name .action -prune -false -o -name \*.py`
    # Requirements Evaluation
    # F="requirements.txt"
    # if [ -r $F ]; then
    #     grep -i pygame $F >/dev/null 2>&1 || echo "No pygame"
    #         C=`wc -l $F`
    #         echo "$C lines long $BN"
    #     else
    #         echo "       0 $F file not readable $BN"
    # fi
    
    # Total lines
    LINES=`wc -l $FILES | tail -1 | ggrep -oP "\d+"`
    
    F="blackjack.py"
    # echo $F
    # ls -1 $F >/dev/null 2>&1  || echo "No $F"
    if [ -r $F ]; then
        if [ -x $F  ]; then
            head -1 $F | grep -i python > /dev/null 2>&1
            if [ $? -eq 0 ]; then
                FV="3"
            else
                FV="2"
            fi
        else
            FV="2"
        fi
    else
        FV="0"
    fi
        

    # Code quality
    # https://stackoverflow.com/questions/4210042/how-do-i-exclude-a-directory-when-using-find
    V=`pylint $FILES | tail -2 | ggrep -oP 'at \K\d+\D+\d+'`
    # V="foo/10"
    
    C=0
    for i in player.py game.py; do
        G=`find . -name $i`
        if [ $G"x" != "x" ]; then
            FN=`basename $G`
            cp $G ${MOSSDEST}/$BN-$FN
            C=$(($C + 1))
        fi
    done
    
    echo "\"$BN\",\"$V\",\"$FV\",\"$LINES\",\"$C\""
    
    # echo && echo
    cd - >& /dev/null
done
